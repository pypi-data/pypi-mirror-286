import requests
import pprint


def get_organizations(url, session):
  orgurl = url + "/api/v2/organizations"
  resp = session.get(orgurl, verify=False)
  try: 
    orgs = resp.json["results"]
  except:
    orgs = []
  if resp.content["count"] == 0:
    print("Organization not found")
    return None
  else:
    return orgs
  

def get_projects(url, session):
  projects = {}
  prjurl = url + "/api/v2/projects"
  resp = session.get(prjurl, verify=False)
  try:
    prjs = resp.json["results"]
  except:
    prjs = []
  pprint.pprint(prjs)

  
  

  
def create_project(project, url, session):
  try:
    name = project["name"]
  except:
    print("Project name is required")
    return None
  try:
    description = project["description"]
  except:
    description = "" 
  try:
    organization = project["organization"]
  except:
    print("Organization name is required")
    return None

  project = {
    "name": name,
    "description": description,
    "organization": organization
  }

  orgurl = url + "/api/v2/projects"
  resp = session.post(orgurl, data=project, verify=False)
  if resp.status_code == 200:
    return resp.content
  else:
    return None
  

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
  resp = session.post(orgurl, data=organization, verify=False)
  if resp.status_code == 200:
    return resp.content
  else:
    return None
  
