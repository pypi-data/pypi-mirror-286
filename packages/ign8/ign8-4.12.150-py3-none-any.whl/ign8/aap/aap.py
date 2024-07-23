import requests
import pprint


def get_organization(organization, url, session):
  orgurl = url + "/api/v2/organizations"
  resp = session.get(orgurl)
  try: 
    orgs = resp.content["results"]
  except:
    orgs = []

  pprint.pprint(resp.content)
  

  if len(orgs) == 0:
    print("Organization not found")
    return None
  else:
    return orgs

def create_organization(organization, url, session):
  try:
    name = organization["name"]
  except:
    print("Organization name is required")
    return None
  try:
    description = organization["description"]
  except:
    description = "" 
  try:
    max_hosts = organization["max_hosts"]
  except:
    max_hosts = 0

  try:
    default_environment = organization["default_environment"]
  except:
    default_environment = 1

  organization = {
    "name": name,
    "description": description,
    "max_hosts": max_hosts,
    "default_environment": default_environment
  }

  orgurl = url + "/api/v2/organizations"
  resp = session.post(orgurl, data=organization)
  if resp.status_code == 200:
    return resp.content
  else:
    return None
  
