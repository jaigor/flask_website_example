import json
import requests

def checkRecaptcha(response, secretkey):
    url = 'https://www.google.com/recaptcha/api/siteverify'
    try:
        data = {'secret': secretkey, 'response': response}
        r = requests.post(url, data).json()
        print(r)
        if r['success']:
            return True
        else:
            return False
    except Exception as e:
        print (e)
        return False