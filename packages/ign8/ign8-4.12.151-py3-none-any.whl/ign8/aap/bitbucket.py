# We need to be able to connect to Bitbucket

import requests
import json
import os
import sys
import time
import hvac
import pprint


#from ..common import prettyllog

def create_repository(bb, project, repo):
  pprint.pprint(repo)
  # This code sample uses the 'requests' library:
  # http://docs.python-requests
  mytoken = bb["token"]
  baseurl = bb["url"]
  url = baseurl + "/rest/api/latest/projects/" + project + "/repos"

  headers = {
    "Accept": "application/json"
    ,"Authorization ": "Bearer {}".format(mytoken)
  }

  payload = {
    "name": repo["name"]
    ,"scmId": "git"
    ,"forkable": True
    ,"project": {"key": project}
  }

  response = requests.request(
    "POST",
    url,
    headers=headers,
    json=payload,
    verify=False
  )

  print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
  return response.text

def get_bitbucket_repositories(bb, project):
  # This code sample uses the 'requests' library:
  # http://docs.python-requests
  mytoken = bb["token"]
  baseurl = bb["url"]
  url = baseurl + "/rest/api/latest/projects/" + project + "/repos"

  headers = {
    "Accept": "application/json"
    ,"Authorization": "Bearer {}".format(mytoken) 
  }

  response = requests.request(
    "GET",
    url,
    headers=headers,
    verify=False
  )
  lastpage = False
  repos = []
  while not lastpage:
    data = json.loads(response.text)
    repos.extend(data["values"])
    if "nextPageStart" in data:
      url = data["nextPageStart"]
    else:
      lastpage = True


  return repos




def get_bitbucket_project(bb, project):
  # This code sample uses the 'requests' library:
  # http://docs.python-requests
  mytoken = bb["token"]
  baseurl = bb["url"]
  url = baseurl + "/rest/api/latest/projects/" + project

  headers = {
    "Accept": "application/json"
    ,"Authorization ": "Bearer {}".format(mytoken)
  }

  response = requests.request(
    "GET",
    url,
    headers=headers,
    verify=False
  )

  print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
  return response


def create_bitbucket_project(bb, project):
  pprint.pprint(bb) 

  # This code sample uses the 'requests' library:
  # http://docs.python-requests
  mytoken = bb["token"]
  baseurl = bb["url"]
  url = baseurl + "/rest/api/latest/projects"

  headers = {
    "Accept": "application/json"
    ,"Authorization": "Bearer {}".format(mytoken)
  }

  payload = {
    "key": project["key"]
    ,"name": project["name"]
    ,"description": project["description"]
    ,"is_private": project["is_private"]
  }

  response = requests.request(
    "POST",
    url,
    headers=headers,
    json=payload,
    verify=False
  )

  print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
  return response



def get_bitbucket_project_list(bb):
  # This code sample uses the 'requests' library:
  # http://docs.python-requests.org
  mytoken = bb["token"]
  baseurl = bb["url"]
  url = baseurl + "/rest/api/latest/projects"


  headers = {
    "Accept": "application/json"
    ,"Authorization": "Bearer {}".format(mytoken)
    }
  projects = []
  lastpage = False
  while not lastpage:
    response = requests.request(
       "GET",
      url,
      headers=headers,
      verify=False
   )
    data = json.loads(response.text)
    projects.extend(data["values"])
    if "nextPageStart" in data:
      url = data["nextPageStart"]
    else:
      lastpage = True
  return projects

def get_bitbucket_token(vaultpath):
    # Get the Bitbucket token
    client = hvac.Client()
    try:
      response = client.read(vaultpath)
    except Exception as e:
      return 1
    

    try:
       response = client.read(vaultpath)
    except Exception as e:
      bbtoken = input("Please enter your Bitbucket token: ")
      bburl = input("Please enter your Bitbucket URL: ")
      bitbucket = {"token": bbtoken, "url": bburl}
      client.write(vaultpath, bitbucket=bitbucket)
       
    try: 
       bb = response["data"]["bitbucket"]
    except Exception as e:
      bbtoken = input("Please enter your Bitbucket token: ")
      bburl = input("Please enter your Bitbucket URL: ")
      bitbucket = {"token": bbtoken, "url": bburl}
      client.write(vaultpath, bitbucket=bitbucket)
    response = client.read(vaultpath)
    bb = response["data"]["bitbucket"]
    return bb



def main():
#    prettyllog("status", "check", "login", "dsv", "0", "Testing", "ERROR")
  bb = get_bitbucket_token("ignite/bitbucket")
  projects = get_bitbucket_project_list(bb)



  return 0

if __name__ == "__main__":
    main()
