docker build -t chat-docker-2 ../.
docker run \
        --rm \
        --name chat-vm-2 \
        -t \
        -d \
        -v $(pwd):/usr/src/app/ \
        -p 10000 \
        --net chatnet \
        --ip 192.168.0.4 \
        chat-docker-2
docker exec -it chat-vm-2 /bin/bash