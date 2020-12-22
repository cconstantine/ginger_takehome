set -e

docker-compose build $1
exec docker-compose run --service-ports $*
