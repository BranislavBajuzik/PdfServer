#!/usr/bin/env bash

# Change dir
pushd "$(dirname "$(readlink -f "$0")")/.." > /dev/null || exit

echo -e "Executing in $PWD\n"

# Build docker image
DOCKER_BUILDKIT=1 docker build --rm -f docker/Dockerfile -t thealt/pdf_server:latest . || { echo "Build failed" ; exit ; }

# Upload image to Docker registry
docker login || { echo "Login failed" ; exit ; }
docker push thealt/pdf_server:latest || { echo "Push failed" ; exit ; }

# Cleanup
popd > /dev/null || exit

echo -e "\nDone!"
