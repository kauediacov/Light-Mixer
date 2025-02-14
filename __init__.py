bl_info = {
    "name": "Light Controller",
    "author": "Higor Pereira Kaue Diacov Vitoria Ferreira",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Light Controller",
    "description": "Control all scene lights from a single panel",
    "category": "Lighting",
}

import bpy
from bpy.types import Panel, PropertyGroup, UIList, Operator
from bpy.props import FloatProperty, BoolProperty, FloatVectorProperty, StringProperty, EnumProperty, PointerProperty, CollectionProperty, IntProperty

class LIGHTCONTROLLER_PG_collection_filter(PropertyGroup):
    collection: PointerProperty(
        type=bpy.types.Collection,
        name="Collection"
    )
    is_isolated: BoolProperty(
        name="Isolate Collection",
        default=False
    )

class LIGHTCONTROLLER_PG_settings(PropertyGroup):
    active_collection_index: IntProperty(default=0)
    is_isolating: BoolProperty(default=False)
    isolated_light: StringProperty(default="")
    collection_filters: CollectionProperty(
        type=LIGHTCONTROLLER_PG_collection_filter,
        name="Collection Filters"
    )
    new_light_name: StringProperty(default="")

class LIGHTCONTROLLER_OT_rename_light(Operator):
    bl_idname = "light_controller.rename_light"
    bl_label = "Rename Light"
    bl_description = "Rename this light"
    
    light_name: StringProperty()
    new_name: StringProperty()
    
    def execute(self, context):
        light_obj = bpy.data.objects.get(self.light_name)
        if light_obj:
            light_obj.name = self.new_name
            light_obj.data.name = self.new_name
        return {'FINISHED'}

class LIGHTCONTROLLER_OT_isolate_collection(Operator):
    bl_idname = "light_controller.isolate_collection"
    bl_label = "Isolate Collection"
    bl_description = "Show only lights in this collection"
    
    index: IntProperty()
    
    def execute(self, context):
        settings = context.scene.light_controller_settings
        collection_filter = settings.collection_filters[self.index]
        
        # Toggle isolation state
        collection_filter.is_isolated = not collection_filter.is_isolated
        
        # If isolating, hide all lights not in this collection
        if collection_filter.is_isolated:
            for obj in bpy.data.objects:
                if obj.type == 'LIGHT':
                    obj.hide_viewport = collection_filter.collection not in obj.users_collection
        else:
            # Show all lights
            for obj in bpy.data.objects:
                if obj.type == 'LIGHT':
                    obj.hide_viewport = False
        
        return {'FINISHED'}

class LIGHTCONTROLLER_OT_select_light(Operator):
    bl_idname = "light_controller.select_light"
    bl_label = "Select Light"
    bl_description = "Select this light in the viewport"
    
    light_name: StringProperty()
    
    def execute(self, context):
        # Deselect all objects
        bpy.ops.object.select_all(action='DESELECT')
        
        # Select and make active the light
        light_obj = bpy.data.objects.get(self.light_name)
        if light_obj:
            light_obj.select_set(True)
            context.view_layer.objects.active = light_obj
        return {'FINISHED'}

class LIGHTCONTROLLER_OT_isolate_light(Operator):
    bl_idname = "light_controller.isolate_light"
    bl_label = "Isolate Light"
    bl_description = "Toggle isolation of this light"
    
    light_name: StringProperty()
    
    def execute(self, context):
        settings = context.scene.light_controller_settings
        
        # If already isolating this light, un-isolate
        if settings.is_isolating and settings.isolated_light == self.light_name:
            settings.is_isolating = False
            settings.isolated_light = ""
            # Show all lights
            for obj in bpy.data.objects:
                if obj.type == 'LIGHT':
                    obj.hide_viewport = False
        else:
            # Isolate this light
            settings.is_isolating = True
            settings.isolated_light = self.light_name
            for obj in bpy.data.objects:
                if obj.type == 'LIGHT':
                    obj.hide_viewport = (obj.name != self.light_name)
        
        return {'FINISHED'}

