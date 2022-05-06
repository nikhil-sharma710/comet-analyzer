NAME ?= nikhilsharma710
APP ?= app
VER ?= 0.1
FPORT ?= 5029
RPORT ?= 6429
RIP ?= 10.96.6.150

im-me:
        - docker images | grep ${NAME}

ps-me:
        - docker ps -a | grep ${NAME}

build-api:
        docker build -t ${NAME}/${APP}-api:${VER} \
                     -f docker/Dockerfile.api \
                     ./

build-db:
        docker pull redis:6

build-wrk:
        docker build -t ${NAME}/${APP}-wrk:${VER} \
                     -f docker/Dockerfile.wrk \
                     ./

run-api:
        docker run -p ${FPORT}:5000 \
                   --name ${NAME}-${APP}_api \
                   -d \
                   --env REDIS_IP=${RIP} \
                   ${NAME}/${APP}:${VER}

run-db:
        docker run -p ${RPORT}:6379 \
                   -v $(pwd)/data:/data:rw \
                   -d \
                   --name=${NAME}-${APP}-db \
                   redis:6 \
                   --save 1 1

run-wrk:
        docker run --name ${NAME}-${APP}-wrk \
                   --env REDIS_IP=${RIP} \
                   -d \
                   ${NAME}/${APP}-wrk:${VER}

rm-api:
        - docker rm -f ${NAME}-${APP}-api
	
rm-db:
        - docker rm -f ${NAME}-${APP}-db

rm-wrk:
        - docker rm -f ${NAME}-${APP}-wrk

cycle-api: rm-api build-api run-api


cycle-db: rm-db build-db run-db


cycle-wrk: rm-wrk build-wrk run-wrk


all: cycle-api cycle-db cycle-wrk
