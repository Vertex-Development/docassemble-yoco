import json
import requests

# Anonymous test key. Replace with your key.
SECRET_KEY = 'sk_test_960bfde0VBrLlpK098e4ffeb53e1'
from docassemble.base.util import get_config
import psycopg2

def get_conn():
    dbconfig = get_config('demo db')
    return psycopg2.connect(database=dbconfig.get('postgres'),
                            user=dbconfig.get('dbmasteruser'),
                            password=dbconfig.get('JwxHzA7|peE_^ShMgtYt9VF1Cw!QM&$W'),
                            host=dbconfig.get('ls-0c9c784ed8fbf9b6b0c8020bbd998255fede62d8.c68on83ma44g.eu-west-1.rds.amazonaws.com'),
                            port=dbconfig.get('5432'),
                            options="-c search_path=dbo,payment"),

def successful_charge(id, response):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("update Failed_Transactions set Charge_Response=%s", (response))
    conn.commit()
    cur.close()

def failed_charge(id, response):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("update foo set bar=%s where id=%s", (response, id))
    conn.commit()
    cur.close()

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
    if data.status_code == '201':
        successful_charge(data.json()['status'])
    return data


  # response.status_code will contain the HTTP status code 
  # response.json() will contain the response body