# Publishing editions
A publishing system that allows readers of an edition to search/browse editions and the materials it contains, and then enter an edition.

# Ingredients
A custom web interface, programmed in Python/Flask, reading MongoDB data.

# Description
There are several forms of dissemination that Pure3D will support:
## Downloads
This is almost the opposite of submission. The AIP is exported as-is into a zipfile for downloading by the end user. Probably it is wise to give the user some options:
* get the original 3D data (high) resolution, big files)
* get viewer-optimized derivatives in the desired quality (low-high-medium)

**N.B.** It remains to be seen whether the download function will be realized within the archive software (e.g. Dataverse) or whehter it will be a part of the dedicated dissemination app.
## Viewing in place
The Pure3D dissemination page has tabs for `home`, `about`, `contact`, `login`, `search`, `surprise me`.
The `home` page shows an introductory text about Pure3D on the left, and a list of available editions on the right.
The `search` page shows faceted and full-text search widgets, with facets coming from the metadata, the kind of files, the quality of files, the license
Once the user has selected an edition, either by searching or by browsing, serve that edition in the browser in one of the following ways:
* (default): in the most recent version of the same viewer in which the edition has been created, in medium quality (this could be a newer version than the one in which the edition has been created)
* (fall-back): in the same viewer and exactly the same version in which the edition has been created
* (optional): choose another viewer altogether, and accept that you might not see articles and notes
* (optional): choose another quality (low, high)

If the user has chosen an edition to view, a tabbed *landing page* is opened with the following tabs:
* `about` Shows the text of the `intro.md` and `usage.md` files on the left and a list of icons that link to all of the 3D models in the dataset. A click brings you to the model page, that consists of the text of `description.md` on the left, and an embedded 3D-viewer with the model loaded on the right, with which end users can interact, and in which they can view annotations and articles
* `project background` Shows the text of the `about.md`
* `sources` Shows links to download the original source data

The `surprise me` page is a magazine view of the available editions, probably a selection of the most recent dozen of them, where each edition is represented by a screenshot from the `candy` folder.

## Harvesting
Offer the OAI-PMH API to fetch (all) metadata
