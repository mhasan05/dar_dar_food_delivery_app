# utils/db.py
from django.db import connection

class DB:
    @staticmethod
    def executesql(query, params=None, as_dict=False, debug=False):
        with connection.cursor() as cursor:
            if debug:
                print("\n📘 SQL Query:", query)
                print("📗 Params:", params)

            cursor.execute(query, params or [])

            # Handle SELECT queries
            if query.strip().lower().startswith("select"):
                rows = cursor.fetchall()
                if as_dict:
                    columns = [col[0] for col in cursor.description]
                    return [dict(zip(columns, row)) for row in rows]
                return rows

            # For INSERT / UPDATE / DELETE
            return cursor.rowcount
