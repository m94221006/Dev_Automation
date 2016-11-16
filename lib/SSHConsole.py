__author__ = 'ricky.wang'
import telnetlib
import time
import re
import httplib2
import logging
import paramiko

class SSHConnect(object):

    def __init__(self,ipaddress,username="admin",password="admin"):
        self.ipaddress = ipaddress
        self.username = username
        self.password=password
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshresult = None
        self.IsConnect =False
        self.set_log("SSHConsole.log")


    def set_log(self,filename):
        logging.basicConfig(filename=filename,level=logging.INFO,format='%(asctime)s [%(levelname)s] (%(threadName)-10s) %(message)s', )
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        formatter = logging.Formatter(' %(asctime)s [%(levelname)s] (%(threadName)-10s) %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)


    def connect(self):
        try:
            self.ssh.connect(self.ipaddress, port=22, username=self.username, password= self.password, timeout=int(10))
            time.sleep(1)
            if(self.ssh):
                self.IsConnect= True
            else:
                self.IsConnect =False

            logging.info("connect status :%s"%(sshconnect.IsConnect))

        except Exception,ex:
            logging.error("[connect]ssh login fail:%s "%(str(ex)))
            self.IsConnect =False
            self.ssh.close()

    def write_command(self, command,logflag =True):
        try:
            if(self.ssh):
                remote_conn = self.ssh.invoke_shell()
                remote_conn.send("%s\n"%(command))
                time.sleep(2)
                self.sshresult = remote_conn.recv(5000)
                if logflag == True:
                    logging.info(self.sshresult)

            else:
                logging.info("Connection not opened.")
        except Exception,ex:
            logging.error("[write_command]write command fail:%s "%(str(ex)))
            self.IsConnect =False
            self.ssh.close()


if __name__ == '__main__':
    sshconnect = SSHConnect("10.2.52.56")
    sshconnect.connect()
    if(sshconnect.IsConnect):
        times = 200000
        for k in range(0, times):
            sshconnect.write_command("debug line cellular 0 atcmd \"AT!GSTATUS?\"")
            sshconnect.write_command("debug line cellular 1 atcmd \"AT!GSTATUS?\"")
            sshconnect.write_command("show gps detail")
            time.sleep(10)

