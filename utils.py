import bpy
import bmesh
from mathutils import Vector
from typing import Literal, Optional, TypedDict
import math

class AxisOptions(TypedDict):
    limiting_axis: Literal['X', 'Y']
    threshold_angle: float

def get_active_object():
    active_object = bpy.context.active_object
    if not active_object or active_object.type != 'MESH':
        print("No active mesh object found.")
        return
    return active_object

def get_active_bmesh():
    active_object = get_active_object()
    if not active_object:
        return None
    return bmesh.from_edit_mesh(active_object.data)

def update_active_bmesh():
    active_object = get_active_object()
    if active_object:
        bmesh.update_edit_mesh(active_object.data)

def get_active_edges(bm: bmesh.types.BMesh, only_selected=True) -> list[bmesh.types.BMEdge]:
    return [e for e in bm.edges if e.select] if only_selected else list(bm.edges)

def truncate(f, n):
    factor = 10 ** n
    return math.trunc(f * factor) / factor

def round_vector_to_unit(vector: Vector, unit_length: float) -> Vector:
    return Vector((
        round(vector.x / unit_length) * unit_length,
        round(vector.y / unit_length) * unit_length,
        round(vector.z / unit_length) * unit_length
    ))

def get_dominant_axis_index(face: bmesh.types.BMFace, use_world_coords=False) -> int:
    if not face.verts:
        return -1

    # Get the normal of the face
    normal = face.normal
    if use_world_coords:
        world_matrix = get_active_object().matrix_world
        normal = world_matrix.to_3x3() @ normal

    # Find the axis with the maximum absolute value
    abs_normal = [abs(normal.x), abs(normal.y), abs(normal.z)]
    axis_index = abs_normal.index(max(abs_normal))

    # XY=2, -XY=-3, XZ=-2, -XZ=1, YZ=0, -YZ=-1
    if [normal.x, normal.y, normal.z][axis_index] < 0:
        return -(axis_index + 1)  # Negative to indicate negative direction, +1 to avoid zero confusion
    else:
        return axis_index
    
def get_sorted_face_corners(face: bmesh.types.BMFace) -> list[Vector]:
    if not face.verts or len(face.verts) < 4:
        return []
    
    world_matrix = get_active_object().matrix_world
    verts_world = [world_matrix @ v.co for v in face.verts]

    axis_index = get_dominant_axis_index(face, use_world_coords=True)
    abs_axis_index = abs(axis_index) - 1 if axis_index < 0 else axis_index

    if abs_axis_index == 0:
        verts_2d = [(v.y, v.z) for v in verts_world]
    elif abs_axis_index == 1:
        verts_2d = [(v.x, v.z) for v in verts_world]
    else:
        verts_2d = [(v.x, v.y) for v in verts_world]

    cx = sum(p[0] for p in verts_2d) / 4
    cy = sum(p[1] for p in verts_2d) / 4

    def angle_from_center(p):
        return math.atan2(p[1] - cy, p[0] - cx)
    
    sorted_indices = sorted(range(4), key=lambda i: angle_from_center(verts_2d[i]))
    sorted_verts_2d = [verts_2d[i] for i in sorted_indices]
    sorted_verts_3d = [verts_world[i] for i in sorted_indices]

    bottom_left_index = min(range(4), key=lambda i: (sorted_verts_2d[i][1], sorted_verts_2d[i][0]))

    sorted_verts_3d = sorted_verts_3d[bottom_left_index:] + sorted_verts_3d[:bottom_left_index]
    sorted_verts_3d = [round_vector_to_unit(v, 0.000001) for v in sorted_verts_3d]

    if axis_index == -3 :
        sorted_verts_3d.reverse()
    elif axis_index == -1 or axis_index == 1:
        # Swap every two vertices
        sorted_verts_3d = [sorted_verts_3d[i+1] if i % 2 == 0 else sorted_verts_3d[i-1] for i in range(len(sorted_verts_3d))]

    return sorted_verts_3d

def get_horizontal_edges(bm: bmesh.types.BMesh, limiting_axis: Literal['X', 'Y'] = None, max_angle_deviation: float = 1.0) -> list[bmesh.types.BMEdge]:
    horizontal_edges = []
    edges = get_active_edges(bm, only_selected=False)
    world_matrix = get_active_object().matrix_world

    for edge in edges:
        if len(edge.verts) != 2:
            continue

        v1, v2 =  edge.verts
        delta = world_matrix @ v2.co - world_matrix @ v1.co
        direction = delta.normalized()
        angle_from_xy = math.degrees(math.asin(abs(direction.z)))

        abs_x_dir = abs(direction.x)
        abs_y_dir = abs(direction.y)
        if limiting_axis is not None:
            if limiting_axis == 'X':
                angle_radians = math.atan2(abs_y_dir, abs_x_dir)
                angle_degrees = math.degrees(angle_radians)
                if angle_degrees <= max_angle_deviation:
                    horizontal_edges.append(edge)
            elif limiting_axis == 'Y':
                angle_radians = math.atan2(abs_x_dir, abs_y_dir)
                angle_degrees = math.degrees(angle_radians)
                if angle_degrees <= max_angle_deviation:
                    horizontal_edges.append(edge)
        else:
            if angle_from_xy <= 5.0:
                horizontal_edges.append(edge)
    
    return horizontal_edges

def get_vertical_edges(bm: bmesh.types.BMesh, max_angle_deviation: float = 1.0) -> list[bmesh.types.BMEdge]:
    vertical_edges = []
    edges = get_active_edges(bm, only_selected=False)
    world_matrix = get_active_object().matrix_world
    z_axis = Vector((0, 0, 1))

    for edge in edges:
        if len(edge.verts) != 2:
            continue

        v1, v2 = edge.verts
        delta = world_matrix @ v2.co - world_matrix @ v1.co
        if delta.length < 1e-6:
            continue

        direction = delta.normalized()
        alignment = abs(direction.dot(z_axis))
        angle = math.degrees(math.acos(alignment))

        if angle <= max_angle_deviation:
            vertical_edges.append(edge)

    return vertical_edges