"""
Clean Start add-on for removing default objects in Blender 3d Scene.
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

#from . import clean_start_main
# path = '/Users/lukas/Documents/BILEK-STUDIO/CODE/TOOLS/PYTHON/BLENDER/clean-start'
# import sys
# from importlib import reload
#
# if path not in sys.path:
#     sys.path.append(path)
# import clean_start_main
# #clean_start_main.unregister()
# #bpy.ops.script.reload()
# reload(clean_start_main)
#if __name__ == "__main__":
#    clean_start_main.register()

# Info about the add-on
import logging

bl_info = {
    "name": "Clean Start",
    "description": "This tool is for deleting default objects in the scene when Blender is launched",
    "author": "© Lukas Bilek 2021. BILEK STUDIO. All rights reserved.",
    "version": (0, 1, 0),
    "blender": (2, 93, 0),
    # "location": "Shape Keys > Shape Keys Specials > Easy Blendshapes",
    # "warning": "", # used for warning icon and text in addons panel
    # "support": "COMMUNITY",
    "category": "Object",
}
import bpy
# from .clean_start_main import (WindowCleanStart,
#                                    CleanStartScene,
#                                    )
#path = '/Users/lukas/Documents/BILEK-STUDIO/CODE/TOOLS/PYTHON/BLENDER/clean-start'
import sys
import pathlib
import json
import re
import addon_utils
import os
parent = pathlib.Path(__file__).resolve().parents[0]
dir = parent.joinpath('data')
config_file = dir.joinpath('config.json')
from importlib import reload

from .clean_start_main import (WindowCleanStart,
                              TOPBAR_MT_BILEK_Tools_menu,
                              MY_MT_Clean_start_sub_menu,
                                CleanStartHelp,
                                LaunchCleanStartWindow,
                              clean_scene,
                            add_tool_submenu
                              )



# List of classes for registering and unregistering
classes = [WindowCleanStart,
           TOPBAR_MT_BILEK_Tools_menu,
           MY_MT_Clean_start_sub_menu,
           CleanStartHelp,
           LaunchCleanStartWindow
           ]
script_path = bpy.utils.script_path_user()


def check_bilek_tools():
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
                print(search.group())
                mod_info_name = mod.bl_info.get('name')
                mod_info_version = mod.bl_info.get('version')

                if mod_info_name != bl_info['name'] and mod_info_version != bl_info['version']:
                    other_bilek_tool_enabled = True
                print(mod.bl_info.get('name'))
    print(other_bilek_tool_enabled, 'other_bilek_tool_enabled')
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

    #bpy.types.MESH_MT_shape_key_context_menu.remove(shape_keys_plus_main.menu_func_buttons)

    # Unregister top bar Menu
    #bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_BILEK_Tools_menu.menu_draw)
    #bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_BILEK_Test_menu.menu_draw)

except:
    print('Nothing to unregister')



# This part is for blender registering the add-on and unregistering them as well.
def register():


    # Register menu under arrow in the Shape Keys
    #bpy.types.MESH_MT_shape_key_context_menu.append(shape_keys_plus_main.menu_func_buttons)

    # Register top bar Menu
    #bpy.types.TOPBAR_MT_editor_menus.append(TOPBAR_MT_BILEK_Tools_menu.menu_draw)

    try:
        if check_bilek_tools():
            if TOPBAR_MT_BILEK_Tools_menu in classes:
                classes.remove(TOPBAR_MT_BILEK_Tools_menu)
        # Register classes
        for cls in classes:
            bpy.utils.register_class(cls)
        bpy.types.TOPBAR_MT_BILEK_Tools_menu.prepend(add_tool_submenu)
        print('adding tool')
    except:
        if check_bilek_tools():
            if not TOPBAR_MT_BILEK_Tools_menu in classes:
                classes.append(TOPBAR_MT_BILEK_Tools_menu)
        # Register classes
        for cls in classes:
            bpy.utils.register_class(cls)
        print('creating bilek tool')
        bpy.types.TOPBAR_MT_editor_menus.append(TOPBAR_MT_BILEK_Tools_menu.menu_draw)
        bpy.types.TOPBAR_MT_BILEK_Tools_menu.prepend(add_tool_submenu)

    bpy.utils.register_class(SimpleOperator)
    bpy.app.handlers.load_post.append(load_fonts)


# Unregister add-on.
def unregister():
    # Unregister classes
    if check_bilek_tools():
        if TOPBAR_MT_BILEK_Tools_menu in classes:
            classes.remove(TOPBAR_MT_BILEK_Tools_menu)

        for cls in classes:
            print (cls, 'cls')
            bpy.utils.unregister_class(cls)
        bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_BILEK_Tools_menu[add_tool_submenu])
    else:
        for cls in classes:
            bpy.utils.unregister_class(cls)

        # Unregister top bar Menu
        bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_BILEK_Tools_menu.menu_draw)

    #bpy.types.MESH_MT_shape_key_context_menu.remove(shape_keys_plus_main.menu_func_buttons)

    # Unregister top bar Menu
    #bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_BILEK_Tools_menu.menu_draw)
    bpy.utils.unregister_class(SimpleOperator)

class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        print ('running cleaning')
        main(context)
        clean_scene()
        return {'FINISHED'}


def main(context):
    for ob in context.scene.objects:
        print(ob)

from bpy.app.handlers import persistent

@persistent
def load_fonts(scene):
    #bpy.app.handlers.load_post.remove(load_fonts)
    print ('load fonts')
    clean_scene()

if __name__ == "__main__":
    register()
    print ('runs cleaning scene')
    # test call
    bpy.ops.object.simple_operator()


