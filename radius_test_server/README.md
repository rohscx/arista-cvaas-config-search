# THIS WILL BUILD A DOCKER IMAGE TO TEST RADIUS REQUESTS
 `docker build -t my-radius-image -f Dockerfile.` 
# RUN THE RADIUS SERVER
  `docker run --rm -d --name my-radius -p 1812-1813:1812-1813/udp my-radius-image`
# TEST ACCOUNTS CAN BE ADDED HERE:
  `./raddb/mods-config/files/authorize`
# DOCUMENTATION
https://hub.docker.com/r/freeradius/freeradius-server/
