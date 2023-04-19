# DBCChecker

> A prototype tool aiming to verify security properties of systems obtained by composition of containers.

## How to run

In order to run the system execute

    docker compose up --build

in the main directory. On older systems where `compose` is not included with `docker`, use `docker-compose`.

## GUI

The GUI offered in the releases is a prototype that aims to simplify the interaction with the REST API.

To execute it you need Java (>=14):

    java -jar serverProverifGui-1.1.0-${PLATFORM}-STANDALONE.jar

where `${PLATFORM}` is either `LINUX` or `WINDOWS` based on your platform.

## Pre-built Docker images

In the releases you can also find pre-built docker images. To import them you can use `docker load`.

## Examples

- **basicReplyAttack**: it represents a vulnerable system, where a reply attack is discovered
