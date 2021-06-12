"""
Shape Keys Plus add-on for Duplicating and Mirroring Shape Keys.
Copyright (C) 2021  Lukas Bilek. BILEK STUDIO.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from . import shape_keys_plus_main

# Info about the add-on
bl_info = {
    "name": "Shape Keys Plus",
    "description": "This tool is for duplicating and miroring shape keys with L-R prefixes and suffixes",
    "author": "© Lukas Bilek 2021. BILEK STUDIO. All rights reserved.",
    "version": (0, 2, 1),
    "blender": (2, 92, 0),
    # "location": "Shape Keys > Shape Keys Specials > Easy Blendshapes",
    # "warning": "", # used for warning icon and text in addons panel
    # "support": "COMMUNITY",
    "category": "Object",
}
import bpy
from .shape_keys_plus_main import (WindowInfo,
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
