docker build -t chat-docker-3 ../.
docker run \
        --rm \
        --name chat-vm-3 \
        -t \
        -d \
        -v $(pwd):/usr/src/app/ \
        -p 10000 \
        --net chatnet \
        --ip 192.168.0.5 \
        chat-docker-3
docker exec -it chat-vm-3 /bin/bash