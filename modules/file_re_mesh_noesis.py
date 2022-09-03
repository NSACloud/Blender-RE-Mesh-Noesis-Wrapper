#Author: NSA Cloud
import bpy

import os
import subprocess

FBX_IMPORT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),"TempFBX","import")#RE-Mesh-Noesis-Wrapper\TempFBX\import
FBX_EXPORT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),"TempFBX","export")#RE-Mesh-Noesis-Wrapper\TempFBX\export
#---RE MESH IO FUNCTIONS---#

def importREMeshFileNoesis(filePath,noesisPath,options):

	fileName = os.path.split(filePath)[1].split(".mesh")[0]
	warningList = []
	errorList = []
	try:
		os.makedirs(FBX_IMPORT_DIR, exist_ok = True)
	except OSError as error:
		errorList.append("Error: Could not create FBX import directory. " + str(error))
		return (warningList,errorList)
	if options["clearScene"]:
		for collection in bpy.data.collections:
			for obj in collection.objects:
				collection.objects.unlink(obj)
			bpy.data.collections.remove(collection)
		for bpy_data_iter in (bpy.data.objects,bpy.data.meshes,bpy.data.lights,bpy.data.cameras):
			for id_data in bpy_data_iter:
				bpy_data_iter.remove(id_data)
		for material in bpy.data.materials:
			bpy.data.materials.remove(material)
		for amt in bpy.data.armatures:
			bpy.data.armatures.remove(amt)
		for obj in bpy.data.objects:
			bpy.data.objects.remove(obj)
			obj.user_clear()

	print("\033[96m__________________________________\nRE Mesh import started.\033[0m")
	noesisCommand = "\""+noesisPath + "\" ?cmode " +"\"" + filePath + "\" " + "\""+os.path.join(FBX_IMPORT_DIR,fileName+".fbx") +"\""
	print("Running Noesis...")
	#print(noesisCommand)
	subprocess.run(noesisCommand,shell=True)
	if os.path.exists(os.path.join(FBX_IMPORT_DIR,fileName+".fbx")):
		options["useBetterFBX"] = False#TEMPORARY
		if options["useBetterFBX"]:#Disabling import from better fbx for now since it's not consistent with Blender's FBX import and will cause issues when exporting
			try:
				print("Importing using Better FBX Importer")
				if "better_fbx" in bpy.context.preferences.addons.keys():
					bpy.ops.better_import.fbx(filepath = os.path.join(FBX_IMPORT_DIR,fileName+".fbx"),use_reset_mesh_origin=False)
				else:
					errorList.append("ERROR: Better FBX Importer addon is not installed.\n")
					return (warningList,errorList)
			except Exception as error:
				errorList.append("ERROR: FBX import failed. Check that the Noesis path is correct and that the RE Mesh plugin is installed.\nAlso check that the correct version of the FBX patch is installed for your version of Blender.\n" + str(error))
				return (warningList,errorList)
		else:		
			try:
				print("Importing using default Blender FBX Importer")
				bpy.ops.import_scene.fbx(filepath = os.path.join(FBX_IMPORT_DIR,fileName+".fbx"))
			except Exception as error:
				errorList.append("ERROR: FBX import failed. Check that the Noesis path is correct and that the RE Mesh plugin is installed.\nAlso check that the correct version of the FBX patch is installed for your version of Blender.\n" + str(error))
				return (warningList,errorList)
	else:
		errorList.append("ERROR: No FBX file was created by Noesis. The mesh file may be corrupted or unreadable.")
		return (warningList,errorList)
	try:
		os.remove(os.path.join(FBX_IMPORT_DIR,fileName+".fbx"))
	except:
		warningList.append("WARNING: Failed to delete temporary FBX from TempFBX directory.")
	print("\033[92m__________________________________\nRE Mesh import finished.\033[0m")
	return (warningList,errorList)
	
