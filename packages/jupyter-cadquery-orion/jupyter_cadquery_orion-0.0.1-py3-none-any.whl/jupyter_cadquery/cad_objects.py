#
# Copyright 2019 Bernhard Walter
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

try:
    import build123d as bd

    HAS_BUILD123D = True

except ImportError:
    HAS_BUILD123D = False

try:
    import alg123d as ad

    HAS_ALG123D = True

except ImportError:
    HAS_ALG123D = False

try:
    from cadquery_massembly import MAssembly, Mate
    from cadquery_massembly.massembly import MateDef

    HAS_MASSEMBLY = True

except ImportError:
    HAS_MASSEMBLY = False

from cachetools import LRUCache

from typing import Optional
from cadquery import (
    Workplane,
    Sketch,
    Shape,
    Solid,
    Face,
    Wire,
    Edge,
    Compound,
    Vector,
    Vertex,
    Location,
    Assembly as CqAssembly,
    Color as CqColor,
)
from pyparsing import col

from jupyter_cadquery.base import _PartGroup, _Part, _Edges, _Faces, _Vertices, _show

from .utils import Color, get_color, flatten, warn
from .ocp_utils import (
    get_rgba,
    is_compound,
    is_shape,
    get_solids,
    get_faces,
    get_wires,
    get_edges,
    get_vertices,
)
from .defaults import get_default, preset


EDGE_COLOR = "Silver"
THICK_EDGE_COLOR = "MediumOrchid"
VERTEX_COLOR = "MediumOrchid"
FACE_COLOR = "Violet"

OBJECTS = {"objs": [], "names": [], "colors": [], "alphas": []}


def plugins():
    if HAS_BUILD123D or HAS_ALG123D or HAS_MASSEMBLY:
        print("Plugins loaded:")
        if HAS_BUILD123D:
            print("- build123d")
        if HAS_ALG123D:
            print("- alg123d")
        if HAS_MASSEMBLY:
            print("- cadquery-massembly")


def web_color(name):
    wc = Color(name)
    return CqColor(*wc.percentage)


def cq_wrap(obj):
    w = Workplane()
    w.objects = obj
    return w


def convert_alg123d_massembly(obj, copy_mates=True):
    if isinstance(obj, ad.MAssembly):
        bma = obj
        ma = MAssembly(
            obj=None if bma.obj is None else Shape.cast(bma.obj.wrapped),
            name=bma.cq_name,
            color=None if bma.color is None else CqColor(*bma.color.to_tuple(percentage=True)),
            loc=None if bma.loc is None else Location(bma.loc.wrapped),
        )

        for child in bma.children:
            ma.add(convert_alg123d_massembly(child, False), name=child.name)

        if copy_mates:
            for name, mate_def in bma.mates.items():
                assy_path = mate_def.assembly.split("/")
                root = assy_path[1]
                assy_path = assy_path[2:]
                assy_name = "/".join(assy_path) if assy_path else root
                ma.mates[name] = MateDef(
                    convert_alg123d_massembly(mate_def.mate),
                    ma.objects[assy_name],
                    mate_def.origin,
                )

        return ma
    else:
        if isinstance(obj, ad.Mate):
            return Mate(obj.origin.to_tuple(), obj.x_dir.to_tuple(), obj.z_dir.to_tuple())


class Part(_Part):
    def __init__(self, shape, name="Part", color=None, show_faces=True, show_edges=True):

        self.cq_shape = shape
        super().__init__(_to_occ(shape), name, color, show_faces, show_edges)

    def to_assembly(self):
        return PartGroup([self])

    def show(self, grid=None, axes=False):
        if grid is None:
            grid = [False, False, False]
        return show(self, grid=grid, axes=axes)


class Faces(_Faces):
    def __init__(self, faces, name="Faces", color=None, show_faces=True, show_edges=True):
        self.cq_shape = faces
        super().__init__(_to_occ(faces.combine()), name, color, show_faces, show_edges)

    def to_assembly(self):
        return PartGroup([self])

    def show(self, grid=None, axes=False):
        if grid is None:
            grid = [False, False, False]
        return show(self, grid=grid, axes=axes)


