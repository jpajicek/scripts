import requests
import json 
import argparse
import time
from datetime import date, timedelta, datetime


apiToken = ''
authorizationType = 'SSWS'
username = ''
password = ''
writefile = 'result.json'
readfile = 'payload.json'


now = datetime.utcnow()
timestamp = str(now.strftime("%Y%m%d_%H-%M"))


def _requestURL(**opts):
    for key, value in opts.items():
        globals()[f"{key}"] = value
        
    _data = json.dumps(payload)

    try:
        if user:
            theRequest = requests.request(method, url, headers=headers, auth=(user, passwd), data=_data)
        else:
            theRequest = requests.request(method, url, headers=headers, data=_data)
        
        return theRequest
    
    except ValueError as e:
        raise ValueError(e)


def printStatus(s):
    if s == 400:
        print(f"Status Code: {s} - Bad Request")
    elif s == 401:
        print(f"Status Code: {s} - Unauthorized")
    elif s == 403:
        print(f"Status Code: {s} - Forbidden")
    elif s == 404:
        print(f"Status Code: {s} - Not Found")
    elif s == 405:
        print(f"Status Code: {s} - Method Not Allowed")
    else:
        print(f"Status Code: {s}")


def setHeaders(_auth,_token):
    if _token != '': 
        authHeader = ', "Authorization": "{} {}"'.format(_auth, _token)
    else:
        authHeader = ''
        
    headers = '{ "Accept": "application/json", "Content-Type": "application/json"'+ authHeader + ' }' 
    return json.loads(headers)


def empty_response(r):
    if r == '':
        print("Received empty response")
        return True
    else:
        return False

    
def printPrettyJson(d):
    try:
        data = json.loads(d)
        print(json.dumps(data, indent=2))
    except ValueError as e:
        print(e)


def writeJsonFile(file, d):
    try:
        data = json.loads(d)
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except ValueError as e:
        print(e)


def readJsonFile(file):
    with open(file, "r") as f:
        json_data = json.loads(f.read())
    return json_data

    
def _createArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username", help="Username")
    parser.add_argument("-p", "--password", help="Password")
    parser.add_argument("-t", "--token", help="API Token")
    parser.add_argument("-a", "--authorization", help="Bearer|Basic|SSWS", default='Bearer')
    parser.add_argument("-w", "--writefile", help="JSON dump filename")
    parser.add_argument("-r", "--readfile", help="JSON payload filename")
    parser.add_argument("-m", "--method", help="GET|POST|etc", default='GET')
    parser.add_argument("--url", help="URL")

    args = parser.parse_args()
    return args

    
def main():
    args = _createArgs()

    _token = args.token if args.token is not None else apiToken
    _user = args.username if args.username is not None else username
    _passwd = args.password if args.password is not None else password
    _writefile = args.writefile if args.writefile is not None else writefile
    _readfile = args.readfile if args.readfile is not None else readfile
    _authorization = args.authorization if args.authorization is not None else authorizationType
    _payload = ''
    
    headers = setHeaders(_authorization,_token)
    
    if args.method != 'GET':
        if _readfile:
            _payload = readJsonFile(_readfile)
        else:
            print("Please provide path to the JSON file payload")
            exit(1)

    data = _requestURL(url=args.url, headers=headers, user=_user, passwd=_passwd, method=args.method, payload=_payload)        

    if not empty_response(data.text):
        if _writefile:
            writeJsonFile(_writefile, data.text)        
        printPrettyJson(data.text)

    printStatus(data.status_code)
    

if __name__ == "__main__":
    main()

