#Author: NSA Cloud
bl_info = {
	"name": "RE Mesh Noesis Wrapper",
	"author": "NSA Cloud",
	"version": (5, 1),
	"blender": (2, 93, 0),
	"location": "File > Import-Export",
	"description": "Import and export RE Engine Mesh files using Noesis.",
	"warning": "",
	"wiki_url": "https://github.com/NSACloud/Blender-RE-Mesh-Noesis-Wrapper",
	"tracker_url": "",
	"category": "Import-Export"}

import bpy
import os

from bpy_extras.io_utils import ExportHelper,ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, CollectionProperty
from bpy.types import Operator, OperatorFileListElement,AddonPreferences

from .modules.file_re_mesh_noesis import importREMeshFileNoesis,exportREMeshFileNoesis

os.system("color")#Enable console colors

def showMessageBox(message = "", title = "Message Box", icon = 'INFO'):

	def draw(self, context):
		self.layout.label(text = message)

	bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

class REMeshNoesisWrapperPreferences(AddonPreferences):
	bl_idname = __name__
 
	noesisPath: StringProperty(
		name="Noesis.exe Path",
		subtype='FILE_PATH',
	)
	useBetterFBX: BoolProperty(
		name="Use Better FBX Addon (Requires Better FBX)",
		description = "Use Better FBX Importer / Exporter addon instead of Blender's default fbx exporter. Do not enable if Better FBX is not installed. WARNING: Export is bugged and chain files will not work properly",
		default = False
	)
	def draw(self, context):
		layout = self.layout
		layout.prop(self, "noesisPath")
		layout.prop(self, "useBetterFBX")

class ImportREMeshNoesis(Operator, ImportHelper):
	'''Import RE Mesh File'''
	bl_idname = "re_mesh_noesis.importfile"
	bl_label = "Import RE Mesh"
	bl_options = {'PRESET', "REGISTER", "UNDO"}
	files : CollectionProperty(
			name="File Path",
			type=OperatorFileListElement,
			)
	directory : StringProperty(
			subtype='DIR_PATH',
			)
	filename_ext = ".mesh.*"
	filter_glob: StringProperty(default="*.mesh.*", options={'HIDDEN'})
	clear_scene : BoolProperty(
	   name = "Clear scene before import.",
	   description = "Clears all objects before importing",
	   default = True)
	def execute(self, context):
		options = {"clearScene":self.clear_scene,"useBetterFBX":bpy.context.preferences.addons[__name__].preferences.useBetterFBX}
		if os.path.isfile(bpy.context.preferences.addons[__name__].preferences.noesisPath.replace("\"","")):#Strip quotation marks if they're in the noesis path
			directory = self.directory
			for file_elem in self.files:
				filepath = os.path.join(directory, file_elem.name)
				if os.path.isfile(filepath):
					result = importREMeshFileNoesis(filepath,bpy.context.preferences.addons[__name__].preferences.noesisPath.replace("\"",""),options)#Returns tuple containing list of warnings and errors
					if result[1] != []:#Error List
						showMessageBox("An error occurred during import. See Window > Toggle System Console for details.","Error","ERROR")
						for error in result[1]:
							print('\033[91m'+error+'\033[0m')
							self.report({"INFO"},"Failed to import RE Mesh. See Window > Toggle System Console for details.")
						for warning in result[0]:
							print('\033[93m'+warning+'\033[0m')
						return {'CANCELLED'}
					elif result[0] != []:#Warning List
						showMessageBox("Warnings occurred during import. See Window > Toggle System Console for details.","Warning","ERROR")
						for warning in result[0]:
							print('\033[93m'+warning+'\033[0m')
					self.report({"INFO"},"Imported RE Mesh successfully.")
					return {'FINISHED'}
		else:
			msg = "Error: Noesis path is not set or is invalid. Set the path to Noesis.exe in Preferences > Addons > RE Mesh Noesis Wrapper. Also make sure fmt_RE_MESH.py is installed to the Noesis python plugins folder"
			showMessageBox(msg,"RE Mesh Import","ERROR")
			print('\033[91m'+msg+'\033[0m')
			self.report({"INFO"},"Noesis.exe path is not set.")
			return {'CANCELLED'}
		
