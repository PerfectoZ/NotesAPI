FROM python:3.10

WORKDIR /app
COPY . /app
RUN apt-get update -y
RUN apt-get install libsodium-dev -y
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080
CMD ["make", "server"]