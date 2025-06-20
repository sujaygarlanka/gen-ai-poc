from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/hello')
def hello():
    return jsonify({'message': 'Hello, world!'})

@app.route('/test')
def test():
    return 'this is a test'

@app.route('/datausa/top-earning-state')
def datausa_top_earning_state():
    """Returns the state with the highest median household income for 2023"""
    url = 'https://datausa.io/api/data?drilldowns=State&measures=Median+Household+Income&year=2023&order=desc&sort=Median+Household+Income&limit=1'
    resp = requests.get(url)
    return jsonify(resp.json())

@app.route('/datausa/youngest-large-county')
def datausa_youngest_large_county():
    url = 'https://datausa.io/api/data?drilldowns=County&measures=Median+Age&year=2023&order=asc&sort=Median+Age&limit=1'
    resp = requests.get(url)
    return jsonify(resp.json())

@app.route('/datausa/largest-counties')
def datausa_largest_counties():
    url = 'https://datausa.io/api/data?drilldowns=County&measures=Population&year=2023&order=desc&sort=Population&limit=5'
    resp = requests.get(url)
    return jsonify(resp.json())

@app.route('/datausa/most-expensive-housing-state')
def datausa_most_expensive_housing_state():
    url = 'https://datausa.io/api/data?drilldowns=State&measures=Median+Property+Value&year=2023&Geography=15'
    resp = requests.get(url)
    return jsonify(resp.json())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080) 