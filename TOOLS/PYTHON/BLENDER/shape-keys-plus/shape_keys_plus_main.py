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
# Import blender python
import bpy
# Import regular expression
import re
import os
import webbrowser
import bpy.utils.previews
import pathlib

parent = pathlib.Path(__file__).resolve().parents[0]
dir = parent.joinpath('icons')
print('dir', dir)

pcoll = bpy.utils.previews.new()


def load_images():
    for entry in os.scandir(dir):
        if entry.name.endswith(".png"):
            name = os.path.splitext(entry.name)[0]
            pcoll.load(name.upper(), entry.path, "IMAGE")
            print('name.upper', name.upper())
            print('entry.path', entry.path)


try:
    load_images()
except:
    print('Something went wrong with loading images for images')

# Sides for later use and accepted.
dict_sides = {
    'L_': 'R_',
    'l_': 'r_',
    'R_': 'L_',
    'r_': 'l_',
    '_L': '_R',
    '_l': '_r',
    '_R': '_L',
    '_r': '_l'
}

class WindowInfo(bpy.types.Operator):
    """
    This is a window for warning. If selected Keys Shapes does not have preffix or suffix, 
    then this window should pop up.
    """

    bl_idname = 'dialog.box'
    bl_label = 'Warning!'

    def draw(self, context):
        layout = self.layout
        layout.label(text='Please update L_ or R_ prefix at Shape Keys')

    def execute(self, context):
        self.report({'WARNING'}, 'Please update L_ or R_ prefix at Shape Keys')
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


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


