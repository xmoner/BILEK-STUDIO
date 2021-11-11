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
# Import blender python
import bpy
import pathlib
import json
import os
import webbrowser
import bpy.utils.previews

# Load images
parent = pathlib.Path(__file__).resolve().parents[0]
dir_icons = parent.joinpath('icons')

pcoll = bpy.utils.previews.new()


# function for loading icon images for a specific path
def load_images():
    """
    Read and load icon files
    Returns:

    """
    for entry in os.scandir(dir_icons):
        if entry.name.endswith(".png"):
            name = os.path.splitext(entry.name)[0]
            pcoll.load(name.upper(), entry.path, "IMAGE")
            # print('name.upper', name.upper())
            # print('entry.path', entry.path)

# Try to load images
try:
    load_images()
except Exception as e:
    print('Something went wrong with loading images for images', e)

# Load Json file (config) where are saved necessary data
dir_data = parent.joinpath('data')
config_file = dir_data.joinpath('config.json')


def objects_off(self, context):
    """
    Change objects off if they are on.
    Args:
        self:
        context:

    Returns:

    """
    if not self.collection_bool:
        self.cube_bool = self.cube_bool_off
        self.camera_bool = self.camera_bool_off
        self.light_bool = self.light_bool_off


class WindowCleanStart(bpy.types.Operator):
    """
    This class runs the tool. It creates the main managing tool window.
    Here you will be able to decide what you want to remove while Blender launch.
    ... or adding your own script to the blender and run when Blender is launched.
    """
    bl_idname = "object.set_clean_start_config"
    bl_label = "Set Clean Start Config"

    # Load data from config file
    with open(config_file, 'r') as myfile:
        data = myfile.read()

    # parse file
    config_data = json.loads(data)

    # Get data and prepare buttons
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
        """
        When execute, then save data to the config file.
        Args:
            context:

        Returns: {finished}

        """
        save_dict = {"Cube": self.cube_bool,
                     "Camera": self.camera_bool,
                     "Light": self.light_bool,
                     "Collection": self.collection_bool,
                     "python_commands": str(self.commands_string),
                     "run_python_commands": self.run_python_commands_bool
                     }
        with open(config_file, 'w') as outfile:
            json.dump(save_dict, outfile, indent=4, sort_keys=True)

        print('{} ...has been saved.'.format(save_dict))
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        """
        create window with buttons and so on.
        Args:
            context: 

        Returns:

        """
        layout = self.layout
        self.col = layout.column()
        self.col.label(text="Options:")

        subsub = self.col.column()
        subsub.active = self.collection_bool

        subsub.prop(self, 'cube_bool')
        subsub.prop(self, 'camera_bool')
        subsub.prop(self, 'light_bool')

        col1 = self.col.column()
        col1.prop(self, 'collection_bool')
        col1.prop(self, 'commands_string')
        col1.prop(self, 'run_python_commands_bool')
        

def clean_scene():
    """
    This function is reading the data from the config and applying to the Blender while it's launching.
    Returns:

    """
    with open(config_file, 'r') as myfile:
        data = myfile.read()
    print('Start process removing')
    
    # parse file
    config_data = json.loads(data)
    for key, value in config_data.items():
        if not value and key != 'python_commands' and key != 'Collection':
            # object = bpy.context.scene.objects.get(key)
            try:
                print(key, value, 'removing')
                object_to_delete = bpy.data.objects[key]
                bpy.data.objects.remove(object_to_delete, do_unlink=True)
            except Exception as err:
                print('could not remove object: {}; {}'.format(key, err))
        elif not value and key == 'Collection':
            collection = bpy.data.collections.get('Collection')
            if collection:
                bpy.data.collections.remove(collection)

        elif key == 'python_commands':
            # print(key, 'key', config_data, 'config_data')
            if config_data['run_python_commands']:
                try:
                    exec(value)
                except Exception as err:
                    show_message_box("Please, check out your script at Clean Start Tool:{} ".format(err), "ERROR!", 'ERROR')


def show_message_box(message="", title="Message Box", icon='INFO'):
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


class CleanStartHelp(bpy.types.Operator):
    """
    Opening a window to the specific help website
    """
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
    

class TOPBAR_MT_BILEK_Tools_menu(bpy.types.Menu):
    """
    Create a menu at TopBar in Blender with other buttons.
    """
    bl_label = "BILEK Tools"
    bl_idname= 'TOPBAR_MT_BILEK_Tools_menu'

    def draw(self, context):
        self.layout.operator(BilekStudioAbout.bl_idname, text="About BILEK STUDIO & Tools",
                             icon_value=pcoll["LOGO_SMALL"].icon_id)
        self.layout.operator(SupportBilekStudio.bl_idname, text="Support BILEK STUDIO",
                             icon_value=pcoll["HEART_SUPPORT"].icon_id)

    def menu_draw(self, context):
        self.layout.menu("TOPBAR_MT_BILEK_Tools_menu")
        print('TopBar Bilek Menu added from Clean Start Tool')

class OBJECT_MT_clean_start_sub_menu(bpy.types.Menu):
    """
    Class for creating a sub menu with buttons for launching Clean Start Tool
    """
    bl_label = "Clean Start"
    bl_idname = "OBJECT_MT_clean_start_sub_menu"

    def draw(self, context):
        self.layout.operator(WindowCleanStart.bl_idname, text="Launch Clean Start Tool",
                             icon_value=pcoll["CLEAN_START_LOGO"].icon_id)
        self.layout.operator(CleanStartHelp.bl_idname, text="Clean Start HELP",
                             icon_value=pcoll["HELP"].icon_id)


def add_tool_submenu(self, context):
    """
    Launching menu in TobBar Menu
    Args:
        self:
        context:

    Returns:

    """
    self.layout.menu(OBJECT_MT_clean_start_sub_menu.bl_idname, icon_value=pcoll["CLEAN_START_LOGO"].icon_id)
