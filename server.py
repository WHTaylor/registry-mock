from flask import Flask, jsonify, abort
import db

app = Flask(__name__)


@app.route('/')
def index():
    return "<h2>Hello, World!</h2><p>Live updates and all sorts</p>"


@app.route('/api/v1/proposals', methods=['GET'])
def get_proposals():
    return jsonify(db.proposals)


@app.route('/api/v1/proposals/<int:proposal_id>', methods=['GET'])
def get_proposal(proposal_id):
    matching_proposal = [p for p in db.proposals if p["id"] == proposal_id]
    if matching_proposal:
        return jsonify(matching_proposal[0])
    else:
        abort(404, f"No proposal with id '{proposal_id}' exists")


if __name__ == "__main__":
    app.run(debug=True)