def exportREMeshFileNoesis(filePath,noesisPath,options):
	
	fileName = os.path.split(filePath)[1].split(".mesh")[0]
	warningList = []
	errorList = []
	try:
		os.makedirs(FBX_EXPORT_DIR, exist_ok = True)
	except OSError as error:
		errorList.append("Error: Could not create FBX export directory. " + str(error))
		return (warningList,errorList)
	print("\033[96m__________________________________\nRE Mesh export started.\033[0m")
	
	#Basic Error Checking
	if options["selection_only"]:
		selection = bpy.context.selected_objects
	else:
		selection = bpy.context.scene.objects
	containsMesh = False
	armatureCount = 0
	for obj in selection:
		if obj.type == "MESH":
			containsMesh = True
			#Check if mesh contains at least one face
			if len(obj.data.loops) == 0:
				errorList.append("ERROR: " + obj.name + " has no faces. A mesh requires at least one face.")
			#Check if parented to armature
			if len(obj.vertex_groups) > 0:
					
				armature = None
				for modifier in obj.modifiers:
					if modifier.type == "ARMATURE":
						#print(modifier.object)
						try:
							if bpy.data.objects.get(modifier.object.name):#Check if armature modifier points to an armature
								armature = modifier.object
						except:
							pass
				if armature != None:
					#Check that every vertex group exists on the armature
					for vertexGroup in obj.vertex_groups:
						emptyVertexGroup = not any(vertexGroup.index in [g.group for g in v.groups] for v in obj.data.vertices)
						if armature.data.bones.get(vertexGroup.name,None) == None and not emptyVertexGroup:
							warningList.append("WARNING: " + obj.name + " is weighted to " + vertexGroup.name + ", but that bone does not exist on the armature." )
				else:
					warningList.append("WARNING: " +obj.name + " contains vertex groups but is not parented to an armature.")
				#Check that naming scheme is valid
			split = obj.name.split("_")
			try:
				if split[0].split("_")[0] != "LODGroup" or split[2].split("_")[0] != "Group" or split[4].split("_")[0] != "SubMesh" or split[6].split("_")[0] != "":
					warningList.append("WARNING: "+obj.name + " does not match the Noesis plugin mesh naming scheme:\n\t LODGroup_X_Group_Y_SubMesh_Z__materialName")
			except:
				warningList.append("WARNING: "+obj.name + " does not match the Noesis plugin mesh naming scheme:\n\tLODGroup_X_Group_Y_SubMesh_Z__materialName")
		elif obj.type == "ARMATURE":
			#Get amount of armatures in selection
			armatureCount += 1
	if armatureCount > 1:
		warningList.append("WARNING: More than one armature is present. Only one armature can be used.")
	if not containsMesh:
		errorList.append("ERROR: No meshes in selection or scene.")
	if errorList == []:
		if options["useBetterFBX"]:
			print("Exporting using Better FBX Exporter")
			if "better_fbx" in bpy.context.preferences.addons.keys():
				bpy.ops.object.mode_set(mode='OBJECT')
				bpy.ops.better_export.fbx(filepath=os.path.join(FBX_EXPORT_DIR,fileName+".fbx"),
				use_selection = options["selection_only"],
				use_animation=False,
				use_optimize_for_game_engine = False,
				use_reset_mesh_origin = False,
				my_fbx_axis = "OpenGL")
			else:
				errorList.append("ERROR: Better FBX Importer addon is not installed.\n")
				return (warningList,errorList)
		else:
			print("Exporting using default Blender FBX Exporter")
			bpy.ops.export_scene.fbx(filepath=os.path.join(FBX_EXPORT_DIR,fileName+".fbx"),
			use_selection = options["selection_only"],
			add_leaf_bones=False,
			object_types={'ARMATURE', 'MESH'})
		args = ""
		if options["rewrite"]:
			args +=" -rewrite"
		if options["bonenumbers"]:
			args += " -bonenumbers"
		if options["flip"]:
			args += " -flip"
		if options["bones"]:
			args += " -bones"
		if options["vfx"]:
			args += " -vfx"
		if options["adv"]:
			args += " -adv"
		if os.path.exists(os.path.join(FBX_EXPORT_DIR,fileName+".fbx")):
			noesisCommand = "\""+noesisPath + "\" ?cmode " +"\"" + os.path.join(FBX_EXPORT_DIR,fileName+".fbx") + "\" " + "\""+filePath+ "\"" + args
			print("Running Noesis...")
			#print(noesisCommand)
			subprocess.run(noesisCommand,shell=True)
			try:
				os.remove(os.path.join(FBX_EXPORT_DIR,fileName+".fbx"))
				#pass
			except:
				warningList.append("WARNING: Failed to delete temporary FBX from TempFBX directory.")
			print("\033[92m__________________________________\nRE Mesh export finished.\033[0m")
	else:
		print("\033[91m__________________________________\nRE Mesh export failed.\033[0m")
	return (warningList,errorList)