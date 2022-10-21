#!/usr/bin/env bash

ssh pure3d.dev 'sudo rm -fr /tmp/app && sudo git clone -b containerize https://github.com/CLARIAH/pure3d.git /tmp/app'
scp .env pure3d.dev:/tmp
if [ "$1" == "restart-only" ];then
  ssh pure3d.dev 'sudo mv /tmp/.env /tmp/app/.env && cd /tmp/app && sudo ./restart.sh'
else
  ssh pure3d.dev 'sudo mv /tmp/.env /tmp/app/.env && cd /tmp/app && sudo ./build.sh && sudo ./restart.sh'
fi