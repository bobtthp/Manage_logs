#coding:utf-8
#/usr/bin/python
import base64
import json
import os
import paramiko

class Password:
    def encrypt(self,args):
        return base64.b64encode(args)
    def decrypt(self,args):
        return base64.b64decode(args)
    def encrypts(self,lists):
        return map(self.encrypt,lists)
    def decrypts(self,lists):
        return map(self.decrypt,lists)

def ssh_cmd(ip,username,passwd,cmds):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip,22,username=username,password=passwd,timeout=30)
        stdin,stdout,stdrr = client.exec_command(cmds)
        result = stdout.readlines()
        #print result
        return result
    except Exception:
        return 'failed'
    finally:
        client.close()

def get_conf():
    conf_path = os.getcwd() + '/conf/config.json'
    conf = json.loads(open(conf_path, 'r').read())
    return conf


class Config:
    def __init__(self,file_path):
        self.path = file_path
    def read_config(self):
        try:
            im_config = json.loads(open(self.path,'r').read())
            return im_config
        except Exception:
            print('please check file path is true or permission is confused , may the format of config file is wrong')
    def init_config(self):
        try:
            im_config = self.read_config()
            conf_path = os.getcwd() + '/conf/config.json'
            my_config = json.loads(open(conf_path,'r').read())
            for ip in im_config.keys():
                if ip in my_config.keys():
                    print (ip,'do not need init')
                else:
                    sid = ssh_cmd(ip,im_config[ip]['username'],im_config[ip]['passwd'],'source ~/.bash_profile;echo $ORACLE_SID')[0].strip('\n')
                    #print(sid)
                    my_config[sid] = {}
                    my_config[sid]['ip'] = ip
                    my_config[sid]['username'] = im_config[ip]['username']
                    my_config[sid]['passwd'] = Password().encrypt(im_config[ip]['passwd'])
                    my_config[sid]['log_addr'] = ssh_cmd(ip,im_config[ip]['username'],im_config[ip]['passwd'],'source ~/.bash_profile;echo $ALTER_PATH')[0].strip('\n')
                    #print(my_config[sid]['log_addr'])
            with open(conf_path,'w') as f:
                json.dump(my_config,f)
            #print (my_config)
        except Exception as e :
            print (e)
            print ('please check ./conf/config.json is exist !')