class Edges(_Edges):
    def __init__(self, edges, name="Edges", color=None, width=1):
        self.cq_shape = edges
        super().__init__(_to_occ(edges), name, color, width)

    def to_assembly(self):
        return PartGroup([self])

    def show(self, grid=None, axes=False):
        if grid is None:
            grid = [False, False, False]
        return show(self, grid=grid, axes=axes)


class Vertices(_Vertices):
    def __init__(self, vertices, name="Vertices", color=None, size=1):
        self.cq_shape = vertices
        super().__init__(_to_occ(vertices), name, color, size)

    def to_assembly(self):
        return PartGroup([self])

    def show(self, grid=None, axes=False):
        if grid is None:
            grid = [False, False, False]
        return show(self, grid=grid, axes=axes)


class PartGroup(_PartGroup):
    def to_assembly(self):
        return self

    def show(self, grid=None, axes=False):
        if grid is None:
            grid = [False, False, False]
        return show(self, grid=grid, axes=axes)

    def add(self, cad_obj):
        self.objects.append(cad_obj)

    def add_list(self, cad_objs):
        self.objects += cad_objs

    def get_pick(self, pick):
        if pick == {}:
            print("First double click on an object in the CAD viewer")
        else:
            objs = [o for o in self.objects if o.id == f'{pick["path"]}/{pick["name"]}']
            if objs:
                return objs[0].cq_shape
            else:
                print(f"no object found for pick {pick}")
        return None


def get_pick(assembly, pick):
    if pick == {}:
        print("First double click on an object in the CAD viewer")
        return None
    if isinstance(assembly, PartGroup):
        return assembly.get_pick(pick)
    else:
        path = pick["path"]
        name = pick["name"]
        id_ = "/".join([path, name])

        short_path = "/".join(id_.split("/")[2:])
        if assembly.objects.get(short_path) is not None:
            return assembly.objects[short_path]
        else:
            short_path = "/".join(id_.split("/")[2:-1])
            if assembly.objects.get(short_path) is not None:
                return assembly.objects[short_path]
        return None


class Assembly(PartGroup):
    def __init__(self, *args, **kwargs):
        import warnings

        super().__init__(*args, **kwargs)
        warnings.warn(
            "Class 'Assembly' is deprecated (too many assemblies ...). Please use class 'PartGroup' instead",
            RuntimeWarning,
        )


def _to_occ(cad_obj):
    def sketch_to_occ(sketch):
        locs = sketch.locs if sketch.locs else [Location()]
        if sketch._faces:  # pylint:disable=protected-access
            objs = flatten([sketch._faces.moved(loc).Faces() for loc in locs])  # pylint:disable=protected-access
        else:
            objs = [edge.moved(loc) for edge in sketch._edges for loc in locs]  # pylint:disable=protected-access

        return [obj.wrapped for obj in objs]

    # special case Wire, must be handled before Workplane
    if _is_wirelist(cad_obj) or _is_edgelist(cad_obj):
        all_edges = []
        for edges in cad_obj.objects:
            all_edges += edges.Edges()
        return [edge.wrapped for edge in all_edges]

    elif isinstance(cad_obj, Sketch):
        return sketch_to_occ(cad_obj)

    elif isinstance(cad_obj, Workplane):
        result = []
        for obj in cad_obj.objects:
            if isinstance(obj, Sketch):
                result += sketch_to_occ(obj)
            else:
                result.append(obj.wrapped)
        return result

    elif isinstance(cad_obj, Shape):
        return [cad_obj.wrapped]

    elif is_compound(cad_obj):
        return [cad_obj]

    elif is_shape(cad_obj):
        return [cad_obj]

    else:
        raise NotImplementedError(type(cad_obj))


def _parent(cad_obj, obj_id):
    if cad_obj.parent is not None:
        if isinstance(cad_obj.parent.val(), Vector):
            return _from_vectorlist(
                cad_obj.parent,
                obj_id,
                name="Parent",
                color=Color(EDGE_COLOR),
                show_parent=False,
            )
        elif isinstance(cad_obj.parent.val(), Vertex):
            return _from_vertexlist(
                cad_obj.parent,
                obj_id,
                name="Parent",
                color=Color(EDGE_COLOR),
                show_parent=False,
            )
        elif isinstance(cad_obj.parent.val(), Edge):
            return _from_edgelist(
                cad_obj.parent,
                obj_id,
                name="Parent",
                color=Color(EDGE_COLOR),
                show_parent=False,
            )
        elif isinstance(cad_obj.parent.val(), Wire):
            return [_from_wirelist(cad_obj.parent, obj_id, name="Parent", color=Color(EDGE_COLOR))]
        else:
            return [
                Part(
                    cad_obj.parent,
                    "Parent_%d" % obj_id,
                    show_edges=True,
                    show_faces=False,
                )
            ]
    else:
        return []