class ExportREMeshNoesis(Operator, ExportHelper):
	'''Export RE Mesh File'''
	bl_idname = "re_mesh_noesis.exportfile"
	bl_label = "Export RE Mesh"
	bl_options = {'PRESET'}
	
	filter_glob: StringProperty(default="*.mesh*", options={'HIDDEN'})
	filename_ext: EnumProperty(
		name="Mesh Version",
		description="Set which game to export the mesh for",
		items=[ (".2109148288", "MHRise (Post Sunbreak)", ""),
				(".2008058288", "MHRise (Pre Sunbreak)", ""),
				(".2101050001", "RE8", ""),
				(".220128762", "RE7 RT Update", ""),
				(".32", "RE7", ""),
				(".2109108288", "RE2/RE3 RT Update", ""),
				(".1902042334", "RE3", ""),
				(".1808312334", "RE2", ""),
				(".2010231143", "REVerse", ""),
				(".1808282334", "DMC5", ""),

			   ]
		)
	#FBX Exporter Settings
	selection_only : BoolProperty(
	   name = "Selected Only",
	   description = "Limit export to selected objects",
	   default = False)
	#Noesis Exporter Arguments
	rewrite : BoolProperty(
	   name = "Rewrite",
	   description = "Rewrite submeshes and materials structure. NOTE: If rewrite is disabled, the materials, mesh count and bones must match the original file",
	   default = True)
	bonenumbers : BoolProperty(
	   name = "Bone Numbers",
	   description = "Add bone numbers to imported bones",
	   default = False)
	flip : BoolProperty(
	   name = "Flip",
	   description = "Reverse handedness from DirectX to OpenGL",
	   default = False)
	bones : BoolProperty(
	   name = "Bones",
	   description = "Write new skeleton on export. NOTE: Rewrite also writes new skeletons",
	   default = False)
	vfx : BoolProperty(
       name = "VFX Model",
       description = "Use this option if you're exporting an EFX model. NOTE: The secondary UV map will break upon export unless you are using the Better FBX addon(Not to be confused with the FBX patch)",
       default = False)
	adv : BoolProperty(
	   name = "Show Advanced",
	   description = "Show advanced export options window",
	   default = False)
	
	def execute(self, context):
		options = {"selection_only":self.selection_only,"rewrite":self.rewrite,"bonenumbers":self.bonenumbers,"flip":self.flip,"bones":self.bones,"adv":self.adv,"vfx":self.vfx,"useBetterFBX":bpy.context.preferences.addons[__name__].preferences.useBetterFBX}
		print(os.path.join(os.path.dirname((bpy.context.preferences.addons[__name__].preferences.noesisPath.replace("\"","")))),"plugins","python","fmt_RE_MESH.py")
		if os.path.isfile(bpy.context.preferences.addons[__name__].preferences.noesisPath.replace("\"","")) and os.path.isfile(os.path.join(os.path.dirname((bpy.context.preferences.addons[__name__].preferences.noesisPath.replace("\"",""))),"plugins","python","fmt_RE_MESH.py")):
			
			result = exportREMeshFileNoesis(self.filepath,bpy.context.preferences.addons[__name__].preferences.noesisPath.replace("\"",""),options)
			report = "Exported RE Mesh successfully."
			if result[1] != []:#Error List
				showMessageBox("An error occurred during export. See Window > Toggle System Console for details.","Error","ERROR")
				for error in result[1]:
					print('\033[91m'+error+'\033[0m')
				for warning in result[0]:
					print('\033[93m'+warning+'\033[0m')
				self.report({"INFO"},"Failed to export RE Mesh. See Window > Toggle System Console for details.")
				return {'CANCELLED'}
			elif result[0] != []:#Warning List
				showMessageBox("Warnings occurred during export. See Window > Toggle System Console for details.","Warning","ERROR")
				report = "Exported RE Mesh with warnings."
				for warning in result[0]:
					print('\033[93m'+warning+'\033[0m')
				
			self.report({"INFO"},report)
			return {"FINISHED"}
		else:
			msg = "Error: Noesis path is not set or is invalid. Set the path to Noesis.exe in Preferences > Addons > RE Mesh Noesis Wrapper."
			showMessageBox(msg,"RE Mesh Import","ERROR")
			print('\033[91m'+msg+'\033[0m')
			self.report({"INFO"},"Noesis.exe path is not set.")
			return {'CANCELLED'}

# Registration
classes = [
	ImportREMeshNoesis,
	ExportREMeshNoesis,
	REMeshNoesisWrapperPreferences
	]


def re_mesh_noesis_import(self, context):
	self.layout.operator(ImportREMeshNoesis.bl_idname, text="RE Mesh (.mesh) (Noesis)")
	
def re_mesh_noesis_export(self, context):
	self.layout.operator(ExportREMeshNoesis.bl_idname, text="RE Mesh (.mesh) (Noesis)")


def register():
	for classEntry in classes:
		bpy.utils.register_class(classEntry)
		
	bpy.types.TOPBAR_MT_file_import.append(re_mesh_noesis_import)
	bpy.types.TOPBAR_MT_file_export.append(re_mesh_noesis_export)
	
	
def unregister():
	for classEntry in classes:
		bpy.utils.unregister_class(classEntry)
		
	bpy.types.TOPBAR_MT_file_import.remove(re_mesh_noesis_import)
	bpy.types.TOPBAR_MT_file_export.remove(re_mesh_noesis_export)
if __name__ == '__main__':
	register()