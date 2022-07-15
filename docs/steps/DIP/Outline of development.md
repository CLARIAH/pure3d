# Developing a dissemination site
# Markdown formatter
* [ ] Make a python script to convert Markdown into HTML
	* [ ] make sure it works on the command line as well, lile `markdown file.md`; the result should then be `file.html`. You can use this to test whether the markdown is right.
	* [ ] You can also use Jupyter Notebook to test how markdown code renders

# Editions on the file system
* [ ] create a few editions on the file system in directory `data/editions` according to the workspace layout in [SIP](../../architecture/SIP.md)
	* but keep the 3D models simple: no distinction between original and derived, and no low, medium, and high resolution distinction
	* put real 3D models in at least two editions
	* put realistic markdown descriptions in (use the materials by Kelly, make sure that you use proper markdown code, and that it displays well, see previous step

# Develop the flask application
* [ ] define url paths to naviagte through the editions
* [ ] make templates for the pages of the [](PURE3DWireframe.pdf)
* [ ] develop the flask app so that the website responds to those urls with the proper actions
	* you can wait with the challenge of loading models in the Voyager viewer, concentrate on everything else than the 3D models
	* you can also wait with implementing search

# Website system
Start with this once you have access to a Linux machine and have moved your development to that Linux machine.
* [ ] make it so that the website runs on the local (Linux or Macos) machine of whoever clones this repository
* [ ] provide scripts for installation and to start the server
	* see `programs/install.sh` and `programs/serve.sh`
	* these should be shell scripts, not windows batch files
* [ ] provide installation instructions
	* see `docs/steps/DIP/README.md