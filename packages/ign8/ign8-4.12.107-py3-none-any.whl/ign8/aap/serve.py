# main file for semaphore

import os
import sys
import time
import yaml
import json
import hvac
import requests
import pprint


from  ..common import prettyllog
from .bitbucket import get_bitbucket_project_list, get_bitbucket_token, get_bitbucket_project, create_bitbucket_project





VERIFY_SSL = False


def awx_create_schedule(name, unified_job_template,  description, tz, start, run_frequency, run_every, end, scheduletype, organization, mytoken, r):
  headers = {"User-agent": "python-awx-client", "Content-Type": "application/json","Authorization": "Bearer {}".format(mytoken)}
  # The scheduling is tricky and must be refined
  if ( scheduletype == "Normal"):
     data = {
      "name": name,
      "unified_job_template": unified_job_template,
      "description": description,
      "local_time_zone": tz,
      "dtstart": start['year'] + "-" + start['month'] + "-" + start['day'] + "T" + start['hour'] + ":" + start['minute'] + ":" + start['second']  + "Z",
      "rrule": "DTSTART;TZID=" + tz + ":" + start['year'] + start['month'] + start['day'] + "T" + start['hour'] + start['minute'] + start['second'] +" RRULE:INTERVAL=" + run_frequency + ";FREQ=" + run_every
    }
  url = os.getenv("TOWER_HOST") + "/api/v2/schedules/"
  resp = requests.post(url,headers=headers, json=data, verify=VERIFY_SSL)
  response = json.loads(resp.content)
  try:
    schedid=response['id']
    prettyllog("manage", "schedule", name, organization, resp.status_code, schedid)
  except:
    prettyllog("manage", "schedule", name, organization, resp.status_code, response)





def input_initial_secret(url=None, user=None, password=None):
  if url == None:
    AAP_URL = input("Enter the AAP URL: ")
  if user == None:
    AAP_USER = input("Enter the AAP USER: ")
  if password == None:
    AAP_PASS = input("Enter the AAP PASSWORD: ") # obscufate the password input
  return dict(AAP_URL=AAP_URL, AAP_USER=AAP_USER, AAP_PASS=AAP_PASS)


def get_credentials_from_vault():
  vaultpath = os.getenv('IGN8_VAULT_PATH')
  if vaultpath == None:
    vaultpath = "ignite"


  # Get credentials from vault
  try:
    client = hvac.Client()
  except:
    return False

  try:
    read_response = client.secrets.kv.read_secret_version(path=vaultpath)
  except:
    # If the path does not exist, create it
    # read the aap user, url and password from vault , obscufate the password input
    # create the path if it does not exist
    secret = input_initial_secret()
    client.secrets.kv.v2.create_or_update_secret(
      path=vaultpath,
      secret=secret
    )
  read_response = client.secrets.kv.read_secret_version(path=vaultpath)
  # check if the path secret contains the AAP_URL, AAP_USER and AAP_PASS
  try:
    URL = read_response['data']['data']['AAP_URL']
  except:
    URL = None
  try:
    USER = read_response['data']['data']['AAP_USER']
  except:
    USER = None
  try:
    PASS = read_response['data']['data']['AAP_PASS']
  except:
    PASS = None

  if URL == None or USER == None or PASS == None:
    secret  = input_initial_secret(URL, USER, PASS)
    client.secrets.kv.v2.create_or_update_secret(
      path=vaultpath,
      secret=secret
    )
    read_response = client.secrets.kv.read_secret_version(path=vaultpath)
  return read_response['data']['data']

def add_token_to_vault(vaultpath, token):
  #read current secret in vault
  client = hvac.Client()
  read_response = client.secrets.kv.read_secret_version(path=vaultpath)
  read_response['data']['data']['AAP_TOKEN'] = token
  client.secrets.kv.v2.create_or_update_secret(
    path=vaultpath,
    secret=read_response['data']['data']
  )
  return True


  

def check_aap_login():
  # Check if the user is logged in

  return True  

