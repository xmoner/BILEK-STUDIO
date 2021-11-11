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
import addon_utils
import re
import inspect
import os
# Info about the add-on
bl_info = {
    "name": "Shape Keys Plus",
    "description": "This tool is for duplicating and miroring shape keys with L-R prefixes and suffixes",
    "author": "© Lukas Bilek 2021. BILEK STUDIO. All rights reserved.",
    "version": (0, 2, 2),
    "blender": (2, 92, 0),
    # "location": "Shape Keys > Shape Keys Specials > Easy Blendshapes",
    # "warning": "", # used for warning icon and text in addons panel
    # "support": "COMMUNITY",
    "category": "Object",
}
import bpy
from . import shape_keys_plus_main
from .shape_keys_plus_main import (WindowInfo,
                                   EasyShapeKeysPlusLeftSide,
                                   EasyShapeKeysPlusRightSide,
                                   MultiplyShapeKeysPlusLeftSide,
                                   MultiplyShapeKeysPlusRightSide,
                                   ShapeKeysPlusHelp,
                                   TOPBAR_MT_BILEK_Tools_menu,
                                   TOPBAR_MT_Shape_keys_plus_sub_menu,
                                   BilekStudioAbout,
                                   SupportBilekStudio,
                                   add_tool_submenu)

# List of classes for registering and unregistering
classes = [WindowInfo,
           EasyShapeKeysPlusLeftSide,
           EasyShapeKeysPlusRightSide,
           MultiplyShapeKeysPlusLeftSide,
           MultiplyShapeKeysPlusRightSide,
           ShapeKeysPlusHelp,
           TOPBAR_MT_BILEK_Tools_menu,
           TOPBAR_MT_Shape_keys_plus_sub_menu,
           BilekStudioAbout,
           SupportBilekStudio]

def check_bilek_tools():
    """
    check if some bilek tools already exists in Blender and are ON.
    if yes, then return True; otherwise False.
    Returns:

    """
    other_bilek_tool_enabled = False
    addons = [
        (mod, addon_utils.module_bl_info(mod))
        for mod in addon_utils.modules(refresh=False)
    ]
    prefs = bpy.context.preferences
    used_ext = {ext.module for ext in prefs.addons}
    for mod, info in addons:
        module_name = mod.__name__

        is_enabled = module_name in used_ext
        if is_enabled:
            # print (mod.bl_info.get('name'))

            data = mod.bl_info.get('author')
            search = re.search(r'(Lukas Bilek).*(BILEK STUDIO)', data)
            if search:
                # print(search.group())
                mod_info_name = mod.bl_info.get('name')
                mod_info_version = mod.bl_info.get('version')

                if mod_info_name != bl_info['name'] and mod_info_version != bl_info['version']:
                    other_bilek_tool_enabled = True
                # print(mod.bl_info.get('name'))
    # print(other_bilek_tool_enabled, 'other_bilek_tool_enabled')
    return other_bilek_tool_enabled


try:
    if check_bilek_tools():
        classes.remove(TOPBAR_MT_BILEK_Tools_menu)
    for cls in classes:
        bpy.utils.unregister_class(cls)
    if check_bilek_tools():
        bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_BILEK_Tools_menu[add_tool_submenu])
    else:
        bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_BILEK_Tools_menu.menu_draw)

except Exception as err:
    print('Nothing to unregister; {}'.format(err))
'''
try:
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bpy.types.MESH_MT_shape_key_context_menu.remove(shape_keys_plus_main.menu_func_buttons)

    # Unregister top bar Menu
    bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_BILEK_Tools_menu.menu_draw)
except:
    print('Nothing to unregister')
'''


# This part is for blender registering the add-on and unregistering them as well.
def register():
    """
    Register add-on
    Returns:

    """
    print('Adding Shape Keys Plus Tool')

    try:
        topbar_mt_bilek = str(os.path.basename(inspect.getfile(bpy.types.TOPBAR_MT_BILEK_Tools_menu)))
    except:
        topbar_mt_bilek = None

    if topbar_mt_bilek != 'shape_keys_plus_main.py' and topbar_mt_bilek is not None:
        [classes.remove(i) for i in [TOPBAR_MT_BILEK_Tools_menu, BilekStudioAbout, SupportBilekStudio] if i in classes]
        for cls in classes:
            bpy.utils.register_class(cls)
            print('registering class:',cls)

    elif topbar_mt_bilek == 'shape_keys_plus_main.py':
        [classes.remove(i) for i in [TOPBAR_MT_BILEK_Tools_menu, BilekStudioAbout, SupportBilekStudio] if i in classes]
        for cls in classes:
            bpy.utils.register_class(cls)
            print('registering class:',cls)

    else:
        [classes.append(i) for i in [TOPBAR_MT_BILEK_Tools_menu, BilekStudioAbout, SupportBilekStudio] if
         i not in classes]
        #
        for cls in classes:
            bpy.utils.register_class(cls)
            print('registering class:',cls)
        try:
            bpy.utils.register_class(TOPBAR_MT_BILEK_Tools_menu)
        except:
            pass
        print('Creating Bilek Menu and Sub Menus with Tools')
        bpy.types.TOPBAR_MT_editor_menus.append(TOPBAR_MT_BILEK_Tools_menu.menu_draw)

    if bpy.types.TOPBAR_MT_BILEK_Tools_menu:
        print('Adding sub menu and Shape Keys Plus Tool')
        bpy.types.TOPBAR_MT_BILEK_Tools_menu.prepend(add_tool_submenu)

    bpy.types.MESH_MT_shape_key_context_menu.append(shape_keys_plus_main.menu_func_buttons)
    print('Shape Keys Plus Tool has been added')


def unregister():
    """
    Unregister add-on

    """
    # Unregister classes
    if check_bilek_tools():
        [classes.remove(i) for i in [TOPBAR_MT_BILEK_Tools_menu,BilekStudioAbout,SupportBilekStudio] if i in classes]

        for cls in classes:
            bpy.utils.unregister_class(cls)
            try:
                bpy.types.TOPBAR_MT_editor_menus.remove(cls)
            except Exception as e:
                print('Could not remove...:', e)
        # bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_BILEK_Tools_menu[add_tool_submenu])
    else:
        for cls in classes:
            bpy.utils.unregister_class(cls)

        # Unregister top bar Menu
        bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_BILEK_Tools_menu.menu_draw)

    # bpy.types.MESH_MT_shape_key_context_menu.remove(shape_keys_plus_main.menu_func_buttons)

    # # Unregister classes
    # for cls in classes:
    #     bpy.utils.unregister_class(cls)
    #
    bpy.types.MESH_MT_shape_key_context_menu.remove(shape_keys_plus_main.menu_func_buttons)
    #
    # # Unregister top bar Menu
    # bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_BILEK_Tools_menu.menu_draw)


if __name__ == "__main__":
    register()
