# -*- coding: UTF-8 -*-
from User import User

P1=User()
P1.connect_server('192.168.43.206','root','Cloud$2020')

cmd=raw_input("CMD:")

P1.command_server(cmd)

