import _thread
import time
from tkinter import *
from tkinter import messagebox
from tkinter.simpledialog import askinteger

from tkinter import *
sys.path.append("API")
from Vcenter import Vcenter
from pyVmomi import vim
from pyVmomi import vmodl
# from tools import tasks
from pyVim.connect import SmartConnect, SmartConnectNoSSL, Disconnect
import atexit
import argparse
import getpass
import traceback
from os import system, path


class GUI:
    def __init__(self):
        # 初始化Tk()
        self.myWindow = Tk()
        # 设置标题
        self.myWindow.title("虚拟中心管理系统")
        # 设置窗口大小
        self.width = 800
        self.height = 650
        # 获取屏幕尺寸以计算布局参数，使窗口居于屏幕中央
        self.screenwidth = self.myWindow.winfo_screenwidth()
        self.screenheight = self.myWindow.winfo_screenheight()
        self.alignstr = '%dx%d+%d+%d' % (
            self.width, self.height, (self.screenwidth - self.width) / 2, (self.screenheight - self.height) / 2)
        self.myWindow.geometry(self.alignstr)
        # 设置窗口是否可变长、宽，True:可变 False:不可变
        self.myWindow.resizable(width=True, height=True)

        host = "192.168.1.233"
        user = "administrator@vsphere.local"
        pwd = "Cloud$2020"
        port = 443
        self.P = Vcenter(host, user, pwd, 443)

        # 包含所有的标签
        self.all_labels()
        # 所有esxi列表
        self.esxi_list()
        # 所有VM的列表
        self.all_vm_list()
        # ESXI/VM的详细信息
        self.detail_info_list()
        # 交互反馈
        self.feedback()
        # 包含所有的按钮
        self.all_buttons()

        # 进入消息循环
        self.myWindow.mainloop()

    # 包含所有的标签
    def all_labels(self):
        self.l1 = Label(self.myWindow, text="ESXI列表", width=20, justify="center")
        self.l1.grid(row=0, column=0)

        self.l2 = Label(self.myWindow, text="VM列表", width=20, justify="center")
        self.l2.grid(row=0, column=1)

        self.l3 = Label(self.myWindow, text="esxi/vm详细信息", width=20, justify="center")
        self.l3.grid(row=0, column=2)

        self.l4 = Label(self.myWindow, text="交互反馈", width=20, justify="center")
        self.l4.grid(row=3, column=0, columnspan='3')

    # 包含所有的按钮
    def all_buttons(self):
        # 虚拟机有关操作
        self.b1 = Button(self.myWindow, text='批量部署虚拟机', relief='raised', font=('Helvetica 10 bold'), width=20, height=2,
                         command=self.deploy)
        self.b1.grid(row=6, column=0, sticky=W, padx=5, pady=5)

        self.b2 = Button(self.myWindow, text='删除虚拟机', font=('Helvetica 10 bold'), width=20, height=2,
                         command=self.delete_vm)
        self.b2.grid(row=7, column=0, sticky=W, padx=5, pady=5)

        self.b3 = Button(self.myWindow, text='虚拟机开机', relief='raised', font=('Helvetica 10 bold'), width=20, height=2,
                         command=self.poweron)
        self.b3.grid(row=6, column=2, sticky=W, padx=5, pady=5)

        self.b4 = Button(self.myWindow, text='虚拟机关机', relief='raised', font=('Helvetica 10 bold'), width=20, height=2,
                         command=self.poweroff)
        self.b4.grid(row=7, column=2, sticky=W, padx=5, pady=5)

        self.b5 = Button(self.myWindow, text='虚拟机重启', relief='raised', font=('Helvetica 10 bold'), width=20, height=2,
                         command=self.reboot)
        self.b5.grid(row=6, column=1, sticky=W, padx=5, pady=5)

        self.b6 = Button(self.myWindow, text='虚拟机的详细信息', relief='raised', font=('Helvetica 10 bold'), width=20,
                         height=2, command=self.vm_information)
        self.b6.grid(row=7, column=1, sticky=W, padx=5, pady=5)

        # ESXI有关操作
        self.b7 = Button(self.myWindow, text='关闭ESXI', relief='raised', font=('Helvetica 10 bold'), width=20, height=2,
                         command=self.shutdown)
        self.b7.grid(row=8, column=0, sticky=W, padx=5, pady=5)

        # 刷新操作
        self.b8 = Button(self.myWindow, text='刷新列表', relief='raised', font=('Helvetica 10 bold'), width=20, height=2,
                         command=self.refresh)
        self.b8.grid(row=8, column=2, sticky=W, padx=5, pady=5)

        # esxi服务器详细信息操作
        self.b9 = Button(self.myWindow, text='ESXI的详细信息', relief='raised', font=('Helvetica 10 bold'), width=20,
                         height=2, command=self.vmm_information)
        self.b9.grid(row=8, column=1, sticky=W, padx=5, pady=5)

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
    def detail_info_list(self):
        self.vms_info = Listbox(self.myWindow, width="60")
        self.vms_info.grid(row=1, column=2, sticky="N")
        self.vm_list = self.P.get_all_vm_list()

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

    # 交互反馈
    def feedback(self):
        self.feedback_listbox = Listbox(self.myWindow, width=110)
        self.feedback_listbox.grid(row=4, column=0, sticky=N, columnspan=3)

        scr7 = Scrollbar(self.myWindow, orient='vertical')
        self.feedback_listbox.configure(yscrollcommand=scr7.set)
        scr7['command'] = self.feedback_listbox.yview
        scr7.grid(row=4, column=0, sticky="E" + "N" + "S", columnspan=3)

        src8 = Scrollbar(self.myWindow, orient="horizontal")
        self.feedback_listbox.configure(xscrollcommand=src8.set)
        src8["command"] = self.feedback_listbox.xview
        src8.grid(row=5, column=0, sticky="S" + "E" + "W", columnspan=3)

    # 对部署虚拟机的进度，进行反馈
    def write_in_list(self, task, get_name, get_ip):
        self.feedback_listbox.insert(END, '正在配置ip为：' + get_ip + '，hostname为' + get_name + '的主机...')
        while 1:
            if self.P.wait_for_task(task) == "success":
                self.feedback_listbox.insert(END, '配置ip为：' + get_ip + '，hostname为' + get_name + '的主机成功')
                break
            if self.P.wait_for_task(task) == "error":
                self.feedback_listbox.insert(END, '配置ip为：' + get_ip + '，hostname为' + get_name + '的主机失败')
                break
            time.sleep(5)

    # 批量部署虚拟机
    def deploy(self):
        info = self.P.get_esxi_info()  # 获取所有vm信息
        if info == FALSE:
            self.feedback_listbox.insert(END, '信息获取失败，可能有虚拟机正在创建或删除')
            return

        vmm_list = self.P.get_obj([vim.HostSystem], None)  # 获取两个esxi
        value = self.vm_lb.get(self.vm_lb.curselection())  # 获得选中的vm名称
        for vmm in vmm_list:
            if value in info[vmm.name]["vm"].keys():
                if info[vmm.name]["vm"][value]["电源状态"] != 'poweredOff':
                    self.feedback_listbox.insert(END, '克隆失败，虚拟机' + vmm.name + '处于未关机状态')
                    return



        total_num = askinteger('部署虚拟机', "需要部署的虚拟机数量：")

        while total_num > 0:
            # 因为当前只有两个esxi，所以平均分配到每个esxi
            if total_num % 2 == 0:
                get_datastore = 'datastore1'
            else:
                get_datastore = 'datastore3'

            get_name = value + '-' + str(total_num)
            get_ip = '192.168.1.' + str(130 + total_num)

            # 往字典中加入新的虚拟机的配置
            conf = {}
            conf[get_name] = {
                'cup_num': 2,
                'memory': 2048,

                'vm_ip': get_ip,
                'vm_subnetmask': '255.255.255.0',
                'vm_gateway': '192.168.1.1',
                'vm_dns': '114.114.114.114',
                'vm_domain': 'localhost',
                'vm_hostname': get_name,
            }

            # 根据模板，并且读取保存在本地的新的虚拟机的配置信息，进行虚拟机的（克隆）部署

            template = self.P.get_obj([vim.VirtualMachine], value)


            task = self.P.clone_vm(template=template, vm_name=get_name,
                                   datacenter_name='Datacenter1', vm_folder="demo1",
                                   datastore_name=get_datastore, cluster_name='cluster1',
                                   resource_pool=None,
                                   power_on=True,
                                   datastorecluster_name='None',
                                   vm_conf=conf[get_name])
            if str(task)=="False":
                self.feedback_listbox.insert(END, '克隆失败，被克隆的虚拟机处于未关机状态')
                return

            _thread.start_new_thread(self.write_in_list, (task, get_name, get_ip,))

            total_num -= 1

    # 按钮事件：显示 ESXI/VM的详细信息
    def vm_information(self):
        info = self.P.get_esxi_info()  # 获取所有vm信息
        if info == FALSE:
            self.feedback_listbox.insert(END, '信息获取失败，可能有虚拟机正在创建或删除')
            return

        vmm_list = self.P.get_obj([vim.HostSystem], None)  # 获取两个esxi
        # print(vmm_list)
        self.vms_info.delete(0, END)  # 删除列表的内容
        value = self.vm_lb.get(self.vm_lb.curselection())  # 获得选中的vm名称
        for vmm in vmm_list:
            if value in info[vmm.name]["vm"].keys():
                self.vms_info.insert(END, value)
                self.vms_info.insert(END, "")

                self.vms_info.insert(END, "电源状态：" + info[vmm.name]["vm"][value]["电源状态"])
                # self.vms_info.insert(END,info[vmm.name]["vm"][value]["电源状态"])
                self.vms_info.insert(END, "")

                self.vms_info.insert(END, "内存(总数MB)：" + str(info[vmm.name]["vm"][value]['内存(总数MB)']))
                # self.vms_info.insert(END,info[vmm.name]["vm"][value]['内存(总数MB)'])
                self.vms_info.insert(END, "")

                self.vms_info.insert(END, "系统信息：" + info[vmm.name]["vm"][value]['系统信息'])
                # self.vms_info.insert(END,info[vmm.name]["vm"][value]['系统信息'])
                self.vms_info.insert(END, "")

                self.vms_info.insert(END, "IP：" + info[vmm.name]["vm"][value]['IP'])
                # self.vms_info.insert(END,info[vmm.name]["vm"][value]['IP'])
                self.vms_info.insert(END, "")

                self.vms_info.insert(END, "Hard disk 1：" + info[vmm.name]["vm"][value]['Hard disk 1'])
                # self.vms_info.insert(END,info[vmm.name]["vm"][value]['Hard disk 1'])
        self.feedback_listbox.insert(END, '信息获取完毕')
        # for vmm in vmm_list:
        #     for item in info[vmm.name]["vm"].items():
        #         self.vms_info.insert(END,item[0])
        #         self.vms_info.insert(END,"电源状态：")
        #         self.vms_info.insert(END,item[1]['电源状态'])
        # self.vms_info.insert(END, item[1]['CPU(内核总数)'])
        # self.vms_info.insert(END, "内存(总数MB)")
        # self.vms_info.insert(END, item[1]['内存(总数MB)'])
        # self.vms_info.insert(END, "系统信息")
        # self.vms_info.insert(END, item[1]['系统信息'])
        # self.vms_info.insert(END, "IP")
        # self.vms_info.insert(END, item[1]['IP'])
        # self.vms_info.insert(END, "Hard disk 1")
        # self.vms_info.insert(END, item[1]['Hard disk 1'])
        # self.vms_info.insert(END,"")
        # self.vms_info.insert(END,"")

    # 获得选中的esxi的所有信息
    def vmm_information(self):
        info = self.P.get_esxi_info()  # 获取所有vm信息
        if info == FALSE:
            self.feedback_listbox.insert(END, '信息获取失败，可能有虚拟机正在创建或删除')
            return

        self.vms_info.delete(0, END)  # 删除列表的内容
        value = self.vmm_lb.get(self.vmm_lb.curselection())  # 获得选中的vmm名称

        self.vms_info.insert(END, value)
        self.vms_info.insert(END, "")

        self.vms_info.insert(END, "厂商：" + info[value]["esxi_info"]["厂商"])
        self.vms_info.insert(END, "")

        self.vms_info.insert(END, "型号：" + info[value]["esxi_info"]["型号"])
        self.vms_info.insert(END, "")

        self.vms_info.insert(END, "SN：" + info[value]["esxi_info"]["SN"])
        self.vms_info.insert(END, "")

        self.vms_info.insert(END, "处理器：" + info[value]["esxi_info"]["处理器"])
        self.vms_info.insert(END, "")

        self.vms_info.insert(END, "处理器使用率：" + info[value]["esxi_info"]["处理器使用率"])
        self.vms_info.insert(END, "")

        self.vms_info.insert(END, "内存(MB)：" + str(info[value]["esxi_info"]["内存(MB)"]))
        self.vms_info.insert(END, "")

        self.vms_info.insert(END, "可用内存(MB)：" + info[value]["esxi_info"]["可用内存(MB)"])
        self.vms_info.insert(END, "")

        self.vms_info.insert(END, "内存使用率：" + info[value]["esxi_info"]["内存使用率"])
        self.vms_info.insert(END, "")

        self.vms_info.insert(END, "系统：" + info[value]["esxi_info"]["系统"])
        self.vms_info.insert(END, "")

        self.feedback_listbox.insert(END, 'esxi' + value + '信息获取完毕')

    # 刷新esxi和vm的列表框
    def refresh(self):
        self.esxi_list()
        self.all_vm_list()
        self.feedback_listbox.insert(END, '列表刷新完毕')

    def poweron(self):
        test = self.vm_lb.curselection()  # 返回一个元组
        for tup in test:
            value = self.vm_lb.get(tup)
            vm = self.P.get_obj([vim.VirtualMachine], value)
            self.P.vm_poweron(vm)
            self.feedback_listbox.insert(END, '虚拟机' + vm.name + '已开机')

    def poweroff(self):
        test = self.vm_lb.curselection()  # 返回一个元组
        for tup in test:
            value = self.vm_lb.get(tup)
            vm = self.P.get_obj([vim.VirtualMachine], value)
            self.P.vm_poweroff(vm)
            self.feedback_listbox.insert(END, '虚拟机' + vm.name + '已关闭')

    def delete_vm(self):
        test = self.vm_lb.curselection()  # 返回一个元组
        for tup in test:
            value = self.vm_lb.get(tup)
            vm = self.P.get_obj([vim.VirtualMachine], value)
            self.P.delete_vm(vm)
            self.feedback_listbox.insert(END, '虚拟机' + vm.name + '已删除')

    def reboot(self):
        test = self.vm_lb.curselection()  # 返回一个元组
        for tup in test:
            value = self.vm_lb.get(tup)
            vm = self.P.get_obj([vim.VirtualMachine], value)
            self.P.vm_reboot(vm)
            self.feedback_listbox.insert(END, '虚拟机' + vm.name + '已重启')

    def shutdown(self):
        test = self.vmm_lb.curselection()  # 返回一个元组
        for tup in test:
            value = self.vmm_lb.get(tup)
            vm = self.P.get_obj([vim.VirtualMachine], value)
            self.P.ESXI_Shutdown(value)
            self.feedback_listbox.insert(END, 'ESXI' + value + '关闭完毕')


if __name__ == '__main__':
    GUI()
