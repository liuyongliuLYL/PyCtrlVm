# -*- coding: UTF-8 -*-
from pyVmomi import vim
from pyVmomi import vmodl
#from tools import tasks
from pyVim.connect import SmartConnect, SmartConnectNoSSL, Disconnect
import atexit
import argparse
import getpass
from Vcenter import Vcenter
from conf import conf

host = "192.168.1.233"
user = "administrator@vsphere.local"
pwd = "Cloud$2020"
port = 433

P=Vcenter(host,user,pwd,443)

print(P.get_obj([vim.Datacenter],None))
print(P.get_obj([vim.Datastore],'datastore1 (1)'))
print(P.get_obj([vim.Folder],None))
print(P.get_obj([vim.VirtualMachine],None))
print(P.get_obj([vim.Datacenter],None)[0].vmFolder)
print(P.get_obj([vim.Folder],'new-folder'))

print(conf)

# 克隆成功，
''' ip配置失败!!! '''
template = P.get_obj([vim.VirtualMachine],'win7')
P.clone_vm(template=template,vm_name='win7-clone2',datacenter_name='Datacenter1',vm_folder=None,datastore_name='datastore1',cluster_name='cluster1',resource_pool=None,power_on=True,datastorecluster_name='None',
   vm_conf=conf['vm1'])

# 删除虚拟机 成功
#P.get_all_vm_list()
#vm = P.get_obj([vim.VirtualMachine],'new-clone1')
#P.vm_poweroff(vm)
#P.delete_vm(vm)
#P.get_all_vm_list()

# 关闭ESXI 成功
#P.ESXI_Shutdown('192.168.1.212')

# 获取虚拟机详细信息
#vm = P.get_obj([vim.VirtualMachine],'new-clone2')
#print(vm.summary.config)
#vm = P.get_obj([vim.VirtualMachine],'new-clone')
#print(vm.summary.config)


'''
(ManagedObject) [
   'vim.Datacenter:datacenter-2'
]
(ManagedObject) [
   'vim.Datastore:datastore-25',
   'vim.Datastore:datastore-19'
]
(ManagedObject) [
   'vim.Folder:group-v3',
   'vim.Folder:group-h4',
   'vim.Folder:group-s5',
   'vim.Folder:group-n6',
   'vim.Folder:group-v17'
]
(vim.vm.Summary.ConfigSummary) {
   dynamicType = <unset>,
   dynamicProperty = (vmodl.DynamicProperty) [],
   name = 'new-clone',
   template = false,
   vmPathName = '[datastore1] new-clone_1/new-clone.vmx',
   memorySizeMB = 1024,
   cpuReservation = 0,
   memoryReservation = 0,
   numCpu = 1,
   numEthernetCards = 1,
   numVirtualDisks = 1,
   uuid = '420626d8-5236-58da-479c-cc47348e36fd',
   instanceUuid = '500677f5-fedd-8095-7e88-6892933d14fa',
   guestId = 'ubuntu64Guest',
   guestFullName = 'Ubuntu Linux (64-bit)',
   annotation = '',
   product = <unset>,
   installBootRequired = false,
   ftInfo = <unset>,
   managedBy = <unset>,
   tpmPresent = false,
   numVmiopBackings = 0,
   hwVersion = <unset>
}
'''