def _from_solidlist(cad_obj, obj_id, name="Solids", color=None, alpha=None, show_parent=True):
    color = get_color(color, get_default("default_color"), alpha)

    result = [Part(cad_obj, "%s_%d" % (name, obj_id), color=color)]
    if show_parent:
        result = _parent(cad_obj, obj_id) + result
    return result


def _from_facelist(cad_obj, obj_id, name="Faces", color=None, alpha=None, show_parent=True):
    color = get_color(color, FACE_COLOR, alpha)

    result = [Faces(cad_obj, "%s_%d" % (name, obj_id), color=color)]
    if show_parent:
        result = _parent(cad_obj, obj_id) + result
    return result


def _from_edgelist(cad_obj, obj_id, name="Edges", color=None, show_parent=True):
    color = get_color(color, THICK_EDGE_COLOR, 1.0)

    result = [Edges(cad_obj, "%s_%d" % (name, obj_id), color=color, width=3)]
    if show_parent:
        result = _parent(cad_obj, obj_id) + result
    return result


def _from_wirelist(cad_obj, obj_id, name="Wires", color=None, show_parent=True):
    color = get_color(color, THICK_EDGE_COLOR, 1.0)

    result = [Edges(cad_obj, "%s_%d" % (name, obj_id), color=color, width=3)]
    if show_parent:
        result = _parent(cad_obj, obj_id) + result
    return result


def _from_vector(vec, obj_id, name="Vector", color=None, show_parent=True):
    color = get_color(color, THICK_EDGE_COLOR, 1.0)

    tmp = Workplane()
    obj = tmp.newObject([vec])
    return _from_vectorlist(obj, obj_id, name, color=color, show_parent=show_parent)


def _from_vectorlist(cad_obj, obj_id, name="Vertices", color=None, show_parent=True):
    color = get_color(color, VERTEX_COLOR, 1.0)

    if cad_obj.vals():
        vectors = cad_obj.vals()
    else:
        vectors = [cad_obj.val()]
    obj = cad_obj.newObject([Vertex.makeVertex(v.x, v.y, v.z) for v in vectors])
    result = [Vertices(obj, "%s_%d" % (name, obj_id), color=color, size=6)]
    if show_parent:
        result = _parent(cad_obj, obj_id) + result
    return result


def _from_vertexlist(cad_obj, obj_id, name="Vertices", color=None, show_parent=True):
    color = get_color(color, VERTEX_COLOR, 1.0)

    result = [Vertices(cad_obj, "%s_%d" % (name, obj_id), color=color, size=6)]
    if show_parent:
        result = _parent(cad_obj, obj_id) + result
    return result


# pylint:disable=protected-access
def _from_sketch(cad_obj, obj_id, color=None, alpha=None, show_parent=True, show_selection=True):

    result = []

    locs = cad_obj.locs if cad_obj.locs else [Location()]

    workplane = Workplane()
    if cad_obj._faces:
        for loc in locs:
            workplane.objects += cad_obj._faces.moved(loc).Faces()
        result += _from_facelist(workplane, obj_id, name="Faces", show_parent=show_parent)
    elif cad_obj._edges:
        workplane.objects = [edge.moved(loc) for edge in cad_obj._edges for loc in locs]
        result += _from_edgelist(workplane, obj_id, name="Edges", show_parent=show_parent)

    if show_selection and cad_obj._selection:
        workplane = Workplane()
        if isinstance(cad_obj._selection[0], Location):
            workplane.objects = [
                Vertex.makeVertex(0, 0, 0).moved(loc * obj) for obj in cad_obj._selection for loc in locs
            ]
            sel = _from_vertexlist(
                workplane,
                obj_id,
                name="Locations",
                color=color,
                show_parent=show_parent,
            )

        elif isinstance(cad_obj._selection[0], Face):
            for loc in locs:
                workplane.objects += flatten([obj._faces.moved(loc).Faces() for obj in cad_obj._selection])
            sel = _from_facelist(
                workplane,
                obj_id,
                name="Faces",
                color=color,
                alpha=alpha,
                show_parent=show_parent,
            )

        elif isinstance(cad_obj._selection[0], (Edge, Wire)):
            workplane.objects = [edge.moved(loc) for edge in cad_obj._selection for loc in locs]
            sel = _from_edgelist(workplane, obj_id, name="Edges", color=color, show_parent=show_parent)

        elif isinstance(cad_obj._selection[0], Vertex):
            workplane.objects = [vertex.moved(loc) for vertex in cad_obj._selection for loc in locs]
            sel = _from_vertexlist(workplane, obj_id, name="Vertices", color=color, show_parent=show_parent)

        result.append(PartGroup(sel, name=f"Selection_{obj_id}"))

    return result


