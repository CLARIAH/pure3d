The Smithsonian Voyager client in the browser expects a WebDav server at the other end.
It uses WebDav to get the 3D models in, and to send the user-created annotations back.
The Voyager software only includes a demo webdav server, within the Node.js ecosystem.

A few quotes from the [dpo-voyager repo](https://github.com/Smithsonian/dpo-voyager):

From `/docker-compose.yml`:

> The server provides unsecured read access to dist/ and read/write access through WebDAV to files/

From `/docs/content/introduction/hosting/_index.md`:

> **Note:** The prebuilt Voyager package requires WebDAV enabled file server access to any content for the Story component to save changes directly to disk. If this is not available to you, try [installing from source](../../introduction/installation/) which includes a simple server, or ['Standalone' mode](../../story/overview/) when using Story.

From `/docs/content/story/overview/index.md`:

> By default, _Voyager Story_ requires a WebDAV file server backend to facilitate saving Voyager files directly to your permanent storage location. If you spin up Voyager from the source ([instructions here](../../introduction/installation/)) a simple server is included. Otherwise, you are responsible for appropriately accessible file storage. 
 > Standalone mode removes the file server requirement by saving Voyager scenes in browser memory and gives you the option to download the complete package directly to your machine. You can try out our deployment of it here: [Voyager Standalone](https://3d.si.edu/voyager-story-standalone)

We are going to develop a webserver in Python-Flask, so we need a WebDav library for Python that gives us enough options to control things.
[WsgiDav](https://wsgidav.readthedocs.io/en/latest/index.html) might be such a library.

I suspect a problem that we need to solve. It is this:

1. user saves annotation in voyager client.
2. voyager client sends annotation to server via a webdav put.
3. the server needs to process that annotation (add provenance, store in DB, resolve conflicts)
4. after this post processing the user should be informed

So we have to hook in the post-processing between the WebDav PUT request and the response that the WebDav server library generates.
In other words: we need a place in the middle, between the incoming WebDav requests and the WebDav server and between the outgoing WebDav responses and the http server.