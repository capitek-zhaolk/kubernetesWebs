#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.shortcuts import render

# Create your views here.

import subprocess, yaml, os, io

def replaces(file_path, new_str):
    list_ = []
    new_lists_ = []
    new_ = []
    global x1, x2

    new_str_ = loopDicts(new_str)

    try:
        # 复制的新文件
        file_pod= '{0}-pod.yaml'.format(new_str_['$1'])
        file_service= '{0}-service.yaml'.format(new_str_['$1'])

        yaml_path_pod = os.path.join('/opt/', file_pod)
        yaml_path_svc = os.path.join('/opt/', file_service)

        # 命令行
        command1 = 'cp -r /home/share/kubernetesWebs/utils/create_pod.yaml  {0}'.format(yaml_path_pod)
        command2 = 'cp -r /home/share/kubernetesWebs/utils/create_service.yaml  {0}'.format(yaml_path_svc)

        # 执行命令行 进行复制新的文件
        p1 = subprocess.Popen(command1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read()
        p2 = subprocess.Popen(command2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read()

        # 读取复制的service文件
        with open(yaml_path_svc, 'r') as f1:
            x1 = yaml.load(f1)

        # for data in x1:
        #     print '111试试数据{0}'.format(x1['spec']['ports'][0]['targetPort'])

        # 替换文件内容
        x1['spec']['ports'][0]['targetPort'] = int(new_str_['$8'].encode('utf-8'))
        x1['spec']['ports'][0]['port'] =  int(new_str_['$7'].encode('utf-8'))
        x1['spec']['selector']['app'] = new_str_['$1'].encode('utf-8')
        x1['metadata']['namespace'] = new_str_['$2'].encode('utf-8')
        x1['metadata']['name'] = new_str_['$1'].encode('utf-8')
        x1['metadata']['labels']['app'] = new_str_['$1'].encode('utf-8')


        with io.open(yaml_path_svc, 'w+') as outfile1:
            yaml.dump(x1, outfile1, default_flow_style=False, allow_unicode=True)


        # 读取复制的pod文件
        with open(yaml_path_pod, 'r') as f2:
            x2 = yaml.load(f2)

        x2['spec']['replicas'] = int(new_str_['$3'].encode('utf-8'))
        x2['spec']['template']['spec']['containers'][0]['image'] = new_str_['$4'].encode('utf-8')
        x2['spec']['template']['spec']['containers'][0]['name'] = new_str_['$1'].encode('utf-8')
        x2['spec']['template']['spec']['containers'][0]['resources']['requests']['cpu'] = new_str_['$5'].encode('utf-8')
        x2['spec']['template']['spec']['containers'][0]['resources']['requests']['memory'] = new_str_['$6'].encode('utf-8')
        x2['spec']['template']['spec']['containers'][0]['resources']['limits']['cpu'] = new_str_['$5'].encode('utf-8')
        x2['spec']['template']['spec']['containers'][0]['resources']['limits']['memory'] = new_str_['$6'].encode('utf-8')
        x2['spec']['template']['spec']['containers'][0]['ports'][0]['containerPort'] = int(new_str_['$8'].encode('utf-8'))
        x2['spec']['template']['metadata']['labels']['app'] = new_str_['$1'].encode('utf-8')
        x2['spec']['selector']['matchLabels']['app'] = new_str_['$1'].encode('utf-8')


        x2['metadata']['labels']['app'] = new_str_['$1'].encode('utf-8')
        x2['metadata']['name'] = new_str_['$1'].encode('utf-8')
        x2['metadata']['namespace'] = new_str_['$2'].encode('utf-8')

        # for data2 in x2:
        #     print '111试试数据{0}'.format(data2)

        with io.open(yaml_path_pod, 'w+') as outfile2:
            yaml.dump(x2, outfile2, default_flow_style=False, allow_unicode=True)

    except Exception as e:
        print e


# 替换传过来的字典类型数据
def loopDicts(dicts_):
    dicts = {}
    for k, v in dicts_.items():
        if k == 'service_port':
            k = '$7'
            dicts[k] = v
        elif k == 'application_title':
            k = '$2'
            dicts[k] = v
        elif k == 'memory':
            k = '$6'
            dicts[k] = v
        elif k == 'application_name':
            k = '$1'
            dicts[k] = v
        elif k == 'application_names':
            k = '$4'
            dicts[k] = v
        elif k == 'cpu':
            k = '$5'
            dicts[k] = v
        elif k == 'create_num':
            k = '$3'
            dicts[k] = v
        elif k == 'pods_port':
            k = '$8'
            dicts[k] = v
    return dicts


# 创建新的目录已保存文件
def createDir():
    pass