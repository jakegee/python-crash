import boto3
import json
import base64
import subprocess
import time
import datetime
TODAY = datetime.datetime.now().strftime("%Y-%m-%d")
def lambda_handler(event, context):
    main()
def configureClient(resource):
    client = boto3.client(resource)
    return client
def cloudformationTrigger(client, name, scriptKey, s3Url, diskSize, emailAddress):
    name = 'daily-' + TODAY + '-' + name
    client.create_stack(
        StackName=name,
        TemplateURL='https://s3-eu-west-1.amazonaws.com/argus-cloudformation-templates-eu/datascience/rServerStack.yml',
        Parameters=[
            {
                'ParameterKey': 'JobName',
                'ParameterValue': name
            },
            {
                'ParameterKey':'scriptKey',
                'ParameterValue': scriptKey
            },
            {
                'ParameterKey': 's3Url',
                'ParameterValue': s3Url
            },
            {
                'ParameterKey': 'diskSize',
                'ParameterValue': diskSize
            },
            {
                'ParameterKey': 'emailAddress',
                'ParameterValue': emailAddress
            }
        ],
        TimeoutInMinutes=5,
        OnFailure='DELETE',
        Tags=[
            {
                'Key': 'Name',
                'Value': name + ' stack'
            }
        ]
    )
def readJson(cloudformationClient):
    s3 = boto3.client('s3')
    jobs = s3.get_object(
        Bucket='am-data-science',
        Key='TestSchedule/testJobs.json'
    )
    data = json.load(jobs['Body'])
    currenttime = datetime.datetime.now()
    print(currenttime)
    dow = int(currenttime.strftime('%w'))
    hour = int(currenttime.strftime('%H'))
    dom = int(currenttime.strftime('%d'))
    minute = int(currenttime.strftime('%M')) # minute as zero padded decimal
    print('weekday:{}, hour:{}, day:{}, minute:{}'.format(str(dow), str(hour), str(dom), str(minute)))
    for job in data:
        if  data[job]['schedule']['scheduleType'] == 'Daily':
            for day in data[job]['schedule']['Days']:
                if day == dow:
                    if data[job]['schedule']['Hour'] == hour and int(data[job]['schedule']['Minute']) == minute:
                        print(data[job]['scriptName'])
                        #cloudformationTrigger(cloudformationClient, data[job]['scriptName'], data[job]['scriptKey'], data[job]['s3Url'], data[job]['diskSize'], data[job]['emailAddress'])
        elif data[job]['schedule']['scheduleType'] == 'Monthly' and data[job]['schedule']['Day'] == dom and data[job]['schedule']['Hour'] == hour and int(data[job]['schedule']['Minute']) == minute:
            print(data[job]['scriptName'])
            #cloudformationTrigger(cloudformationClient, data[job]['scriptName'], data[job]['scriptKey'], data[job]['s3Url'], data[job]['diskSize'], data[job]['emailAddress'])
        time.sleep(3)
def main():
    cloudformationClient = configureClient('cloudformation')
    readJson(cloudformationClient)
