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

# Workspaces and user roles
Work on editions happens in an online *workspace*, offered by the Pure3D infrastructure.
A workspace is an online folder with a predefined structure, see below. 
Some folders are under direct control of the editors, other folders contain generated/derived materials.

Authenticated users can ask to set up such a workspace, of which they become a user in the role of *admin*. 

These are the rights associated with the roles:
* *reader*: read, comment access to the workspace
* *editor*: read, comment, write access to the workspace
* *admin*: read, comment, write, admin access to the workspace

Admin tasks are:
* invite other users to the workspace
* delete users from the workspace
* change the roles of workspace users
* publish and archive the edition that is made in the workspace
* clear the workspace after the work is done

# Conflict reduction
When multiple users have write access to the same resources, save conflicts may occur. Unhandled save conflicts may lead to data loss. There are several strategies to handle save conflicts.
* **LOCK** prevent simultaneous write access by a locking system
* **COPY** make multiple copies in case of conflict and merge them later
* **PASSIVE** we leave it to the underlying systems, e.g. MongoDB or the (WebDav) file system, if we are convinced that they have a suitable save-conflict-strategy.

Below, we refer to these solutions as *save-conflict-strategy*.

Examples where extra care is needed:
* the forms for entering metadata
* using the 3d-viewers to make annotations

Note on the **COPY** strategy: the system remembers the moments of checkout and of save for each edit action. When the user triggers a save action, it will be checked if there has been other save actions after the checkout action. If so, the save action will be applied to a copy with the name of the user attached to it, instead of overwriting a previously saved version.
This prevents people from unknowingly overwriting each other's updates.

# Scenarios
## A user logs in, a new user registers
By means of CLARIAH authentication. 
After log in, users will see a list of their workspaces with the kind of access they have to them.
From this list they can enter a workspace.

## Entering a workspace
This will bring users to the main page of the workspace, from where they can see all accessible data in the workspace.

## Requesting a fresh workspace
Users may point to an existing edition and ask to load it into the workspace in order to work on a new version of that edition.
If no such edition is given, a bare workspace will be created, ready for working on a brand new edition.

Additionally:
* a form is presented to fill out and/or update essential metadata (Dublin Core). The response will be saved to a file in the workspace.
* the requesting user is given the *admin* role over the work space.

## An admin manages workspace users
The system maintains a list of users the workspace and their roles. Admins may change the roles, and add/delete users to/from the workspace.

Users are added by means of an email address. An invitation will be send to that email address. Any authenticated user with that email address has access to the workspace. If the recipient is not a registered user, (s)he can register with that email address, after which (s)he has access to the workspace.

*save-conflict-strategy*: **LOCK**

## An editor updates metadata
This can be the mandatory Dublin Core metadata or metadata according to any other registered schema. 

*save-conflict-strategy*: **LOCK**

## An editor adds a 3D model
 There will be guidelines and tools to help the editors to upload 3D data of good quality and to produce derivatives that are optimised to show in 3D viewers.
 Models of original quality and derived models can be uploaded to dedicated folders.
 
*save-conflict-strategy*: **PASSIVE**

## An editor adds rich text and media
The texts should be written in `.md` files from where media files can be referenced.
Texts and media should be placed in a prescribed folder organisation.
It should be clear which Markdown syntax is supported and which parts are not supported.

Editors can trigger a preview of the formatted texts. The system will run a Markdown formatter and put the results in a generated read-only directory.

There are two destinations for these texts:
* on the interface of the Pure3D website: (short) descriptions, usage instructions, colofons;
* articles that are referenced by annotations created in the 3D viewers
 
*save-conflict-strategy*: **COPY**

## An editor works with annotations using a 3D viewer
The system presents an embedded 3D viewer (e.g. the Smithsonian Voyager) and lets the editor add/modify/delete annotations.

*save-conflict-strategy*: **COPY**

## An editor resolves a save conflict
The system presents the versions involved in a save conflict, showing which users saved what at what time, and lets the editor choose between the versions. If none of the versions is right, the editor can supply a new version.

## An admin publishes a workspace
 When an admin deems the edition-in-the-works to be publishable, (s)he can publish the workspace. 
* The system will generate formatted pages from the markdown and media for the last time.
* The workspace contents is copied to the AIP storage and put in place there. It will become the first version of a new edition or the next version of an existing edition.
* A persistent identifier will be registered for the edition version
* The list of all versions of the edition will be updated
* The system will offer to update the list of contributors in the Dublin Core metadata based on the list of all admins, editors and readers that have been involved with the workspace.

## An admin clears a workspace
When an admin clears a workspace, all data in it gets removed and all users of it loose access to it.
We could consider to give admins a grace period of 30 days during which their workspace remains accessible (read-only) for all of its users, and during which admins can reverse this action.

# Workspace structure

Here is the file and folder layout of a workspace

`meta` ==all metadata==
* `dc.json`  ==Dublin Core==
* `license.txt` ==text of license==
* `license.json` ==properties of license==
* *xxx*`.json` ==metadata according to schema *xxx*==

`3d` ==all 3d data==
* `original` ==source data as is; as many models as needed, arbitrary names for models, arbitrary names for data files==
  * *modelA* - *x*`.gltf`
  * *modelB* - *y*`.gltf`
  
* `derived` ==viewer-optimized data processed from original data; model names must match those in `original`, arbitrary names for data files; fixed names for viewers==
  * `high` ==high quality optimization==
    * `voyager`
      * *modelA* - *x1*`.gltf`
      * *modelB* - *y1*`.gltf`
    * `virtualinteriors`
      * *modelA* - *x2*`.gltf`
      * *modelB* - *y2*`.gltf`
  * `medium`==medium quality optimization==
    * `voyager`
      * *modelA* - *x3*`.gltf`
      * *modelB* - *y3*`.gltf`
    * `virtualinteriors`
      * *modelA* - *x4*`.gltf`
      * *modelB* - *y4*`.gltf`
  * `low`==low quality optimization==
    * `voyager`
      * *modelA* - *x5*`.gltf`
      * *modelB* - *y5*`.gltf`
    * `virtualinteriors`
      * *modelA* - *x6*`.gltf`
      * *modelB* - *y6*`.gltf`
  
* `fallback` ==impression of the data for when supporting software no longer works, arbitrary collection of images, movies, pdf documents, plain text documents==
  * *screenshot*`.png`
  * *movie*`.mp4`
  * *doc*`.pdf`
  * *explanation*`.txt`
  
`candy` ==a bunch of salient screenshots that can be used as icons to represent the edition==
* *logo*`.png`
* *icon*`.png`
  
`media` ==supporting images, movies, sounds, etc. to be referenced by texts below; any number of files with arbitrary names==
* *sound*`.mp3`
* *movie*`.mp4`
* *image*`.png`

`texts` ==markdown-formatted texts for various purposes==
* `intro.md` ==short introduction to the edition==
* `about.md` ==more details about the edition, colofon like==
* `description.md` ==a longer narrative that describes the edition==
* `usage.md` ==ways in which readers can use the edition==
* `articles` ==texts that can be called up within the 3d viewers; arbitrary number with arbitrary names==
  * *a1*`.md`
  * *a2*`.md`
  * *an*`.md`
  
`rendered` ==rendered markdown texts==
* `intro.html`
* `about.html`
* `description.html`
* `usage.html`
* `articles` ==rendered articles==
  * *a1*`.html`
  * *a2*`.html`
  * *an*`.html`

`annotations` ==annotations as saved from the 3d-viewers; files, formats and names dependent on the viewer, may contain unresolved save conflicts==
* *x*`.json`
* *y*`.json`
* *y*`-conflict.json`