def to_edge(mate, loc=None, scale=1) -> Workplane:
    w = Workplane()
    for d in (mate.x_dir, mate.y_dir, mate.z_dir):
        edge = Edge.makeLine(mate.origin, mate.origin + d * scale)
        w.objects.append(edge if loc is None else edge.moved(loc))

    return w


def _from_mate(cad_obj, name="Mate", mate_scale=1):
    rgb = (Color((255, 0, 0)), Color((0, 128, 0)), Color((0, 0, 255)))
    return Edges(to_edge(cad_obj, scale=mate_scale), name=name, width=3, color=rgb)


def from_assembly(cad_obj, top, loc=None, render_mates=False, mate_scale=1, default_color=None):
    loc = Location()
    render_loc = cad_obj.loc

    if cad_obj.color is None:
        if default_color is None:
            color = Color(get_default("default_color"))
        else:
            color = Color(default_color)
    else:
        color = Color(get_rgba(cad_obj.color))

    # Special handling for edge lists in an MAssembly
    is_edges = [isinstance(obj, Edge) for obj in cad_obj.shapes]
    if is_edges and all(is_edges):
        if cad_obj.color is None:
            if default_color is None:
                color = Color(get_default("default_edgecolor"))
            else:
                color = Color(default_color)
        else:
            color = Color(get_rgba(cad_obj.color))

        workplane = Workplane()
        workplane.objects = cad_obj.shapes
        parent = [
            Edges(
                workplane,
                name="%s_0" % cad_obj.name,
                color=color,
            )
        ]
    else:
        if cad_obj.color is None:
            if default_color is None:
                color = Color(get_default("default_color"))
            else:
                color = Color(default_color)
        else:
            color = Color(get_rgba(cad_obj.color))
        parent = [
            Part(
                Workplane(shape),
                "%s_%d" % (cad_obj.name, i),
                color=color,
            )
            for i, shape in enumerate(cad_obj.shapes)
        ]

    if render_mates and cad_obj.mates is not None:
        rgb = (Color((255, 0, 0)), Color((0, 128, 0)), Color((0, 0, 255)))
        pg = PartGroup(
            [
                Edges(
                    to_edge(mate_def.mate, scale=mate_scale),
                    name=name,
                    width=3,
                    color=rgb,
                )
                for name, mate_def in top.mates.items()
                if mate_def.assembly == cad_obj
            ],
            name="mates",
            loc=Location(),  # mates inherit the parent location, so actually add a no-op
        )
        if pg.objects:
            parent.append(pg)

    children = [from_assembly(c, top, loc, render_mates, mate_scale) for c in cad_obj.children]
    return PartGroup(parent + children, cad_obj.name, loc=render_loc)


def _from_workplane(
    cad_obj,
    obj_id,
    name="Part",
    color=None,
    alpha=None,
    default_color=None,
    show_parent=False,
):
    color = get_color(color, default_color, alpha)

    result = Part(cad_obj, "%s_%d" % (name, obj_id), color=color)
    # if show_parent:
    #     result = _parent(cad_obj, obj_id) + result
    return result


def _is_solidlist(cad_obj):
    return (
        hasattr(cad_obj, "objects")
        and cad_obj.objects != []
        and all([isinstance(obj, Solid) for obj in cad_obj.objects])
    )


def _is_facelist(cad_obj):
    return (
        hasattr(cad_obj, "objects")
        and cad_obj.objects != []
        and all([isinstance(obj, Face) for obj in cad_obj.objects])
    )


