from tkinter import *
from tkinter import messagebox
from tkinter.simpledialog import askinteger

from tkinter import *
#from Vcenter import Vcenter
from pyVmomi import vim
from pyVmomi import vmodl
# from tools import tasks
from pyVim.connect import SmartConnect, SmartConnectNoSSL, Disconnect
import atexit
import argparse
import getpass
import traceback
from os import system, path

sys.path.append("API")
from Vcenter import Vcenter

class GUI():
    def __init__(self):
        host = "192.168.1.233"
        user = "administrator@vsphere.local"
        pwd = "Cloud$2020"
        port = 433
        self.P = Vcenter(host, user, pwd, 443)

        # 初始化Tk()
        self.myWindow = Tk()
        # 设置标题
        self.myWindow.title("虚拟中心管理系统")
        # 设置窗口大小
        self.width = 1000
        self.height = 600
        # 获取屏幕尺寸以计算布局参数，使窗口居于屏幕中央
        self.screenwidth = self.myWindow.winfo_screenwidth()
        self.screenheight = self.myWindow.winfo_screenheight()
        self.alignstr = '%dx%d+%d+%d' % (
            self.width, self.height, (self.screenwidth - self.width) / 2, (self.screenheight - self.height) / 2)
        self.myWindow.geometry(self.alignstr)
        # 设置窗口是否可变长、宽，True:可变 False:不可变
        self.myWindow.resizable(width=True, height=True)

        # 包含所有的标签
        self.all_labels()
        # esxi列表
        self.esxi_list()
        # 所有VM的主要信息
        self.all_vm_list()
        # 单个VM详细信息
        self.all_vm_general_info_list()
        # 所有VM列表(名字)
        self.vm_detail_info_list()
        # 包含所有的按钮
        self.all_buttons()

        self.xls_text = StringVar()
        self.xls = Entry(self.myWindow, textvariable=self.xls_text)

        # 进入消息循环
        self.myWindow.mainloop()

    # 包含所有的标签
    def all_labels(self):
        self.l1 = Label(self.myWindow, text="ESXI列表", width=20, justify="center")
        self.l1.grid(row=0, column=0)

        self.l2 = Label(self.myWindow, text="VM列表", width=20, justify="center")
        self.l2.grid(row=0, column=1)

        self.l3 = Label(self.myWindow, text="所有VM大致信息", width=20, justify="center")
        self.l3.grid(row=0, column=2)

        self.l4 = Label(self.myWindow, text="单个VM详细信息", width=20, justify="center")
        self.l4.grid(row=0, column=3)

    # 包含所有的按钮
    def all_buttons(self):
        # 虚拟机有关操作
        self.b1 = Button(self.myWindow, text='批量部署虚拟机', relief='raised', font=('Helvetica 10 bold'), width=20, height=2,
                         command=self.deploy)
        self.b1.grid(row=3, column=0, sticky=W, padx=5, pady=5)

        self.b2 = Button(self.myWindow, text='删除虚拟机', font=('Helvetica 10 bold'), width=20, height=2,
                         command=self.delete_vm)
        self.b2.grid(row=4, column=0, sticky=W, padx=5, pady=5)

        self.b3 = Button(self.myWindow, text='虚拟机开机', relief='raised', font=('Helvetica 10 bold'), width=20, height=2,
                         command=self.poweron)
        self.b3.grid(row=3, column=2, sticky=W, padx=5, pady=5)

        self.b4 = Button(self.myWindow, text='虚拟机关机', relief='raised', font=('Helvetica 10 bold'), width=20, height=2,
                         command=self.poweroff)
        self.b4.grid(row=4, column=2, sticky=W, padx=5, pady=5)

        self.b5 = Button(self.myWindow, text='虚拟机重启', relief='raised', font=('Helvetica 10 bold'), width=20, height=2,
                         command=self.reboot)
        self.b5.grid(row=3, column=1, sticky=W, padx=5, pady=5)

        self.b6 = Button(self.myWindow, text='虚拟机的详细信息', relief='raised', font=('Helvetica 10 bold'), width=20,
                         height=2)
        self.b6.grid(row=4, column=1, sticky=W, padx=5, pady=5)

        # ESXI有关操作
        self.b7 = Button(self.myWindow, text='关闭ESXI', relief='raised', font=('Helvetica 10 bold'), width=20, height=2,
                         command=self.shutdown)
        self.b7.grid(row=5, column=0, sticky=W, padx=5, pady=5)

    # esxi列表
    def esxi_list(self):
        # 列表框
        self.vmm_lb = Listbox(self.myWindow)
        self.vmm_lb.grid(row=1, column=0, sticky="N")
        self.vm_list = self.P.get_obj([vim.HostSystem], None)
        for esxi in self.vm_list:
            self.vmm_lb.insert(END, esxi.name)

        # 纵向滚动条
        scr1 = Scrollbar(self.myWindow, orient='vertical')
        self.vmm_lb.configure(yscrollcommand=scr1.set)
        scr1['command'] = self.vmm_lb.yview
        scr1.grid(row=1, column=0, sticky="E" + "N" + "S")
        # 横向滚动条
        src2 = Scrollbar(self.myWindow, orient="horizontal")
        self.vmm_lb.configure(xscrollcommand=src2.set)
        src2["command"] = self.vmm_lb.xview
        src2.grid(row=2, column=0, sticky="S" + "E" + "W")

    # 所有VM的主要信息
    def all_vm_general_info_list(self):
        self.vms_info = Listbox(self.myWindow, width="60")
        self.vms_info.grid(row=1, column=2, sticky="N")
        self.vm_list = self.P.get_all_vm_list()
        for vm in self.vm_list:
            self.vms_info.insert(END, self.P.get_obj([vim.VirtualMachine], vm.name).summary.config)

        scr3 = Scrollbar(self.myWindow, orient='vertical')
        self.vms_info.configure(yscrollcommand=scr3.set)
        scr3['command'] = self.vms_info.yview
        scr3.grid(row=1, column=2, sticky="E" + "N" + "S")

        src4 = Scrollbar(self.myWindow, orient="horizontal")
        self.vms_info.configure(xscrollcommand=src4.set)
        src4["command"] = self.vms_info.xview
        src4.grid(row=2, column=2, sticky="S" + "E" + "W")

    # 所有VM列表(名字),
    def all_vm_list(self):
        # selectmode='extended' ，列表框设置成可以多选，达到批量选中后进行操作的目的
        self.vm_lb = Listbox(self.myWindow, selectmode='extended')
        self.vm_lb.grid(row=1, column=1, sticky=N)
        self.vm_list = self.P.get_all_vm_list()
        for vm in self.vm_list:
            self.vm_lb.insert(END, vm)

        scr5 = Scrollbar(self.myWindow, orient='vertical')
        self.vm_lb.configure(yscrollcommand=scr5.set)
        scr5['command'] = self.vm_lb.yview
        scr5.grid(row=1, column=1, sticky="E" + "N" + "S")

        src6 = Scrollbar(self.myWindow, orient="horizontal")
        self.vm_lb.configure(xscrollcommand=src6.set)
        src6["command"] = self.vm_lb.xview
        src6.grid(row=2, column=1, sticky="S" + "E" + "W")

    # 单个VM详细信息
    def vm_detail_info_list(self):
        self.vm_info = Listbox(self.myWindow)
        self.vm_info.grid(row=1, column=3, sticky=N)

        scr7 = Scrollbar(self.myWindow, orient='vertical')
        self.vm_info.configure(yscrollcommand=scr7.set)
        scr7['command'] = self.vm_info.yview
        scr7.grid(row=1, column=3, sticky="E" + "N" + "S")

        src8 = Scrollbar(self.myWindow, orient="horizontal")
        self.vm_info.configure(xscrollcommand=src8.set)
        src8["command"] = self.vm_info.xview
        src8.grid(row=2, column=3, sticky="S" + "E" + "W")

    # 批量部署虚拟机
    def deploy(self):
        total_num = askinteger('部署虚拟机', "需要部署的虚拟机数量：")

        # read from local 。原始的本地存在模板机的信息
        f = open("D:\\conf.txt", 'r')
        conf = eval(f.read())
        f.close()

        while total_num > 0:
            # 因为当前只有两个esxi，所以平均分配到每个esxi
            if total_num % 2 == 0:
                get_datastore = 'datastore1'
            else:
                get_datastore = 'datastore3'
            get_name = 'ubuntu16_' + str(total_num)
            get_ip = '192.168.1.' + str(130 + total_num)

            # 往字典中加入新的虚拟机的配置
            conf[get_name] = {
                'cup_num': 2,
                'memory': 2048,

                'vm_ip': get_ip,
                'vm_subnetmask': '255.255.255.0',
                'vm_gateway': '192.168.1.1',
                'vm_dns': '114.114.114.114',
                'vm_domain': 'localhost',
                'vm_hostname': get_name,

                'datastore': get_datastore
            }
            # 根据模板，并且读取保存在本地的新的虚拟机的配置信息，进行虚拟机的（克隆）部署
            template = self.P.get_obj([vim.VirtualMachine], 'ubuntu_tem')
            self.P.clone_vm(template=template, vm_name=get_name,
                            datacenter_name='Datacenter1', vm_folder="demo1",
                            datastore_name=get_datastore, cluster_name='cluster1',
                            resource_pool=None,
                            power_on=True,
                            datastorecluster_name='None',
                            vm_conf=conf['ubuntu_tem'])

            total_num -= 1

        # save to local
        f = open("D:\\conf.txt", 'w')
        f.write(str(conf))
        f.close()

    def poweron(self):
        test = self.vm_lb.curselection()  # 返回一个元组
        for tup in test:
            value = self.vm_lb.get(tup)
            vm = self.P.get_obj([vim.VirtualMachine], value)
            self.P.vm_poweron(vm)

    def poweroff(self):
        test = self.vm_lb.curselection()  # 返回一个元组
        for tup in test:
            value = self.vm_lb.get(tup)
            vm = self.P.get_obj([vim.VirtualMachine], value)
            self.P.vm_poweroff(vm)

    def delete_vm(self):
        test = self.vm_lb.curselection()  # 返回一个元组
        for tup in test:
            value = self.vm_lb.get(tup)
            vm = self.P.get_obj([vim.VirtualMachine], value)
            self.P.delete_vm(vm)

    def reboot(self):
        test = self.vm_lb.curselection()  # 返回一个元组
        for tup in test:
            value = self.vm_lb.get(tup)
            vm = self.P.get_obj([vim.VirtualMachine], value)
            self.P.vm_reboot(vm)

    def shutdown(self):
        test = self.vmm_lb.curselection()  # 返回一个元组
        for tup in test:
            value = self.vmm_lb.get(tup)
            vm = self.P.get_obj([vim.VirtualMachine], value)
            self.P.ESXI_Shutdown(value)


if __name__ == '__main__':
    GUI()
