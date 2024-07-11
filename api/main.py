from flask import Flask, jsonify, request
from model.db_layer import DatabaseLayer

app = Flask(__name__)
db = DatabaseLayer()

@app.route('/edos', methods=['GET'])
def get_edos():
    try:
        edos = db.get_edos()
        r = {'data': edos}
        http_code = 200
        if not edos:
            r['message'] = 'data not found'
            http_code = 400
        return jsonify(r), http_code
    except Exception as error:
        app.logger.debug('db error: ', error)
        return jsonify({'message': 'Unexpected error'})

@app.route('/edos', methods=['POST'])
def post_edos():
    if not request.json or 'title' not in request.json or 'author' not in request.json:
        return jsonify({'message': 'Missing data on request'}), 400
    

if __name__ == "__main__":
    app.run(debug=True)
