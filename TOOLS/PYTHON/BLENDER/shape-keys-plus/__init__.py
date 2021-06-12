from . import shape_keys_plus_main
# Info about the add-on
bl_info = {
    "name": "Shape Keys Plus",
    "description": "This tool is for duplicating and miroring shape keys with L-R prefixes and suffixes",
    "author": "© Lukas Bilek 2021. BILEK STUDIO. All rights reserved.",
    "version": (0, 2, 0),
    "blender": (2, 92, 0),
    # "location": "Shape Kyes > Shape Keys Specials > Easy Blendshapes",
    #"warning": "", # used for warning icon and text in addons panel
    #"support": "COMMUNITY",
    "category": "Object",
}
import bpy
from . shape_keys_plus_main import (WindowInfo,
           EasyShapeKeysPlusLeftSide,
           EasyShapeKeysPlusRightSide,
           MultiplyShapeKeysPlusLeftSide,
           MultiplyShapeKeysPlusRightSide,
           ShapeKeysPlusHelp,
           TOPBAR_MT_BILEK_Tools_menu,
           TOPBAR_MT_Shape_keys_plus_sub_menu,
           BilekStudioAbout,
           SupportBilekStudio)

# List of classes for registering and unregistering
classes = (WindowInfo,
           EasyShapeKeysPlusLeftSide,
           EasyShapeKeysPlusRightSide,
           MultiplyShapeKeysPlusLeftSide,
           MultiplyShapeKeysPlusRightSide,
           ShapeKeysPlusHelp,
           TOPBAR_MT_BILEK_Tools_menu,
           TOPBAR_MT_Shape_keys_plus_sub_menu,
           BilekStudioAbout,
           SupportBilekStudio)

try:
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bpy.types.MESH_MT_shape_key_context_menu.remove(shape_keys_plus_main.menu_func_buttons)

    # Unregister top bar Menu
    bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_BILEK_Tools_menu.menu_draw)
except:
    print('Nothing to unregister')


# This part is for blender registering the add-on and unregistering them as well.
def register():
    # Register classes
    for cls in classes:
        bpy.utils.register_class(cls)

    # Register menu under arrow in the Shape Keys
    bpy.types.MESH_MT_shape_key_context_menu.append(shape_keys_plus_main.menu_func_buttons)

    # Register top bar Menu
    bpy.types.TOPBAR_MT_editor_menus.append(TOPBAR_MT_BILEK_Tools_menu.menu_draw)


# Unregister add-on.
def unregister():
    # Unregister classes
    for cls in classes:
        bpy.utils.unregister_class(cls)

    bpy.types.MESH_MT_shape_key_context_menu.remove(shape_keys_plus_main.menu_func_buttons)

    # Unregister top bar Menu
    bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_BILEK_Tools_menu.menu_draw)


if __name__ == "__main__":
    register()