class LIGHTCONTROLLER_OT_show_all_lights(Operator):
    bl_idname = "light_controller.show_all_lights"
    bl_label = "Show All Lights"
    bl_description = "Show all lights in the scene"
    
    def execute(self, context):
        settings = context.scene.light_controller_settings
        settings.is_isolating = False
        settings.isolated_light = ""
        
        for obj in bpy.data.objects:
            if obj.type == 'LIGHT':
                obj.hide_viewport = False
        return {'FINISHED'}

class LIGHTCONTROLLER_OT_add_collection_filter(Operator):
    bl_idname = "light_controller.add_collection_filter"
    bl_label = "Add Collection Filter"
    bl_description = "Add a new collection filter"
    
    def execute(self, context):
        settings = context.scene.light_controller_settings
        if len(settings.collection_filters) < 5:
            settings.collection_filters.add()
        return {'FINISHED'}

class LIGHTCONTROLLER_OT_remove_collection_filter(Operator):
    bl_idname = "light_controller.remove_collection_filter"
    bl_label = "Remove Collection Filter"
    bl_description = "Remove this collection filter"
    
    index: IntProperty()
    
    def execute(self, context):
        settings = context.scene.light_controller_settings
        settings.collection_filters.remove(self.index)
        return {'FINISHED'}

class LIGHTCONTROLLER_PT_lights_list(Panel):
    bl_label = "All Lights"
    bl_idname = "LIGHTCONTROLLER_PT_lights_list"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Light Controller"
    
    def draw(self, context):
        layout = self.layout
        settings = context.scene.light_controller_settings
        
        # Show All Lights button
        row = layout.row(align=True)
        row.operator("light_controller.show_all_lights", icon='HIDE_OFF')
        
        # Get all lights
        lights = [obj for obj in bpy.data.objects if obj.type == 'LIGHT']
        
        # Draw lights list
        box = layout.box()
        row = box.row()
        row.label(text=f"Total Lights: {len(lights)}")
        
        self.draw_lights_list(context, layout, lights)

    def draw_lights_list(self, context, layout, lights):
        settings = context.scene.light_controller_settings
        
        for light_obj in lights:
            self.draw_light_controller(context, layout, light_obj)

    def draw_light_controller(self, context, layout, light_obj):
        settings = context.scene.light_controller_settings
        light = light_obj.data
        is_selected = light_obj == context.active_object
        is_isolated = settings.is_isolating and settings.isolated_light == light_obj.name
        
        # Light box with outline
        box = layout.box()
        if is_selected:
            box.alert = True
        elif is_isolated:
            box.enabled = True
        
        # Header with name and controls
        row = box.row(align=True)
        
        # Select button
        op = row.operator("light_controller.select_light", text="", icon='RESTRICT_SELECT_OFF')
        op.light_name = light_obj.name
        
        # Visibility toggles
        row.prop(light_obj, "hide_viewport", text="", icon='HIDE_OFF' if not light_obj.hide_viewport else 'HIDE_ON', emboss=False)
        row.prop(light_obj, "hide_render", text="", icon='RESTRICT_RENDER_OFF' if not light_obj.hide_render else 'RESTRICT_RENDER_ON', emboss=False)
        
        # Light name (always editable)
        name_row = row.row(align=True)
        name_row.use_property_split = True
        name_row.use_property_decorate = False
        name_row.prop(light_obj, "name", text="", icon=f'LIGHT_{light.type}')
        
        # Isolate button
        op = row.operator("light_controller.isolate_light", text="", icon='SOLO_ON' if is_isolated else 'SOLO_OFF')
        op.light_name = light_obj.name
        
        # Light controls
        col = box.column(align=True)
        col.use_property_split = True
        col.use_property_decorate = False
        
        # Power (numeric only)
        col.prop(light, "energy", text="Power")
        
        # Color
        col.prop(light, "color", text="")
        
        # Spread (for all light types)
        if light.type == 'SPOT':
            col.prop(light, "spot_size", text="Spread")
        elif light.type == 'AREA':
            col.prop(light, "size", text="Spread")
        elif light.type == 'POINT':
            col.prop(light, "shadow_soft_size", text="Spread")
        elif light.type == 'SUN':
            col.prop(light, "angle", text="Spread")
        
        # Shadow toggle and settings
        row = col.row(align=True)
        row.prop(light, "use_shadow", text="Shadow", toggle=True, icon='MOD_OPACITY')
        
        if light.use_shadow:
            shadow_col = col.column(align=True)
            shadow_col.prop(light, "shadow_soft_size", text="Size")
            shadow_col.prop(light, "shadow_buffer_bias", text="Bias")
        
        # Nodes toggle with editor button
        row = col.row(align=True)
        row.prop(light, "use_nodes", text="Nodes", toggle=True, icon='NODETREE')
        if light.use_nodes:
            op = row.operator("light_controller.open_node_editor", text="", icon='WINDOW')
            op.light_name = light_obj.name

