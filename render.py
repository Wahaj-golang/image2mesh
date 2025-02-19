# import_floorplan.py
import bpy
import json
import os
import bmesh
from mathutils import Vector

def create_extruded_mesh(name, points, height=3.0):
    """Create a 3D mesh in Blender by extruding a 2D polygon."""
    # Create a new mesh and object
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    
    # Build geometry using BMesh
    bm = bmesh.new()
    verts = []
    for p in points:
        # p is [x, y]; set z=0 for the base
        v = bm.verts.new((p[0], p[1], 0))
        verts.append(v)
    
    try:
        face = bm.faces.new(verts)
    except Exception as e:
        print("Error creating face for", name, ":", e)
        bm.free()
        return None

    # Extrude the face along the Z-axis
    bm.faces.ensure_lookup_table()
    face = bm.faces[0]
    extrude_result = bmesh.ops.extrude_face_region(bm, geom=[face])
    geom_extruded = extrude_result["geom"]
    verts_extruded = [ele for ele in geom_extruded if isinstance(ele, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, verts=verts_extruded, vec=(0, 0, height))
    
    # Write the BMesh to the Mesh datablock and free the BMesh
    bm.to_mesh(mesh)
    bm.free()
    
    return obj

def main():
    # Assume the JSON file is in the same directory as this script
    script_dir = os.path.dirname(bpy.data.filepath) if bpy.data.filepath else os.getcwd()
    json_file = os.path.join(script_dir, "generated_geometry_data.json")
    
    if not os.path.exists(json_file):
        print("Error: JSON file not found:", json_file)
        return
    
    with open(json_file, "r") as f:
        geometry_data = json.load(f)
    
    # Loop over each element in the JSON and create the corresponding mesh
    for i, item in enumerate(geometry_data):
        points = item["points"]
        if item["type"] == "wall":
            create_extruded_mesh(f"Wall_{i}", points, height=3.0)
        elif item["type"] == "door":
            create_extruded_mesh(f"Door_{i}", points, height=2.2)
        else:
            print("Unknown type:", item["type"])
    
    # Optional: frame all objects in the viewport
    # for area in bpy.context.screen.areas:
    #     if area.type == 'VIEW_3D':
    #         override = bpy.context.copy()
    #         override['area'] = area
    #         bpy.ops.view3d.view_all(override)
    #         break
    
    # Export the entire scene as an OBJ file
    export_path = os.path.join(script_dir, "floorplan_export")
    bpy.ops.export_scene.gltf(filepath=export_path, use_selection=False)
    print("Scene exported to", export_path)

if __name__ == "__main__":
    main()
