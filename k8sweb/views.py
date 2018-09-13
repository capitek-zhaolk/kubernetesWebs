#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.shortcuts import render
import time
# Create your views here.

import requests
import json
import traceback
from django.shortcuts import render_to_response, render
from kubernetesWebs.settings import REGISTERY_IP_ADDR, REGISTERY_IP_ADDR_PORT

USER_LISTS = {
    "Kubernetes" : {'name':'Kubernetes', 'b':u'已部署', 'y':u'运行', 'times':time.time},
    "admin" : {'name': "admin", 'b':u'已部署', 'y':u'运行', 'times':time.time},
}


# Docker私有仓库服务器
repo_ip = REGISTERY_IP_ADDR
repo_port = REGISTERY_IP_ADDR_PORT

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
    return render(request, 'services.html')

def application(request):
    imageNames = getImagesName(repo_ip, repo_port)
    return render(request, 'application.html', {'list':USER_LISTS, 'imageNames':imageNames})

def colony(request):
    return render(request, 'colony.html')

def detail(request):
    namespace = request.GET.get('namespace')
    detail_info = USER_LISTS[namespace]
    return render(request, 'application-lists.html', {'detail_info': detail_info})