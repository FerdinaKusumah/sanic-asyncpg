# Sanic Asyncpg

Example how to use [Python Sanic](https://github.com/huge-success/sanic) and [Postgre Asyncpg](https://github.com/MagicStack/asyncpg)  

## Prerequisites
1. Install python sanic

```shell
    $ pip install sanic
```
2. Install PostgreSQL Database Client
```bash
    $ pip install asyncpg
```
3. Create conection pool
```python
from asyncpg import create_pool

@app.listener('before_server_start')
async def register_db(app, loop):
    # Create a database connection pool
    conn = "postgres://{user}:{password}@{host}:{port}/{database}".format(
        user='postgres', password='secret', host='localhost',
        port=5432, database='some_database'
    )
    app.config['pool'] = await create_pool(
        dsn=conn,
        min_size=10, #in bytes,
        max_size=10, #in bytes,
        max_queries=50000,
        max_inactive_connection_lifetime=300,
        loop=loop)
```

4. To see detail code you can check `main.py`
5. Happy coding :)

## Reference
1. [Sanic](https://github.com/huge-success/sanic)
2. [Asyncpg](https://github.com/MagicStack/asyncpg)