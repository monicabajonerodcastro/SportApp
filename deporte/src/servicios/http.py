import requests

def post_request(url, headers = None, data = None):
    return requests.post(url=url, headers=headers, json=data)

def get_request(url, headers = None):
    return requests.get(url=url, headers=headers)

