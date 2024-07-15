# Placer-EDO

For documentation see high_level_design_doc.pdf

## How to run

- [Install Docker](https://docs.docker.com/engine/install/)
- Open a terminal and run

```
docker-compose up --build
```

## Web crawler

If no city is provided, it will default to running NYC on startup with docker-compose. You can check the logs with `docker logs placer-edo_web-crawler_1`. After seeing `Web crawler finished for city={city}`, you can query the results:

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

- Access the web client at `localhost:6060` with credentials: email: admin@admin.com | password: password
- Connect to the postgresdb with username: admin | password: password


## Re-running a Specific City

By default, the cache is persisted for 5 hours. If a city is rerun within this interval, you will see a log message like `City: {city} already processed.` If you want to recalculate everything, delete the cache by following these steps:

- Access `localhost:5540`
- Connect to the Redis instance with hostname: `cache` port: `6379`
- Delete all the keys related to the city
  - Example keys to delete for city: "New York"
  - new_york_edo_full_contact
  - ny_edo
  - New York
  - new_york_edo_contact

Note that rerunning a city does not delete data from the PostgreSQL database, so you may have multiple copies of EDOs. Use the API, PGAdmin, or delete the folder `./data/db` to manage records appropriately.
