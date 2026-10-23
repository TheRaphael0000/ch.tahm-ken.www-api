# api.tahm-ken.ch

## dev setup

requirements:
- docker or redis
- uv (Python package and project manager)

```bash
# start a redis server, you can also just set it in the .env file below
docker compose -f compose-dev.yaml up -d

cp .env_sample .env
vim .env # set your Riot API key

# start dev server
uv run fastapi dev app --port 80
```

if you want to start the whole stack without dev capabilities

```bash
cp .env_sample .env
vim .env # set your Riot API key
docker compose -f compose-local.yaml up --build
```

TIP: restart the redis server if you have trouble with your API key, we are caching 4XX responses in the redis too...