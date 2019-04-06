from sanic import Sanic, response
from asyncpg import create_pool


app = Sanic(__name__)


@app.route("/api/foo/bar")
async def test(request):
    pool = request.app.config['pool']
    async with pool.acquire() as conn:
        sql = '''
                SELECT actor_id, first_name, last_name, last_update
                FROM public.actor; 
            '''
        rows = await conn.fetch(sql)
        return response.json({'status': 200, 'data': jsonify(rows)}, status=200)


@app.listener('before_server_start')
async def register_db(app, loop):
    # Create a database connection pool
    conn = "postgres://{user}:{password}@{host}:{port}/{database}".format(
        user='postgres', password='secret', host='localhost',
        port=5432, database='some_database'
    )
    app.config['pool'] = await create_pool(
        dsn=conn,
        # in bytes
        min_size=10,
        # in bytes
        max_size=10,
        # maximum query
        max_queries=50000,
        # maximum idle times
        max_inactive_connection_lifetime=300,
        loop=loop)


@app.listener('after_server_stop')
async def close_connection(app, loop):
    pool = app.config['pool']
    async with pool.acquire() as conn:
        await conn.close()


def jsonify(records):
    """
    Parse asyncpg record response into JSON format
    """
    list_return = []
    for r in records:
        itens = r.items()
        list_return.append({i[0]: i[1].rstrip() if type(
            i[1]) == str else i[1] for i in itens})
    return list_return


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000,
            access_log=True, debug=True)