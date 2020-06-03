# -*- coding: UTF-8 -*-
from User import User



host=raw_input("host:")
user=raw_input("user:")
passwd=raw_input("password:")

P1=ESXI()

P1.connect_server(host,user,passwd)


print "All vm list:"
print P1.get_vm_list()

vm_name = raw_input("Select which vm:")
P1.get_vm_by_name(vm_name)

f=raw_input("Do you want to power on "+vm_name+"?(Y/N)")
if(f=="Y"):
	P1.vm_power_on()

raw_input("power off?")
P1.vm_power_off()

P1.disconnect_server()
