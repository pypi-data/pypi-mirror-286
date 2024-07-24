import os
import requests
import pprint
from ..common import prettyllog
import hvac



client = hvac.Client()



def getenv(myenv):
    myenv['VAULT_URL'] = os.environ.get("IGN8_VAULT_URL", None)
    myenv['VAULT_TOKEN'] = os.environ.get("IGN8_VAULT_TOKEN", None)
    return myenv

def initiate_secret(path):

    client.enable_secrets_engine("kv", path=path)   
    pathexist = False
    mystoredsecret = None
    try: 
        mystoredsecret = client.read(path)
        return True
    except Exception as e:
        pathexist = False

    confluence_token = None
    try: 
        confluence_token = mystoredsecret["data"]["confluence"]['token']
    except Exception as e:
        confluence_token = input("Please enter your Confluence token: ")
    confluence_url = None
    try: 
        confluence_url = mystoredsecret["data"]["confluence"]['url']
    except Exception as e:
        confluence_url = input("Please enter your Confluence URL: ")

    password_state_token = None
    try: 
        password_state_token = mystoredsecret["data"]["password_state"]['token']
    except Exception as e:
        password_state_token = input("Please enter your Password State token: ")
    password_state_url = None
    try: 
        password_state_url = mystoredsecret["data"]["password_state"]['url']
    except Exception as e:
        password_state_url = input("Please enter your Password State URL: ")

    bitbucket_token = None
    try: 
        bitbucket_token = mystoredsecret["data"]["bitbucket"]['token']
    except Exception as e:
        bitbucket_token = input("Please enter your Bitbucket token: ")
    bitbucket_url = None
    try: 
        bitbucket_url = mystoredsecret["data"]["bitbucket"]['url']
    except Exception as e:
        bitbucket_url = input("Please enter your Bitbucket URL: ")
    
    mysecret = {"
        "confluence": {"token": confluence_token, "url": confluence_url},
        "password_state": {"token": password_state_token, "url": password_state_url},
        "bitbucket": {"token": bitbucket_token, "url": bitbucket_url}
    }
    client.write(path, data=mysecret)

    return True

def get_secret(path):
    pathexist = False
    mystoredsecret = None
    try: 
        mystoredsecret = client.read(path)
        return mystoredsecret
    except Exception as e:
        pathexist = False
    return mystoredsecret



def checkaccess():
    myenv = getenv({})
    if myenv['VAULT_URL'] is None:
        prettyllog("vault", "checkaccess", myenv['VAULT_URL'], "-", "000", "Environment not set vault url", "ERROR")
        return None
    if myenv['VAULT_TOKEN'] is None:
        prettyllog("vault", "checkaccess", myenv['VAULT_URL'], "-", "000", "Environment not set vault token", "ERROR")
        return None
    
    headers = {'X-Vault-Token': myenv['VAULT_TOKEN']}   
    checkaccess = requests.get(myenv['VAULT_URL']+"/api/v1/healthcheck/", headers=headers, verify=False)
    if checkaccess.status_code == 200:
        return True
    else:
        print("Vault access failed")
        return None


def getlogin(path):
    if checkaccess():

        vaultlogin = requests.get("http://localhost:8000/api/v1/vault/login/?path=" + path)
        if vaultlogin.status_code == 200:
            return vaultlogin.json()
        else:
            return None
    else:
        return None
    