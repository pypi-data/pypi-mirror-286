import json
from typing import Optional, Union
import atexit

from flask import Flask, make_response, request, Request, Response
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
import requests
import base64
import hashlib

import os
import threading
from abc import ABC, abstractmethod
from streamlit_pyvista.helpers.utils import (find_free_port, is_server_available,
                                             is_server_alive, wait_for_server_alive, ServerItem)
from streamlit_pyvista.message_interface import ServerMessageInterface, EndpointsInterface
import logging
from streamlit_pyvista import ROOT_URL
from streamlit_pyvista.helpers.cache import save_file_content, update_cache, DEFAULT_CACHE_DIR, \
    DEFAULT_VIEWER_CACHE_NAME
from streamlit_pyvista.helpers.streamlit_pyvista_logging import root_logger

logging.getLogger('werkzeug').disabled = True


class ServerManagerBase(ABC):
    """ This class is the base for any ServerManager implementation """

    def __init__(self, host: str = "0.0.0.0", port: int = 8080, ) -> None:
        self.app = Flask(__name__)
        # register API endpoints
        self.app.add_url_rule(EndpointsInterface.InitConnection, "init_connection", self.init_connection)
        self.app.add_url_rule(ROOT_URL + EndpointsInterface.InitConnection, "init_connection", self.init_connection)

        self.servers_running = []
        self.host = host
        self.port = port
        self.viewer_runner_script = None
        self.timeout = 10

        # Set up a scheduler used to periodically kill servers that are not in use
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self._lifecycle_task_kill_server, 'interval',
                               kwargs={"servers_running": self.servers_running}, seconds=3*60, max_instances=3)

        update_cache()

        atexit.register(self._on_server_stop)

    @abstractmethod
    def init_connection(self) -> Response:
        """
        This function receive request of clients that require a trame server to display meshes. It's in this class that
        we need by any means start a trame server and get its endpoints
        Returns:
            Response: A response containing a json with all required endpoint for a MeshViewerComponent to work properly
        """
        pass

    def run_server(self):
        """ Start the flask server and the scheduler """
        self.scheduler.start()
        self.app.run(host=self.host, port=self.port, debug=False, use_reloader=False)
        root_logger.info(f"Started Server Manager {self.port} Service")

    def _on_server_stop(self):
        """ Function called when the manager is stopped that stop all managed trame servers and stop the scheduler """
        for server in self.servers_running:
            if is_server_alive(server.host):
                requests.get(f"{server.host}/kill_server", timeout=1)
        self.scheduler.shutdown()
        update_cache()
        root_logger.info(f"Server Manager {self.port}  was successfully stopped")

    @staticmethod
    def _get_viewer_content_from_request(cur_req: Request) -> tuple[Optional[bytes], Optional[Union[str, Response]]]:
        """
        get the content of the viewer file passed over the http request
        Args:
            cur_req(Request):
                request to extract the content from
        Returns:
            tuple[Optional[bytes], Optional[str]]:
                Return a tuple (content, checksum) filled with None if any error happens
        """
        # Check that the request is a json and parse it
        if cur_req.is_json:
            req = json.loads(cur_req.json)
        else:
            r = make_response({"Invalid format": "init_connection expected a json with field 'Viewer' "}, 400)
            return None, r
        c = req.get(ServerMessageInterface.Keys.Viewer, None)
        if c is None:
            r = make_response({"Viewer missing": "You should include the content of your viewer "
                                                 "class file in the init_connection request"}, 400)
            return None, r
        c = base64.b64decode(c)
        checksum = hashlib.sha256(c).hexdigest()
        return c, checksum

    @staticmethod
    @abstractmethod
    def get_launch_path() -> str:
        """
        This function must be used to get the path to the file of the manager that will be launched
        Returns:
            str: the path to the file that launch the server
        """
        pass

    def _find_available_server(self, server_type: str) -> Optional[ServerItem]:
        """
        Check in the servers_running attribute if any server is there idling if it's the case it returns
        the address of this server
        Args:
            server_type(str):
                the type of the viewer, define by the checksum of .py file containing the viewer
        Returns:
            Optional[ServerItem]: The address of idling server, if none is found return None
        """
        dead_servers = []
        for server in self.servers_running:
            if not is_server_alive(server.host):
                dead_servers.append(server)
                continue
            if server_type == server.type and is_server_available(server):
                self.servers_running.remove(server)
                return server
        for s in dead_servers:
            self._remove_and_kill_server(s)
        return None

    def _remove_and_kill_server(self, server: ServerItem):
        """
        Take a server and send a signal to kill it and remove it frmo running server list

        Args:
            server (ServerItem): The server to remove
        """
        try:
            requests.get(f"{server.host}/kill_server", timeout=1)
        except requests.exceptions.Timeout:
            pass
        self.servers_running.remove(server)

    def _lifecycle_task_kill_server(self, servers_running: list[ServerItem]) -> list[ServerItem]:
        """
        Task executed periodically by the scheduler to kill all unused server
        Args:
            servers_running(list[ServerItem]): A list of server currently running

        Returns:
            list[ServerItem]: The server that were killed
        """
        elements_to_remove = []
        for server in servers_running:
            if is_server_alive(server.host) and is_server_available(server):
                elements_to_remove.append(server)
        for el in elements_to_remove:
            self._remove_and_kill_server(el)

        root_logger.debug(
            f"Server Manager {self.port} lifecycle task killed the following servers: {elements_to_remove}")
        update_cache()
        return elements_to_remove


