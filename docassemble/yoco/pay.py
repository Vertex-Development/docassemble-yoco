import json
import requests

# Anonymous test key. Replace with your key.
SECRET_KEY = 'sk_test_960bfde0VBrLlpK098e4ffeb53e1'


def yoco_charge(token, amount):
    response = requests.post(
                                'https://online.yoco.com/v1/charges/',
                                headers={
                                'X-Auth-Secret-Key': SECRET_KEY,
                                },
                                json={
                                        'token': token,
                                        'amountInCents': amount,
                                        'currency': 'ZAR',
                                    },
                                )       
    data = response
    return data


  # response.status_code will contain the HTTP status code 
  # response.json() will contain the response body