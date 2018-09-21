#!/usr/bin/env python
#-*- coding:utf-8 -*-

import time, sys
# Create your views here.

import requests
try:
    import simplejson as json
except:
    import json
import traceback
import paramiko, os
from django.shortcuts import render_to_response, render, HttpResponse, redirect
from kubernetesWebs.settings import REGISTERY_IP_ADDR, REGISTERY_IP_ADDR_PORT, K8SURL, K8SROOT, K8SPASSWORD, K8SREMOTEPATH, LOCALK8SREMOTEPATH

from django.http import JsonResponse, HttpResponseRedirect

from kubernetes import client, config

from django import forms

import subprocess

from createyaml.views import replaces

# Docker私有仓库服务器
repo_ip = REGISTERY_IP_ADDR
repo_port = REGISTERY_IP_ADDR_PORT


# 获取Pods
def getPodsList():
    config.load_kube_config()
    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    return ret

# 获取私有仓库的镜像名称和版本号
def getImagesName(repo_ip, repo_port):
    docker_dicts = {}
    try:
        url = "http://" + repo_ip + ":" + str(repo_port) + "/v2/_catalog"
        res = requests.get(url).content.strip()
        res_dict = json.loads(res)
        images_type = res_dict['repositories']

        for i in images_type:
            url2 = "http://" + repo_ip + ":" + str(repo_port) + "/v2/" + str(i) + "/tags/list"
            res2 = requests.get(url2).content.strip()
            res_dict2 = json.loads(res2)
            name = res_dict2['name']
            tags = res_dict2['tags']

            if tags not in [None]:
                for tag in tags:
                    key_ = name
                    tag_ = tag
                    docker_dicts[key_] = tag_

    except:
        docker_dicts["error"] = u"错误！没有找到相关信息，请检查镜像仓库服务器配置是否正确！"

    return docker_dicts

# 首页显示
def index(request):
    return render(request, 'index.html')

# 镜像列表页
def images(request):
    data = getImagesName(repo_ip, repo_port)
    return render(request, 'myImages.html', {'images_data':data})

def services(request):
    # res = getPodsList()
    # return render(request, 'services.html', {'res': res})
    return render(request, 'services.html')

def application(request):
    podslist = getPodsList()

    # print podslist

    return render(request, 'application.html', {'podslist': podslist})

def colony(request):
    return render(request, 'colony.html')

def detail(request):
    USER_LISTS = {}
    USER_LISTS_VALUE = {}

    podslist = getPodsList()

    namespace = request.GET.get('namespace')
    for k in podslist.items:
        k_name = k.metadata.name
        USER_LISTS_VALUE['k_name'] = k.metadata.name
        USER_LISTS_VALUE['start_time'] = k.status.start_time
        USER_LISTS_VALUE['run_status'] = k.status.phase

        USER_LISTS[k_name] = USER_LISTS_VALUE

    # print '数据是{0}'.format(USER_LISTS)

    detail_info = USER_LISTS[namespace]
    return render(request, 'application-lists.html', {'detail_info': detail_info})


# 点击创建Pods按钮，弹出创建层
# 数据数据并把数据写入到后台
def aa(request):
    imageNames = getImagesName(repo_ip, repo_port)
    return render(request, 'application-create.html', {'imageNames':imageNames})


def configure(request):
    imagesName = getImagesName(repo_ip, repo_port)
    return render(request, 'configure.html', {'imageNames':imagesName})

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def jsonConfigure(request):
    contexts = {}
    new_dicts = {}
    yaml_files = {}
    new_ = []

    global k_ , v_
    if request.method == 'POST':
        if request.is_ajax():
            batch = request.POST.get('batch')
            application_name = request.POST.get('application_name')
            radio_ = request.POST.getlist('radio_')
            create_num = request.POST.get('create_num')
            application_title = request.POST.get('application_title')
            service_port = request.POST.get('service_port')
            pods_port = request.POST.get('pods_port')

            # 镜像地址
            application_names = '{0}:5000/{1}'.format(REGISTERY_IP_ADDR, batch)
            for ins in range(len(radio_)):
                if ins == 0:
                    new_ = radio_[ins].split(' ')
            for ins in range(len(new_)):
                if ins == 0:
                    k_ = 'cpu'
                    v_ = new_[ins]
                    yaml_files[k_] = v_
                elif ins == 1:
                    k_ = 'memory'
                    v_ = new_[1]
                    yaml_files[k_] = v_

            context = { 'application_name': application_name, 'application_names': application_names, 'create_num': create_num, 'application_title': application_title, 'service_port': service_port, 'pods_port':pods_port}

            #包含所有数据的字典数据
            new_dicts = dict(context.items() + yaml_files.items())

            # 修改文件
            replaces(r'/kubernetesWebs/utils/create_yaml.yaml', new_dicts)

            contexts = {'mess': 'ok'}

            return HttpResponse(json.dumps(contexts), content_type="application/json")

    return render(request, 'configure.html')



# 假如 K8S集群跟 项目不再一个服务器
# 首先在K8S集群服务器获取相应的 ./kube/config 配置文件
















