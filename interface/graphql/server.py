from flask import Flask, request, jsonify
from ariadne import graphql_sync
from ariadne.explorer import ExplorerGraphiQL
from interface.graphql.schema import schema

app = Flask(__name__)

@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return ExplorerGraphiQL().html(None), 200

@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(schema, data, context_value=request)
    return jsonify(result)
