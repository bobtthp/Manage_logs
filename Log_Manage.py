#coding:utf-8
#/usr/bin/python
import datetime
import os
from Tools import ssh_cmd
import Tools
import sys
import time
class Log:
    def __init__(self):
        now = datetime.datetime.now() - datetime.timedelta(1)
        self.now = datetime.datetime.strftime(now,"%a %b %d")
        #self.now = 'Sun Sep 16'
        self.log_path = os.getcwd() + '/logs'
    def import_log(self,file_path):
        linenum = 0
        line_list = []
        with open(file_path,'r') as f:
            for line in f.readlines():
                linenum += 1
                if line.find(self.now) != -1:
                    line_list.append(linenum)
        start = line_list[0]
        end   = line_list[-1]
        with open(file_path,'r') as f:
            for lines in f.readlines()[start:end]:
                with open(self.now + '.log','a') as f:
                    f.write(lines)
    def init_log_dir(self):
        log_home = os.getcwd() + '/logs/'
        date  = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d")
        build_log_path = log_home + date
        try:
            if not os.path.exists(log_home):
                os.mkdir(log_home)
        finally:
            if not os.path.exists(build_log_path):
                os.mkdir(build_log_path)
        return build_log_path
    def get_alter_log(self,ip,username,passwd,alter_log_path,build_log_path,sid):
        get_log_cmd = '''sed -n '/%s/{p;:1;n;:2;/%s/{p;b1};N;b2}'  %s ''' % (self.now,self.now,alter_log_path)
        #print get_log_cmd
        log_info = ssh_cmd(ip=ip,username=username,passwd=passwd,cmds=get_log_cmd)
        write_log_path = (build_log_path + '/' + sid + '.log')
        with open(write_log_path,'w') as f:
            for line in log_info:
                f.write(line)
            f.close()

def main():
    build_log_path = Log().init_log_dir()
    config = Tools.get_conf()
    for sid in config.keys():
        print (sid + " is working !")
        alter_log_path = config[sid]['log_addr'] + '/alert_' + sid + '.log'
        Log().get_alter_log(config[sid]['ip'], config[sid]['username'], Tools.Password().decrypt(config[sid]['passwd']),
                            alter_log_path=alter_log_path, build_log_path=build_log_path, sid=sid)
        time.sleep(1)
    print ('job exec over !')

if __name__ == "__main__":
    if sys.argv[1] == 'init':
        print ('exec init config !')
        Tools.Config('./import.json').init_config()
    elif sys.argv[1] == 'run':
        print ('exec run Log_Manage job !')
        main()
    else:
        print (
            '''
            Usage :
            python Log_Manage.py init   : init config for Log_Manage.py
            python Log_Manage.py run    : exec run Log_Manage job
            
            '''
        )

