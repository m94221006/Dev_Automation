from lib.powerCycle import *
from lib.TelnetConsole import *
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


def command_result_comparsion(telnetconsole,checkcommandlist,checkaction,checkitem):
    for index, value in enumerate(checkcommandlist):
        check_string_list = checkitem[index].split(":")
        check_action = checkaction[index]
        for chekc_index, check_string in enumerate(check_string_list):
            check_string = ("%s(.*) %s") % (check_string, check_action)
            check_result = telnetconsole.send_command_match(value,check_string,10,"localdomain")
            logging.info("[command_result_comparsion][command:%s][check:%s] result :%s"%(value,check_string,check_result))






if __name__ == '__main__':
    set_log("coolboot.log")
    type ='console'
    consoleip = "10.2.66.50"
    consoleport = 2038
    consoletype = "router"
    device_user_name = "admin"
    device_user_pwd = "admin"
    din_relay_ip = "10.2.66.56"
    din_relay_user ="admin"
    din_relay_pwd ="lilee1234"
    din_relay_device_name = "LMS-2"
    test_cycle = 20000
    power_cycle_sleep = 60
    checkcommandlist = ["show interface all","show mobility tunnel all"]
    checkaction =["up","UA"]
    checkitem=["dialer 1","dialer 1"]
    try:
        powerCycle = powerCycle()
        telnetconsole = Telnet_Console(consoleip,consoleport)
        for k in range(0, test_cycle):
            if telnetconsole.kill_User(consoletype) :
                power_cycle_result =powerCycle.powerControl(din_relay_ip, din_relay_user, din_relay_pwd, din_relay_device_name )
                logging.info("[power_cycle_result]result :%s"%(power_cycle_result))
                if power_cycle_result:
                        logging.info("[power_cycle_sleep]60 seconds")
                        time.sleep(power_cycle_sleep)
                        login_result= telnetconsole.login()
                        logging.info("[telnet login]result :%s"%(login_result))
                        if login_result:
                            logging.info("update terminal paging disable")
                            telnetconsole.send_command("update terminal paging disable",5,"localdomain")
                            time.sleep(5)
                            command_result_comparsion(telnetconsole,checkcommandlist,checkaction,checkitem)
    except Exception,ex:
        logging.error("[coolboot]exception fail:%s "%(str(ex)))