def login_aap_basicauth(url, user, password):
  headers = {"User-agent": "python-awx-client", "Content-Type": "application/json"} 
  data = {"username": user, "password": password}
  pingurl = url + "/api/v2/ping"
  session = requests.Session()
  session.auth = (user, password)
  session.verify = False
  resp = session.get(pingurl)
  if resp.status_code != 200:
    print("Login failed")
    return False
  return session

def aap_ping(url, session):
  pingurl = url + "/api/v2/ping"
  resp = session.get(pingurl)
  if resp.status_code != 200:
    return False
  return True




    






def getawxdata(item, mytoken, r):
  headers = {"User-agent": "python-awx-client", "Content-Type": "application/json","Authorization": "Bearer {}".format(mytoken)}
  url = os.getenv("TOWER_HOST") + "/api/v2/" + item
  intheloop = "first"
  while ( intheloop == "first" or intheloop != "out" ):
    try:
      resp = requests.get(url,headers=headers, verify=VERIFY_SSL)
    except:
      intheloop = "out"
    try:
      mydata = json.loads(resp.content)
    except:
      intheloop = "out"
    try:
      url = os.getenv("TOWER_HOST") + "/api/v2/" + (mydata['next'])
    except: 
      intheloop = "out"
    savedata = True
    try:
      myresults = mydata['results'] 
    except:
      savedata = False
    if ( savedata == True ):
      for result in mydata['results']:
        key = os.getenv("TOWER_HOST") + item +":id:" + str(result['id'])
        r.set(key, str(result), 600)
        key = os.getenv("TOWER_HOST") + item +":name:" + result['name']
        r.set(key, str(result['id']), 600 )
        key = os.getenv("TOWER_HOST") + item +":orphan:" + result['name']
        r.set(key, str(result), 600)

  
def refresh_awx_data(mytoken,r ):
  items = { 
    "ad_hoc_commands",
    "analytics,applications",
    "credential_input_sources",
    "credentials",
    "credential_types",
    "execution_environments",
    "groups",
    "hosts",
    "inventory_sources",
    "inventory_updates",
    "jobs",
    "job_templates",
    "labels",
    "metrics",
    "notifications",
    "notification_templates",
    "organizations",
    "projects",
    "project_updates",
    "roles",
    "schedules",
    "system_jobs",
    "system_job_templates",
    "teams",
    "unified_jobs",
    "unified_job_templates",
    "workflow_approvals",
    "workflow_job_nodes",
    "workflow_jobs",
    "workflow_job_template_nodes",
    "workflow_job_templates"
  }
  #items = {"organizations", "projects", "credentials", "hosts", "inventories", "credential_types", "labels" , "instance_groups", "job_templates", "execution_environments"}    
  for item in items:
    getawxdata(item, mytoken, r)




def check_git(repository):
  
  # Check if the git repository exists
  return True


  




