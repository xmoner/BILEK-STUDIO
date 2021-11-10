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
# Import blender python
import bpy
import pathlib
import json
import logging
import os
import webbrowser
import bpy.utils.previews

# Load images
parent = pathlib.Path(__file__).resolve().parents[0]
dir_icons = parent.joinpath('icons')

pcoll = bpy.utils.previews.new()

# Load Icon Images
def load_images():
    for entry in os.scandir(dir_icons):
        if entry.name.endswith(".png"):
            name = os.path.splitext(entry.name)[0]
            pcoll.load(name.upper(), entry.path, "IMAGE")
            print('name.upper', name.upper())
            print('entry.path', entry.path)


try:
    load_images()
except:
    print('Something went wrong with loading images for images')

# Load Json file (config)
dir_data = parent.joinpath('data')
config_file = dir_data.joinpath('config.json')


def objects_off(self, context):
    if not self.collection_bool:
        self.cube_bool = self.cube_bool_off
        self.camera_bool = self.camera_bool_off
        self.light_bool = self.light_bool_off


class WindowCleanStart(bpy.types.Operator):
    bl_idname = "object.set_clean_start_config"
    bl_label = "Set Clean Start Config"

    with open(config_file, 'r') as myfile:
        data = myfile.read()

    # parse file
    config_data = json.loads(data)
    print(config_data, 'config_data')
    for key, value in config_data.items():
        if key == 'Cube':
            cube_bool: bpy.props.BoolProperty(default=value, name="Keep Cube")
            cube_bool_off: bpy.props.BoolProperty(default=False, name="Keep Cube")
        if key == 'Camera':
            camera_bool: bpy.props.BoolProperty(default=value, name="Keep Camera")
            camera_bool_off: bpy.props.BoolProperty(default=False, name="Keep Camera")

        if key == 'Light':
            light_bool: bpy.props.BoolProperty(default=value, name="Keep Light")
            light_bool_off: bpy.props.BoolProperty(default=False, name="Keep Light")

        if key == 'Collection':
            collection_bool: bpy.props.BoolProperty(default=value, name="Keep Collection", update=objects_off)
        if key == 'python_commands':
            commands_string: bpy.props.StringProperty(default=value, name="Python Commands")
        if key == 'run_python_commands':
            run_python_commands_bool: bpy.props.BoolProperty(default=value, name="Run Your Python Commands")

    def execute(self, context):
        save_dict = {"Cube": self.cube_bool,
                     "Camera": self.camera_bool,
                     "Light": self.light_bool,
                     "Collection": self.collection_bool,
                     "python_commands": str(self.commands_string),
                     "run_python_commands": self.run_python_commands_bool
                     }
        print(self.commands_string, 'commands_string')
        with open(config_file, 'w') as outfile:
            json.dump(save_dict, outfile, indent=4, sort_keys=True)
        print('{} saved'.format(save_dict))
        logging.info('{} saved'.format(save_dict))
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        self.col = layout.column()
        self.col.label(text="Custom Interface!")

        subsub = self.col.column()
        subsub.active = self.collection_bool

        subsub.prop(self, 'cube_bool')
        subsub.prop(self, 'camera_bool')
        subsub.prop(self, 'light_bool')

        col1 = self.col.column()
        col1.prop(self, 'collection_bool')
        col1.prop(self, 'commands_string')
        col1.prop(self, 'run_python_commands_bool')


class CleanStartScene(object):
    """
    in this class is generating shape keys. More info what it is doing is written in the begining of the script.
    """

    def __init__(self, delete_objects=None):
        # clean scene based on given tasks
        # read file
        with open(config_file, 'r') as myfile:
            data = myfile.read()

        # parse file
        config_data = json.loads(data)
        print(config_data)

        results = bpy.ops.object.set_clean_start_config('INVOKE_DEFAULT')
        print(results, 'results')
        for key, value in config_data.items():
            # print (key,value)
            if value == 'delete':
                get_object = bpy.context.scene.objects.get(key)
                print(get_object)
                if get_object:
                    logging.info("{} found in scene".format(key))
                    obj = bpy.context.scene.objects[key]
                    bpy.ops.object.delete({"selected_objects": [obj]})
                    logging.info('Object {} has been removed'.format(key))
                else:
                    logging.info('{} not found in scene'.format(key))


class TOPBAR_MT_BILEK_Test_menu(bpy.types.Menu):
    bl_label = "BILEK TEST"

    def draw(self, context):
        CleanStartScene()

    def menu_draw(self, context):
        self.layout.menu("TOPBAR_MT_BILEK_Test_menu")


