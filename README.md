# Blender RE Mesh Noesis Wrapper
This addon utilizes the Noesis RE Mesh plugin to import and export RE Engine mesh files directly to Blender.

All RE Engine games supported by the Noesis plugin are also supported by this addon.

![Blender Preview](https://github.com/mhvuze/MonsterHunterRiseModding/blob/main/img/guides/models/REMeshNoesisWrapper/REMESH_wrapper_preview.png)
## Requirements
* [Noesis](https://richwhitehouse.com/index.php?content=inc_projects.php&showproject=91)
* [Noesis RE Mesh Plugin](https://github.com/alphazolam/fmt_RE_MESH-Noesis-Plugin)
* [Blender 2.8 or higher (version 2.93.0 recommended)](https://www.blender.org/download/)
* [Blender FBX Importer Patch](https://www.nexusmods.com/witcher3/mods/6118)

## Setting Up
Download all of the required files listed above.

Then download the addon by clicking Code > Download Zip.

Install Noesis anywhere. Extract the Noesis RE Mesh Plugin from the download. Then drag fmt_RE_MESH.py into the python folder inside the plugins folder where Noesis is installed. 

Install Blender if it isn't installed already. Back up the folder located at: ***Blender Install Folder*/*Blender Version*/scripts/addons/io_scene_fbx**

Drag the files from the FBX Importer patch into that folder. Make sure you downloaded the correct version for your Blender version.

In Blender, navigate to File > Preferences > Addons > Install From Zip File, then select the zip file for the RE Mesh Wrapper. Make sure the box next to the addon is checked, then set the Noesis.exe path in the addon preferences.

![Addon Preferences](https://github.com/mhvuze/MonsterHunterRiseModding/blob/main/img/guides/models/REMeshNoesisWrapper/REMESH_wrapper_preferences.png)

You should now be able to import and export RE Meshes via the File > Import or Export menus.

## Important Info
**NOTE: If you get the "Failed to Import RE Mesh" error, you likely have the wrong version of FBX Importer Patch.** 

**You need to use the version of the patch compatible with the version of Blender you're using.**

Any problems with exporting meshes are issues with the Noesis plugin or Blender itself, not this addon. 

Direct any problems you're having to the [RE Mesh plugin page](https://residentevilmodding.boards.net/thread/14726/re8-mhrise-modding-tools) unless you're positive it's an issue with this addon.

Materials are not imported. You will have to convert the textures using Tex Chopper and set up the materials in Blender if you want to have materials.

The naming scheme of meshes must match the Noesis plugin format: 

**LODGroup_X_Group_Y_SubMesh_Z__materialName**

The number and names of materials must match the .mdf2 file or you will get checkerboard patterns on the mesh in game.

For a more in depth guide on usage of this addon, see here:

https://github.com/mhvuze/MonsterHunterRiseModding/wiki/Importing-and-Editing-Models-with-Blender-(Noesis)

### Secondary UV Map Issue
The secondary UV map will break upon exporting from Blender. This is an issue with Blender's FBX exporter.

If you need to be able to export the second UV map, you can buy the [Better FBX Importer/Exporter](https://www.blendermarket.com/products/better-fbx-importer--exporter) addon.

This is only as a last resort though and I wouldn't recommend it unless you really need the secondary UV.

Enable "Use Better FBX Addon" in the addon preferences to use it with the wrapper.

**See Also:**

https://github.com/NSACloud/RE-Chain-Editor
