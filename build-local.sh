#!/usr/bin/env bash

source .env
echo "building docker images ...."
docker build --no-cache -f Dockerfile.local -t pure3dapp:${dockertag} \
  --build-arg gitlocation=${gitlocation} \
  --build-arg gitbranch=${gitbranch} \
  --build-arg SECRET_FILE=${SECRET_FILE} \
  --build-arg DATA_DIR=${DATA_DIR} \
  --build-arg mysecret=${mysecret} \
  .

if [ "$?" == "0" ]; then
  echo "docker images completed ...."
  docker images | grep pure3dapp:${dockertag}
else
  echo "docker image building failed!"
  exit 1
fi

sleep 3

docker tag pure3dapp:${dockertag} registry.diginfra.net/vicd/pure3dapp:${dockertag}
docker tag pure3dapp:${dockertag} registry.diginfra.net/vicd/pure3dapp:latest
docker images | grep registry.diginfra.net/vicd/pure3dapp:${dockertag}