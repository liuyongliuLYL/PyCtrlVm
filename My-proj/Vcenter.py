# -*- coding: UTF-8 -*-
from pyVmomi import vim
from pyVmomi import vmodl
#from tools import tasks
from pyVim.connect import SmartConnect, SmartConnectNoSSL, Disconnect
import atexit
import argparse
import getpass
import traceback

# vcenter 虚拟机管理API
class Vcenter():
    si = "" #vcenter连接
    template = ""
    host = ""
    user = ""
    pwd = ""
    port = ""

    #连接Vcenter服务器
    def __init__(self,host,user,password,port):

        self.si = SmartConnectNoSSL(
            host=host,
            user=user,
            pwd=password,
            port=port)
        # disconnect this thing
        atexit.register(Disconnect, self.si)
        self.content = self.si.RetrieveContent()
    '''
    def wait_for_task(task):
        """ wait for a vCenter task to finish """
        task_done = False
        while not task_done:
            if task.info.state == 'success':
                return task.info.result

            if task.info.state == 'error':
                print("there was an error")
                task_done = True
    '''
    def get_obj(self, vimtype, name):
        """
        Return an object by name, 
        if name is None all found object is returned
        """
        obj = None
        container = self.content.viewManager.CreateContainerView(
            self.content.rootFolder, vimtype, True)
        if name == None:
            return container.view
        for c in container.view:
            if name:
                if c.name == name:
                    obj = c
                    break
            else:
                obj = c
                break

        return obj

    #关闭ESXI服务器, name是ESXI服务器的ip
    def ESXI_Shutdown(self,name):
        esxi_obj_all = self.get_obj([vim.HostSystem],None)
        for esxi in esxi_obj_all:
            if name == esxi.name:
                esxi.ShutdownHost_Task(True)
                return True
                break
        return False
        #print(esxi.name)
        #print(dir(esxi))
            

    # 获取所有虚拟机信息
    def get_all_vm_list(self):
        vm_list = self.get_obj([vim.VirtualMachine],None)
        for c in vm_list:
            print(c.name)

    def get_customspec(self, vm_ip=None, vm_subnetmask=None, vm_gateway=None, vm_dns=None,
                        vm_domain=None, vm_hostname=None):
        # guest NIC settings  有关dns和域名的配置错误 更改了
        adaptermaps = []
        guest_map = vim.vm.customization.AdapterMapping()
        guest_map.adapter = vim.vm.customization.IPSettings()
        guest_map.adapter.ip = vim.vm.customization.FixedIp()
        guest_map.adapter.ip.ipAddress = vm_ip
        guest_map.adapter.subnetMask = vm_subnetmask
        guest_map.adapter.gateway = vm_gateway
        if vm_domain:
            guest_map.adapter.dnsDomain = vm_domain
        adaptermaps.append(guest_map)
        
        # DNS settings
        globalip = vim.vm.customization.GlobalIPSettings()
        if vm_dns:
            globalip.dnsServerList = [vm_dns]
            globalip.dnsSuffixList = vm_domain
        
        # Hostname settings
        ident = vim.vm.customization.LinuxPrep()
        if vm_domain:
            ident.domain = vm_domain
        ident.hostName = vim.vm.customization.FixedName()
        if vm_hostname:
            ident.hostName.name = vm_hostname
        customspec = vim.vm.customization.Specification()
        customspec.nicSettingMap = adaptermaps
        customspec.globalIPSettings = globalip
        customspec.identity = ident
        return customspec
    #克隆虚拟机
    def clone_vm(self,
            template, vm_name,
            datacenter_name, vm_folder, datastore_name,
            cluster_name, resource_pool, power_on, datastorecluster_name,
            vm_conf):
        """
        Clone a VM from a template/VM, datacenter_name, vm_folder, datastore_name
        cluster_name, resource_pool, and power_on are all optional.
        """

        cup_num = vm_conf['cup_num']
        memory = vm_conf['memory']
        vm_ip = vm_conf['vm_ip'] 
        vm_subnetmask = vm_conf['vm_subnetmask']
        vm_gateway = vm_conf['vm_gateway']
        vm_dns = vm_conf['vm_dns']
        vm_domain = vm_conf['vm_domain']
        vm_hostname = vm_conf['vm_hostname']


        # 获取 数据中心 对象实例
        datacenter = self.get_obj([vim.Datacenter], datacenter_name)
        
        if vm_folder:
            destfolder = self.get_obj([vim.Folder], vm_folder)
        else:
            destfolder = datacenter.vmFolder
        
        if datastore_name:
            datastore = self.get_obj([vim.Datastore], datastore_name)
        else:
            datastore = self.get_obj(
                [vim.Datastore], template.datastore[0].info.name)

        # 集群
        cluster = self.get_obj([vim.ClusterComputeResource], cluster_name)

        if resource_pool:
            resource_pool = self.get_obj([vim.ResourcePool], resource_pool)
        else:
            resource_pool = cluster.resourcePool

        vmconf = vim.vm.ConfigSpec()
        '''
        if datastorecluster_name:
            podsel = vim.storageDrs.PodSelectionSpec()
            pod = get_obj(content, [vim.StoragePod], datastorecluster_name)
            podsel.storagePod = pod

            storagespec = vim.storageDrs.StoragePlacementSpec()
            storagespec.podSelectionSpec = podsel
            storagespec.type = 'create'
            storagespec.folder = destfolder
            storagespec.resourcePool = resource_pool
            storagespec.configSpec = vmconf

            try:
                rec = content.storageResourceManager.RecommendDatastores(
                    storageSpec=storagespec)
                rec_action = rec.recommendations[0].action[0]
                real_datastore_name = rec_action.destination.name
            except:
                real_datastore_name = template.datastore[0].info.name

            datastore = get_obj(content, [vim.Datastore], real_datastore_name)
        '''
        # set relospec
        relospec = vim.vm.RelocateSpec()
        relospec.datastore = datastore
        relospec.pool = resource_pool

        clonespec = vim.vm.CloneSpec()
        clonespec.location = relospec
        clonespec.powerOn = power_on

        # ip配置
        if all([vm_ip, vm_subnetmask, vm_gateway]):
            clonespec.customization = self.get_customspec(vm_ip, vm_subnetmask, vm_gateway, vm_domain, vm_dns, vm_hostname)
        vmconf = vim.vm.ConfigSpec()
        if cup_num:
            vmconf.numCPUs = cup_num
        if memory:
            vmconf.memoryMB = memory
        if vmconf is not None:
            clonespec.config = vmconf

        print("cloning VM...")
        task = template.Clone(folder=destfolder, name=vm_name, spec=clonespec)
        #wait_for_task(task)
    
    # 删除虚拟机  需要先关闭电源
    def delete_vm(self,vm):
        try:
            vm.Destroy_Task()
        except:
            return False
        return True
    
    # 虚拟机电源管理
    def vm_poweron(self,vm):
        try:
            vm.PowerOn()
        except:
            return False
        return True
    def vm_poweroff(self,vm):
        try:
            vm.PowerOff()
        except:
            return False
        return True
    def vm_reboot(self,vm):
        try:
            vm.ResetVM_Task()
        except:
            return False
        return True

