#
# Copyright 2021 Bernhard Walter
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from jupyter_cadquery import PartGroup, Part
from jupyter_cadquery.cad_objects import to_assembly
from jupyter_cadquery.base import _tessellate_group, get_normal_len, _combined_bb
from jupyter_cadquery.defaults import get_default, get_defaults, preset
from typing import Optional
from cachetools import LRUCache
import pickle
import zmq

ZMQ_PORT = 5555
REQUEST_TIMEOUT = 2000

OBJECTS = {"objs": [], "names": [], "colors": [], "alphas": []}


def set_port(port):
    global ZMQ_PORT
    ZMQ_PORT = port


def connect(context):
    endpoint = f"tcp://localhost:{ZMQ_PORT}"
    socket = context.socket(zmq.REQ)
    socket.connect(endpoint)
    return socket


def send(data):
    context = zmq.Context()
    socket = connect(context)

    msg = pickle.dumps(data, 4)
    print(" sending ... ", end="")
    socket.send(msg)

    retries_left = 3
    while True:
        if (socket.poll(REQUEST_TIMEOUT) & zmq.POLLIN) != 0:
            reply = socket.recv_json()

            if reply["result"] == "success":
                print("done")
            else:
                print("\n", reply["msg"])
            break

        retries_left -= 1

        # Socket is confused. Close and remove it.
        socket.setsockopt(zmq.LINGER, 0)
        socket.close()
        if retries_left == 0:
            break

        print("Reconnecting to server…")
        # Create new connection
        socket = connect(context)

        print("Resending ...")
        socket.send(msg)


class Progress:
    def update(self):
        print(".", end="", flush=True)


def _convert(*cad_objs, names=None, colors=None, alphas=None, cache: Optional[LRUCache]=None, **kwargs):
    part_group = to_assembly(
        *cad_objs,
        names=names,
        colors=colors,
        alphas=alphas,
        render_mates=kwargs.get("render_mates", False),
        mate_scale=kwargs.get("mate_scale", 1),
        default_color=kwargs.get("default_color", get_default("default_color")),
        show_parent=kwargs.get("show_parent", get_default("show_parent")),
    )

    if len(part_group.objects) == 1 and isinstance(part_group.objects[0], PartGroup):
        part_group = part_group.objects[0]

    # Do not send defaults for postion, rotation and zoom unless they are set in kwargs
    config = {
        k: v
        for k, v in get_defaults().items()
        if not k in ("position", "rotation", "zoom", "cad_width", "tree_width", "height", "glass")
    }

    for k, v in kwargs.items():
        if v is not None:
            config[k] = v

    shapes, states = _tessellate_group(part_group, kwargs, Progress(), config.get("timeit"), cache=cache)

    config["normal_len"] = get_normal_len(
        preset("render_normals", config.get("render_normals")),
        shapes,
        preset("deviation", config.get("deviation")),
    )

    bb = _combined_bb(shapes).to_dict()
    # add global bounding box
    shapes["bb"] = bb

    data = {
        "data": dict(shapes=shapes, states=states),
        "type": "data",
        "config": config,
        "count": part_group.count_shapes(),
    }
    return data


import numpy as np


def to_array(track):
    return [track.path, track.action, track.times, track.values]


def animate(tracks, speed):
    data = {
        "data": [to_array(track) for track in tracks],
        "type": "animation",
        "config": {"speed": speed},
    }
    send(data)


def show(*cad_objs, names=None, colors=None, alphas=None, cache: Optional[LRUCache] = None,**kwargs):
    """Show CAD objects in Jupyter

    Valid keywords:
    - height:            Height of the CAD view (default=600)
    - tree_width:        Width of navigation tree part of the view (default=250)
    - cad_width:         Width of CAD view part of the view (default=800)
    - default_color:     Default mesh color (default=(232, 176, 36))
    - default_edgecolor: Default mesh color (default=(128, 128, 128))
    - render_edges:      Render edges  (default=True)
    - render_normals:    Render normals (default=False)
    - render_mates:      Render mates (for MAssemblies)
    - mate_scale:        Scale of rendered mates (for MAssemblies)
    - deviation:         Shapes: Deviation from linear deflection value (default=0.1)
    - angular_tolerance: Shapes: Angular deflection in radians for tessellation (default=0.2)
    - edge_accuracy:     Edges: Precision of edge discretization (default: mesh quality / 100)
    - optimal_bb:        Use optimal bounding box (default=False)
    - axes:              Show axes (default=False)
    - axes0:             Show axes at (0,0,0) (default=False)
    - grid:              Show grid (default=False)
    - ticks:             Hint for the number of ticks in both directions (default=10)
    - ortho:             Use orthographic projections (default=True)
    - transparent:       Show objects transparent (default=False)
    - ambient_intensity  Intensity of ambient ligth (default=1.0)
    - direct_intensity   Intensity of direct lights (default=0.12)
    - position:          Relative camera position that will be scaled (default=(1, 1, 1))
    - rotation:          z, y and y rotation angles to apply to position vector (default=(0, 0, 0))
    - zoom:              Zoom factor of view (default=2.5)
    - reset_camera:      Reset camera position, rotation and zoom to default (default=True)
    - show_parent:       Show the parent for edges, faces and vertices objects
    - theme:             Theme "light" or "dark" (default="light")
    - tools:             Show the viewer tools like the object tree
    - timeit:            Show rendering times, levels = False, 0,1,2,3,4,5 (default=False)
    - cache:             LRU Cache for tesselation          
    NOT SUPPORTED ANY MORE:
    - mac_scrollbar      The default now
    - bb_factor:         Removed
    - display            Use 'viewer="<viewer title>"' (for sidecar display) or 'viewer=None' (for cell display)
    - quality            Use 'deviation'to control smoothness of rendered egdes
    """

    data = _convert(*cad_objs, names=names, colors=colors, alphas=alphas, cache=cache, **kwargs)
    send(data)


def reset():
    global OBJECTS

    OBJECTS = {"objs": [], "names": [], "colors": [], "alphas": []}


def show_object(obj, name=None, options=None, clear=False, **kwargs):
    global OBJECTS

    if clear:
        reset()

    if options is None:
        color = None
        alpha = 1.0
    else:
        color = options.get("color")
        alpha = options.get("alpha", 1.0)

    OBJECTS["objs"].append(obj)
    OBJECTS["names"].append(name)
    OBJECTS["colors"].append(color)
    OBJECTS["alphas"].append(alpha)

    show(*OBJECTS["objs"], names=OBJECTS["names"], colors=OBJECTS["colors"], alphas=OBJECTS["alphas"], **kwargs)
