from sqlalchemy import inspect, text

from ..database import engine

async def dump_db_state():
    async with engine.connect() as conn:
        def _inspect(sync_conn):
            insp = inspect(sync_conn)
            result = {}
            for table_name in insp.get_table_names():
                cols = insp.get_columns(table_name)
                result[table_name] = [(c["name"], str(c["type"])) for c in cols]
            return result
        schema = await conn.run_sync(_inspect)

    for table_name, cols in schema.items():
        async with engine.connect() as conn:
            res = await conn.execute(text(f'SELECT COUNT(*) FROM "{table_name}"'))
            count = res.scalar()
        print(f"[{table_name}] wierszy: {count}")
        for name, col_type in cols:
            print(f"    - {name}: {col_type}")