class GenerateShapesKeys(object):
    """
    in this class is generating shape keys. More info what it is doing is written in the begining of the script.
    """

    def __init__(self, side=None, multiply_operation=None):
        """
        :params side str: get side (prefix or suffix such as L or R "left and right")
        :params multiply_operation str: "Yes" or "No" for generating multiple shape keys.
        """

        # get name of the side for generating shape keys
        self.side = side

        # get type of multiply_operation generating more shape keys or not
        self.multiply_operation = multiply_operation

        if self.multiply_operation == 'No':
            # th
            self.generate_mirror_shape_keys()
        else:
            self.generate_multiply_mirror_shape_keys()

    def generate_mirror_shape_keys(self):
        """
        This function is duplicating and mirroring selected shape keys.
        In addition it is renaming the shape key to the right or left side such as L_ or _L etc.
        """
        # Get list of the selected objects from the scene
        self.SEL_OBJECTS = bpy.context.selected_objects
        print('self.SEL_OBJECTS', self.SEL_OBJECTS)
        print(self.side)
        if len(self.SEL_OBJECTS) == 0:
            # Shows a message box with a message, custom title, and a specific icon
            return ShowMessageBox("Please, select an object in the scene!", "WARNING!", 'ERROR')
        # elif len(self.SEL_OBJECTS) > 1:
        #    return  ShowMessageBox( "Selecting multiple objects is disabled. Blender Bug.","WARNING!", 'ERROR')

        # deselect all objects in the scene
        # bpy.context.active_object.select_set(False)

        print('test', self.SEL_OBJECTS)
        for one_object in self.SEL_OBJECTS:
            print('Changing:', one_object.name)

            ob = bpy.context.scene.objects[one_object.name]  # Get the object
            bpy.ops.object.select_all(action='DESELECT')  # Deselect all objects
            bpy.context.view_layer.objects.active = ob  # Make the cube the active object
            ob.select_set(True)

            print('selected objects', one_object.name)

            blendshape = one_object.active_shape_key
            blendshape_name = blendshape.name
            print('blendshape_name', blendshape_name)

            # Set an active shape key value to 1
            blendshape.value = 1

            if self.side == 'l':
                search_side = re.search(r'^l_|^L_|_l$|_L$', blendshape_name)
            else:
                search_side = re.search(r'^r_|^R_|_l$|_R$', blendshape_name)

            if not search_side:
                print('problem', blendshape_name)
                # Show up mistake - pop up a window
                bpy.ops.dialog.box('INVOKE_DEFAULT')
                return ValueError
            else:
                # Deactivate all blendhshapes/shape keys except duplicated one
                list_blend_keys = list(one_object.data.shape_keys.key_blocks)
                print('list_blend_keys', list_blend_keys)
                for sh_key in list_blend_keys:
                    if not sh_key.name == blendshape_name:
                        sh_key.value = 0
                    else:
                        try:
                            # Here we have to find the right side of the shape key and remove it if exists

                            index = one_object.data.shape_keys.key_blocks.find(
                                blendshape_name.replace(search_side.group(), dict_sides[search_side.group()]))
                            # print (blendshape_name,':', index)

                            bpy.context.scene.objects[one_object.name].active_shape_key_index = index

                            bpy.ops.object.shape_key_remove(all=False)
                            # print ('removed:', index, blendshape_name.replace('_L','_R') )
                        except:
                            print('Nothing to delete')

                # Make active correct shape key
                index = one_object.data.shape_keys.key_blocks.find(blendshape_name)
                bpy.context.scene.objects[one_object.name].active_shape_key_index = index

                # Copy values Range Min and Max
                value_min = bpy.data.shape_keys[one_object.data.shape_keys.name].key_blocks[blendshape_name].slider_min
                value_max = bpy.data.shape_keys[one_object.data.shape_keys.name].key_blocks[blendshape_name].slider_max

                # Copy expression values of the current shape key
                # key_shape_expression = bpy.data.shape_keys[one_object.data.shape_keys.name].animation_data.drivers[index].driver.expression

                # Create new blendshape/Shape Key    
                active_blendshape = one_object.shape_key_add(from_mix=True)
                # active_blendshape = one_object.active_shape_key
                # print ('active_blendshape:',active_blendshape.name)
                # print ('search_side:',search_side.group())

                # If side from button is L_ then go that way, otherwise different way.
                if self.side == 'l':
                    if search_side.group() == 'L_':
                        active_blendshape.name = 'R_' + blendshape_name.replace('L_', '')
                    #    print ('L_',active_blendshape.name, blendshape_name)
                    elif search_side.group() == '_L':
                        active_blendshape.name = blendshape_name.replace('_L', '') + '_R'
                    #    print ('_L')
                    elif search_side.group() == 'l_':
                        active_blendshape.name = 'r_' + blendshape_name.replace('l_', '')
                    #    print ('l_')
                    elif search_side.group() == '_l':
                        active_blendshape.name = blendshape_name.replace('_l', '') + '_r'
                        #    print ('_l')
                else:
                    if search_side.group() == 'R_':
                        active_blendshape.name = 'L_' + blendshape_name.replace('R_', '')
                    #    print ('L_',active_blendshape.name, blendshape_name)
                    elif search_side.group() == '_R':
                        active_blendshape.name = blendshape_name.replace('_R', '') + '_L'
                    #    print ('_L')
                    elif search_side.group() == 'r_':
                        active_blendshape.name = 'l_' + blendshape_name.replace('r_', '')
                    #    print ('l_')
                    elif search_side.group() == '_r':
                        active_blendshape.name = blendshape_name.replace('_r', '') + '_l'

                        # Deactivate all blendhshapes/shape keys except duplicated one
                list_blend_keys = list(one_object.data.shape_keys.key_blocks)
                for sh_key in list_blend_keys:
                    sh_key.value = 0

                # try:
                #     key_shape_expression = bpy.data.shape_keys[one_object.data.shape_keys.name].animation_data.drivers[index].driver.expression
                # except:
                #     key_shape_expression = None

                # if key_shape_expression:
                #     # set previous active blendshape/shape key value back to 1
                #     blendshape.value = 0 

                # now we have to get the correct active shape keys
                index = one_object.data.shape_keys.key_blocks.find(active_blendshape.name)
                print(one_object.name, ':', index)
                active_index = bpy.context.scene.objects[one_object.name].active_shape_key_index = index
                # bpy.ops.object.shape_key_mirror(use_topology=False)

                # here we have to mirror the blenshapes and it work via override context
                # mirror shape key which is selected in the Shape Keys attribute
                override = bpy.context.copy()
                override['object'] = one_object
                bpy.ops.object.shape_key_mirror(override, use_topology=False)

                # Now we have to paste Range mix and Max values which were stored before duplicating shape key
                bpy.data.shape_keys[one_object.data.shape_keys.name].key_blocks[index].slider_min = value_min
                bpy.data.shape_keys[one_object.data.shape_keys.name].key_blocks[index].slider_max = value_max

                # Paste expression values of the current shape key
                # bpy.data.shape_keys[one_object.data.shape_keys.name].animation_data.drivers[index].driver.expression = key_shape_expression

                # set previous active blendshape/shape key value back to 1
                blendshape.value = 1

                # set current active blendshape/shape key value back to 1
                active_blendshape.value = 1

            # pop up a window when the process is finished    
            ShowMessageBox(message='Finished', title='Info', icon='INFO')

    def generate_multiply_mirror_shape_keys(self):
        """
        This function is duplicating and mirroring all shape keys from one side such as L_ or R_.
        In addition it is renaming the shape keys to the right or left sides such as L_ or _L etc.
        """

        # Get list of the selected objects from the scene
        self.SEL_OBJECTS = bpy.context.selected_objects
        print('self.SEL_OBJECTS', self.SEL_OBJECTS)
        print(self.side)
        if len(self.SEL_OBJECTS) == 0:
            # Shows a message box with a message, custom title, and a specific icon
            return ShowMessageBox("Please, select an object in the scene!", "WARNING!", 'ERROR')
        # elif len(self.SEL_OBJECTS) > 1:
        #    return  ShowMessageBox( "Selecting multiple objects is disabled. Blender Bug.","WARNING!", 'ERROR')

        # print ('test', self.SEL_OBJECTS)
        for one_object in self.SEL_OBJECTS:
            print('Changing:', one_object.name)

            ob = bpy.context.scene.objects[one_object.name]  # Get the object
            bpy.ops.object.select_all(action='DESELECT')  # Deselect all objects
            bpy.context.view_layer.objects.active = ob  # Make the cube the active object
            ob.select_set(True)

            # First we need to get a list of all shapes keys via key_blocks
            list_key_blocks = list(one_object.data.shape_keys.key_blocks)
            get_list_right_side = []
            for key in list_key_blocks:
                if self.side == 'l':
                    search_right_side = re.search(r'^r_|^R_|_r$|_R$', key.name)

                elif self.side == 'r':
                    search_right_side = re.search(r'^l_|^L_|_l$|_L$', key.name)

                if search_right_side:
                    get_list_right_side.append(key)

            print('List of right sides:', get_list_right_side)

            # Remove all right side shape keys
            for key in get_list_right_side:
                index = one_object.data.shape_keys.key_blocks.find(key.name)
                print(key.name, ':', index)

                bpy.context.scene.objects[one_object.name].active_shape_key_index = index

                bpy.ops.object.shape_key_remove(all=False)

            # Now we need to store shape keys values from the object (Left side)
            # dict_shape_keys_values = {}
            list_left_key_blocks = list(one_object.data.shape_keys.key_blocks)
            # for key in list_left_key_blocks:
            #   if key.name != 'Basis':
            #        index = one_object.data.shape_keys.key_blocks.find(key.name)
            #        dict_shape_keys_values[key]=index

            # print (dict_shape_keys_values)

            # Now it's time to duplicate and mirror all shape keys from Left side. 
            for key in list_left_key_blocks:
                # search and match names Left sides
                blendshape_name = key.name
                print('blendshape_name:', blendshape_name)
                if self.side == 'l':
                    search_side = re.search(r'^l_|^L_|_l$|_L$', blendshape_name)
                elif self.side == 'r':
                    search_side = re.search(r'^r_|^R_|_r$|_R$', blendshape_name)

                # if there is not left side, then skip it.
                if not search_side:
                    print('skipping shape key because it does not match L or R:')
                    print('skipped Shape Key:', key.name)
                    continue

                # Deactivate all blendhshapes/shape keys except duplicated one
                list_blend_keys = list(one_object.data.shape_keys.key_blocks)
                for sh_key in list_blend_keys:
                    if not sh_key.name == key.name:
                        sh_key.value = 0
                    else:
                        sh_key.value = 1

                # Copy values Range Min and Max
                value_min = bpy.data.shape_keys[one_object.data.shape_keys.name].key_blocks[blendshape_name].slider_min
                value_max = bpy.data.shape_keys[one_object.data.shape_keys.name].key_blocks[blendshape_name].slider_max

                # Get index from specific key blocks
                index = one_object.data.shape_keys.key_blocks.find(blendshape_name)

                # Copy expression values of the current shape key
                # key_shape_expression = bpy.data.shape_keys[one_object.data.shape_keys.name].animation_data.drivers[index].driver.expression

                # Create new blendshape/Shape Key    
                active_blendshape = one_object.shape_key_add(from_mix=True)
                # active_blendshape = one_object.active_shape_key

                print('active_blendshape:', active_blendshape.name)
                print('blendshape_name:', blendshape_name)
                print('search side', search_side.group())
                print('self.side:', self.side)

                # Rename name for duplicated and mirrored shape keys
                if self.side == 'l':
                    if search_side.group() == 'L_':
                        active_blendshape.name = 'R_' + blendshape_name.replace('L_', '')
                        # print ('L_',active_blendshape.name, blendshape_name)
                    elif search_side.group() == '_L':
                        active_blendshape.name = blendshape_name.replace('_L', '') + '_R'
                        # print ('_L')
                    elif search_side.group() == 'l_':
                        active_blendshape.name = 'r_' + blendshape_name.replace('l_', '')
                        # print ('l_')
                    elif search_side.group() == '_l':
                        active_blendshape.name = blendshape_name.replace('_l', '') + '_r'
                        # print ('_l')
                elif self.side == 'r':
                    if search_side.group() == 'R_':
                        active_blendshape.name = 'L_' + blendshape_name.replace('R_', '')
                        # print ('R_',active_blendshape.name, blendshape_name)
                    elif search_side.group() == '_R':
                        active_blendshape.name = blendshape_name.replace('_R', '') + '_L'
                        # print ('_R')
                    elif search_side.group() == 'r_':
                        active_blendshape.name = 'l_' + blendshape_name.replace('r_', '')
                        # print ('r_')
                    elif search_side.group() == '_r':
                        active_blendshape.name = blendshape_name.replace('_r', '') + '_l'
                        # print ('_r')

                # Deactivate all blendhshapes/shape keys except duplicated one
                list_blend_keys = list(one_object.data.shape_keys.key_blocks)
                for sh_key in list_blend_keys:
                    sh_key.value = 0

                # now we have to get the correct active shape keys
                index = one_object.data.shape_keys.key_blocks.find(active_blendshape.name)
                print(one_object.name, ':', index)
                active_index = bpy.context.scene.objects[one_object.name].active_shape_key_index = index
                # bpy.ops.object.shape_key_mirror(use_topology=False)

                # here we have to mirror the blenshapes and it work via override context
                # mirror shape key which is selected in the Shape Keys attribute
                override = bpy.context.copy()
                override['object'] = one_object
                bpy.ops.object.shape_key_mirror(override, use_topology=False)

                # Now we have to paste Range mix and Max values which were stored before duplicating shape key
                bpy.data.shape_keys[one_object.data.shape_keys.name].key_blocks[index].slider_min = value_min
                bpy.data.shape_keys[one_object.data.shape_keys.name].key_blocks[index].slider_max = value_max

                # print ('key_shape_expression', key_shape_expression, active_index, one_object.data.shape_keys.name, index)

                # Paste expression values of the current shape key
                # bpy.data.shape_keys[one_object.data.shape_keys.name].animation_data.drivers[index].driver.expression = '222'

                # set previous active blendshape/shape key value back to 1
                # blendshape.value = 1

                # set current active blendshape/shape key value back to 1
                active_blendshape.value = 1

            # print ('finished:', one_object.name)

            # pop up a window when the process is finished    
            ShowMessageBox(message='Finished', title='Info', icon='INFO')


