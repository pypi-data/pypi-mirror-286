import requests
import pprint


def get_organization(organization, url, session):
  orgurl = url + "/api/v2/organizations"
  resp = session.get(orgurl)
  pprint.pprint(resp.content)







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