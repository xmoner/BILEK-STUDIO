"""
Clean Start add-on for removing default objects and running commands in Blender 3d Scene when launching.
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

# Info about the add-on

bl_info = {
    "name": "Clean Start",
    "description": "This tool is for deleting default objects in the scene when Blender is launched",
    "author": "© Lukas Bilek 2021. BILEK STUDIO. All rights reserved.",
    "version": (0, 1, 1),
    "blender": (2, 93, 0),
    "category": "Object",
}
import bpy
import pathlib
import re
import addon_utils

parent = pathlib.Path(__file__).resolve().parents[0]
dir = parent.joinpath('data')
config_file = dir.joinpath('config.json')

from importlib import reload
from bpy.app.handlers import persistent

from .clean_start_main import (WindowCleanStart,
                               TOPBAR_MT_BILEK_Tools_menu,
                               OBJECT_MT_clean_start_sub_menu,
                               CleanStartHelp,
                               clean_scene,
                               add_tool_submenu,
                               BilekStudioAbout,
                               SupportBilekStudio
)

# List of classes for registering and unregistering
classes = [WindowCleanStart,
           TOPBAR_MT_BILEK_Tools_menu,
           OBJECT_MT_clean_start_sub_menu,
           CleanStartHelp,
           BilekStudioAbout,
           SupportBilekStudio
           ]
script_path = bpy.utils.script_path_user()


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


# This part is for blender registering the add-on and unregistering them as well.
def register():
    """
    Register add-on
    Returns:

    """
    if check_bilek_tools():
        print ('tools are on')
        [classes.remove(i) for i in [TOPBAR_MT_BILEK_Tools_menu, BilekStudioAbout, SupportBilekStudio] if i in classes]
        # Register classes
        for cls in classes:
            bpy.utils.register_class(cls)
        bpy.types.TOPBAR_MT_BILEK_Tools_menu.prepend(add_tool_submenu)
        print('adding tool')
    else:
        [classes.append(i) for i in [TOPBAR_MT_BILEK_Tools_menu, BilekStudioAbout, SupportBilekStudio] if i not in classes]

        # Register classes
        for cls in classes:
            bpy.utils.register_class(cls)
        print('Creating Bilek Menu and Sub Menus with Tools')
        bpy.types.TOPBAR_MT_editor_menus.append(TOPBAR_MT_BILEK_Tools_menu.menu_draw)
        print('Adding sub menu and Clean Start Tool')
        bpy.types.TOPBAR_MT_BILEK_Tools_menu.prepend(add_tool_submenu)
        print('Clean Start Tool has been added')

    # run clean scene in blender while Blender is launching
    bpy.app.handlers.load_post.append(run_clean_scene)


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



@persistent
def run_clean_scene(scene):
    """
    This function runs function during launching Blender and the first scene
    Args:
        scene:

    Returns:

    """
    print('Running Cleaning scene...')
    clean_scene()
    print('Finished cleaning scene')


if __name__ == "__main__":
    register()
