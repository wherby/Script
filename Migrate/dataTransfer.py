import os,sys
import shutil
import base64
import boto
import boto.s3.connection
from boto.s3.key import Key
import json
import httplib
from optparse import OptionParser
import logging
logging.getLogger('boto').setLevel(logging.DEBUG)
__author__ = 'Huabei Yin'

TOKEN = "Exrp6w5If9in3O347KMtQnwGQt2U"
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

def encode_url_safe(urn):
     return base64.b64encode(urn).replace('=','')

def encode_url_unsafe(urn):
     return base64.b64encode(urn)

def get_s3_config(target_env):
    env_s3_table = {
        'dev':{
            'buble_endpoint':'developer-dev.api.autodesk.com',
            'accese_key':'AKIAIQEZM3543JPE7IQQ',
            'secret_key':'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',
            'bucket':'autodesk-translation-storage-dev'
        },
        'staging':{
            'buble_endpoint':'developer-stg.api.autodesk.com',
            'accese_key':'AKIAJ7GUWKNTXMC2774A',
            'secret_key':'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',
            'bucket':'autodesk-360-translation-storage-staging'
        }
    }
    return env_s3_table[target_env]
    
def create_s3_conn(config):
    print config['accese_key']
    print config['secret_key']
    print config['bucket']

    connection = boto.connect_s3(
        aws_access_key_id = config['accese_key'],
        aws_secret_access_key = config['secret_key'],
        )
    return connection

def transfer(config, content):
    jContent = json.loads(content)
    for f in jContent['files']:
        print f['roleName']
        safe_urn = encode_url_safe(f['urn']) # old urn
        unsafe_urn = encode_url_unsafe(f['urn']) # new urn

        try:
            response = get_response(config['buble_endpoint'],'/viewingservice/v1/thumbnails/{urn}'.format(
            urn = unsafe_urn))
            print response.status
            if response.status == 404:
                try:
                    response2 = get_response(config['buble_endpoint'],'/viewingservice/v1/thumbnails/{urn}'.format(
                    urn = safe_urn))
                    print response2.status
                    if response2.status == 200:
                        try:
                            pass
                            # move_bubble(design=unsafe_urn, source= safe_urn, endpoint=config['buble_endpoint'])
                        except Exception, e:
                            pass
                except Exception, e:
                    pass            
        except Exception, e:
            pass

def move_bubble(design, source, endpoint):
    postData = {
        "design": design,
        "source": source
    }
    response = post_response(endpoint,'/derivativeservice/v2/registration',json.dumps(postData))
    print response.read()

def get_response(endpoint, path):
    print "https://"+endpoint+path
    conn = httplib.HTTPSConnection(endpoint,443)
    conn.request('GET',path,headers = {
        "Authorization":"Bearer " +TOKEN,
        "Content-Type":"application/json; charset=utf-8"
        })
    return conn.getresponse()

def post_response(endpoint, path, postData):
    print "https://"+endpoint+path
    conn = httplib.HTTPSConnection(endpoint,443)
    conn.request('POST', path , postData, {
        "Authorization":"Bearer "+TOKEN,
        "Content-Type":"application/json; charset=utf-8"
        })
    return conn.getresponse()

def doTestTransfer(target_env):
    config = get_s3_config(target_env)
    conn = create_s3_conn(config)
    bucket = conn.get_bucket(config['bucket'])
    # key  = bucket.get_key('columbus/Huabei_Yin.txt')
    # key  = bucket.get_key('columbus/Wesley_Miao.txt')
    key  = bucket.get_key('columbus/Herbert_He.txt')
    # 
    content = key.get_contents_as_string()
    # content = '{"files":[{"roleName":"SteamEngine.dwf","urn":"urn:adsk.test.filesystem:fs.file:/test/TestFiles/DWF/SteamEngine.dwf?version=columbus"},{"roleName":"2.dwf","urn":"urn:adsk.test.filesystem:fs.file:/test/TestFiles/DWF/2.dwf?version=columbus"},{"roleName":"wall.dwf","urn":"urn:adsk.storage:fs.file:user/3c7b158771e54346bcc2cc4a03c4d75a?version=columbus"},{"roleName":"A.dwf","urn":"urn:adsk.objects:os.object:columbus/huabei_yind-_-b1413769820226A.dwf"}],"user":"huabei_yin"}'
    # content ='{"files":[{"roleName":"AK47.dwf","urn":"urn:adsk.objects:os.object:columbus/Wesley_Miaod-_-b1420519395091AK47.dwf"},{"roleName":"A-7thAve-Mockup-ModelVE.rvt","urn":"urn:adsk.objects:os.object:columbus/Wesley_Miaod-_-b1420708518994A-7thAve-Mockup-ModelVE.rvt"},{"roleName":"Car1.dwf","urn":"urn:adsk.objects:os.object:columbus/Wesley_Miaod-_-b1424825257829Car1.dwf"},{"roleName":"Car2.dwf","urn":"urn:adsk.objects:os.object:columbus/Wesley_Miao%2F1424851931355%2FCar2.dwf"},{"roleName":"Parent.dwg","urn":"urn:adsk.objects:os.object:columbus/Wesley_Miao%2F1424852531589%2FParent.dwg"},{"roleName":"Parent.dwg","urn":"urn:adsk.objects:os.object:columbus/Wesley_Miao%2F1424852727390%2Fdwg_xref.zip"},{"roleName":"rac_basic_sample_project.rvt","urn":"urn:adsk.objects:os.object:columbus/Wesley_Miao%2F1424854783948%2Frac_basic_sample_project.rvt"}],"user":"Wesley_Miao","settings":{}}'
    print content
    transfer(config, content)

def getUserName(filePath):
    #print "a:" +filePath 
    a=filePath[filePath.rfind('/')+1:]
    return a[:a.rfind(".")].replace('_',' ')


def doTransfer(target_env):
    config = get_s3_config(target_env)

    conn = create_s3_conn(config)

    bucket = conn.get_bucket(config['bucket'])

    f=open("record52.txt",'w')
    f.writelines('{"all":[')
    print "start transfer....."
    for key in bucket.list("columbus/",'/'):

        #print "start transfer for [" + key.name +"]"
        print getUserName(key.name)
        name=getUserName(key.name)
        if name=='Tao Zhou':
            f.writelines('{')
            f.writelines('"name":"'+getUserName(key.name)+'",\n')
            content = key.get_contents_as_string()
            print content
            f.writelines('"f":'+content+'\n')
        #transfer(config, content)
            print "completed transfer for [" + key.name +"]"
            f.writelines('},')
    print "transfer completed....."
    f.writelines(']}')
    f.close()

def doTransfer2(target_env):
    config = get_s3_config(target_env)

    conn = create_s3_conn(config)

    bucket = conn.get_bucket(config['bucket'])

    f=open("name2.txt",'w')
    #f.writelines('{"all":[')
    print "start transfer....."
    for key in bucket.list("columbus/",'/'):
        #f.writelines('{')
        #print "start transfer for [" + key.name +"]"

        print getUserName(key.name)
        f.writelines(getUserName(key.name).replace(' ','_')+'\n')
        content = key.get_contents_as_string()
        print content
        #f.writelines('"f":'+content+'\n')
        #transfer(config, content)
        print "completed transfer for [" + key.name +"]"
        #f.writelines('},')
    print "transfer completed....."
    #f.writelines(']}')
    f.close()

def main():
    print "transfer completed....."
    (options, actions) = parse_options()
    target_env = get_target_env(actions)
    doTransfer2(target_env)

if __name__ != "__main__":
    print("This script can only be run in command line.")
    exit(-1)
else:
    main()