# Class where it is running the class for duplicating and mirroring Left shape keys
class EasyShapeKeysPlusLeftSide(bpy.types.Operator):
    bl_idname = "object.duplicate_left_side_shape_keys_plus"
    bl_label = "Duplicate & Mirror Left Shape Keys"
    bl_description = "Duplicate & Mirror Left Shape Keys"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        GenerateShapesKeys(side='l',
                           multiply_operation='No')
        return {'FINISHED'}


# Class where it is running the class for duplicating and mirroring Right shape keys
class EasyShapeKeysPlusRightSide(bpy.types.Operator):
    bl_idname = "object.duplicate_right_side_shape_keys_plus"
    bl_label = "Duplicate & Mirror Left Shape Keys"
    bl_description = "Duplicate & Mirror Left Shape Keys"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        GenerateShapesKeys(side='r',
                           multiply_operation='No')
        return {'FINISHED'}

    # Class where it is running the class for duplicating and mirroring multiply shape keys for Left side


class MultiplyShapeKeysPlusLeftSide(bpy.types.Operator):
    bl_idname = "object.multiply_duplicate_left_side_shape_keys_plus"
    bl_label = "Duplicate & mirror All Left Shape Keys "
    bl_description = "Duplicate & Mirror All Left Shape Keys"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        GenerateShapesKeys(side='l',
                           multiply_operation='Yes')
        return {'FINISHED'}

    # Class where it is running the class for duplicating and mirroring multiply shape keys for Right side


