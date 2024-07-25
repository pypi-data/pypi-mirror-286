from typing import Optional

import pyvista as pv
import argparse
from pyvista.trame.ui import plotter_ui
from trame.ui.vuetify3 import VAppLayout
from trame.widgets import vuetify3 as vuetify
from trame.widgets import html
from trame.decorators import TrameApp, change, controller
from trame.app import Server

import os
import time, threading
import asyncio

from streamlit_pyvista.trame_viewers.trame_backend import TrameBackend
from streamlit_pyvista.helpers.streamlit_pyvista_logging import root_logger
from streamlit_pyvista.lazy_mesh import LazyMesh, LazyMeshList

MILLISECOND = 1
SECOND = 1000 * MILLISECOND


def get_viewer_path():
    return os.path.abspath(__file__)


@TrameApp()
class TrameAdvancedViewer(TrameBackend):
    """
    This class is a subclass of TrameBackend and is used to create a more advanced viewer that can display a mesh and
    warp option to warp the mesh
    """

    def __init__(self, plotter: Optional[pv.Plotter] = None, server: Optional[Server] = None,
                 port: int = 8080, host: str = "0.0.0.0"):
        """
        Initialize the TrameAdvancedViewer object.

        Parameters:
        - plotter (Optional[pv.Plotter]): A PyVista Plotter object. If provided, it will be used for rendering.
        - server (Optional[Server]): A Trame Server object. If provided, it will be used for serving the application.
        - port (int): The port number to use for the server. Default is 8080.
        - host (str): The host address to bind the server to. Default is "0.0.0.0".
        """
        self.slider_playing = False
        TrameBackend.__init__(self, plotter, server, port, host)

        self._setup_timer()
        self.loop = None

        self.height += 500

    def _setup_timer(self):
        """ Set up the timer callback and timeout """
        self.default_timer_timeout = 250 * MILLISECOND
        self.state.timer_timeout = self.default_timer_timeout
        self.timer = threading.Thread(target=self._timer_callback)

    def _setup_state(self):
        """ Set up all the state variables to initial values """
        self.state.is_full_screen = False
        self.state.mesh_representation = self.state.options[0] if self.state.options is not None else None
        self.state.warped_field = None
        self.state.original_resolution = False
        self.state.can_toggle_resolution = True

        # Option's dropdown
        self.state.options = [None]
        self.state.options_warp = [None]

        # Inputs
        self.state.warp_input = 1
        self.state.wireframe_on = True
        self.state.slider_value = 0
        self.state.play_pause_icon = "mdi-play"

    def _timer_callback(self):
        """ This function is called on all timer tick and update the mesh viewed to animate a sequence of mesh
        playing """

        # The animation needs to stop when the server stop or if the animation was paused by the user
        while self.slider_playing and self.server.running:
            # Increment the counter while keeping it within the bound of the mesh sequence
            self.state.slider_value = (self.state.slider_value + 1) % self.sequence_bounds[1]
            # Call function on the main thread using thread safe method to update the server states and ui
            self.loop.call_soon_threadsafe(self._update_mesh_displayed_from_index, self.state.slider_value)
            self.loop.call_soon_threadsafe(self.server.force_state_push, "slider_value")

            time.sleep(self.get_sanitized_timer())
        # After the animation was stopped, reset the timer
        self.timer = threading.Thread(target=self._timer_callback)

    def get_sanitized_timer(self):
        if self.state.timer_timeout == "":
            return self.default_timer_timeout / SECOND
        timeout_ms = int(self.state.timer_timeout)
        return min(max(100 * MILLISECOND, timeout_ms), 2 * SECOND) / SECOND

    @change("mesh_representation")
    def _update_mesh_representation(self, mesh_representation, **kwargs):
        """ This function is automatically called when the state 'mesh_representation' is changed.
        This state is used to determine which vector field is shown """
        # Remove the scalar bar representing the last vector field shown
        self._clear_scalar_bars()

        # Replace the string input "None" with None
        if mesh_representation == "None":
            self.state.mesh_representation = None

        # Set all element of the mesh sequence with the same field shown
        for i in range(self.sequence_bounds[1]):
            if self.mesh_array is not None:
                self.mesh_array[i].set_active_scalars(self.state.mesh_representation)

        # Update ui elements
        self._update_mesh_displayed_from_index(self.state.slider_value)
        self._update_warp_input()

    @change("original_resolution")
    def _update_original_resolution(self, **kwargs):
        if self.mesh_array is None or self.state.slider_value >= self.sequence_bounds[1]:
            return
        self.mesh_array.set_show_decimated(not self.state.original_resolution)
        if self.state.original_resolution:
            self.warp_free_mesh = self.mesh_array[self.state.slider_value]
            self._replace_mesh_displayed(self.mesh_array[self.state.slider_value])
        else:
            self._update_mesh_displayed_from_index(self.state.slider_value)

    @change("warp_input")
    def _update_warp_input(self, **kwargs):
        """ This function is automatically called when the state 'warp_input' is changed. """
        try:
            new_warp = float(self.state.warp_input)
            if self.current_mesh is None:
                return
            if self.state.warped_field in self.current_mesh.point_data.keys():
                dim = self.current_mesh.point_data.get_array(self.state.warped_field).ndim  # 1 if scalar, 2 if vector
            elif self.state.warped_field in self.current_mesh.cell_data.keys():
                dim = self.current_mesh.cell_data.get_array(self.state.warped_field).ndim
            elif self.state.warped_field in self.current_mesh.field_data.keys():
                dim = self.current_mesh.field_data.get_array(self.state.warped_field).ndim
            else:
                self.state.options_warp.remove(self.state.warped_field)
                return

            # if the dimension of the field is 1 or 2 we can warp by a scalar, else we warp by a vector
            if dim <= 2:
                new_pyvista_mesh = self.warp_free_mesh.warp_by_scalar(self.state.warped_field,
                                                                      factor=new_warp)
            else:
                new_pyvista_mesh = self.warp_free_mesh.warp_by_vector(self.state.warped_field,
                                                                      factor=new_warp)

            # Show the mesh that was warped
            self._replace_mesh_displayed(new_pyvista_mesh)
        except ValueError:
            return
        except Exception as e:
            root_logger.error(f"An error occurred with the warp {self.state.warp_input}")
            root_logger.error(e)

    @change("warped_field")
    def _update_warped_field(self, warped_field, **kwargs):
        """ This function is automatically called when the state 'warped_field' is changed.
         This state is used to describe which vector field of the mesh we want to warp. """
        if warped_field is None or warped_field == "None":
            return
        self._update_warp_input(warped_field=warped_field)

    @change("wireframe_on")
    def _update_wireframe_on(self, **kwargs):
        """ This function is automatically called when the state 'wireframe_on' is changed.
         This state is used to store whether we should show the wireframe of the mesh or the plain mesh. """
        self._replace_mesh_displayed(self.current_mesh)

    @change("slider_value")
    def _slider_value_change(self, slider_value, **kwargs):
        """ This function is automatically called when the state 'slider_value' is changed.
         This state is used to store the frame to actually displayed in a sequence. """
        self._update_mesh_displayed_from_index(int(slider_value))
        self.state.warp_input = 0

    def _clear_scalar_bars(self):
        """ Remove all the scalar bars shown on the plotter """
        if self.pl is None:
            return
        bar_to_remove = [key for key in self.pl.scalar_bars.keys()]
        [self.pl.remove_scalar_bar(title=key) for key in bar_to_remove]

    def _clear_viewer(self):
        """ Reset the viewer and its related attribute to an empty viewer """
        super()._clear_viewer()
        self._clear_scalar_bars()
        self.state.slider_value = 0
        self.state.warped_field = None
        self.state.warp_input = 0
        self.state.option_warp = None

    def _replace_mesh_displayed(self, new_mesh):
        """
        Change the mesh displayed in the plotter and its related data
        Args:
            new_mesh: the new mesh to display
        """
        if new_mesh is None:
            return

        # set custom style
        kwargs_plot = {}
        if self.state.wireframe_on:
            kwargs_plot["style"] = "wireframe"

        # update mesh and set its active scalar field, as well as adding the scalar bar
        self.current_mesh = new_mesh

        # Set the active scalar and create it's scalar bar if it does not exist
        self.current_mesh.set_active_scalars(self.state.mesh_representation)

        self.pl.mapper = self._show_scalar_bar(self.state.mesh_representation)

        # Replace actor with the new mesh (automatically update the actor because they have the same name)
        self.pl.add_mesh(self.current_mesh, style="wireframe" if self.state.wireframe_on else None,
                         name="displayed_mesh", show_scalar_bar=True,
                         scalar_bar_args={"mapper": self.pl.mapper})

        self.state.can_toggle_resolution = not self.mesh_array.has_decimated_version(self.state.slider_value)

        self.pl.render()

    def _show_scalar_bar(self, field: str = None):
        """
        Show the scalar bar associated with the field
        Args:
            field (str): The associated field of the bar that you want to show

        """
        if field is None:
            # If the field is not specified try to get the actual field displayed in the plotter
            field = self.state.mesh_representation

        if self.mesh_array is None or field is None:
            return

        # Get the bounds of the bar or compute it if it does not exist
        if self.bounds_scalar is None:
            self._computes_bounds_scalar()

        # Create the pyvista scalar bar
        bounds = self.bounds_scalar.get(field, None)
        if bounds is not None:
            self.pl.mapper.lookup_table.SetTableRange(bounds[0], bounds[1])
            self.pl.add_scalar_bar(self.state.mesh_representation)

        # Return the mapper to display the good max and min value on the bar
        return self.pl.mapper

    def _option_dropdown(self):
        """
        This function generate a dropdown to select which field is displayed

        Returns:
            The ui element displaying the mesh_representation dropdown
        """
        return vuetify.VSelect(
            v_model=("mesh_representation", "None"),
            items=("options", self.state.options),
            label="Representation",
            hide_details=True,
            dense=True,
            outlined=True,
            classes="pt-1",
        )

    def _build_slider(self):
        """
        This function build the ui component containing the slider to select the frame displayed

        Returns:
            A row containing a play-pause button and a slider

        """
        row = html.Div(style='display:flex;justify-content:center;align-content:center;gap:20px;')
        with row:
            with vuetify.VBtn(
                    icon=True,
                    click=self._play_button
            ):
                vuetify.VIcon("{{ play_pause_icon }}")
            html.Div("{{ slider_value }}")
            vuetify.VSlider(
                ref="slider",
                label="",
                min=self.sequence_bounds[0],
                max=self.sequence_bounds[1] - 1,
                v_model=("slider_value", 8),
                step=1
            )
        return row

    @controller.set("play_button")
    def _play_button(self):
        """ This function is called by the play-pause button of the slider is played and manage the state
        of the timer that updates the frame displayed in a periodic manner. """
        if self.sequence_bounds[1] <= 1:
            root_logger.error("Impossible to start the sequence since it's a unique mesh")
            return

        # Invert the state of the play button and if it's playing start the timer updating frame at a fixed interval
        self.slider_playing = not self.slider_playing
        if self.slider_playing and not self.timer.is_alive():
            self.state.play_pause_icon = "mdi-pause"
            self._store_mesh_list_states()
            self.loop = asyncio.get_event_loop()
            self.timer.start()
        else:
            self.state.play_pause_icon = "mdi-play"
            self._restore_mesh_list_states()

    def _store_mesh_list_states(self):
        self.prev_orig = self.state.original_resolution
        self.state.original_resolution = False
        self.mesh_array.set_show_decimated(True)

    def _restore_mesh_list_states(self):
        self.mesh_array.set_show_decimated(not self.prev_orig)
        self.state.original_resolution = self.prev_orig

    def _build_warp_option(self):
        """
        This function build the dropdown used to select which field is being warped
        Returns: a vuetify dropdown component
        """
        return vuetify.VSelect(
            v_model=("warped_field"),
            items=("options_warp", self.state.options_warp),
            label="Warped Field",
            hide_details=True,
            dense=True,
            outlined=True,
            classes="pt-1",
        )

    def _build_warper(self):
        """
        build the ui component responsible for the warping which is in more details a column with a dropdown and an
        input of type number

        Returns:
            A vuetify Column containing all the element of the component
        """
        warper = vuetify.VCol(cols="6")
        with warper:
            self._build_warp_option()

            # if self.state.warped_field != "None" and self.state.warped_field is not None:
            html.Input(type="number", label="warp",
                       v_model=("warp_input", 0.0),
                       ref=f"warp-input",
                       step="1"
                       )
        return warper

    def _build_mesh_control_layout(self):
        """
        This function return all the control part of the ui.

        Returns:
            A vuetify component representing all the control layout

        Note:
            The ui generated by this class is composed of:
                - The dropdown to select the vector field to display
                - The warp control
                - The slider controller
                - other various control

        """
        layout = html.Div()
        with (layout):
            with vuetify.VRow(dense=True):
                with vuetify.VCol(cols="6"):
                    # If there are options show the dropdown
                    if self.state.options[0] is not None and len(self.state.options) > 1:
                        self._option_dropdown()
                # If there are options create the warper layout
                if self.state.options[0] is not None and len(self.state.options) > 1:
                    self._build_warper()
            vuetify.VCheckbox(v_model=("wireframe_on",), label="Wireframe on", id="wireframe_checkbox",
                              style="padding: 3px;")
            with vuetify.VTooltip(
                    text="Check to have the version with full resolution. The checkbox might be disabled if the "
                         "mesh is small enough to be always displayed without decimation") as elem_to_test:
                with vuetify.Template(v_slot_activator="{ props }"):
                    with html.Div(v_bind="props",
                                  on_icon="mdi-account-check",
                                  off_icon="mdi-account-check-outline",
                                  ):
                        vuetify.VCheckbox(
                            label="See mesh with its original resolution",
                            id="original_res_checkbox",

                            v_model=("original_resolution",),

                            classes="mx-1",
                            disabled=("can_toggle_resolution",)
                        )

            # If the viewer display a sequence of mesh show the slider
            if self.sequence_bounds[1] > 1:
                vuetify.VTextField(
                    v_model=("timer_timeout", 250),
                    type="number",
                    label="Enter the time to wait between each frame in ms between 100 to 2000",
                    outlined=True,
                )
                self._build_slider()

            with vuetify.VBtn(click=self._request_full, style="position: absolute; bottom:25px; right:25px;",
                              icon=True):
                vuetify.VIcon("mdi-fullscreen" if not self.state.is_full_screen else "mdi-fullscreen-exit")
        return layout

    def estimate_controller_height(self):
        """
        This function make an estimation of the size the component might required in the worst case

        Returns:
            The computed worst case height
        """
        # Get the worst dimension of any warper to find how many input would be required and add the height
        # of all these input to the default height
        if self.mesh_array is not None and self.state.mesh_representation is not None:
            ndim = self.mesh_array[0].get_array(self.state.mesh_representation).shape[1]
            return 30 * ndim, 9 * 30
        return 0.2 * self.height, 9 * 30

    def _build_ui(self):
        """
        Build all the ui frontend with all different components

        Returns:
            A VAppLayout for the server
        """
        with VAppLayout(self.server) as layout:
            with layout.root:
                with html.Div(
                        style=f"height: {self.height}px ;width:100%"):  # add the following arg: style="height: 100vh; width:100vw" to have the plotter taking all screen
                    with html.Div(ref="container",
                                  style=f"height:{self.height - self.controller_height}px;padding: 0;"):
                        # Create the plotter section
                        with vuetify.VCol(style=f"height:100%;padding: 0;"):
                            # If the slider is playing we force the app to use remote rendering to avoid bug
                            # with local rendering
                            if self.slider_playing:
                                plotter_ui(self.pl, default_server_rendering=True, mode="server",
                                           style="width: 100%; height:100%;background-color: black;")
                            else:
                                plotter_ui(self.pl, default_server_rendering=True,
                                           style="width: 100%; height:100%;background-color: black;")
                    with vuetify.VCol(style=f"height:{self.controller_height}px;padding: 0;width:100%;"):
                        # Create the whole control layout
                        self._build_mesh_control_layout()

        return layout

    def _request_full(self):
        """ Make a js call to request full screen on the iframe """
        self.server.js_call("container", "requestFullscreen")
        self.state.is_full_screen = not self.state.is_full_screen


if __name__ == "__main__":
    import sys

    # Add command line argument and support
    parser = argparse.ArgumentParser(description='Launch a trame server instance')
    # Add the port argument that allow user to specify the port to use for the server from command line
    parser.add_argument('--port', type=int, help='Specify the port of the server')
    # Add --server flag that is used to specify whether to use the trame as only a server and block the
    # automatic open of a browser
    parser.add_argument('--server', action="store_true", help='Specify if the trame is opened as a server')
    args = parser.parse_args()
    mv = TrameAdvancedViewer(port=args.port)
    if sys.platform == 'win32':
        # On Windows, use asyncio.run() with custom event loop policy
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(mv.run())
