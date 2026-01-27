import bpy
from .properties import CS2_PG_Properties


class CS2_PT_MainPanel(bpy.types.Panel):
    """Tooltip for the panel"""
    bl_idname = "CS2_PT_main_panel"
    bl_label = "Cities Skylines 2 UV Helper"
    # bl_space_type = "IMAGE_EDITOR"
    # bl_region_type = "UI"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "CS2"


    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.label(text="Screen Resolution")
        layout.prop(scene.seamless_uv_tiler, "screen_resolution", text="")

        row = layout.row()
        layout.prop(scene.seamless_uv_tiler, "material_length", text="Material Length")

        row = layout.row()
        layout.prop(scene.seamless_uv_tiler, "material_height", text="Material Height")

        # Seperation Groupig
        box = layout.box()
        row = box.row()
        icon = 'TRIA_DOWN' if scene.seamless_uv_tiler.show_separation else 'TRIA_RIGHT'
        row.prop(scene.seamless_uv_tiler, "show_separation", text="UV Seperation", icon=icon, emboss=False)

        if scene.seamless_uv_tiler.show_separation:
            row = box.row()  
            row.operator("seamless_uv_tiler.separate_uv_horizontal", text="Seperate UVs Horizontally")

            row = box.row()  
            row.operator("seamless_uv_tiler.separate_uv_vertical", text="Separate UVs Vertically")


        # Alignment Grouping
        box = layout.box()
        box.label(text="Alignment")

        row = box.row()
        row.operator("seamless_uv_tiler.align_uvs_horizontal", text="Align Horizontally")

        row = box.row()
        row.operator("seamless_uv_tiler.align_uvs_vertical", text="Align Vertically")

        row = box.row()
        row.prop(scene.seamless_uv_tiler, "merge_threshold", text="Merge Threshold")

def register():
    bpy.utils.register_class(CS2_PT_MainPanel)

def unregister():
    bpy.utils.unregister_class(CS2_PT_MainPanel)