class MultiplyShapeKeysPlusRightSide(bpy.types.Operator):
    bl_idname = "object.multiply_duplicate_right_side_shape_keys_plus"
    bl_label = "Duplicate & mirror All Left Shape Keys "
    bl_description = "Duplicate & Mirror All Left Shape Keys"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        GenerateShapesKeys(side='r',
                           multiply_operation='Yes')
        return {'FINISHED'}

    # Class where it is running the class for duplicating and mirroring multiply shape keys for Right side


class ShapeKeysPlusHelp(bpy.types.Operator):
    bl_idname = "object.shape_keys_plus_help"
    bl_label = "Shape Keys Plus Help"
    bl_description = "Shape Keys Plus Help will take to you to the website."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        webbrowser.open(
            'https://github.com/xmoner/BILEK-STUDIO/tree/master/TOOLS/PYTHON/BLENDER/shape-keys-plus#readme')
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


class TOPBAR_MT_Shape_keys_plus_sub_menu(bpy.types.Menu):
    bl_label = "Shape Keys Plus"
    bl_idname = "TOPBAR_MT_Shape_keys_plus_sub_menu"

    def draw(self, context):
        self.layout.operator(EasyShapeKeysPlusLeftSide.bl_idname, text="Duplicate & mirror from L_ > R_",
                             icon_value=pcoll["L_R_SIDE"].icon_id)
        self.layout.operator(EasyShapeKeysPlusRightSide.bl_idname, text="Duplicate & mirror from R_ > L_",
                             icon_value=pcoll["R_L_SIDE"].icon_id)

        self.layout.operator(MultiplyShapeKeysPlusLeftSide.bl_idname, text="Duplicate & mirror all L_ >> R_",
                             icon_value=pcoll["L_R_SIDE_ALL"].icon_id)
        self.layout.operator(MultiplyShapeKeysPlusRightSide.bl_idname, text="Duplicate & mirror all R_ >> L_",
                             icon_value=pcoll["R_L_SIDE_ALL"].icon_id)
        self.layout.operator(ShapeKeysPlusHelp.bl_idname, text="Shape Keys Plus HELP", icon_value=pcoll["HELP"].icon_id)


