bl_info = {
    "name": "Share/Lock Auto Light Renamer",
    "author": "Matthieu MattRM Barbié and Sonnet 4.5",
    "version": (1, 0, 0),
    "blender": (5, 0, 0),
    "location": "Automatic",
    "description": "Automatically renames lights with _LGT suffix when created for Share/Lock pipeline",
    "category": "Lighting",
}

import bpy
from bpy.app.handlers import persistent

# Set to track already processed lights
processed_lights = set()

@persistent
def auto_rename_light_handler(scene, depsgraph=None):
    """
    Automatically rename newly created lights with _LGT suffix
    """
    for obj in bpy.context.scene.objects:
        if obj.type == 'LIGHT':
            # Check if this light has already been processed
            if obj.name not in processed_lights:
                # Check if the light doesn't already have _LGT suffix
                if not '_LGT' in obj.name:
                    # Get the base name without any numerical suffix
                    base_name = obj.name.split('.')[0]
                    
                    # Create new name with _LGT suffix
                    new_name = f"{base_name}_LGT"
                    
                    # Rename the object
                    obj.name = new_name
                
                # Mark this light as processed
                processed_lights.add(obj.name)

@persistent
def cleanup_processed_lights(scene):
    """
    Clean up the set of processed lights when objects are deleted
    """
    current_light_names = {obj.name for obj in bpy.context.scene.objects if obj.type == 'LIGHT'}
    processed_lights.intersection_update(current_light_names)

def register():
    """Register the addon"""
    # Clear the processed lights set
    processed_lights.clear()
    
    # Register handlers
    if auto_rename_light_handler not in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.append(auto_rename_light_handler)
    
    if cleanup_processed_lights not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(cleanup_processed_lights)
    
    print("Share/Lock Auto Light Renamer addon: Enabled")

def unregister():
    """Unregister the addon"""
    # Remove handlers
    if auto_rename_light_handler in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(auto_rename_light_handler)
    
    if cleanup_processed_lights in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(cleanup_processed_lights)
    
    # Clear the set
    processed_lights.clear()
    
    print("Share/Lock Auto Light Renamer addon: Disabled")

if __name__ == "__main__":
    register()