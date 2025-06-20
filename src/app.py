from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/hello')
def hello():
    return jsonify({'message': 'Hello, world!'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80) 