import ipaddress
import os
import subprocess
import threading

import requests
from flask import request, make_response

from streamlit_pyvista import ROOT_URL
from streamlit_pyvista.helpers.cache import save_file_content, DEFAULT_CACHE_DIR, DEFAULT_VIEWER_CACHE_NAME
from streamlit_pyvista.helpers.streamlit_pyvista_logging import root_logger
from streamlit_pyvista.helpers.utils import (find_free_port, is_server_alive,
                                             wait_for_server_alive, ServerItem)
from streamlit_pyvista.message_interface import (EndpointsInterface, ProxyMessageInterface,
                                                 ServerMessageInterface)
from streamlit_pyvista.server_managers.server_manager import ServerManagerBase


def run_trame_viewer(server_port: int, file_path: str):
    """ Launch a Trame server using python subprocess """
    try:
        subprocess.run(["python3", file_path,
                        "--server", "--port", str(server_port)],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                       # Comment the line above for debugging error in subprocess
                       check=True)
    except subprocess.CalledProcessError as e:
        root_logger.error(f"Trame Server {server_port} crashed with following error: {e}")


def run_proxy():
    threading.Thread(target=lambda: (subprocess.run(["streamlit-pyvista", "run", "proxy"],
                                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)),
                     daemon=True).start()


class ServerManagerProxified(ServerManagerBase):
    """ Implementation of ServerManagerBase that make use of a proxy for remote connection """

    def __init__(self, host: str = "0.0.0.0", port: int = 8080, proxy_host: str = "127.0.0.1", proxy_port: int = 5000):
        super().__init__(host, port)

        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.base_url = ROOT_URL

    def _extract_proxy_host(self):
        """
        Extract the proxy host from the request headers.
        """
        # Identify host used to access the server
        self.proxy_host = request.headers.get("Host").split(":")
        # Extract only the hostname and use proxy port
        if len(self.proxy_host) > 1:
            self.proxy_host[1] = str(self.proxy_port)
            self.proxy_host = ":".join(self.proxy_host)
        else:
            self.proxy_host = self.proxy_host[0]

    def _get_host_for_client(self, server_id: int) -> str:
        """
        Change the host's endpoint to use the proxy, check if the host is an ip
        or a domain to reply with the right host

        Args:
            server_id (int): The id of the server.

        Returns:
            str: The host for the client.
        """
        try:
            ipaddress.ip_address(self.proxy_host)
            host = f"{EndpointsInterface.Protocol}://{self.proxy_host}{self.base_url}/server/{server_id}"
        except ValueError:
            host = f"{EndpointsInterface.Protocol}://{self.proxy_host}{self.base_url}/server/{server_id}"
        return host

    def init_connection(self):

        # Get the host of the proxy
        self._extract_proxy_host()

        file_content, checksum = self._get_viewer_content_from_request(request)
        if file_content is None:
            return make_response({
                                     "Invalid body": f"Expected to have the viewer content encoded in base64 in"
                                                     f" the {ServerMessageInterface.Keys.Viewer} field of the json"},
                                 400)

        # Check if any server already running is available and if one was found use it and response with its endpoints
        available_server = self._find_available_server(checksum)

        if available_server is not None:
            self.servers_running.append(available_server)
            res = requests.get(f"{available_server.host}/init_connection").json()
            res[ServerMessageInterface.Keys.Host] = (
                f"{EndpointsInterface.Protocol}://{self.proxy_host}{self.base_url}"
                f"/server/{available_server.host.split('/')[-1]}"
            )
            return make_response(res, 200)

        file_path = save_file_content(file_content, f"{DEFAULT_CACHE_DIR}/{DEFAULT_VIEWER_CACHE_NAME}")[0]

        port = find_free_port()
        # Run the trame server in a new thread
        threading.Thread(target=run_trame_viewer, args=[port, file_path]).start()
        # Wait for server to come alive
        if not wait_for_server_alive(f"{EndpointsInterface.Localhost}:{port}", timeout=self.timeout):
            return make_response({
                "Server Timeout Error": f"Unable to connect to Trame instance on port {port},\
                                                                          the server might have crashed"},
                400)
        res = requests.get(f"{EndpointsInterface.Localhost}:{port}/init_connection")
        res = res.json()

        # Add the new server to the proxy server list
        proxy_url = f"{EndpointsInterface.Localhost}:{self.proxy_port}"
        # Launch the proxy if it's not already running
        if not is_server_alive(proxy_url):
            run_proxy()
        if not wait_for_server_alive(proxy_url, timeout=self.timeout):
            return make_response({
                "Server Timeout Error": f"Unable to connect to the proxy, the server might have crashed"}, 400)
        proxy_res = requests.get(f"{proxy_url}{self.base_url}{EndpointsInterface.Proxy.UpdateAvailableServers}",
                                 json={ProxyMessageInterface.Keys.Action: ProxyMessageInterface.Actions.Add,
                                       ProxyMessageInterface.Keys.ServerURL: res['host']})

        server_id = proxy_res.json()[ProxyMessageInterface.Keys.ServerID]

        res[ServerMessageInterface.Keys.Host] = self._get_host_for_client(server_id)

        root_logger.debug(
            f"Trame Server {port} was launched successfully and routed with the proxy with id={server_id}")
        # Since communication with the server running is local, no need to use the url, localhost + port is always
        # working
        self.servers_running.append(
            ServerItem(f"{EndpointsInterface.Localhost}:{self.proxy_port}{self.base_url}/server/{server_id}", checksum))
        return make_response(res, 200)

    def _remove_and_kill_server(self, server: ServerItem):
        super()._remove_and_kill_server(server)
        payload = {ProxyMessageInterface.Keys.Action: ProxyMessageInterface.Actions.Remove,
                   ProxyMessageInterface.Keys.ServerURL: server.host}
        requests.get(f"{EndpointsInterface.Protocol}://{self.proxy_host}{self.base_url}"
                     f"{EndpointsInterface.Proxy.UpdateAvailableServers}",
                     json=payload)

    @staticmethod
    def get_launch_path():
        return os.path.abspath(__file__)

    def _lifecycle_task_kill_server(self, servers_running):
        servers_killed = super()._lifecycle_task_kill_server(servers_running)
        # Complete the routine by notifying the proxy of all the server that needs to be unreferenced
        for server in servers_killed:
            payload = {ProxyMessageInterface.Keys.Action: ProxyMessageInterface.Actions.Remove,
                       ProxyMessageInterface.Keys.ServerURL: server.host}
            requests.get(f"{EndpointsInterface.Protocol}://{self.proxy_host}{self.base_url}"
                         f"{EndpointsInterface.Proxy.UpdateAvailableServers}", json=payload)

        return servers_killed


if __name__ == "__main__":
    server_manager = ServerManagerProxified()
    server_manager.run_server()
