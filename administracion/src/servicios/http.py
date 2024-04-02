import requests

def post_request(url, headers = None, data = None):
    return requests.post(url=url, headers=headers, json=data)

