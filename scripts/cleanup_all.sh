set -e
read -p "This will stop the app and remove all stored data. Are you sure? [y/N]: " -r
if [[ $REPLY =~ ^[Yy]$ ]]
then
  docker-compose down --rmi all -v
fi
