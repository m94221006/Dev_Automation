from lib.powerCycle import *
from lib.TelnetConsole import *
from lib.SSHConsole import *
import sys
import re
import logging


def set_log(filename):
    logging.basicConfig(filename=filename,level=logging.INFO,format='%(asctime)s [%(levelname)s] (%(threadName)-10s) %(message)s', )
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter(' %(asctime)s [%(levelname)s] (%(threadName)-10s) %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


def command_result_comparsion(console,consoletype,checkcommandlist,checkaction,checkitem):
    for index, value in enumerate(checkcommandlist):
        check_string_list = checkitem[index].split(":")
        check_action = checkaction[index]
        for chekc_index, check_string in enumerate(check_string_list):
            check_string = ("%s(.*) %s") % (check_string, check_action)
            check_result = False
            if consoletype =="telnet":
                check_result = console.send_command_match(value,check_string,10,"localdomain")
            elif consoletype == "ssh":
                check_result = console.write_command_match(value,check_string)
            logging.info("[command_result_comparsion][command:%s][check:%s] result :%s"%(value,check_string,check_result))






if __name__ == '__main__':
    set_log("coolboot.log")
    type ='ssh'
    consoleip = "10.2.53.54"
    consoleport = 2038
    consoletype = "router"
    device_user_name = "admin"
    device_user_pwd = "admin"
    din_relay_ip = "10.2.53.199"
    din_relay_user ="root"
    din_relay_pwd ="lilee1234"
    din_relay_device_name = "R1-WDU-LMS3.0"
    test_cycle = 20000
    power_cycle_sleep = 120
    checkcommandlist = ["show interface all","show mobility tunnel all"]
    checkaction =["up","UA"]
    checkitem=["dialer 0","dialer 0"]
    try:
        powerCycle = powerCycle()
        if type == "telnet":
            telnetconsole = Telnet_Console(consoleip,consoleport)
            for k in range(0, test_cycle):
                if telnetconsole.kill_User(consoletype) :
                    power_cycle_result =powerCycle.powerControl(din_relay_ip, din_relay_user, din_relay_pwd, din_relay_device_name )
                    logging.info("[power_cycle_result]result :%s"%(power_cycle_result))
                    if power_cycle_result:
                            logging.info("[power_cycle_sleep]%s seconds"%(power_cycle_sleep))
                            time.sleep(power_cycle_sleep)
                            login_result= telnetconsole.login()
                            logging.info("[telnet login]result :%s"%(login_result))
                            if login_result:
                                logging.info("update terminal paging disable")
                                telnetconsole.send_command("update terminal paging disable",5,"localdomain")
                                time.sleep(5)
                                command_result_comparsion(telnetconsole,type,checkcommandlist,checkaction,checkitem)
        elif type =="ssh":
            sshconsole =  SSHConnect(consoleip)
            for k in range(0, test_cycle):
                power_cycle_result =powerCycle.powerControl(din_relay_ip, din_relay_user, din_relay_pwd, din_relay_device_name )
                logging.info("[power_cycle_result]result :%s"%(power_cycle_result))
                if power_cycle_result:
                    logging.info("[power_cycle_sleep]%s seconds"%(power_cycle_sleep))
                    time.sleep(power_cycle_sleep)
                    sshconsole.connect()
                    logging.info("[ssh login]result :%s"%(sshconsole.IsConnect))
                    if sshconsole.IsConnect:
                        logging.info("update terminal paging disable")
                        sshconsole.write_command("update terminal paging disable",False)
                        time.sleep(5)
                        command_result_comparsion(sshconsole,type,checkcommandlist,checkaction,checkitem)
                        time.sleep(1)
                        sshconsole.disconnect()


    except Exception,ex:
        logging.error("[coolboot]exception fail:%s "%(str(ex)))


