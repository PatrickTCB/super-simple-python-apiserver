#!/bin/sh
DOCKERHOST=localhost:8500
docker build -t $DOCKERHOST/sspapi:latest .