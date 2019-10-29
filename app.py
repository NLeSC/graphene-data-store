#!/usr/bin/env python

from database import db_session, init_db
from flask import Flask
from schema import schema

from flask_graphql import GraphQLView

from flask_cors import CORS


app = Flask(__name__)
app.debug = True
CORS(app)

app.add_url_rule(
    "/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    init_db()
    app.run()
