import os
import boto3
import json
from botocore.exceptions import ClientError

"""Including sample event to prove functions can mutate the right parts of the message"""
def lambda_handler(event, context, env_dev, env_uat, env_liveeu):
    event = {
    "account": "803700595459",
    "detailType": "CodePipeline Stage Execution State Change",
    "region": "eu-west-1",
    "source": "aws.codepipeline",
    "time": "2020-04-02T15:13:44Z",
    "notificationRuleArn": "arn:aws:codestar-notifications:eu-west-1:803700595459:notificationrule/eac314920eebe4dd54e45a5675caa24eab8b3a95",
    "detail": {
        "pipeline": "AnsiblePipeline",
        "execution-id": "18fba762-fce1-4d6e-898f-e0e2e9e6ef4c",
        "state": "STARTED",
        "stage": "DeployDEV",
        "version": 7
    },
    "resources": [
        "arn:aws:codepipeline:eu-west-1:803700595459:AnsiblePipeline"
    ],
    "additionalAttributes": {
        "sourceActions": [
            {
                "sourceActionName": "Source",
                "sourceActionProvider": "CodeCommit",
                "sourceActionVariables": {
                    "BranchName": "master",
                    "CommitId": "d17ef562e6dc06e8322632a59524b44b5aa3dbf7",
                    "RepositoryName": "Core_API_Proxy"
                }
            }
        ]
    }
}
    # env_dev = 'dev'
    # env_uat = 'uat'
    # env_liveeu = 'liveEU'
    # message_dict = {}
    # results = json.loads(message)
    # message_dict = results
    # #print(message_dict.values())
    # #['0', 'dd93259d-579f-43c4-9cb2-6021293efce7', 'CodePipeline Pipeline Execution State Change', 'aws.codepipeline', '803700595459', '2020-03-30T15:29:56Z', 'eu-west-1', ['arn:aws:codepipeline:eu-west-1:803700595459:AnsiblePipeline'], {'pipeline': 'AnsiblePipeline', 'execution-id': '20567b42-c2ef-4a39-9e87-3e69f7ce5199', 'state': 'STARTED', 'version': 7.0}]
    # #print(message_dict['detail'])
    # pipe_details = (message_dict['detail'])
    # #print(pipe_details)
    # #{'pipeline': 'AnsiblePipeline', 'execution-id': '20567b42-c2ef-4a39-9e87-3e69f7ce5199', 'state': 'STARTED', 'version': 7.0}

    stated = event['detail']['state']
    staged = event['detail']['stage']    
    #message = event['Records'][0]['Sns']['Message']
    # print(stated)
    # print(staged) 
    states = ['STARTED','SUCCEEDED','FAILED']
    stages = ['DeployDEV','DeployUAT','DeployLiveEU']
    if stated in states:
        if staged in stages:
            if 'DeployDEV' == staged:
                staged = env_dev
            elif 'DeployUAT' == staged:
                staged = env_uat
            else:
                staged = env_liveeu
            print(stated)
            print(staged)
            alert_subject = f"HAProxy pipeline deployed in {staged} has {stated}"
            alert_message = f"The Core API HAProxy pipeline has {stated} deployment in {staged}"
            print(alert_subject)
            print(alert_message)
            # alert_message = message
            # send_sns_alert(subject=alert_subject,message=alert_message)
lambda_handler('event', '0', 'DEV', 'UAT', 'Live EU')
    # print(message_dict[key])
    # status_detail = ['STARTED', 'SUCCEEDED', 'FAILED']

#     Parse message string and process into a dictionary for ease of use.
#     Turns each line into a key value pair and stores them in a dictionary.
# for part in message_parts:
#     splitparts = part.split('=')
#         # Removes quotes and double quotes.
#     key = splitparts[0].strip('\"\'')
#     value = splitparts[1].strip('\"\'')
#     message_dict[key] = value
# print(message_dict)

    # if message_dict['status'] in status_detail:
    #     print('status')
        # Alert needs to be raised.
        # Example: 'StackName: DELETE_FAILED'
    #     alert_subject = '{}: {}'.format(message_dict['StackName'],
    #                                     message_dict['ResourceStatus'])
    #     alert_message = message
    #     send_sns_alert(subject=alert_subject,message=alert_message)
    # elif message_dict['ResourceStatus'] in OKSTATUS:
    #     print(message_dict['StackName'],message_dict['ResourceType'],message_dict['ResourceStatus'])

