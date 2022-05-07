NAME ?= nikhilsharma710
APP ?= app
VER ?= 0.1
FPORT ?= 5029
RPORT ?= 6429

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
	RIP=$$(docker inspect ${NAME}-${APP}-db | grep \"IPAddress\" | head -n1 | awk -F\" '{print $$4}') && \
	docker run -p ${FPORT}:5000 \
                   --name ${NAME}-${APP}_api \
                   -d \
                   --env REDIS_IP=${RIP} \
                   ${NAME}/${APP}:${VER}

run-db:
	docker run --name ${NAME}-db \
		   -p ${RPORT}:6379 \
                   -v $(pwd)/data:/data:rw \
                   -d \
                   redis:6 \
                   --save 1 1

run-wrk:
	RIP=$$(docker inspect ${NAME}-${APP}-db | grep \"IPAddress\" | head -n1 | awk -F\" '{print $$4}') && \
	docker run --name ${NAME}-${APP}-wrk \
                   --env REDIS_IP=${RIP} \
                   -d \
                   ${NAME}/${APP}-wrk:${VER}


clean-api:
	- docker stop ${NAME}-${APP}-api && docker rm -f ${NAME}-${APP}-api
	
clean-db:
	- docker stop ${NAME}-${APP}-db && docker rm -f ${NAME}-${APP}-db

clean-wrk:
	- docker stop ${NAME}-${APP}-wrk && docker rm -f ${NAME}-${APP}-wrk

push-api:
	docker push ${NAME}/${APP}-api:${VER}

push-wrk:
	docker push ${NAME}/${APP]-wrk:${VER}



cycle-api: clean-api build-api run-api

cycle-db: clean-db build-db run-db

cycle-wrk: clean-wrk build-wrk run-wrk

push-all: push-api push-wrk

all: cycle-api cycle-db cycle-wrk
