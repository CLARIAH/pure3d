# Archive system
A repository that accepts SIPs, stores them as AIPs and can export them as DIPs.
The SIPs come from [SIP](SIP.md), and the DIPs go to [DIP](DIP.md).
The AIPs are stored and harvestable, they get a PID.

# Ingredients
* A securely backed up filesystem with a proper data layout, something like the
[Oxford Common File Layout](https://ocfl.io/1.0/spec/). Or an instance of Dataverse, provided by DANS.
* A MongoDB database for storing metadata and annotations. 
* An index system for the full text contents of articles, annotations, and metadata. 

Later we might replace this by more or less off-the-shelf archive software, such as
[Archivematica](https://www.archivematica.org/en/) or [Packrat](https://github.com/Smithsonian/dpo-packrat) or [DataVerse](https://dataverse.org) (using an instance provided by DANS).

# Description
A repository has to do many things that have to do with archive management.
We leave them undescribed for now. Instead we focus on the extra things a repository must do in order to support a 3D scholarly edition.

## Parts of the AIP
### From the SIP
An edition at rest has all the parts that have been submitted in the SIP:
* metadata (controlled vocabularies)
* descriptions (free form narratives)
* 3d data (original and derivatives)
* media
* articles
* annotations
### An addition to the SIP
The archive needs to add several things to a SIP when it is consolidated as an AIP:
* a persistent identifier
* a  version number (either an initial version number or a following one)
* a pointer to the 3D-viewer(version) that has been used to create the SIP
* an instruction how to serve the 3D-viewer with access to the articles and annotations
## Additional processing
In order to be able to manage and disseminate AIPs, the repository must maintain tables and indexes that facilitate the usual operations.
* for metadata this is more or less standard, but by no means trivial
* articles and annotations must be full-text indexed, in such a way that faceted search is possible on provenance facets (from the Dublin Core metadata and from other metadata provided in the SIP)
## Management
The 3D-viewers used are crucial for accessing editions later on. 3D-viewers are typically Javascript applications that run in the browser. These applications are dependent on countless javascript modules, but they are bundled together. We have to preserve that bundle.
Pure3D is in control of the 3D-viewers that submitters can use. Over time, these viewers will be updated, with the risk that older AIPs as rest will not work properly anymore when disseminated with the help of such newer viewer versions.
That is why the repository should maintain every viewer version that has been used for any submission.
Pure3D can still decide to use the newest viewer version by default for all dissemination, but give users the option to fall-back to older versions if they choose to do that.