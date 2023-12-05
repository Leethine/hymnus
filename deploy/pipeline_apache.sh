#!/usr/bin/bash
cp Dockerfile_Apache ../Dockerfile
cp hymnus-httpd.conf ../
cd ..
podman container stop --all
podman container prune -f
podman image prune -f
podman build -t my-httpd .
podman run -d --name hymnus-app -p 8080:80 my-httpd
#podman exec -it hymnus-app bash
rm Dockerfile
rm hymnus-httpd.conf
