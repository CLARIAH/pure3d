# Archive system
A repository that accepts SIPs, stores them as AIPs and can export them as DIPs.
The SIPs come from [[SIP]], and the DIPs go to [[DIP]].
The AIPs are stored and harvestable, they get a PID.

## Ingredients
* A securely backed up filesystem with a proper data layout, something like the
[Oxford Common File Layout](https://ocfl.io/1.0/spec/).
* A MongoDB database for storing metadata and annotations
* An index system for the full text contents of articles, annotations, and metadata.

Later we might replace this by more or less off-the-shelf archive software, such as
[Archivematica](https://www.archivematica.org/en/) or [Packrat](https://github.com/Smithsonian/dpo-packrat).