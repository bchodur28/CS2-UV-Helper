import bpy

from .utils import (get_active_bmesh, get_horizontal_edges, get_vertical_edges, update_active_bmesh)
from .uv_helper import (align_selected_uvs_for_seamless_tiling, separate_selected_uv_faces, align_uvs_in_grid)

import bpy
import importlib

class CS2_OT_NewFeature(bpy.types.Operator):
    bl_idname = "cs2.new_feature"
    bl_label = "New Feature"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        # Implement the new feature logic here
        active_bmesh = get_active_bmesh()
        if active_bmesh:
            edges = get_horizontal_edges(active_bmesh, limiting_axis="X", max_angle_deviation=5.0)
            for edge in edges:
                edge.select = True
            update_active_bmesh()
            
        return {'FINISHED'}

# Temporally for developement use
# class CS2_OT_ReloadAddon(bpy.types.Operator):
#     bl_idname = "cs2.reload_addon"
#     bl_label = "Reload Cities Skylines 2"

#     def execute(self, context):
#         from . import uv_helper, utils, properties, panels, operators

#         # Reload helper modules first
#         importlib.reload(utils)
#         importlib.reload(uv_helper)

#         # Reload modules that define Blender classes
#         importlib.reload(properties)
#         importlib.reload(operators)
#         importlib.reload(panels)

#         # Unregister & re-register all classes
#         for m in [properties, operators, panels]:
#             try:
#                 m.unregister()
#             except Exception:
#                 pass
#             m.register()

#         self.report({'INFO'}, "CS2 Addon reloaded")
#         return {'FINISHED'}

# def register():
#     bpy.utils.register_class(CS2_OT_ReloadAddon)

# def unregister():
#     bpy.utils.unregister_class(CS2_OT_ReloadAddon)


class CS2_OT_align_uvs_horizontal(bpy.types.Operator):
    """Tooltip for the operator"""
    bl_idname = "cs2.align_uvs_horizontal"
    bl_label = "Align UVs horizontally for Seamless Tiling"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        align_selected_uvs_for_seamless_tiling(context)

        return {'FINISHED'}
    
class CS2_OT_align_uvs_vertical(bpy.types.Operator):
    """Tooltip for the operator"""
    bl_idname = "cs2.align_uvs_vertical"
    bl_label = "Align UVs vertically for Seamless Tiling"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        align_selected_uvs_for_seamless_tiling(context, False)

        return {'FINISHED'}
    
class CS2_OT_separate_uv_horizontal(bpy.types.Operator):
    """Tooltip for the operator"""
    bl_idname = "cs2.separate_uv_horizontal"
    bl_label = "Seperate the uvs horizontally by a fix amount"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        separate_selected_uv_faces(horizontal=True)

        return {'FINISHED'}

class CS2_OT_separate_uv_vertical(bpy.types.Operator):
    """Tooltip for the operator"""
    bl_idname = "cs2.separate_uv_vertical"
    bl_label = "Seperate the uvs vertically by a fix amount"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        separate_selected_uv_faces()

        return {'FINISHED'}
    
class CS2_OT_align_uvs_in_grid(bpy.types.Operator):
    """Tooltip for the operator"""
    bl_idname = "cs2.align_uvs_in_grid"
    bl_label = "Align UVs in Grid"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        align_uvs_in_grid(context)
        return {'FINISHED'}

def register():
    bpy.utils.register_class(CS2_OT_align_uvs_horizontal)
    bpy.utils.register_class(CS2_OT_align_uvs_vertical)
    bpy.utils.register_class(CS2_OT_separate_uv_horizontal)
    bpy.utils.register_class(CS2_OT_separate_uv_vertical)
    bpy.utils.register_class(CS2_OT_align_uvs_in_grid)
    #bpy.utils.register_class(CS2_OT_ReloadAddon)
    bpy.utils.register_class(CS2_OT_NewFeature)

def unregister():
    bpy.utils.unregister_class(CS2_OT_align_uvs_horizontal)
    bpy.utils.unregister_class(CS2_OT_align_uvs_vertical)
    bpy.utils.unregister_class(CS2_OT_separate_uv_horizontal)
    bpy.utils.unregister_class(CS2_OT_separate_uv_vertical)
    bpy.utils.unregister_class(CS2_OT_align_uvs_in_grid)
    #bpy.utils.unregister_class(CS2_OT_ReloadAddon)
    bpy.utils.unregister_class(CS2_OT_NewFeature)