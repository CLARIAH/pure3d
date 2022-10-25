![logo](images/pure3d.png)
[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)

# How to build and run the pure3d app
The app now builds and deploys all on remote server

### to build on the server:
Push your changes to remote branch. Then run locally the following command. 
```shell
./start.sh
```
The app will be build and deployed on remote server. When ready you can check the URL to see the latest changes. 

### to restart the app on the server:
Push your changes to remote branch. Then run locally the following command. 
```shell
./start.sh restart-only
```

### to build the app locally on your computer:
Run locally the following command. 
```shell
./build-local.sh
```

### to build and push your local built image, use `push` parameter on your local build:
Run locally the following command. 
```shell
./build-local.sh push
```

### notes
 * please add `pure3d.dev` as host alias to your ssh config, and make sure you can run sudo without password