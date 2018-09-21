#!/bin/bash
#用来生成yaml文件
echo apiVersion: apps/v1beta1
echo kind: Deployment
echo metadata:
echo   name: $1
echo   namespace: $2
echo   labels:
echo     app: $1
echo spec:
echo  replicas: $3
echo   selector:
echo     matchLabels:
echo       app: $1
echo   template:
echo     metadata:
echo       labels:
echo         app: $1
echo     spec:
echo       containers:
echo       - name: $1
echo         image: $4
echo         resources:
echo           limits:
echo             cpu: $5
echo             memory: $6
echo           requests:
echo             cpu: $5
echo             memory: $6
echo         ports:
echo         - containerPort: $8
echo           protocol: TCP
echo ---
echo apiVersion: v1
echo kind: Service
echo metadata:
echo   name: $1
echo   namespace: $2
echo   labels:
echo     app: $1
echo spec:
echo   selector:
echo     app: $1
echo   ports:
echo   - port: $7
echo     targetPort: $8
