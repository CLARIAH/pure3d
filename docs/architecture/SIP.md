# Ingest system
The ingest system is an online file system that gives authenticated users the following functions:
* manage files and folders in a workspace (uploading, downloading, organising)
* view 3D data in 3D viewers
* store the results of editing in dedicated annotations
* publish the contents as a dataset to the AIP system

# Ingredients
* CLARIAH authentication
* NextCloud or something else under CLARIAH authentication
* Deployment of Smithsonian Voyager in such a way that users save into the workspace that they are using
* A way to get the contents of a workspace into the AIP system.

# Description
Here is a sequence of events to support
* An edition writer logs in and requests a space to create a new edition
* The system asks for essential metadata (Dublin Core) and saves that to file
* Then it creates a fresh workspace, with a set of predefined folders, and puts the previously collected Dublin Core metadata in it
* The edition writer can share this workspace with co-workers by means of an invitation system. Invited coworkers must be able to authenticate themselves in order to get read/write access.
* The edition writers upload 3D data into a dedicated directory. They also upload related media into another dedicated toplevel directory.
* There are guidelines and tools to help the writers to upload 3D data of good quality and to produce derivatives that are optimized to show in 3D viewers
* They can view the 3D data in the Smithsonian Voyager viewer, in which they can make annotations and write articles, with almost arbitrary HTML content.
* When they save work from within the 3D viewer, annotations, articles and tours are saved in dedicated directories.
* At anytime, a dialogue can be invoked to modify the Dublin Core metadata. There are also dialogues to enter metadata according various other schemes.
* When all edition writers agree that the work is publishable, the workspace can be published. That means, it contents is copied to the AIP storage and put in place there. It will become the first version of a new edition.
* Edition writers may also request to update an existing edition. They get a workspace, filled with the contents of an existing AIP, and they can do essentially the same work as described above. Upon publishing, the workspace is saved as a new *version* of the edition in question.

Here is the file and folder layout of a workspace
* folder `meta`: with json files containing metadata. These files can be created/updated by filling out forms, or they can be directly manufactured by the edition writers, or both.
	* file `dc.json`: the file with Dublin Core metadata
	* a `license.txt` file, containing the text of a license
	* a `license.json` file, containing attributes of the license, e.g. its url, whether it is open, and something that codes the permissions that Pure3D has to show it to users for viewing/downloading
	* `.json` files corresponding with other supported metadata schemes
* folder `description`: contains the introductory texts of the edition, as a set of markdown files. These markdown files may link to each other and to files in the `media` folder below. There will be some overlap between the content of these files and the more formal content of the metadata files.
	* `intro.md`: short introduction to the edition
	* `about.md`: more details about the edition, colofon like
	* `description.md`: a longer narrative that describes the edition
	* `usage.md`: ways in which readers can use the edition
* folder `3d`: with the 3D data files.
	* subfolder `original` with original resolution files of a single 3D model; probably a single `.obj` or `.gltf` file possibly augmented with `.mtl` files etc.
	* subfolder `derivatives` with a subfolder for each supported viewer, e.g. `voyager`. And for each viewer subdirectories named `low`, `high`, `medium` with a derivative of that quality of the original.
* folder `candy` with a few screenshots that give a candid view on the 3D data, to be used in iconic representations of the edition in several places of the Pure3D interface.
* folder `fallback` with screenshots and plain texts of how key parts of the edition look in the viewer. This is meant as a fallback for the very long-term when most of the software that supports editions have become obsolete beyond repair.
* folder `media`: with text/image/video material that can be referenced in articles and annotation bodies. May contain subfolders, the organisation is up to the edition writers.
* folder `articles`: where articles, created within the Voyager, are saved.  This folder is under edit control of the system, although the editors can read its files.
* folder `annotations`: where annotations, created within the Voyager, are stored. This folder is under edit control of the system, although the editors can read its files.