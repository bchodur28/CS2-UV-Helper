import bpy
import bmesh
from typing import List
from mathutils import Vector
import math
import random
import numpy as np
from .properties import CS2_PG_Properties
from .utils import get_active_bmesh, get_active_object, truncate

class UvIsland:
    def __init__(self):
        self.faces: List[bmesh.types.BMFace] = []
        self.uv_coord = Vector((0,0))
        self.world_coord = Vector((0,0,0))
        self.uv_dimension = Vector((0,0))
        self.normal = Vector((0.0, 0.0, 0.0))
        self.face_count = 0

def separate_selected_uv_faces(horizontal=False):
    active_object = bpy.context.active_object
    bm = bmesh.from_edit_mesh(active_object.data)
    
    selected_faces = [face for face in bm.faces if face.select]

    uv_layer = bm.loops.layers.uv.verify()

    uv_verts = {}

    for face in selected_faces:
        uv_coords = [loop[uv_layer].uv for loop in face.loops]
        
        centroid = Vector((0.0, 0.0))
        for uv in uv_coords:
            centroid += Vector((uv.x, uv.y))

        centroid /= len(uv_coords)

        key = truncate(centroid.x if horizontal else centroid.y, 1)
        print(f'Key: {key}')
        uv_verts.setdefault(key, []).extend(uv_coords)

    offset = 0.1
    for index, key in enumerate(sorted(uv_verts.keys())):
        move_amount = index * offset
        for uv in uv_verts[key]:
            if horizontal:
                uv.x += move_amount
            else:
                uv.y += move_amount
    
    bmesh.update_edit_mesh(active_object.data)

def align_selected_uvs_for_seamless_tiling(context: bpy.types.Context, horizontal: bool = True):
    active_object = bpy.context.active_object
    bm = bmesh.from_edit_mesh(active_object.data)

    material_length_cm = float(context.scene.cs2_pg_properties.material_length) * 100.0
    material_height_cm = float(context.scene.cs2_pg_properties.material_height) * 100.0
    screen_resolution = float(context.scene.cs2_pg_properties.screen_resolution)
    merge_threshold = float(context.scene.cs2_pg_properties.merge_threshold)
    texel_density = calculate_texel_density(screen_resolution)

    uv_layer = bm.loops.layers.uv.verify()
    uv_islands = get_selected_uv_islands(merge_threshold)
    print(f"UV Islands count: {len(uv_islands)}")

    texel_size_per_cm = (1.0/screen_resolution) * texel_density
    
    sort_uv_islands_by_uv_coords(uv_islands, horizontal)

    material_length = material_length_cm * texel_size_per_cm
    material_height = material_height_cm * texel_size_per_cm
    
    move = 0.0
    # Bottom left origin
    to_uv_coord = uv_islands[0].uv_coord - (uv_islands[0].uv_dimension / 2.0)
    for island in uv_islands:
        shuffle_amount = (island.uv_dimension.x if horizontal else island.uv_dimension.y) + move

        # Bottom left origin
        island_origin = island.uv_coord - (island.uv_dimension / 2.0)
        direction = island_origin - to_uv_coord

        offset = Vector((move, 0.0)) if horizontal else Vector((0.0, move))
        axis_direction = Vector((direction.x, 0.0)) if horizontal else Vector((0.0, direction.y))

        for face in island.faces:
            for loop in face.loops:
                loop[uv_layer].uv = (loop[uv_layer].uv - axis_direction) + offset

        move = shuffle_amount % (material_length if horizontal else material_height)

    bmesh.update_edit_mesh(active_object.data)
    bm.free()

