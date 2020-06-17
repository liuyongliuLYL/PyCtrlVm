# -*- coding: UTF-8 -*-
# 虚拟机配置信息
conf = dict()
conf = {
    'vm1': {
        'cup_num' : 2,
        'memory' : 2048,

        'vm_ip' : '192.168.1.179', 
        'vm_subnetmask' : '255.255.255.0', 
        'vm_gateway' : '192.168.1.1', 
        'vm_dns' : '114.114.114.114', 
        'vm_domain' : 'localhost',
        'vm_hostname' : 'ubuntu16-1'  #不支持下划线
    }
}
