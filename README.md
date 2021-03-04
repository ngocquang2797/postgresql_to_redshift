## Step 1: Docker build
$ docker-compose build

## Step 3: activate interactive bash shell on the container
$ docker-compose run -p 3001:3001 --rm app /bin/bash