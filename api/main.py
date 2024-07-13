from flask import Flask, jsonify, request
from model.db_layer import DatabaseLayer, EDO

app = Flask(__name__)
db = DatabaseLayer()
edo_params = 'ids', 'names', 'mobileNumbers', 'emails', 'addresses'

@app.route('/get_edos', methods=['POST'])
def get_edos():
    try:
        data = request.json
        if not _is_valid(data):
            return jsonify({'message': f"Unexpected data on request {type(data['names'])}"}), 400
        edos, message = db.get_edos(
            ids=data.get('ids', []),
            names=data.get('names', []),
            mobile_numbers=data.get('mobileNumbers', []),
            emails=data.get('emails', []),
            addresses=data.get('addresses', [])
        )
        data_list = [
            {
                'id': edo._id, 
                'name': edo.name, 
                'mobileNumber': edo.mobile_number,
                'email': edo.email,
                'physicalAddress': edo.address,
                'created_at': edo.created_at
            }
            for edo in edos
        ]
        r = {'data': data_list}
        http_code = 200
        if message:
            r['message'] = message
        if not edos:
            r['message'] = 'data not found'
            http_code = 400
        return jsonify(r), http_code
    except Exception as error:
        app.logger.debug('db error: ', error)
        return jsonify({'message': 'Unexpected error'}), 500

@app.route('/post_edo', methods=['POST'])
def post_edos():
    if not request.json or 'name' not in request.json:
        return jsonify({'message': 'Missing data on request'}), 400
    
    edo = EDO(
        request.json['name'], 
        request.json.get('mobileNumber', ''), 
        request.json.get('email', ''),
        request.json.get('address', '')
    )
    err = db.post_edo(edo)
    if err is not None:
        return jsonify({'message': f"Unexpected error {err}"}), 500
    return jsonify({'message': 'success'}), 200

@app.route('/delete_edos', methods=['POST'])
def delete_edos():
    params = [p in request.json for p in edo_params]

    if not any(params):
        return jsonify({'message': 'Missing data on request'}), 400
    
    deleted_records, err = db.delete_edos(
        ids=request.json.get('ids', []),
        names=request.json.get('names', []),
        mobile_numbers=request.json.get('mobileNumbers', []),
        emails=request.json.get('emails', []),
        addresses=request.json.get('addresses', [])
    )

    if err is not None:
        return jsonify({'message': f'Unexpected error: {err}'}), 500
    plural = '' if deleted_records == 1 else 's'
    return jsonify({'message': f'deleted: {deleted_records} record{plural}'})

def _is_valid(data):
    for param in edo_params:
        if param in data and type(data[param]) is not list:
            return False
    return True

if __name__ == "__main__":
    app.run(debug=True)