def _is_vertexlist(cad_obj):
    return (
        hasattr(cad_obj, "objects")
        and cad_obj.objects != []
        and all([isinstance(obj, Vertex) for obj in cad_obj.objects])
    )


def _is_edgelist(cad_obj):
    return (
        hasattr(cad_obj, "objects")
        and cad_obj.objects != []
        and all([isinstance(obj, Edge) for obj in cad_obj.objects])
    )


def _is_wirelist(cad_obj):
    return (
        hasattr(cad_obj, "objects")
        and cad_obj.objects != []
        and all([isinstance(obj, Wire) for obj in cad_obj.objects])
    )


def _debug(msg):
    # print("DEBUG:", msg)
    pass


def to_assembly(
    *cad_objs,
    names=None,
    colors=None,
    alphas=None,
    name="Group",
    render_mates=None,
    mate_scale=1,
    default_color=None,
    show_parent=True,
):
    if names is None:
        names = [None] * len(cad_objs)

    if colors is None:
        colors = [None] * len(cad_objs)

    if alphas is None:
        alphas = [1.0] * len(cad_objs)

    default_color = get_default("default_color") if default_color is None else default_color
    assembly = PartGroup([], name)
    obj_id = 0

    for obj_name, obj_color, obj_alpha, cad_obj in zip(names, colors, alphas, cad_objs):

        # Handle build123d objects and convert them to a format support by the following conversions

        if HAS_BUILD123D:

            if hasattr(cad_obj, "_obj_name"):  # BuildPart, BuildSketch, BuildLine
                _debug(f"CAD Obj {obj_id}: {type(cad_obj)}")
                cad_obj = getattr(cad_obj, cad_obj._obj_name)
                if not isinstance(cad_obj, bd.Compound):
                    cad_obj = Shape.cast(cad_obj.wrapped)

            elif isinstance(cad_obj, bd.ShapeList):
                cad_obj = cq_wrap([Shape.cast(obj.wrapped) for obj in cad_obj])

            if isinstance(cad_obj, bd.Shape):
                _debug(f"CAD Obj {obj_id}: build123d.Shape (Solid, Face, Wire, Edge, Vertex)")
                if isinstance(cad_obj, bd.Compound):
                    t = type(list(cad_obj)[0])
                    if all(isinstance(obj, t) for obj in cad_obj):
                        cad_obj = cq_wrap([Shape.cast(obj.wrapped) for obj in cad_obj])
                    else:
                        cad_obj = Shape.cast(cad_obj.wrapped)
                else:
                    cad_obj = Shape.cast(cad_obj.wrapped)

        if HAS_ALG123D:
            if isinstance(cad_obj, (ad.MAssembly, ad.Mate)):
                _debug(f"CAD Obj {obj_id}: alg123d MAssembly or Mate")
                cad_obj = convert_alg123d_massembly(cad_obj)

        # Handle TopDS_Compound

        if is_compound(cad_obj):
            _debug(f"CAD Obj {obj_id}: TopoDS Compound")

            if next(get_solids(cad_obj), None) is not None:
                objs = get_solids(cad_obj)

            elif next(get_faces(cad_obj), None) is not None:
                objs = get_faces(cad_obj)

            elif next(get_wires(cad_obj), None) is not None:
                objs = get_wires(cad_obj)

            elif next(get_edges(cad_obj), None) is not None:
                objs = get_edges(cad_obj)

            elif next(get_vertices(cad_obj), None) is not None:
                objs = get_vertices(cad_obj)

            else:
                raise NotImplementedError("Unknow TopoDS Compund")

            cad_obj = cq_wrap([Shape.cast(obj) for obj in objs])

        elif is_shape(cad_obj):
            _debug(f"CAD Obj {obj_id}: TopoDS Shape")
            cad_obj = Shape.cast(cad_obj)

        # Conversions

        if isinstance(cad_obj, (PartGroup, Part, Faces, Edges, Vertices)):
            _debug(f"CAD Obj {obj_id}: PartGroup, Part, Faces, Edges, Vertices")
            assembly.add(cad_obj)

        elif HAS_MASSEMBLY and isinstance(cad_obj, MAssembly):
            _debug(f"CAD Obj {obj_id}: MAssembly")
            assembly.add(
                from_assembly(
                    cad_obj,
                    cad_obj,
                    render_mates=render_mates,
                    mate_scale=mate_scale,
                    default_color=default_color,
                )
            )

        elif HAS_MASSEMBLY and isinstance(cad_obj, Mate):
            _debug(f"CAD Obj {obj_id}: Mate")
            obj_name = "Mate_%d" % obj_id if obj_name is None else obj_name
            assembly.add(_from_mate(cad_obj, name=obj_name, mate_scale=mate_scale))

        elif isinstance(cad_obj, CqAssembly):
            _debug(f"CAD Obj {obj_id}: cqAssembly")
            assembly.add(from_assembly(cad_obj, cad_obj, default_color=default_color))

        elif isinstance(cad_obj, Sketch):
            _debug(f"CAD Obj {obj_id}: Sketch")
            assembly.add_list(
                _from_sketch(
                    cad_obj,
                    obj_id,
                    obj_color,
                    obj_alpha,
                    show_parent=show_parent,
                )
            )

        elif isinstance(cad_obj, Face):
            _debug(f"CAD Obj {obj_id}: Face")
            obj_name = "Faces" if obj_name is None else obj_name
            assembly.add_list(
                _from_facelist(
                    Workplane(cad_obj),
                    obj_id,
                    obj_name,
                    obj_color,
                    obj_alpha,
                    show_parent=show_parent,
                )
            )

        elif isinstance(cad_obj, Wire):
            _debug(f"CAD Obj {obj_id}: Wire")
            obj_name = "Wires" if obj_name is None else obj_name
            assembly.add_list(
                _from_wirelist(
                    Workplane(cad_obj),
                    obj_id,
                    obj_name,
                    obj_color,
                    show_parent=show_parent,
                )
            )

        elif isinstance(cad_obj, Edge):
            _debug(f"CAD Obj {obj_id}: Edge")
            obj_name = "Edges" if obj_name is None else obj_name
            assembly.add_list(
                _from_edgelist(
                    Workplane(cad_obj),
                    obj_id,
                    obj_name,
                    obj_color,
                    show_parent=show_parent,
                )
            )

        elif isinstance(cad_obj, Vertex):
            _debug(f"CAD Obj {obj_id}: Vertex")
            obj_name = "Vertices" if obj_name is None else obj_name
            assembly.add_list(
                _from_vertexlist(
                    Workplane(cad_obj),
                    obj_id,
                    obj_name,
                    obj_color,
                    show_parent=show_parent,
                )
            )

        elif _is_solidlist(cad_obj) and len(cad_obj.objects) > 1:
            _debug(f"CAD Obj {obj_id}: solidlist")
            obj_name = "Solids" if obj_name is None else obj_name
            assembly.add_list(
                _from_solidlist(
                    cad_obj,
                    obj_id,
                    obj_name,
                    obj_color,
                    obj_alpha,
                    show_parent=show_parent,
                )
            )

        elif _is_facelist(cad_obj):
            _debug(f"CAD Obj {obj_id}: facelist")
            obj_name = "Faces" if obj_name is None else obj_name
            assembly.add_list(
                _from_facelist(
                    cad_obj,
                    obj_id,
                    obj_name,
                    obj_color,
                    obj_alpha,
                    show_parent=show_parent,
                )
            )

        elif _is_edgelist(cad_obj):
            _debug(f"CAD Obj {obj_id}: edgelist")
            obj_name = "Edges" if obj_name is None else obj_name
            assembly.add_list(_from_edgelist(cad_obj, obj_id, obj_name, obj_color, show_parent=show_parent))

        elif _is_wirelist(cad_obj):
            _debug(f"CAD Obj {obj_id}: wirelist")
            obj_name = "Wires" if obj_name is None else obj_name
            assembly.add_list(_from_wirelist(cad_obj, obj_id, obj_name, obj_color, show_parent=show_parent))

        elif _is_vertexlist(cad_obj):
            _debug(f"CAD Obj {obj_id}: vertexlist")
            obj_name = "Vertices" if obj_name is None else obj_name
            assembly.add_list(_from_vertexlist(cad_obj, obj_id, obj_name, obj_color, show_parent=show_parent))

        elif isinstance(cad_obj, Vector):
            _debug(f"CAD Obj {obj_id}: Vector")
            obj_name = "Vector" if obj_name is None else obj_name
            assembly.add_list(_from_vector(cad_obj, obj_id, obj_name, obj_color, show_parent=show_parent))

        elif isinstance(cad_obj, Compound):
            _debug(f"CAD Obj {obj_id}: Compound")
            obj_name = "Group" if obj_name is None else obj_name
            show_parent = False
            assembly2 = PartGroup([], name="%s_%s" % (obj_name, obj_id))
            for i, obj in enumerate(cad_obj):
                w = Workplane(obj)
                if isinstance(obj, Vertex):
                    assembly2.add_list(_from_vertexlist(w, i, "Vertices", obj_color, show_parent=show_parent))

                elif isinstance(obj, Edge):
                    assembly2.add_list(_from_edgelist(Workplane(obj), i, "Edges", obj_color, show_parent=show_parent))

                elif isinstance(obj, Wire):
                    assembly2.add_list(_from_wirelist(w, i, "Wires", obj_color, show_parent=show_parent))

                elif isinstance(obj, Face):
                    assembly2.add_list(_from_facelist(w, i, "Faces", obj_color, obj_alpha, show_parent=show_parent))

                elif isinstance(obj, Solid):
                    assembly2.add_list(_from_solidlist(w, i, "Solids", obj_color, obj_alpha, show_parent=show_parent))

            assembly.add(assembly2)

        elif isinstance(cad_obj, Shape):
            _debug(f"CAD Obj {obj_id}: Shape")
            obj_name = "Part" if obj_name is None else obj_name
            assembly.add(
                _from_workplane(
                    Workplane(cad_obj),
                    obj_id,
                    obj_name,
                    obj_color,
                    obj_alpha,
                    default_color=default_color,
                    show_parent=show_parent,
                )
            )

        elif hasattr(cad_obj, "val") and isinstance(cad_obj.val(), Vector):
            _debug(f"CAD Obj {obj_id}: Vector val()")
            obj_name = "Vector" if obj_name is None else obj_name
            assembly.add_list(
                _from_vectorlist(
                    cad_obj,
                    obj_id,
                    obj_name,
                    obj_color,
                    show_parent=show_parent,
                )
            )

        elif isinstance(cad_obj, Workplane):
            _debug(f"CAD Obj {obj_id}: Workplane")
            obj_name = "Part" if obj_name is None else obj_name
            if len(cad_obj.vals()) == 1 and not isinstance(cad_obj.val(), Sketch):
                assembly.add(
                    _from_workplane(
                        cad_obj,
                        obj_id,
                        obj_name,
                        obj_color,
                        obj_alpha,
                        default_color=default_color,
                        show_parent=show_parent,
                    )
                )
            else:
                assembly2 = PartGroup([], name="Group_%s" % obj_id)
                for j, obj in enumerate(cad_obj.vals()):
                    if isinstance(obj, Sketch):
                        for sketch_obj in _from_sketch(obj, j, show_parent=False):
                            assembly2.add(sketch_obj)
                    else:
                        assembly2.add(
                            _from_workplane(
                                Workplane(obj),
                                j,
                                obj_name,
                                obj_color,
                                obj_alpha,
                                default_color=default_color,
                                show_parent=show_parent,
                            )
                        )
                assembly.add(assembly2)

        else:
            raise NotImplementedError("Type:", cad_obj)

        obj_id += 1
    return assembly


