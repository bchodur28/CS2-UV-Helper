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
    bl_category = "CS2 UV Helper"


    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Seperation Groupig
        box = layout.box()
        row = box.row()
        icon = 'TRIA_DOWN' if scene.cs2_pg_properties.show_separation else 'TRIA_RIGHT'
        row.prop(scene.cs2_pg_properties, "show_separation", text="UV Seperation", icon=icon, emboss=False)

        if scene.cs2_pg_properties.show_separation:
            row = box.row()  
            row.operator("cs2.separate_uv_horizontal", text="Seperate UVs Horizontally")

            row = box.row()  
            row.operator("cs2.separate_uv_vertical", text="Separate UVs Vertically")


        # Seamless Alignment Grouping
        box = layout.box()
        row = box.row()
        icon = 'TRIA_DOWN' if scene.cs2_pg_properties.show_seamless_align else 'TRIA_RIGHT'
        row.prop(scene.cs2_pg_properties, "show_seamless_align", text="UV Seamless Alignment", icon=icon, emboss=False)

        if scene.cs2_pg_properties.show_seamless_align:

            row = box.row()
            row.label(text="Screen Resolution")
            row.prop(scene.cs2_pg_properties, "screen_resolution", text="")

            row = box.row()
            row.prop(scene.cs2_pg_properties, "material_length", text="Material Length")

            row = box.row()
            row.prop(scene.cs2_pg_properties, "material_height", text="Material Height")

            row = box.row()
            row.prop(scene.cs2_pg_properties, "merge_threshold", text="Merge Threshold")

            row = box.row()
            row.operator("cs2.align_uvs_horizontal", text="Align Horizontally")

            row = box.row()
            row.operator("cs2.align_uvs_vertical", text="Align Vertically")

        box = layout.box()
        row = box.row()
        icon = 'TRIA_DOWN' if scene.cs2_pg_properties.show_seamless_align else 'TRIA_RIGHT'
        row.prop(scene.cs2_pg_properties, "show_grid_alignment", text="UV Grid Alignment", icon=icon, emboss=False)

        if scene.cs2_pg_properties.show_grid_alignment:
            row = box.row()
            row.prop(scene.cs2_pg_properties, "grid_padding", text="Grid Padding")

            row = box.row()
            row.prop(scene.cs2_pg_properties, "randomize_grid_items", text="Randomized Grid Items")

            row = box.row()
            row.operator("cs2.align_uvs_in_grid", text="Align in Grid")

        # row = layout.row()
        # row.operator("cs2.reload_addon", text="Reload Addon", icon='FILE_REFRESH')

        # row = layout.row()
        # row.operator("cs2.new_feature", text="Do Something")

def register():
    bpy.utils.register_class(CS2_PT_MainPanel)


def unregister():
    bpy.utils.unregister_class(CS2_PT_MainPanel)


