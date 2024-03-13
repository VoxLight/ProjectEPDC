if [ "$1" == "dev" ]; then
    docker-compose -f docker-compose.dev.yml down
    docker-compose -f docker-compose.dev.yml build
    docker-compose -f docker-compose.dev.yml up
    exit 0
elif [ "$1" == "prod" ]; then
    docker-compose -f docker-compose.prod.yml down
    docker-compose -f docker-compose.prod.yml build
    docker-compose -f docker-compose.prod.yml up
    exit 0
else
    echo "Invalid argument. Please use 'dev' or 'prod'"
    exit 1
fi
