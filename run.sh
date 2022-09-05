#!/bin/sh
DOCKERHOST=docker.phn1.net:8500
docker run -d --restart unless-stopped --name siri-extender -p 8081:8080 docker.phn1.net/siri-extender:latest
