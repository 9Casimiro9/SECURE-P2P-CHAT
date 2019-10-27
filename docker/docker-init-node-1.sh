docker build -t chat-docker-node-1 ../.
docker run \
        --rm \
        --name chat-node-1 \
        -t \
        -d \
        -v $(pwd):/usr/src/app/ \
        -p 10000 \
        --net chatnet \
        --ip 192.168.0.3 \
        chat-docker-node-1
docker exec -it chat-node-1 /bin/bash