class LIGHTCONTROLLER_OT_open_node_editor(Operator):
    bl_idname = "light_controller.open_node_editor"
    bl_label = "Open Node Editor"
    bl_description = "Open shader editor for this light"
    
    light_name: StringProperty()
    
    def execute(self, context):
        # Find the light
        light_obj = bpy.data.objects.get(self.light_name)
        if not light_obj or light_obj.type != 'LIGHT':
            return {'CANCELLED'}
            
        # Set as active object
        context.view_layer.objects.active = light_obj
        light_obj.select_set(True)
        
        # Find or create shader editor area
        shader_area = None
        for area in context.screen.areas:
            if area.type == 'NODE_EDITOR':
                shader_area = area
                break
                
        if not shader_area:
            # Try to split the largest area
            largest_area = max(context.screen.areas, key=lambda a: a.width * a.height)
            largest_area.type = 'NODE_EDITOR'
            shader_area = largest_area
            
        if shader_area:
            shader_area.spaces.active.tree_type = 'ShaderNodeTree'
            shader_area.spaces.active.shader_type = 'OBJECT'
            
        return {'FINISHED'}

class LIGHTCONTROLLER_PT_collections(Panel):
    bl_label = "Collections"
    bl_idname = "LIGHTCONTROLLER_PT_collections"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Light Controller"
    
    def draw(self, context):
        layout = self.layout
        settings = context.scene.light_controller_settings
        
        # Collection filters
        box = layout.box()
        row = box.row()
        row.label(text="Collection Filters")
        if len(settings.collection_filters) < 5:
            row.operator("light_controller.add_collection_filter", text="", icon='ADD')
        
        # Draw collection filters
        for i, collection_filter in enumerate(settings.collection_filters):
            box = layout.box()
            # Collection header
            row = box.row(align=True)
            row.prop(collection_filter, "collection", text="")
            op = row.operator("light_controller.isolate_collection", text="", icon='SOLO_ON' if collection_filter.is_isolated else 'SOLO_OFF')
            op.index = i
            row.operator("light_controller.remove_collection_filter", text="", icon='X').index = i
            
            # Show lights in this collection if it has one assigned
            if collection_filter.collection:
                lights = [obj for obj in collection_filter.collection.objects if obj.type == 'LIGHT']
                if lights:
                    box.label(text=f"Lights in collection: {len(lights)}")
                    # Draw full light controller for each light in collection
                    for light_obj in lights:
                        LIGHTCONTROLLER_PT_lights_list.draw_light_controller(self, context, box, light_obj)

classes = (
    LIGHTCONTROLLER_PG_collection_filter,
    LIGHTCONTROLLER_PG_settings,
    LIGHTCONTROLLER_OT_rename_light,
    LIGHTCONTROLLER_OT_isolate_collection,
    LIGHTCONTROLLER_OT_select_light,
    LIGHTCONTROLLER_OT_isolate_light,
    LIGHTCONTROLLER_OT_show_all_lights,
    LIGHTCONTROLLER_OT_add_collection_filter,
    LIGHTCONTROLLER_OT_remove_collection_filter,
    LIGHTCONTROLLER_OT_open_node_editor,
    LIGHTCONTROLLER_PT_lights_list,
    LIGHTCONTROLLER_PT_collections,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # Register settings
    bpy.types.Scene.light_controller_settings = PointerProperty(type=LIGHTCONTROLLER_PG_settings)

def unregister():
    # Unregister settings
    del bpy.types.Scene.light_controller_settings
    
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
