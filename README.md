


### Install requirments.txt file

```
 pip install -r requirements.txt
```

## Run the app comand

```
uvicorn src.main:app --reload
```

# Connect to PostgreSQL

```
docker-compose exec db psql -U vmwhoami_user -d vmwhoami_db
```