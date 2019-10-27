echo "Stoping all containers"
docker stop $(docker ps -a -q)
echo "Removing all containers"
docker rm $(docker ps -a -q)
echo "Removing chat images"
docker image rm chat-docker-1 chat-docker-2 chat-docker-3 chat-docker-node-1 -f