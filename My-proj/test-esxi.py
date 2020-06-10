# -*- coding: UTF-8 -*-

from User import User

server_ip = "192.168.1.212"
user_name = "root"
password  = "Cloud$2020"

U = User(server_ip,user_name,password)
U.command_server("reboot")