def show(*cad_objs, names=None, colors=None, alphas=None, cache: Optional[LRUCache] = None, **kwargs):
    """Show CAD objects in Jupyter

    Valid keywords:

    DISPLAY OPTIONS
    - viewer:             Name of the sidecar viewer (default=""):
                          "" uses the default sidecar (if exists) and None forces to use notebook cell
    - anchor:             How to open sidecar: "right", "split-right", "split-bottom", ... (default="right")
    - cad_width:          Width of CAD view part of the view (default=800)
    - tree_width:         Width of navigation tree part of the view (default=250)
    - height:             Height of the CAD view (default=600)
    - theme:              Theme "light" or "dark" (default="light")
    - pinning:            Allow replacing the CAD View by a canvas screenshot (default=True in cells, else False)

    TESSELLATION OPTIONS
    - angular_tolerance:  Shapes: Angular deflection in radians for tessellation (default=0.2)
    - deviation:          Shapes: Deviation from linear deflection value (default=0.1)
    - edge_accuracy:      Edges: Precision of edge discretization (default=None, i.e. mesh quality / 100)
    - default_color:      Default face color (default=(232, 176, 36))
    - default_edge_color: Default edge color (default="#707070")
    - optimal_bb:         Use optimal bounding box (default=False)
    - render_normals:     Render vertex normals(default=False)
    - render_edges:       Render edges  (default=True)
    - render_mates:       Render mates (for MAssemblies, default=False)
    - mate_scale:         Scale of rendered mates (for MAssemblies, default=1)

    VIEWER OPTIONS
    - control:            Use trackball controls ('trackball') or orbit controls ('orbit') (default='trackball')
    - up:                 Use z-axis ('Z') or y-axis ('Y') as up direction for the camera (or 'L' for legacy z-axis up mode)
    - axes:               Show axes (default=False)
    - axes0:              Show axes at (0,0,0) (default=False)
    - grid:               Show grid (default=[False, False, False])
    - ticks:              Hint for the number of ticks in both directions (default=10)
    - ortho:              Use orthographic projections (default=True)
    - transparent:        Show objects transparent (default=False)
    - black_edges:        Show edges in black (default=False)
    - position:           Absolute camera position that will be scaled (default=None)
    - quaternion:         Camera rotation as quaternion (x, y, z, w) (default=None)
    - target:             Camera target to look at (default=None)
    - zoom:               Zoom factor of view (default=2.5)
    - reset_camera:       Reset camera position, rotation and zoom to default (default=True)
    - zoom_speed:         Mouse zoom speed (default=1.0)
    - pan_speed:          Mouse pan speed (default=1.0)
    - rotate_speed:       Mouse rotate speed (default=1.0)
    - ambient_intensity   Intensity of ambient light (default=0.75)
    - direct_intensity    Intensity of direct lights (default=0.15)
    - show_parent:        Show the parent for edges, faces and vertices objects
    - show_bbox:          Show bounding box (default=False)
    - collapse:           Collapse CAD tree (1: collapse nodes with single leaf, 2: collapse all nodes)
    - cad_width:          Width of CAD view part of the view (default=800)
    - tree_width:         Width of navigation tree part of the view (default=250)
    - height:             Height of the CAD view (default=600)
    - tools:              Show the viewer tools like the object tree (default=True)
    - glass:              Show the viewer in glass mode, i.e (CAD navigation as transparent overlay (default=False)
    - timeit:             Show rendering times, levels = False, 0,1,2,3,4,5 (default=False)
    - parallel:           (Linux only) Whether to use multiprocessing for parallel tessellation
    - js_debug:           Enable debug output in browser console (default=False)

    NOT SUPPORTED ANY MORE:
    - mac_scrollbar       The default now
    - bb_factor:          Removed
    - display             Use 'viewer="<viewer title>"' (for sidecar display) or 'viewer=None' (for cell display)
    - quality             Use 'deviation'to control smoothness of rendered edges
    """

    render_mates = preset("render_mates", kwargs.get("render_mates"))
    mate_scale = preset("mate_scale", kwargs.get("mate_scale"))
    default_color = preset("default_color", kwargs.get("default_color"))
    show_parent = preset("show_parent", kwargs.get("show_parent"))

    if isinstance(kwargs.get("grid"), bool):
        warn(
            "Using bool for grid is deprecated, please use (xy-grid, xz-grid. yz-grid)",
            DeprecationWarning,
            "once",
        )
        kwargs["grid"] = (kwargs["grid"], False, False)

    if cad_objs:

        assembly = to_assembly(
            *cad_objs,
            names=names,
            colors=colors,
            alphas=alphas,
            render_mates=render_mates,
            mate_scale=mate_scale,
            default_color=default_color,
            show_parent=show_parent,
        )

        if assembly is None:
            raise ValueError("%s cannot be viewed" % cad_objs)

        if len(assembly.objects) == 1 and isinstance(assembly.objects[0], PartGroup):
            # omit leading "PartGroup" group
            return _show(assembly.objects[0], cache=cache, **kwargs)
        else:
            return _show(assembly, cache=cache, **kwargs)

    else:

        return _show(None, cache=cache, **kwargs)


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

    show(
        *OBJECTS["objs"],
        names=OBJECTS["names"],
        colors=OBJECTS["colors"],
        alphas=OBJECTS["alphas"],
        **kwargs,
    )
