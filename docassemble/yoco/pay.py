import json
import requests
from docassemble.base.util import get_config, log
import psycopg2
# Anonymous test key. Replace with your key.
SECRET_KEY = 'sk_test_960bfde0VBrLlpK098e4ffeb53e1'


def get_conn():
    # Connect to an existing database
    # Fetch the database details from the configuration file. Change name and options for live. 
    dbconfig = get_config('demo db')
    return psycopg2.connect(database=dbconfig.get('name'),
                            user=dbconfig.get('user'),
                            password=dbconfig.get('password'),
                            host=dbconfig.get('host'),
                            port=dbconfig.get('port'),
                            options="-c search_path=ideal,public")


def write_response_to_db(response):
    conn = get_conn()
    # Open a cursor to perform database operations
    cur = conn.cursor()
    # Pass data to fill a query placeholders and let Psycopg perform
    # the correct conversion (no more SQL injections!)
    log(response.ok)
    if response.ok:
        log("Successful response")
        postgres_insert_query = """ INSERT INTO "SuccessfulPayments" (fun, bomb) VALUES (%s, %s)"""
        record_to_insert = ("hello", "toad")
        cur.execute(postgres_insert_query, record_to_insert)
    else:
        log("Unsuccessful response")
        cur.execute("INSERT INTO SuccessfulPayments (StatusCode) VALUES (%s)",
        ("world"))     
    # Make the changes to the database persistent
    conn.commit()
    # Close communication with the database
    cur.close()
    conn.close()



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
    log(response)      
    log(response.text)
    log(response.json())
    log(response.ok)
    write_response_to_db(response)
    return response


  # response.status_code will contain the HTTP status code 
  # response.json() will contain the response body

#   Lessons: 

#   With table names and column names, these will automatically be interpreted 
#   as lower case. Need to use double quotation marks to get around this. 
#   For example SuccessfulPayments needs to be "SuccessfulPayments"