#!/usr/bin/env python3

from flask import Flask, json

companies = [{"id": 1, "name": "Company One"}, {"id": 2, "name": "Company Two"}]

api = Flask(__name__)
api.env = 'development'

@api.route('/companies', methods=['GET'])
def get_companies():
  return json.dumps(companies)

@api.route('/companies', methods=['POST'])
def post_companies():
  return json.dumps({"success": True}), 201

if __name__ == '__main__':
    api.run(debug=True, host='0.0.0.0')