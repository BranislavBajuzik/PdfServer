#!/usr/bin/env bash

# Change dir
pushd "$(dirname "$(readlink -f "$0")")/.." > /dev/null || exit

echo -e "Executing in $PWD\n"

# Build docker image
DOCKER_BUILDKIT=1 docker build --rm -f docker/Dockerfile -t thealt/pdf_server:latest .

# Upload image to Docker registry
docker login
docker push thealt/pdf_server:latest

# Cleanup
popd > /dev/null || exit

echo -e "\nDone!"
