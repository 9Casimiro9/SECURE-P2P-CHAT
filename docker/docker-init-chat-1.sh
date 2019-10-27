docker build -t chat-docker-1 ../.
docker run \
        --rm \
        --name chat-vm-1 \
        -t \
        -d \
        -v $(pwd):/usr/src/app/ \
        -p 10000 \
        --net chatnet \
        --ip 192.168.0.2 \
        chat-docker-1
docker exec -it chat-vm-1 /bin/bash