import json
import base64
import requests
from bnipython.lib.util.utils import getTimestamp, generateTokenSignature

class HttpClient():
    def __init__(self, verify=True):
        self.verify = verify

    def tokenRequest(self, options={'url', 'path', 'username', 'password'}):
        url = f"{options['url']}{options['path']}"
        username = options['username']
        password = options['password']
        authorize = base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode()
        headers = {
            'User-Agent': 'bni-python/0.1.0',
            'Authorization': f'Basic {authorize}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        payload = 'grant_type=client_credentials'

        response = requests.post(url, headers=headers, data=payload, verify=self.verify)
        return response.json()

    def request(self, options={'method', 'apiKey', 'accessToken', 'url', 'path', 'data'}):
        url = f"{options['url']}{options['path']}?access_token={options['accessToken']}"
        headers = {
            'User-Agent': 'bni-python/0.1.0',
            'x-api-key': options['apiKey'],
            'Content-Type': 'application/json'
        }
        payload = json.dumps(options['data'])
        response = requests.request(options['method'], url, headers=headers, data=payload, verify=self.verify)
        return response.json()

    def tokenRequestSnapBI(self, options={'url', 'clientId', 'privateKeyPath'}):
        timeStamp = getTimestamp()
        payload = json.dumps({
            "grantType": "client_credentials",
            "additionalInfo": {}
        })
        headers = {
            'Content-Type': 'application/json',
            'X-SIGNATURE': generateTokenSignature({
                'privateKeyPath': options['privateKeyPath'],
                'clientId': options['clientId'],
                'timeStamp': timeStamp
            }),
            'X-TIMESTAMP': timeStamp,
            'X-CLIENT-KEY': options['clientId']
        }
        response = requests.post(options['url'], headers=headers, data=payload, verify=self.verify)
        return response.json()

    def requestSnapBI(self, options={'method', 'apiKey', 'accessToken', 'url', 'data', 'additionalHeader'}):
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'bni-python/0.1.0',
            'Authorization': f'Bearer {options['accessToken']}',
        }
        headers.update(options['additionalHeader'])
        payload = json.dumps(options['data'])
        response = requests.request(options['method'], options['url'], headers=headers, data=payload, verify=self.verify)
        return response.json()

    def requestV2(self, options={'method', 'apiKey', 'accessToken', 'url', 'path', 'data', 'signature', 'timestamp'}):
        url = f"{options['url']}{options['path']}?access_token={options['accessToken']}"
        headers = {
            'User-Agent': 'bni-python/0.1.0',
            'x-api-key': options['apiKey'],
            'x-signature': options['signature'],
            'x-timestamp': options['timestamp'],
            'Content-Type': 'application/json'
        }
        payload = json.dumps(options['data'])
        response = requests.request(options['method'], url, headers=headers, data=payload, verify=self.verify)
        return response.json()
