# -*- coding: UTF-8 -*-
import ssl
import paramiko
import sys, re, getpass, argparse, subprocess
from pysphere import MORTypes, VIServer
from pysphere.vi_virtual_machine import VIVirtualMachine

class User():
	server_ip = ""
	user_name = ""
	password  = ""
	server    = ""

	vm = "" #当前虚拟机的实例
	vm_name = "" #当前虚拟机名称
	vm_os = ""

	ssh = "" #SSH连接对象
	#def __init__(self):


	#连接ESXI
	def __init__(self,host,user,passwd):
		self.server_ip=host
		self.user_name=user
		self.password=passwd
		try:
			#关闭ssl验证
			ssl._create_default_https_context = ssl._create_unverified_context
			#连接ESXI
			self.server = VIServer()
			self.server.connect(host, user, passwd)
		except:
			print("Connect error!!!")
			return False
		return True
	#断开连接
	def disconnect_server(self):
		try:
			self.server.disconnect()
		except:
			#print "error!!"
			return False
		return True
	

	# 建立SSH连接
	def SSH_connect(self):
		try:
			# 建立一个sshclient对象
			self.ssh = paramiko.SSHClient()
			# 允许将信任的主机自动加入到host_allow 列表，此方法必须放在connect方法的前面
			self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			# 调用connect方法连接服务器
			# 需要管理员账号
			self.ssh.connect(hostname=self.server_ip, port=22, username=self.user_name, password=self.password)
			return True
		except:
			return False
	# 关闭连接
	def SSH_disconnect(self):
		try:
			self.ssh.close()
			return True
		except:
			return False
	#SSH远程执行CMD命令
	def command_server(self,cmd):
		try:
			self.SSH_connect()
			# 执行命令
			# stdin, stdout, stderr = self.ssh.exec_command(cmd)

			self.ssh.exec_command(cmd)
			# 执行命令后SSH马上断开了，如何查看指令执行进度？？
			
			self.SSH_disconnect()
			# 结果放到stdout中，如果有错误将放到stderr中
			print(">>>"+cmd)
			# print stdout.read().decode()
			
			return True
		except:
			return False

	#当前所有虚拟机list
	def get_vm_list(self):
		try:
			return self.server.get_registered_vms()
		except:
			print("Failure!!!")
			return False
	#获取指定名称的虚拟机实例
	def get_vm_by_name(self,vm_name):
		try:
			self.vm = self.server.get_vm_by_name(vm_name)
			self.vm_name = vm_name
		except:
			print("Get vm error!")
			return False
		return self.vm
	#获取该虚拟机的状态
	def vm_get_status(self):
		try:
			print(self.vm.get_status())
		except:
			print("Failure!!!")
			return False
		return True


	'''改变虚拟机电源状态'''
    #开机
	def vm_power_on(self):
		try:
			if(self.vm.is_powered_off()):
				self.vm.power_on();
			else:
				print("vm "+vm_name+" is already power on!!!")
		except:
			print("Failure!!!")
			return False
		return True
    #关机
	def vm_power_off(self):
		try:
			if(self.vm.is_powered_on()):
				self.vm.power_off();
			else:
				print("vm "+vm_name+" is already power off!!!")
		except:
			print("Failure!!!")
			return False
		return True
	#重启  #sync_run=False 异步
	def vm_reset(self):
		try:
			self.vm.reset()
			return True
		except:
			return False
	#挂起   suspend()
	def vm_suspend(self):
		pass
 