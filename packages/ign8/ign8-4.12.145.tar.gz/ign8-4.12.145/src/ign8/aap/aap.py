import requests
import pprint


def get_organization(organization, url, session):
  orgurl = url + "/api/v2/organizations"
  resp = session.get(orgurl)
  pprint.pprint(resp.content)
  try: 
    orgs = resp.content["results"]
  except:
    orgs = []

  if len(orgs) == 0:
    print("Organization not found")
    return None
  else:
    pprint.pprint(orgs)
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
  pprint.pprint(resp.reason)
  pprint.pprint(resp.text)
  print("---------------------------")
  print(resp.status_code)
  print("---------------------------")

  if resp.status_code == 200:
    print("Organization created")
    return resp.content
  else:
    print("Organization not created")
    return None
  







#{
#name*	string
#title: Name
#maxLength: 512
#minLength: 1
#x-nullable: true
#description	string
#title: Description
#default:
#x-nullable: true
#max_hosts	integer
#t#itle: Max hosts
#d#efault: 0
#maximum: 2147483647
#minimum: 0
#Maximum number of hosts allowed to be managed by this organization.

#default_environment	integer
#title: Default environment
#x-nullable: true
#The default execution environment for jobs run by this organization.

 
#}