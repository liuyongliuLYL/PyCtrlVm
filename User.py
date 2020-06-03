# -*- coding: UTF-8 -*-
import ssl
from pysphere import VIServer
import paramiko

class User():
	server_ip = ""
	user_name = ""
	password  = ""
	server    = ""

	vm = "" #当前虚拟机的实例
	vm_name = "" #当前虚拟机名称
	vm_os = ""
	#def __init__(self):
		
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
	#ESXI远程控制-SSH
	def command_server(self,cmd):
		# 建立一个sshclient对象
		ssh = paramiko.SSHClient()
		# 允许将信任的主机自动加入到host_allow 列表，此方法必须放在connect方法的前面
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		# 调用connect方法连接服务器
		# 需要管理员账号
		ssh.connect(hostname=self.server_ip, port=22, username=self.user_name, password=self.password)
		# 执行命令
		# command="poweroff"
		stdin, stdout, stderr = ssh.exec_command(cmd)
		# 结果放到stdout中，如果有错误将放到stderr中
		print stdout.read().decode()
		print 'ok'
		# 关闭连接
		ssh.close()

		return True



	#当前所有虚拟机list
	def get_vm_list(self):
		try:
			return self.server.get_registered_vms()
		except:
			print "Failure!!!"
			return False
	#获取数据存储list
	def get_datastores(self):
	    ret = []
	    for d in self.host_config.Datastore:
	        if d.Datastore.Accessible:
	            ret.append(d.Datastore.Name)
	    logger.debug("%s:found %s datastores", __name__, len(ret))
	    return ret


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



	''' 克隆虚拟机，ip配置 '''
	'''https://qiita.com/eli/items/f2438a45f06cf3813b9a'''
	def clone_vm(content, template, vm_name,
	             power_on=True,
	             vm_ip=None, vm_subnetmask=None, vm_gateway=None, vm_domain=None,
	             vm_hostname=None):
	    """
	    从模板/虚拟机来克隆虚拟机。
	    数据中心名称，目标虚拟机文件夹，数据存储名称，
	    集群名称，资源池，是否自动开机均为可选项
	    """
	    datacenter = get_obj(content, [vim.Datacenter], datacenter_name)
	 
	    relospec = vim.vm.RelocateSpec()
	    relospec.datastore = datastore
	    relospec.pool = resource_pool
	 
	    clonespec = vim.vm.CloneSpec()
	    clonespec.location = relospec
	    clonespec.powerOn = power_on
	    if all([vm_ip, vm_subnetmask, vm_gateway, vm_domain]):
	        clonespec.customization = get_customspec(vm_ip, vm_subnetmask, vm_gateway, vm_domain, vm_hostname)
	    elif any([vm_ip, vm_subnetmask, vm_gateway, vm_domain]):
	        raise CheckError('虚拟机的IP、子网掩码、网关、DNS域必须同时提供')
	 
	    print '开始克隆虚拟机'
	    task = template.Clone(folder=destfolder, name=vm_name, spec=clonespec)
	    wait_for_task(task)
	 
	 
	def get_customspec(vm_ip=None, vm_subnetmask=None, vm_gateway=None,
	                   vm_domain=None, vm_hostname=None):
	    # guest NIC settings
	    adaptermaps = []
	    guest_map = vim.vm.customization.AdapterMapping()
	    guest_map.adapter = vim.vm.customization.IPSettings()
	    guest_map.adapter.ip = vim.vm.customization.FixedIp()
	    guest_map.adapter.ip.ipAddress = vm_ip
	    guest_map.adapter.subnetMask = vm_subnetmask
	    guest_map.adapter.gateway = vm_gateway
	    guest_map.adapter.dnsDomain = vm_domain
	    adaptermaps.append(guest_map)
	 
	    # DNS settings
	    globalip = vim.vm.customization.GlobalIPSettings()
	    globalip.dnsServerList = [vm_gateway]
	    globalip.dnsSuffixList = vm_domain
	 
	    # Hostname settings
	    ident = vim.vm.customization.LinuxPrep()
	    ident.domain = vm_domain
	    ident.hostName = vim.vm.customization.FixedName()
	    if vm_hostname:
	        ident.hostName.name=vm_hostname
	        #ident.hostName.name = vm_hostname
	    customspec = vim.vm.customization.Specification()
	    customspec.nicSettingMap = adaptermaps
	    customspec.globalIPSettings = globalip
	    customspec.identity = ident
	    return customspec
 







