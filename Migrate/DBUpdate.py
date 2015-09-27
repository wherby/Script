import json
import httplib
from optparse import OptionParser
import logging
from pprint import pprint
import base64
import pickle

TOKEN ="ItCkvmVvm3oYxijTgUgbaAeLJrkM"

failed=[]

config="";
def parse_options():

    parser = OptionParser("usage: %prog [options] dev|staging")

    (options, actions) = parser.parse_args()

    # Normalize the actions
    actions = map(lambda x: x.lower(), actions)

    # Remove duplicated actions
    def unique(seq):
        seen = set()
        seen_add = seen.add
        return [x for x in seq if x not in seen and not seen_add(x)]

    actions = unique(actions)

    return options, actions
    
def get_target_env(actions):
    target = "dev"
    if len(actions) > 0:
        target = actions[0]
    return target

def get_s3_config(target_env):
    global config
    env_s3_table = {
        'dev':{
            'buble_endpoint':'developer-dev.api.autodesk.com',
            'columbus_endpoint':"columbus-dev.autodesk.com"
        },
        'staging':{
            'buble_endpoint':'developer-stg.api.autodesk.com',
            'columbus_endpoint':"columbus-staging.autodesk.com"
        }
    }
    config=env_s3_table[target_env]
    pprint(config)
    return env_s3_table[target_env]


def post_response(endpoint, path, postData):
    print "https://"+endpoint+path
    conn = httplib.HTTPSConnection(endpoint,443)
    conn.request('POST', path , postData, {
        "Authorization":"Bearer "+TOKEN,
        "Content-Type":"application/json; charset=utf-8"
        })
    response=conn.getresponse()
    body=response.read()
    conn.close()
    return body

def post_response2(endpoint, path, postData):
    print "http://"+endpoint+path
    conn = httplib.HTTPConnection(endpoint,9001)
    conn.request('POST', path , postData, {
        "Authorization":"Bearer "+TOKEN,
        "Content-Type":"application/json; charset=utf-8"
        })
    response=conn.getresponse()
    body=response.read()
    #pprint(response)
    #print "body is :" +body
    conn.close()
    return body

def readFile():
    f=open("C:\\Users\\zhoust\\Documents\\record53.txt")
    
    data=json.load(f)
    pprint(data)
    for a in data["all"]:
        username=a["name"]
        for f2 in a["f"]["files"]:
            while getToken()==False:
                pass
            roleName=f2["roleName"]
            urn=f2["urn"]
            #insertDB(roleName,urn,username)
            rec=get_oxygen()
            if rec.has_key(username):
                for id in rec[username]:
                    insertDB(roleName,urn,username,id)
            else:
                pass
                #print "username is not get "+username
    f.close()

def insertDB(rolename,urn,username,userid):
    endpoint=config["columbus_endpoint"]
    data={"userId":userid,
          "userName":username,
          "userEmail":"",
          "physicalUrn":urn,
          "fileName":rolename
        }
    pprint(json.dumps(data))
    response=post_response2(endpoint,'/AddStorageItem',json.dumps(data))
    print response
    data=json.loads(response)
    print data["urn"]
    logUrn=data["urn"]
    move_bubble(logUrn,urn,rolename)


def get_oxygen():
    data=pickle.load(open("C:\\Users\\zhoust\\Documents\\oxygen.p",'rb'))
    #pprint(data)
    return data

def move_bubble(design, source, roleName):
    designT=design
    sourceT=source
    design=base64.urlsafe_b64encode(design)
    source=base64.urlsafe_b64encode(source)
    endpoint=config["buble_endpoint"]
    
    postData = {
        "design": design,
        "source": source,
        "from":{
            "urn":source,
            "filename":roleName
            }
    }

    postData = {
        "design": design,
        "source": source
    }
    pprint(postData)

    response = post_response(endpoint,'/derivativeservice/v2/registration',json.dumps(postData))
    result=response
    #print result
    if(result=='{"Result":"Success"}'):
        print "success"
    else:
        if source.find("=")!=-1:
            move_bubble2(designT,sourceT,roleName);
        else:
            print "fail to move "+source
            failed.append(source)


def move_bubble2(design, source, roleName):

    design=base64.urlsafe_b64encode(design)
    source=base64.urlsafe_b64encode(source).replace("=", "")
    endpoint=config["buble_endpoint"]
    
    postData = {
        "design": design,
        "source": source,
        "from":{
            "urn":source,
            "filename":roleName
            }
    }

    postData = {
        "design": design,
        "source": source
    }
    pprint(postData)

    response = post_response(endpoint,'/derivativeservice/v2/registration',json.dumps(postData))
    result=response
    #print result
    if(result=='{"Result":"Success"}'):
        print "success"
    else:
        print "fail to move "+source
        failed.append(source)

def logFailed():
    f=open("failed.txt",'w')
    for failfile in failed:
        f.writelines(failfile+'\n')
    f.close

def get_response(endpoint, path):
    print "https://"+endpoint+path
    conn = httplib.HTTPSConnection(endpoint,443)
    conn.request('GET',path,headers = {
        "Authorization":"Bearer " +TOKEN,
        "Content-Type":"application/json; charset=utf-8"
        })
    return conn.getresponse()

def get_response2(endpoint, path):
    print "http://"+endpoint+path
    conn = httplib.HTTPConnection(endpoint,9001)
    conn.request('GET',path,headers = {
        "Content-Type":"application/json; charset=utf-8"
        })
    response=conn.getresponse()
    body=response.read()

    #pprint(response)
    print "body is :" +body
    conn.close()
    return body

 


def test_urn():
    urna="urn:adsk.s3:derived.file:ColumbusUserFiles/users/Alex_Bicalho/001-FST-0022 - ISO 7380 - M8 x 10.ipt"
    response = get_response(config['buble_endpoint'],'/viewingservice/v1/thumbnails/{urn}'.format(urn=urna))
    print response.status

def getToken():
    global TOKEN
    endpoint=config["columbus_endpoint"]
    tokenInfo= get_response2(endpoint,'/OAuth2Token')
    tokenInfo=json.loads(tokenInfo)
    #pprint(tokenInfo)
    TOKEN=tokenInfo["token"]
    expires=int(tokenInfo["expires"])
    if(expires>100):
        return True
    else:
        return False
    
    
def setToken():
    global TOKEN
    

def main():
    (options, actions) = parse_options()
    target_env = get_target_env(actions)
    get_s3_config(target_env)
    print "start....."
    print config

    readFile()
    logFailed()
    

if __name__ != "__main__":
    print("This script can only be run in command line.")
    exit(-1)
else:
    main()
