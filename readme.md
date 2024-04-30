# Docker commands to build and run the container

docker build -t django-api .

docker run -p 8000:8000 -ti django-api

docker stop $(docker ps -a -q)