def align_uvs_in_grid(context: bpy.types.Context, only_selected=True):
    active_object = get_active_object()
    bm = get_active_bmesh()
    if not bm or not active_object:
        return
    
    face_uv_loops = get_face_uv_loops(bm, only_selected=only_selected)
    if len(face_uv_loops) == 0:
        return
    
    randomize = float(context.scene.cs2_pg_properties.randomize_grid_items)
    padding = float(context.scene.cs2_pg_properties.grid_padding)
    print(f"Padding: {padding}")

    if randomize:
        random.shuffle(face_uv_loops)

    starting_location = Vector((0.0, 0.0))
    starting_row_location = starting_location.copy()

    num_of_rows = math.floor(math.sqrt(len(face_uv_loops)))

    next_row_height = 0
    for i, face_uvs in enumerate(face_uv_loops):
        face_uv_bottom_left = get_face_uv_bottom_left_origin(face_uvs)
        width, height = calculate_face_uv_dimensions(face_uvs)
        next_row_height = max(height, next_row_height)

        shift_x = width + padding
        move_to = starting_location - face_uv_bottom_left
        for loops in face_uvs:
            loops.uv += move_to
        if (i + 1) % num_of_rows == 0:
            starting_location = starting_row_location + Vector((0, next_row_height + padding))
            starting_row_location = starting_location.copy()
            next_row_height = 0
        else:
            starting_location += Vector((shift_x, 0))

    bmesh.update_edit_mesh(active_object.data)

def get_selected_uv_islands(merge_threshold=0.0):
    active_object = bpy.context.active_object
    bm = bmesh.from_edit_mesh(active_object.data)
    world_matrix = active_object.matrix_world

    uv_layer = bm.loops.layers.uv.verify()

    selected_faces = [face for face in bm.faces if face.select]

    islands: List[UvIsland] = []
    visited = set()

    for face in selected_faces:
        if face not in visited:
            island_world_coord = Vector((0.0,0.0,0.0))
            face_count = 0
            island_normal = Vector((0.0, 0.0, 0.0))
            island = UvIsland()
            stack = [face]
            min_uv_x = float("inf")
            min_uv_y = float("inf")
            max_uv_x = float("-inf")
            max_uv_y = float("-inf")

            while stack:
                current_face = stack.pop()
                if current_face not in visited:
                    visited.add(current_face)
                    island.faces.append(current_face)
                    face_count += 1

                    island_normal += current_face.normal @ world_matrix.to_3x3()

                    # Calculate the centroid of the current face
                    face_center = sum((world_matrix @ loop.vert.co for loop in current_face.loops), Vector((0.0, 0.0, 0.0))) / len(current_face.loops)
                    island_world_coord += face_center  # Sum the face centers

                    for loop in current_face.loops:

                        uv = loop[uv_layer].uv

                        min_uv_x = min(min_uv_x, uv.x)
                        min_uv_y = min(min_uv_y, uv.y)
                        max_uv_x = max(max_uv_x, uv.x)
                        max_uv_y = max(max_uv_y, uv.y)

                        for neighbor_loop in loop.vert.link_loops:
                            neighbor_face = neighbor_loop.face
                            neighbor_uv = neighbor_loop[uv_layer].uv

                            if (neighbor_face not in visited and (neighbor_uv - uv).length < 0.001):
                                stack.append(neighbor_face)

            island_normal.normalize()
            uv_dimension = Vector((max_uv_x - min_uv_x, max_uv_y - min_uv_y))
            island.uv_dimension = uv_dimension
            island.uv_coord = (uv_dimension / 2.0) + Vector((min_uv_x, min_uv_y))
            island.world_coord = island_world_coord / face_count
            island.normal = island_normal
            island.face_count = face_count
            islands.append(island)

    if merge_threshold > 0.0:
        merged_islands = []
        while islands:
            island = islands.pop(0)
            merged = False

            for other_island in merged_islands:
                if uv_islands_overlap(island, other_island, merge_threshold):
                    # Merge into existing island
                    other_island.faces.extend(island.faces)
                    
                    # Recalculate properties after merging
                    all_faces = other_island.faces
                    min_uv_x = min(loop[uv_layer].uv.x for face in all_faces for loop in face.loops)
                    min_uv_y = min(loop[uv_layer].uv.y for face in all_faces for loop in face.loops)
                    max_uv_x = max(loop[uv_layer].uv.x for face in all_faces for loop in face.loops)
                    max_uv_y = max(loop[uv_layer].uv.y for face in all_faces for loop in face.loops)

                    other_island.uv_dimension = Vector((max_uv_x - min_uv_x, max_uv_y - min_uv_y))
                    other_island.uv_coord = (other_island.uv_dimension / 2.0) + Vector((min_uv_x, min_uv_y))

                    total_world_coord = sum((world_matrix @ loop.vert.co for face in all_faces for loop in face.loops), Vector((0.0, 0.0, 0.0)))
                    total_verts = sum(len(face.loops) for face in all_faces)
                    other_island.world_coord = total_world_coord / total_verts if total_verts > 0 else Vector((0.0, 0.0, 0.0))

                    merged = True
                    break
            
            if not merged:
                merged_islands.append(island)

        return merged_islands
    print(f"Island Count is: {len(islands)}")
    return islands