def read_config():
  config = {}
  config['mainproject'] = {}
  config['subprojects'] = {}
  configpath = os.getenv("IGN8_CONFIG_PATH")
  if configpath == None:
    configpath = "/etc/ign8"
    # check if the path exists
  if not os.path.exists(configpath):
    os.makedirs(configpath)
  if not os.path.exists(configpath + "/ign8.d"):
    os.makedirs(configpath + "/ign8.d")
  # check if the path exists
  if not os.path.exists(configpath) or not os.path.exists(configpath + "/ign8.d"):
    return False
  
  filesindir = os.listdir(configpath)
  # we can only have one ign8.yaml and a directory ign8.d
  if "ign8.yml" in filesindir:
    with open("/etc/ign8/ign8.yml", 'r') as f:
      data = yaml.safe_load(f)
      config['mainproject'] = data  
    
  if "ign8.d" in filesindir:
    for subproject in data['subprojects']:
      subprojectname = subproject['name'].replace(" ", "_")
      if os.path.exists("/etc/ign8/ign8.d/%s.yml" % subprojectname):
        with open("/etc/ign8/ign8.d/%s.yml" % subprojectname, 'r') as f:
          data = yaml.safe_load(f)
          config['subprojects'][subprojectname] = {}
      else:
        # Create a file for the subproject
        open("/etc/ign8/ign8.d/%s.yml" % subprojectname, 'w').close()
        subprojectheader = { "subproject": subprojectname}
        subprojecttemplates =  { "templates": [{ "name":"checkup", "description": "Ping playbook to check connectivity"}] }
        subprojectschedules =  { "schedules": [{ "name":"checkup", "description": "Ping schedule to check connectivity continiously", "schedule": "run every 15 minutes"}] }

        with open("/etc/ign8/ign8.d/%s.yml" % subprojectname, 'w') as f:
          yaml.dump(subprojectheader, f)
          yaml.dump(subprojecttemplates, f)
          yaml.dump(subprojectschedules, f)
  # We need to read the main project file  in config path
  with open("/etc/ign8/ign8.yml", 'r') as f:
    data = yaml.safe_load(f)
    config['mainproject'] = data
  # iterate over the subprojects
  for subproject in data['subprojects']:
    subprojectname = subproject['name'].replace(" ", "_")
    with open("/etc/ign8/ign8.d/%s.yml" % subprojectname, 'r') as f:
      data = yaml.safe_load(f)
      config['subprojects'][subprojectname] = data
  return config

  return True

csfrtoken = None


def main():
    prettyllog("Ignite aap", "init", "login", "automation platform", "0", "Initializinf", "INFO")
    secrets = get_credentials_from_vault()
    url = secrets['AAP_URL']
    session = login_aap_basicauth(url, secrets['AAP_USER'], secrets['AAP_PASS'])
    if session == False:
      prettyllog("Ignite aap", "init", "login", "automation platform", "0", "Login failed", "ERROR")
      return False
    if aap_ping(url, session):
      prettyllog("Ignite aap", "init", "login", "automation platform", "0", "Login successfull", "INFO")
    else:
      prettyllog("Ignite aap", "init", "login", "automation platform", "0", "Ping aap platform api failed", "ERROR")


    prettyllog("Ignite aap", "init", "login", "automation platform", "0", "initiate iternal loop", "INFO")
    while True:
      prettyllog("Ignite aap", "Main loop", "Star", "automation platform", "0", "Start of iteration", "INFO")
      #################################################################################################################################################### Read config #######################################################
      prettyllog("Ignite aap", "Main loop", "Read Config", "automation platform", "0", "Read configuration", "INFO")
      config = read_config()

      prettyllog("Ignite aap", "Main loop", "Refresh AWX data", "automation platform", "0", "Get access to GIT repo", "INFO")
      bbtoken = get_bitbucket_token("ignite/bitbucket")
      mainprojectexists = False
      while not mainprojectexists:
        projects = get_bitbucket_project_list(bbtoken)
        pprint.pprint(config)
      # Check if må main project exists i bitbucket
        projectkey = None
        for project in projects:
          if project['name'] == config['mainproject']['mainproject']:
            projectkey = project['key']
            break
        if projectkey == None:
          projectdata = {
            "name": config['mainproject']['mainproject'],
            "description": "Main project for ignite aap",
            "is_private": True
          }
          projectkey = create_bitbucket_project(bbtoken, config['mainproject']['mainproject'])
        else:
          mainprojectexists = True
      # Check if the main project exists in AWX


      




      prettyllog("Ignite aap", "Main loop", "Refresh AWX data", "automation platform", "0", "Main project exists", "INFO")

      
      prettyllog("Ignite aap", "Main loop", "Refresh AWX data", "automation platform", "0", "Check if main project exists", "INFO")




      #################################################################################################################################################### Read config #######################################################

      prettyllog("Ignite aap", "Main loop", "login", "automation platform", "0", "End of iteration", "INFO")
      count = 10
      for i in range(count):
        prettyllog("Ignite aap", "Main loop", "login", "automation platform", "0", "Sleeping (%02d/10)" % i, "INFO")
        time.sleep(1)
    return 0




