#!/usr/bin/env python3

import requests

def main():
    response = requests.get('http://localhost:5000/companies')
    assert(response.status_code == 200)

    resp_json = response.json()
    print(resp_json)

if __name__=='__main__':
    main()