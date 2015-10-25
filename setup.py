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