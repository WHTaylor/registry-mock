from flask import Flask, jsonify, abort, request, url_for
import get_request_handler
import post_request_handler
from request_arg_parser import parse_args
from copy import deepcopy

app = Flask(__name__)


@app.route('/')
def index():
    return "<h2>Hello, World!</h2><p>Live updates and all sorts</p>"


@app.route('/api/v1/proposals', methods=['GET'])
def get_proposals():
    try:
        filters, selects = parse_args(request.args)
        proposal_data = get_request_handler.get_proposals(filters, selects)
        return return_format(proposal_data)
    except ValueError as err:
        abort(400, err)


@app.route('/api/v1/proposals/<int:proposal_id>', methods=['GET'])
def get_proposal(proposal_id):
    try:
        filters, selects = parse_args(request.args)
        filters['id'] = [proposal_id]
        matching_proposal = get_request_handler.get_proposals(filters, selects)
        if matching_proposal:
            return return_format(matching_proposal)
        else:
            abort(404, "No such proposal")
    except ValueError as err:
        abort(400, err)


@app.route('/api/v1/proposals', methods=['POST'])
def create_proposal():
    try:
        new_proposal = post_request_handler.create_proposal(request.json)
        return get_proposal(new_proposal['id'])
    except ValueError as err:
        abort(400, err)


def return_format(proposal_data):
    ids_replaced_with_uris = []
    for proposal in deepcopy(proposal_data):
        proposal['uri'] = url_for("get_proposal", proposal_id=proposal['id'], _external=True)
        ids_replaced_with_uris.append(proposal)
    return jsonify(ids_replaced_with_uris)


if __name__ == "__main__":
    app.run(debug=True)
