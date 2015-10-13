import os
from flask import Flask
from celery import Celery
import swiftclient.client
import uuid

config = {'user':os.environ['OS_USERNAME'], 
          'key':os.environ['OS_PASSWORD'],
          'tenant_name':os.environ['OS_TENANT_NAME'],
          'authurl':os.environ['OS_AUTH_URL']}

conn = swiftclient.client.Connection(auth_version=2, **config)

bucket_name = "Test".format(str(uuid.uuid4()))
conn.put_container(bucket_name)



object_id = conn.put_object(bucket_name, "test_object", "Hi Swift")

config = {'username':os.environ['OS_USERNAME'], 
          'api_key':os.environ['OS_PASSWORD'],
          'project_id':os.environ['OS_TENANT_NAME'],
          'auth_url':os.environ['OS_AUTH_URL'],
           }
from novaclient.client import Client
nc = Client('2',**config)

image = nc.images.find(name="Ubuntu Server 14.04 LTS (Trusty Tahr)")
flavor = nc.flavors.find(name="m1.medium")
usrdata = open('/home/linkan/Dokument/Datormoln/labb2/userdata.yml', 'r')
instance = nc.servers.create(name="HEHEHE", image=image,flavor=flavor,key_name="cloudK",userdata=usrdata)

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

import paramiko
ssh = paramiko.SSHClient()
key = paramiko.RSAKey.from_private_key_file('/home/linkan/.ssh/cloud.key')
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
 
try:
    ssh.connect(str(floating_ip.ip), username='ubuntu', pkey=key)
    print 'Connection'
except Exception as e:
    print e