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
    "addresses": ["..."],
    "contacts": ["..."],
    "cities": ["..."],
    "states": ["..."],
    "zipCodes": ["..."],
    "websites": ["..."]
}
```

### Add new data
```
curl -X POST -H "Content-Type: application/json" -d '[PAYLOAD]' http://localhost:5050/post_edo
```

Payload example
```
{
    "name": "test",  # required field
    "email": "abc@abc.com",
    "mobileNumber": "...",
    "email" "...",
    "address": "...",
    "contact": "...",
    "city": "...",
    "state": "...",
    "zipCode": "...",
    "website": "..."
}
```

## PG Admin

- To connect to the web client go to `localhost:6060` email: admin@admin.com | password: password
- Connect to the postgresdb with username: admin | password: password


## To re run an specific city

By default the cache is persisted 5 hours so by design if a city is rerunned before this interval you will get a log such as `City: {city} already processed.`. If you want to recalculate everything the cache should be delated following the next steps:

- Access `localhost:5540`
- Connect to the redis instance with hostname: `cache` port: `6379`
- Delete all the keys related to the city
  - Example keys to delete for city: "New York"
  - new_york_edo_full_contact
  - ny_edo
  - New York
  - new_york_edo_contact

Keep in mind that rerunning a city do not delete the data on the postgres database so you might end with more than one copy of the EDOs (you can use the API or the PGAdmin to delete records)
