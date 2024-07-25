import argparse
import boto3
from botocore.exceptions import ClientError
from flask import Flask, request
import json
import psycopg2
import requests
from typing import Dict

app = Flask(__name__)
file = 'jama_items.json'

def get_secret() -> Dict[str, str]:
    secret_name = "rds!db-07a423cb-58bc-4487-8d00-52abbdf4a90d"
    region_name = "us-east-1"
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e
    return json.loads(get_secret_value_response['SecretString'])

host = 'database-1.cybctmk5bo2q.us-east-1.rds.amazonaws.com'
port = 5432
secret = get_secret()
user = secret['username']
password = secret['password']

conn = psycopg2.connect(database="postgres",
                        host=host,
                        user=user,
                        password=password,
                        port=port)

cur = conn.cursor()

@app.route('/rest/v1/items/<id>', methods=['GET'])
def index(id):
  items = {file}
  with open() as f:
    items = json.loads(f.read())
  return json.dumps(items[str(id)])

@app.route('/rest/v1/items', methods=['GET'])
def get_items():
  items = {}
  with open(file) as f:
    items = json.loads(f.read())
  ret_items = list(items.values())
  ret_val = {
    'meta': {
      'pageInfo': {
        'startIndex': 0,
        'totalResults': len(ret_items)
      }
    },
    'data': ret_items
  }
  return json.dumps(ret_val)

@app.route('/rest/v1/users/', methods=['GET'])
def get_users():
  return json.dumps({ "data" : [ { "lastName" : "Chalana", "avatarUrl" : "avatarUrl", "active" : True, "customData" : [ { "name" : "Akshay Chalana", "value" : "value" }, { "name" : "Akshay Chalana", "value" : "value" } ], "title" : "Mr.", "firstName" : "Akshay", "licenseType" : "NAMED", "uid" : "uid", "phone" : "phone", "location" : "location", "id" : 5, "authenticationType" : { "name" : "name", "id" : 6 }, "email" : "akshay@saphira.ai", "username" : "username" }], "meta" : { "pageInfo" : { "startIndex" : 5, "resultCount" : 5, "totalResults" : 1 }, "status" : "OK", "timestamp" : "2000-01-23T04:56:07.000+00:00" }, "links" : { "key" : { "href" : "href", "type" : "type" } }, "linked" : { "key" : { "key" : "{}" } } })

@app.route('/rest/v1/testruns/<id>', methods=['PUT'])
def put_testrun(id):
  req = request.json
  # Identify associated req from Saphira
  response = requests.get(f'http://localhost/get_req_for_test?project_id=a4bab04e-2c43-4514-9e9c-87dc03f05c04.json&title={id}')
  print(f'Adding testrun to Req {response.text}')
  # TODO: Add protection against bad response
  cur.execute(f"INSERT INTO test_results (test_case_id, requirement_id, result, data_point, deviation) VALUES ({id}, '{response.text}', {req.get('passing', False)}, {req.get('value', 0)}, {req.get('deviation', 0)})")
  conn.commit()

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('-p', '--port')
  parser.add_argument('-f', '--file')
  args = parser.parse_args()
  file = args.file or file
  app.run(host='0.0.0.0', port=args.port or 8080, debug=True)