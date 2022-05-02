NAME ?= nikhilsharma710
APP ?= app
VER ?= 0.1.0
FPORT ?= 5029
RIP

im-me:
	- docker images | grep ${NAME}

ps-me:
	- docker ps -a | grep ${NAME}

build-api:
	docker build -t ${NAME}/${APP}_api:${VER} -f docker/Dockerfile.api .

build-db:


build-wrk:


run-api:
	docker run -p ${FPORT}:5000 \
                   --name ${NAME}_${APP}_api \
                   -d \
                   --env REDIS_IP=${RIP} \
                   ${NAME}/${APP}:${VER}

rm-api:
	- docker rm -f ${NAME}_${APP}_api

rm-db:


rm-wrk:


cycle-api: rm-api build-api run-api


cycle-db:


cycle-wrk: 


all: cycle-api cycle-db cycle-wrk
