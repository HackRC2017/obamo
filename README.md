# Obamo

Returns the estimated reading time of Radio-Canada news.

## Build

```bash
docker build -t obamo .
```

```bash
echo 'NEURO_API_KEY="{YOUR_API_KEY}"' >> neuro_api.env
```

## Run

"Production" mode:

```bash
docker run -d \
    -p 5000:5000 \
    --name obamo \
    --env-file neuro_api.env \
    obamo
```

Development mode:

```bash
docker run -d \
    -p 5000:5000 \
    -e FLASK_DEBUG=1 \
    --env-file neuro_api.env \
    --name obamo \
    -v $PWD:/usr/src/app \
    obamo
```

## API

`/ping` - validate the server is working:

```bash
curl http://localhost:5000/ping
```

`/readtime` - get the estimated reading time for the given news story URL:

```bash
curl -X POST \
     -H 'Content-Type: application/json' \
     -d '{"url": "https://services.radio-canada.ca/hackathon2017/neuro/v1/news-stories/1023332"}'\
     http://localhost:5000/readtime
```
