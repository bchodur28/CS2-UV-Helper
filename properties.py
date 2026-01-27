import bpy
from bpy.props import EnumProperty, FloatProperty, BoolProperty

def get_screen_resolution_dropdown_options():
    return [
        ('512', '512px', 'Screen resolution of 512px'),
        ('1024', '1024px', 'Screen resolution of 1024px'),
        ('2048', '2048px', 'Screen resolution of 2048px'),
        ('4096', '4096px', 'Screen resolution of 4096px'),
    ]

def get_coord_options():
    return [
        ('UV_COORD', 'UV Coordinates', 'Uses UV coordinates to decide the tiling order for Islands'),
        ('WORLD_COORD', 'World Coordinates', 'Uses world coordinates to decide the tiling order for Islands'),
    ]

class CS2_PG_Properties(bpy.types.PropertyGroup):
    screen_resolution: EnumProperty(
        name="Screen Resolution",
        description= "Select a Resolution",
        items=get_screen_resolution_dropdown_options(),
        default='4096'
    )

    coord_system: EnumProperty(
        name="Coordinate System",
        description="What coordinate to use for tiling the islands",
        items=get_coord_options(),
        default='UV_COORD'
    )

    material_length: FloatProperty(
        name="Material Length (cm)",
        description="Length of the material in centimeters",
        default=2.0,
        min=1.0,
        soft_max=1000.0,
        precision=1,
        unit='LENGTH'
    )

    material_height: FloatProperty(
        name="Material Height (cm)",
        description="Height of the material in centimeters",
        default=2.0,
        min=1.0,
        soft_max=1000.0,
        precision=1,
        unit='LENGTH'
    )

    merge_threshold: FloatProperty(
        name="Merge Threshold",
        description="Threshold for determining if face is part of island (default .001)",
        default=0.001,
        min=0.0,
        soft_max=1,
        precision=3,
        step=0.001,
    )

    grid_padding: FloatProperty(
         name="Grid Padding",
         description="Padding between UV islands in grid alignment",
         default=0.003,
         min=0.0,
         precision=3,
         step=0.001,
    )

    use_auto_align: BoolProperty(
        name="Auto Align",
        description="Only for Vertical Align. Aligns islands to bottom corner before shuffle calculation. NOTE: leave unchecked if first alignment was horizontal.",
        default=False
    )

    show_separation: bpy.props.BoolProperty(
        name="Show Separation",
        default=True
    )

    show_seamless_align: bpy.props.BoolProperty(
        name="Show Alignment",
        default=True
    )

    show_grid_alignment: bpy.props.BoolProperty(
        name="Show Grid Alignment",
        default=True
    )

    randomize_grid_items: bpy.props.BoolProperty(
        name="Randomized Grid Items",
        description="True will ensure items in grid are randomized.",
        default=True
    )

def register():
        bpy.utils.register_class(CS2_PG_Properties)
        bpy.types.Scene.cs2_pg_properties = bpy.props.PointerProperty(type=CS2_PG_Properties)


def unregister():
    if hasattr(bpy.types.Scene, "cs2_pg_properties"):
        del bpy.types.Scene.cs2_pg_properties
    bpy.utils.unregister_class(CS2_PG_Properties)