def run_trame_viewer(server_port: int, file_path: str):
    """ Launch a Trame server using python subprocess """
    try:
        subprocess.run(
            ["python3", file_path,
             "--server", "--port", str(server_port)],
            # stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,  # Comment this line for debugging error in subprocess
            check=True)
    except subprocess.CalledProcessError as e:
        root_logger.error(f"Trame Server {server_port} crashed with following error: {e}")


class ServerManager(ServerManagerBase):
    """ Implementation of a ServerManagerBase to run trame viewer locally """

    def __init__(self, host: str = "0.0.0.0", port: int = 8080):
        super().__init__(host, port)

    def init_connection(self) -> Response:

        # Check that the request is a json and parse it
        file_content, checksum_or_response = self._get_viewer_content_from_request(request)
        if file_content is None:
            return checksum_or_response
        checksum = checksum_or_response

        # Check if any server already running is available and if one was found use it and response with its endpoints
        available_server = self._find_available_server(checksum)
        if available_server is not None:
            root_logger.debug(f"Trame Server {available_server.host} was available and is used for a new request")
            self.servers_running.append(available_server)
            r = requests.get(
                f"{available_server.host}{EndpointsInterface.InitConnection}")
            return make_response(r.content, 200)

        port = find_free_port()
        file_path = save_file_content(file_content, f"{DEFAULT_CACHE_DIR}/{DEFAULT_VIEWER_CACHE_NAME}")[0]

        # Run the trame server in a new thread
        threading.Thread(target=run_trame_viewer, args=[port, file_path]).start()
        # Wait for server to come alive
        if not wait_for_server_alive(f"{EndpointsInterface.Localhost}:{port}", self.timeout):
            return make_response({
                "Server timeout error": f"Unable to connect to Trame instance on port {port},\
                                                              the server might have crashed"},
                400)
        root_logger.debug(f"Trame Server {port} was launched successfully")
        # Get endpoints of the server
        res = requests.get(f"{EndpointsInterface.Localhost}:{port}{EndpointsInterface.InitConnection}").json()
        self.servers_running.append(ServerItem(res[ServerMessageInterface.Keys.Host], checksum, file_path))
        return make_response(res, 200)

    @staticmethod
    def get_launch_path():
        return os.path.abspath(__file__)


if __name__ == "__main__":
    server_manager = ServerManager()
    server_manager.run_server()
