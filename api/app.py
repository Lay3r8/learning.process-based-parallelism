import falcon.asgi
import psycopg2
from psycopg2.extras import RealDictCursor
import json


class AccidentsResource:
    def __init__(self) -> None:
        self.connection = psycopg2.connect(
            dbname="postgres",
            user="username",
            password="password",
            host="localhost",
            port="5432"
        )

    async def on_get(self, req, resp):
        with self.connection:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM accidents")
                accidents = cursor.fetchall()
                resp.body = json.dumps(accidents, indent=2, sort_keys=True, default=str)
                resp.content_type = falcon.MEDIA_JSON

    async def on_post(self, req, resp):
        data = await req.media
        with self.connection:
            with self.connection.cursor() as cursor:
                accident_id = data["accident_id"]
                severity = data["severity"]
                timestamp = data["timestamp"]
                timezone = data["timezone"]
                latitude = data["latitude"]
                longitude = data["longitude"]
                description = data["description"]
                try:
                    cursor.execute(
                        "INSERT INTO accidents (accident_id, severity, timestamp, timezone, latitude, longitude, description) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (accident_id, severity, timestamp, timezone, latitude, longitude, description)
                    )
                except psycopg2.errors.UniqueViolation:
                    raise falcon.HTTPConflict(
                        description=f"The following accident ID already exists: {accident_id}"
                    )
                cursor.execute('SELECT LASTVAL()')
                user_id = cursor.fetchone()[0]
                data["id"] = user_id
                resp.text = json.dumps(data)
                resp.content_type = falcon.MEDIA_JSON
                resp.status = falcon.HTTP_201


class AccidentResource:
    def __init__(self) -> None:
        self.connection = psycopg2.connect(
            dbname="postgres",
            user="username",
            password="password",
            host="localhost",
            port="5432"
        )

    async def on_get(self, req, resp, accident_id):
        with self.connection:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "SELECT * FROM accidents WHERE id=%s",
                    (accident_id,)
                )
                accident = cursor.fetchone()
                if accident is None:
                    raise falcon.HTTPNotFound()
                resp.body = json.dumps(accident, indent=2, sort_keys=True, default=str)
                resp.content_type = falcon.MEDIA_JSON


api = falcon.asgi.App()
api.add_route('/accidents', AccidentsResource())
api.add_route('/accidents/{accident_id}', AccidentResource())