def clean_scene():
    with open(config_file, 'r') as myfile:
        data = myfile.read()
    print('start process removing')
    # parse file
    config_data = json.loads(data)
    for key, value in config_data.items():
        if not value and key != 'python_commands' and key != 'Collection':
            # object = bpy.context.scene.objects.get(key)
            # if object:
            try:
                print(key, value, 'removing')
                object_to_delete = bpy.data.objects[key]
                bpy.data.objects.remove(object_to_delete, do_unlink=True)
            except Exception as e:
                print('could not remove object: {}'.format(key))
        elif not value and key == 'Collection':
            collection = bpy.data.collections.get('Collection')
            if collection:
                bpy.data.collections.remove(collection)

        elif key == 'python_commands':
            print(key, 'key', config_data, 'config_data')
            if config_data['run_python_commands']:
                print('python runs')
                try:
                    exec(value)
                except Exception as e:
                    ShowMessageBox("Please, check out your script at Clean Start Tool:{} ".format(e), "ERROR!", 'ERROR')


def ShowMessageBox(message="", title="Message Box", icon='INFO'):
    """
    This function is poping up a window with a text

    :params message str: get text
    :params title str: get name of the title
    :params icon str: get name of the icon such as INFO, WARNING etc.
    """

    def draw(self, context):
        # create label with text
        self.layout.label(text=message)

    # Pop up a window which could include "menu".
    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)


# Class where it is running the class for duplicating and mirroring Left shape keys
class LaunchCleanStartWindow(bpy.types.Operator):
    bl_idname = "object.launch_clean_start_window"
    bl_label = "Launch Clean Start Tool"
    bl_description = "It will launch a tool called Clean Start"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        CleanStartScene()
        return {'FINISHED'}


class CleanStartHelp(bpy.types.Operator):
    bl_idname = "object.clean_start_help"
    bl_label = "Clean Start Help"
    bl_description = "Clean Start Help will take to you to the website."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        webbrowser.open(
            'https://github.com/xmoner/BILEK-STUDIO/tree/master/TOOLS/PYTHON/BLENDER/clean-start#readme')
        return {'FINISHED'}


# Class about Bilek Studio
class BilekStudioAbout(bpy.types.Operator):
    bl_idname = "object.bilek_studio_about"
    bl_label = "About BILEK STUDIO & Tools"
    bl_description = "BILEK STUDIO About will take to you to the website where you get more information about the studio."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        webbrowser.open('https://github.com/xmoner/BILEK-STUDIO#readme')
        return {'FINISHED'}


# Class for support BILEK STUDIO with website
class SupportBilekStudio(bpy.types.Operator):
    bl_idname = "object.support_bilek_studio"
    bl_label = "Support BILEK STUDIO"
    bl_description = "Please Support BILEK STUDIO if you like the tools.This button will take to you to the website where you get more information about the studio."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        webbrowser.open('https://github.com/xmoner/BILEK-STUDIO/tree/master/SUPPORT#readme')
        return {'FINISHED'}


class MY_MT_Clean_start_sub_menu(bpy.types.Menu):
    bl_label = "Clean Start"
    bl_idname = "OBJECT_MT_clean_start_sub_menu"

    def draw(self, context):
        self.layout.operator(LaunchCleanStartWindow.bl_idname, text="Launch Clean Start Tool",
                             icon_value=pcoll["CLEAN_START_LOGO"].icon_id)
        self.layout.operator(CleanStartHelp.bl_idname, text="Clean Start HELP",
                             icon_value=pcoll["HELP"].icon_id)


class TOPBAR_MT_BILEK_Tools_menu(bpy.types.Menu):
    bl_label = "BILEK Tools"

    def draw(self, context):
        self.layout.operator(BilekStudioAbout.bl_idname, text="About BILEK STUDIO & Tools",
                             icon_value=pcoll["LOGO_SMALL"].icon_id)
        self.layout.operator(SupportBilekStudio.bl_idname, text="Support BILEK STUDIO",
                             icon_value=pcoll["HEART_SUPPORT"].icon_id)

    def menu_draw(self, context):
        self.layout.menu("TOPBAR_MT_BILEK_Tools_menu")


def add_tool_submenu(self, context):
    self.layout.menu(MY_MT_Clean_start_sub_menu.bl_idname, icon_value=pcoll["CLEAN_START_LOGO"].icon_id)

#
# def register():
#     bpy.utils.register_class(MY_MT_Clean_start_sub_menu)
#     bpy.utils.register_class(MY_MT_CustomSubMenu)
#     bpy.types.TOPBAR_MT_BILEK_Tools_menu.append(add_tool_submenu)
#
# def unregister():
#     bpy.types.TOPBAR_MT_BILEK_Tools_menu.remove(add_tool_submenu)
#     bpy.utils.unregister_class(MY_MT_CustomSubMenu)
#     bpy.utils.unregister_class(MY_MT_Clean_start_sub_menu)
