#!/bin/bash

apt update
apt install docker.io

docker pull twingate/connector:latest