class TOPBAR_MT_BILEK_Tools_menu(bpy.types.Menu):
    """
    Create a menu at TopBar in Blender with other buttons.
    """
    bl_label = "BILEK Tools"
    bl_idname= 'TOPBAR_MT_BILEK_Tools_menu'

    def draw(self, context):
        self.layout.menu("TOPBAR_MT_Shape_keys_plus_sub_menu", icon_value=pcoll["SHAPE_KEYS_PLUS_LOGO"].icon_id)
        self.layout.operator(BilekStudioAbout.bl_idname, text="About BILEK STUDIO & Tools",
                             icon_value=pcoll["LOGO_SMALL"].icon_id)
        self.layout.operator(SupportBilekStudio.bl_idname, text="Support BILEK STUDIO",
                             icon_value=pcoll["HEART_SUPPORT"].icon_id)

    def menu_draw(self, context):
        self.layout.menu("TOPBAR_MT_BILEK_Tools_menu")
        print('TopBar Bilek Menu added from Shape Keys Plus Tool')


def menu_func_buttons(self, context):
    """
    Create buttons in the Shape keys Attributes
    Args:
        self:
        context:

    Returns:

    """
    self.layout.operator(MultiplyShapeKeysPlusRightSide.bl_idname, text="Duplicate & mirror all R_ >> L_",
                         icon_value=pcoll["R_L_SIDE_ALL"].icon_id)
    self.layout.operator(MultiplyShapeKeysPlusLeftSide.bl_idname, text="Duplicate & mirror all L_ >> R_",
                         icon_value=pcoll["L_R_SIDE_ALL"].icon_id)
    self.layout.operator(EasyShapeKeysPlusRightSide.bl_idname, text="Duplicate & mirror from R_ > L_",
                         icon_value=pcoll["R_L_SIDE"].icon_id)
    self.layout.operator(EasyShapeKeysPlusLeftSide.bl_idname, text="Duplicate & mirror from L_ > R_",
                         icon_value=pcoll["L_R_SIDE"].icon_id)

    self.layout.operator(ShapeKeysPlusHelp.bl_idname, text="Shape Keys Plus HELP", icon_value=pcoll["HELP"].icon_id)

    # print ('pcoll', pcoll, pcoll['ICON_SMALL'])

# def menu_func_for_R(self, context):
#     self.layout.operator(EasyBlendshapes.bl_idname,text="Duplicate & mirror from R_ >> L_")

def add_tool_submenu(self, context):
    """
    Launching menu in TobBar Menu
    Args:
        self:
        context:

    Returns:

    """
    self.layout.menu(TOPBAR_MT_Shape_keys_plus_sub_menu.bl_idname, icon_value=pcoll["SHAPE_KEYS_PLUS_LOGO"].icon_id)
