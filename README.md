# api.tahm-ken.ch

## dev setup

requirements:
- docker or redis
- uv (Python package and project manager)

```bash
# start a redis server
docker compose -f compose-dev.yaml up -d

# create config file
cp .env_sample .env
vim .env # set your Riot API key

# start dev server
uv run fastapi dev app --port 80
```