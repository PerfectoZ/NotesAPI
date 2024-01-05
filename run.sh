docker network inspect notesapi >/dev/null 2>&1 || docker network create notesapi
docker pull mongo
docker run -d --name mong -p 27017:27017 mongo
docker network connect notesapi mong
docker build -t notesapp .
docker run -d --name notes -p 8080:8080 notesapp
docker network connect notesapi notes