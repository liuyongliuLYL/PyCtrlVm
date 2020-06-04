# -*- coding: UTF-8 -*-
import ssl
import paramiko
import sys, re, getpass, argparse, subprocess
from time import sleep
from pysphere import MORTypes, VIServer, VITask, VIProperty, VIMor, VIException
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


	def print_verbose(self,message):
		print message

	#连接ESXI
	def connect_server(self,host,user,passwd):
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
			print "Connect error!!!"
			return False
		return True
	#断开连接
	def disconnect_server(self):
		try:
			self.server.disconnect()
		except:
			print "error!!"
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
			print ">>>"+cmd
			# print stdout.read().decode()
			print 'done'
			
			return True
		except:
			return False
	#克隆 通过SSH执行CMD复制服务器上的虚拟机文件 指定模板虚拟机所在文件夹名称 和 克隆虚拟机文件夹名称
	def vm_clone(self,template,vm_name):# 默认 datastore1
		try:
			self.command_server("cp -r /vmfs/volumes/datastore1/"+template+"/ "+"/vmfs/volumes/datastore1/"+vm_name+"/")
			return True
		except:
			return False

	#当前所有虚拟机list
	def get_vm_list(self):
		try:
			return self.server.get_registered_vms()
		except:
			print "Failure!!!"
			return False
	
	''' 
	#获取数据存储list
	def get_datastores(self):
		pass
	#获取所有资源池
	def find_resource_pool(self):
		rps = self.server.get_resource_pools()
		ans = []
		for mor, path in rps.iteritems():
			self.print_verbose('Parsing RP %s' % path)
			#if re.match('.*%s' % name,path):
			ans.append(mor)
		return mor
	#获取所有文件夹
	def find_folder(self):
		folders = self.server._get_managed_objects(MORTypes.Folder)
		ans = []
		try:
			for mor, folder_name in folders.iteritems():
				self.print_verbose('Parsing folder %s' % folder_name)
				#if folder_name == name:
				ans.append(mor)
			return ans
		except IndexError:
			return None
		return None
	'''

	#获取指定名称的虚拟机实例
	def get_vm_by_name(self,vm_name):
		try:
			self.vm = self.server.get_vm_by_name(vm_name)
			self.vm_name = vm_name
		except:
			print "Get vm error!"
			return False
		return self.vm
	#获取该虚拟机的状态
	def vm_get_status(self):
		try:
			print self.vm.get_status()
		except:
			print "Failure!!!"
			return False
		return True


	'''改变虚拟机电源状态'''
    #开机
	def vm_power_on(self):
		try:
			if(self.vm.is_powered_off()):
				self.vm.power_on();
			else:
				print "vm "+vm_name+" is already power on!!!"
		except:
			print "Failure!!!"
			return False
		return True
    #关机
	def vm_power_off(self):
		try:
			if(self.vm.is_powered_on()):
				self.vm.power_off();
			else:
				print "vm "+vm_name+" is already power off!!!"
		except:
			print "Failure!!!"
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
 







