import json
import requests
from docassemble.base.util import get_config, log, create_session
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
                            options="-c search_path=payment")


def write_response_to_db(response):

    j_response = response.json()

    interview_filename = 'docassemble.playground1pay:pay.yml'
    session_id = create_session(interview_filename)

    conn = get_conn()
    # Open a cursor to perform database operations
    cur = conn.cursor()
    # Pass data to fill a query placeholders and let Psycopg perform
    # the correct conversion (no more SQL injections!)
    log(response.ok)
    if response.ok:
        log("Successful response")
        # Define the data to be inserted
        # Define the data to be inserted

        # Define the data to be inserted
        source_data = (j_response['id'], j_response['source']['brand'], j_response['source']['maskedCard'], j_response['source']['expiryMonth'], j_response['source']['expiryYear'], j_response['source']['fingerprint'], j_response['source']['object'])
        # Define the data to be inserted
        metadata_data = (j_response['id'], session_id) 

        if (j_response['liveMode'] == False):
            live_mode = False
        else:
            live_mode = True

        charge_data = (j_response['id'], j_response['object'], j_response['status'], j_response['currency'], j_response['amountInCents'], live_mode)

        # Execute the INSERT statement
        cur.execute("INSERT INTO source (id, brand, masked_card, expiry_month, expiry_year, fingerprint, object) VALUES (%s, %s, %s, %s, %s, %s, %s)", source_data)

        # Execute the INSERT statement
        cur.execute("INSERT INTO metadata (id, docassemble_session) VALUES (%s, %s)", metadata_data)

        # Execute the INSERT statement
        cur.execute("INSERT INTO charge (id, object, status, currency, amount_in_cents, live_mode) VALUES (%s, %s, %s, %s, %s, %s)", charge_data)
    else:
        log("Unsuccessful response") 

        # Define the data to be inserted
        error_data = (j_response['errorType'], j_response['errorCode'], j_response['errorMessage'], j_response['displayMessage'])

        # Execute the INSERT statement
        cur.execute("INSERT INTO payment_errors (error_type, error_code, error_message, display_message) VALUES (%s, %s, %s, %s)", error_data)

    # Commit the transaction 
    conn.commit()

    # Close the cursor and connection
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