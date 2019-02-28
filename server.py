from flask import Flask, jsonify, abort, request
import get_request_handler
from request_arg_parser import parse_args

app = Flask(__name__)


@app.route('/')
def index():
    return "<h2>Hello, World!</h2><p>Live updates and all sorts</p>"


@app.route('/api/v1/proposals', methods=['GET'])
def get_proposals():
    try:
        filters, selects = parse_args(request.args)
        return jsonify(get_request_handler.get_proposals(filters, selects))
    except ValueError as err:
        abort(400, err)


@app.route('/api/v1/proposals/<int:proposal_id>', methods=['GET'])
def get_proposal(proposal_id):
    try:
        filters, selects = parse_args(request.args)
        filters['id'] = [proposal_id]
        matching_proposal = get_request_handler.get_proposals(filters, selects)
        if matching_proposal:
            return jsonify(matching_proposal[0])
        else:
            abort(404, f"No proposal with id '{proposal_id}' exists")
    except ValueError as err:
        abort(400, err)


if __name__ == "__main__":
    app.run(debug=True)