def uv_islands_overlap(island1, island2, threshold):
    """Returns True if two UV islands overlap within the given threshold."""
    min1, max1 = island1.uv_coord - (island1.uv_dimension / 2), island1.uv_coord + (island1.uv_dimension / 2)
    min2, max2 = island2.uv_coord - (island2.uv_dimension / 2), island2.uv_coord + (island2.uv_dimension / 2)

    # Check if bounding boxes overlap within the threshold
    return (
        (max1.x + threshold > min2.x and min1.x - threshold < max2.x) and
        (max1.y + threshold > min2.y and min1.y - threshold < max2.y)
    )

def sort_uv_islands_by_uv_coords(uv_islands: List[UvIsland], horizontally: bool = True):
    if len(uv_islands) <= 1:
        return uv_islands
    
    if horizontally:
        uv_islands.sort(key=get_x_uv)
    else:
        uv_islands.sort(key=get_y_uv)

def calculate_texel_density(resolution=1024):
    active_object = bpy.context.active_object
    bm = bmesh.from_edit_mesh(active_object.data)
    uv_layer = bm.loops.layers.uv.active
    
    if not uv_layer:
        return 0.0
    
    selected_faces = [f for f in bm.faces if f.select]
    if not selected_faces:
        return 0.0
    
    total_texel_density = 0.0
    num_edges = 0
    
    for face in selected_faces:
        # Get UV and 3D vertices
        loops = face.loops
        for i in range(len(loops)):
            # Current and next loop (for edge length)
            loop1 = loops[i]
            loop2 = loops[(i + 1) % len(loops)]
            
            # UV space edge length (in pixels)
            uv1 = loop1[uv_layer].uv
            uv2 = loop2[uv_layer].uv
            uv_edge_length_px = (uv2 - uv1).length * resolution
            
            # 3D space edge length (in world units)
            v1 = loop1.vert.co
            v2 = loop2.vert.co
            world_edge_length = (v2 - v1).length
            
            # Avoid division by zero
            if world_edge_length > 0:
                texel_density = uv_edge_length_px / world_edge_length
                total_texel_density += texel_density
                num_edges += 1
    
    if num_edges == 0:
        return 0.0
    
    avg_texel_density = total_texel_density / num_edges
    # pixels / cm
    return round(avg_texel_density / 100.0, 3)

def calculate_face_uv_dimensions(face_uvs: list[bmesh.types.BMLoop]) -> tuple[float, float]:
    if not face_uvs:
        return (0.0,0.0)
    
    min_uv_x = min(loop.uv.x for loop in face_uvs)
    max_uv_x = max(loop.uv.x for loop in face_uvs)
    min_uv_y = min(loop.uv.y for loop in face_uvs)
    max_uv_y = max(loop.uv.y for loop in face_uvs)

    return (max_uv_x - min_uv_x, max_uv_y - min_uv_y)

def get_face_uv_loops(bm: bmesh.types.BMesh, only_selected=True) -> list[list[bmesh.types.BMLoop]]:
    uv_layer = bm.loops.layers.uv.active
    if not uv_layer:
        print("No active UV layer found.")
        return []

    uv_faces = []
    for face in bm.faces:
        if only_selected and not face.select:
            continue
        face_uvs = [loop[uv_layer] for loop in face.loops]
        uv_faces.append(face_uvs)

    return uv_faces

def get_face_uv_bottom_left_origin(face_uvs: list[bmesh.types.BMLoop]) -> Vector:
    if not face_uvs:
        return Vector((0.0, 0.0))

    min_uv_x = min(loop.uv.x for loop in face_uvs)
    min_uv_y = min(loop.uv.y for loop in face_uvs)

    return Vector((min_uv_x, min_uv_y))

def get_x_uv(uv_island: UvIsland):
    return uv_island.uv_coord.x

def get_y_uv(uv_island: UvIsland):
    return uv_island.uv_coord.y