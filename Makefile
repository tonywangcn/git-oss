SRV_NAME=git-oss
REPO_EX=docker.pkg.github.com

NAME_SPACE=tonywangcn
REPO=${REPO_EX}
TAG=$(shell date +%Y%m%d%H%M%S)
FIXTAG?=prod
NAME=${REPO}/${NAME_SPACE}/${SRV_NAME}/${SRV_NAME}

build:
	echo build ${NAME}:${TAG}
	cp docker/Dockerfile .
	docker build -t ${NAME}:${FIXTAG} .
	docker tag ${NAME}:${FIXTAG} ${NAME}:${TAG}
	rm Dockerfile

	echo push into ${REPO}
	docker push ${NAME}:${TAG}
	docker push ${NAME}:${FIXTAG}

dev:
	docker-compose up -d

prod:
	docker-compose -f docker-compose-prod.yml up -d

down:
	docker-compose down
