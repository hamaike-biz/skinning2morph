import bpy

bl_info = {
    "name": "Skinning2Morph",
    "author": "hamaike",
    "version": (0, 1),
    "blender": (2, 81,),
    "location": "COMMUNITY",
    "description": "Create Morph from Skinning.",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}


def frame_range(scene):
    """Return a range object with with scene's frame start, end, and step"""
    return range(scene.frame_start, scene.frame_end, scene.frame_step)


# operatator
class P2M_OT_converter(bpy.types.Operator):
    bl_idname = "pose.2morph"
    bl_label = "convert2morph"
    bl_description = "Poselib converts to Morph 001"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        # logger(obj.type)
        return context.mode == 'OBJECT'

    def draw(self, context):
        layout = self.layout
        layout.label(text="OK!")

    def execute(self, context):

        active_object = bpy.context.active_object
        modifiers = active_object.modifiers
        track_name = active_object.parent.animation_data.nla_tracks.active.name
        shape_keys_len = len(bpy.data.shape_keys)

        if shape_keys_len > 0:
            last_shape_key_index = len(bpy.data.shape_keys[0].key_blocks) - 1
        else:
            last_shape_key_index = 0

        for modifier in modifiers:
            if modifier.type == 'ARMATURE':

                self.create_shapekeys_from_armature(modifier, context, active_object)

                for frame_index in frame_range(context.scene):
                    context.scene.frame_set(frame_index)

                    active_object.active_shape_key_index = last_shape_key_index + frame_index
                    active_object.active_shape_key.value = 1.000
                    active_object.active_shape_key.keyframe_insert(data_path="value")
                    current_shapekey_name = f'{track_name}_{frame_index}'
                    active_object.active_shape_key.name = current_shapekey_name

                for frame_index in frame_range(context.scene):
                    current_shapekey_name = f'{track_name}_{frame_index}'
                    for shapekey in bpy.data.shape_keys:
                        for keyblock_index, keyblock in enumerate(shapekey.key_blocks):
                            if keyblock.name == current_shapekey_name:
                                pass
                            elif f'{track_name}_' in keyblock.name:
                                keyblock.value = 0.000
                                keyblock.keyframe_insert(data_path="value", frame=frame_index)

                # 0 フレーム目の value は全て 0.000 にする
                for shapekey in bpy.data.shape_keys:
                    for keyblock_index, keyblock in enumerate(shapekey.key_blocks):
                        keyblock.value = 0.000
                        keyblock.keyframe_insert(data_path="value", frame=0)

                active_object.data.shape_keys.animation_data.action.name = f'KeyAction{track_name}'
                logger(active_object.data.shape_keys.animation_data.action.name)

        return {'FINISHED'}

    def create_shapekeys_from_armature(self, modifier, context, active_object):
        modifier_name = modifier.name
        modifier_obj = modifier.object
        for frame_index in frame_range(context.scene):
            context.scene.frame_set(frame_index)
            bpy.context.view_layer.objects.active = modifier_obj
            bpy.context.view_layer.objects.active = active_object
            bpy.ops.object.modifier_apply_as_shapekey(
                keep_modifier=False,
                modifier=bpy.context.object.modifiers[modifier_name].name
            )
            newmod = active_object.modifiers.new(modifier_name, "ARMATURE")
            newmod.object = modifier_obj


class VIEW3D_PT_Skinning2Morph(bpy.types.Panel):
    """Creates a Panel in 3D Viewport"""
    bl_label = "Skinning2Morph"
    bl_idname = "VIEW3D_PT_armature_2_morph"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Skinning2Morph"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        scene = context.scene
        col = layout.column(align=True)
        col.prop(scene, "frame_start", text="Frame Start")
        col.prop(scene, "frame_end", text="End")
        col.prop(scene, "frame_step", text="Step")
        row = layout.row()
        row.operator("pose.2morph")
        row = layout.row()
        row.operator("morph.exporter")


class VIEW3D_PT_MorphExporter(bpy.types.Panel):
    bl_label = "export mesh"
    bl_idname = "morph.exporter"
    bl_description = "Poselib converts to Morph 001"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Skinning2Morph"

    def draw(self, context):
        pass

    def execute(self, context):
        logger("execute!!")


def logger(*args):
    print(f' ')
    print(f'########## START LOG ##########')
    print(args)
    print(f'########## END LOG ##########')
    print(f' ')


def menu_func(self, context):
    self.layout.operator("pose.2morph")


classes = [
    P2M_OT_converter,
    VIEW3D_PT_MorphExporter,
    VIEW3D_PT_Skinning2Morph
]


# アドオン有効化時の処理
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    # bpy.types.VIEW3D_MT_object.append(menu_func)
    # bpy.utils.register_class(VIEW3D_PT_VertexAnimation)
    print("アドオンを有効化しました")


# アドオン無効化時の処理
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    print("アドオンを無効化しました")


if __name__ == "__main__":
    register()
