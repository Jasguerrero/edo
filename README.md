# Placer-EDO

## How to run

- [Install Docker](https://docs.docker.com/engine/install/)
- On terminal

```
docker-compose up --build
```

## Web crawler

If no city is provided it will run NYC by default

```
docker-compose run web-crawler [CITY]
```

## API

### Get data
```
curl -X POST -H "Content-Type: application/json" -d '[PAYLOAD]' http://localhost:5050/get_edos
```

Payload example
```
{
    "ids": ["1", "2", "3"]
    "names": ["test"],
    "emails": ["abc@abc.com", "def@def.com"],
    "mobileNumbers": ["..."],
    "emails" ["..."],
    "addresses": ["..."]
}
```
