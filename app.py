from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Dummy authentication credentials (replace with your own)
USERNAME = "admin"
PASSWORD = "admin"

# Dummy database to store user information
users = {}


# Authentication middleware
def authenticate(username, password):
    return username == USERNAME and password == PASSWORD


@app.route('/api/add_person', methods=['POST'])
def add_person():
    if not authenticate(request.authorization.username, request.authorization.password):
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.json
    user_id = len(users) + 1
    users[user_id] = data
    return jsonify({'message': 'Person added successfully', 'user_id': user_id})


@app.route('/api/delete_person/<int:user_id>', methods=['DELETE'])
def delete_person(user_id):
    if not authenticate(request.authorization.username, request.authorization.password):
        return jsonify({'message': 'Unauthorized'}), 401

    if user_id in users:
        del users[user_id]
        return jsonify({'message': 'Person deleted successfully'})
    else:
        return jsonify({'message': 'User not found'}), 404


@app.route('/api/update_person/<int:user_id>', methods=['PUT'])
def update_person(user_id):
    if not authenticate(request.authorization.username, request.authorization.password):
        return jsonify({'message': 'Unauthorized'}), 401

    if user_id in users:
        data = request.json
        users[user_id].update(data)
        return jsonify({'message': 'Person updated successfully'})
    else:
        return jsonify({'message': 'User not found'}), 404


@app.route('/api/list_persons', methods=['GET'])
def list_persons():
    if not authenticate(request.authorization.username, request.authorization.password):
        return jsonify({'message': 'Unauthorized'}), 401

    return jsonify(users)


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
