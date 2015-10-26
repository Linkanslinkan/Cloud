import os
import swiftclient.client
import time
import uuid
from novaclient.client import Client

################### CONFIG FOR CLIENT CONNECTION ######################

config = {'user':os.environ['OS_USERNAME'], 
          'key':os.environ['OS_PASSWORD'],
          'tenant_name':os.environ['OS_TENANT_NAME'],
          'authurl':os.environ['OS_AUTH_URL']}


conn = swiftclient.client.Connection(auth_version=2, **config)

############### PUT BUCKET IN CONTAINER #####################

bucket_name = "EHEHHE".format(str(uuid.uuid4()))
conn.put_container(bucket_name)

###### SETTINGS FOR SERVER CREATION #######################

config = {'username':os.environ['OS_USERNAME'], 
          'api_key':os.environ['OS_PASSWORD'],
          'project_id':os.environ['OS_TENANT_NAME'],
          'auth_url':os.environ['OS_AUTH_URL'],
           }

nc = Client('2',**config)

#################### CREATE SERVER ###########################

image = nc.images.find(name="Ubuntu Server 14.04 LTS (Trusty Tahr)")
flavor = nc.flavors.find(name="m1.medium")
usrdata = open('/home/linkan/Dokument/Datormoln/labb2/userdata.yml', 'r')
instance = nc.servers.create(name="HEHEHE", image=image,flavor=flavor,key_name="cloudK",userdata=usrdata)


############### ADDING FLOATING IP TO INSTANCE ####################


status = instance.status
while status == 'BUILD':
    time.sleep(5)
    instance = nc.servers.get(instance.id)
    status = instance.status
print "status: %s" % status

IPlist = nc.floating_ips.list()
if not IPlist:
    floating_ip = nc.floating_ips.create()
    instance = nc.servers.find(name="HEHEHE")
    instance.add_floating_ip(floating_ip)
    print floating_ip
else:
    floating_ip = IPlist[2]
    instance.add_floating_ip(floating_ip)
    print floating_ip
    
instance.add_security_group("default")


print floating_ip.ip

############# SSH CONNET TO VM ###################

time.sleep(15)
import paramiko
ip = floating_ip.ip
ssh = paramiko.SSHClient()
key = paramiko.RSAKey.from_private_key_file('/home/linkan/.ssh/cloud.key')
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
 
try:
    ssh.connect(ip, username='ubuntu', pkey=key)
    print 'Connection'
except Exception as e:
    print e

##### PROVISIONING THE VM     #######################

commands = [
          'sudo apt-get update -y',
          'sudo apt-get install python-pip -y',
          'sudo pip install Flask',
          'sudo apt-get install rabbitmq-server -y',
          'sudo apt-get install git -y',
          'sudo pip install celery',
          'git clone https://github.com/Linkanslinkan/Cloud.git', #.git
          'cd Cloud;pwd;ls'
          #'celery worker -A tasks.celery --loglevel==INFO',
          #'python tasks.py > /dev/null 2>&1 &'
          # install git, clone rep, cd, start worker, python tasks.py
        ]

for command in commands:
    try:
        print 'TRYING:  {}'.format(command)
        stdin, stdout, stderr = ssh.exec_command(command)
        print 'SUCCESS!!! MAFACKAAAA.'
        print stdout.read()
        print stderr.read()
        
    except Exception as e:
        print 'Faaaail: {}'.format(e)


######## DELETE OBJECTS FROM CONTAINER AND DELETE CONTAINER

(result, object_list) = conn.get_container(bucket_name)
for obj in object_list: 
    conn.delete_object(bucket_name, obj['name'])

conn.delete_container(bucket_name)

#### DELETE SERVER

server = nc.servers.find(name = "HEHEHE")
server.delete()



######################## JOX

def tweet_parse(tweet_to_count):

  dictionary = {'han': 0, 'hon': 0, 'den': 0, 'det':0,'denna':0 ,'denne':0,'hen':0}
  tweets_file = open(tweet_to_count,'r')

  for line in tweets_file:
    try:
      tweet = json.loads(line)
      if tweet['text'][:2] != 'RT':
        tweetArr = tweet['text'].split()
        for word in tweetArr:
          if "han" == word:
            dictionary['han'] = dictionary['han'] + 1
          elif "hon" == word:
            dictionary['hon'] = dictionary['hon'] + 1
          elif "den" == word:
            dictionary['den'] = dictionary['den'] + 1
          elif "det" == word:
            dictionary['det'] = dictionary['det'] + 1
          elif "denna" == word:
            dictionary['denna'] = dictionary['denna'] + 1
          elif "denne" == word:
            dictionary['denne'] = dictionary['denne'] + 1 
          elif "hen" == word:
            dictionary['hen'] = dictionary['hen'] + 1
    except:
      continue
  result = json.dumps(dictionary)
  return result




def download(name):
    url = 'http://smog.uppmax.uu.se:8080/swift/v1/tweets/{}'.format(name)
    
    file_name = url.split('/')[-1]
    u = urllib2.urlopen(url)
    f = open(file_name,'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)
    
    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
          break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,

  f.close()
  return file_name








 
@app.route('/count')
def count():
  testURL = 'http://smog.uppmax.uu.se:8080/swift/v1/tweets/'
  print testURL
  testFiles = os.popen('curl {}'.format(testURL)).read().rsplit('\n')
  for files in testFiles:
    temp = download(files)
    result = tweet_parse(temp)
    print result

    '''
    while (result.ready == False):
      pass
    return result.get()
    '''
@app.route("/", methods = ['GET'])
def starter():
  name = 'Linkan'
  return render_template('start.html',name=name)

'''
@app.route("/linkan")
def parse():
  result = tweet_parse.delay()
  while(result.ready == False):
    pass
  return result.get()
'''









# || Exit when cd with paramiko


# def get_resource_as_string(name, charset='utf-8'):
#     with app.open_resource(name) as f:
#         return f.read().decode(charset)

# app.jinja_env.globals['get_resource_as_string'] = get_resource_as_string