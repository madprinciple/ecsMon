from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
import boto3
import urllib.request

# Create your views here.
from django.http import HttpResponse

hc_endpoint = 'https://console-sit2.blu.today'
hc_port = '443'
hc_path = '/1.0/health'


def index(request):
    SerDict={}
    ConInsDict={}
    #return HttpResponse("Hello, world. You're at the polls index.")

    ecs = boto3.client('ecs')
    serviceList = ecs.list_services(
    cluster='Blu-UAT-Mercury'
    )
    sarns=serviceList['serviceArns'] #sarns is a list
    for i in sarns:
        serDetails= ecs.describe_services(
            cluster='Blu-UAT-Mercury',
            services=[i]
        )
        serviceName=serDetails['services'][0]['serviceName']
        serviceStatus=serDetails['services'][0]['status']
        serviceDesiredCount=serDetails['services'][0]['desiredCount']
        serviceRunningCount=serDetails['services'][0]['runningCount']
        servicePendingCount=serDetails['services'][0]['pendingCount']
        event0_time=serDetails['services'][0]['events'][0]['createdAt']
        event0_message=serDetails['services'][0]['events'][0]['message']
        event1_time=serDetails['services'][0]['events'][1]['createdAt']
        event1_message=serDetails['services'][0]['events'][1]['message']
        event2_time=serDetails['services'][0]['events'][2]['createdAt']
        event2_message=serDetails['services'][0]['events'][2]['message']
        event3_time=serDetails['services'][0]['events'][3]['createdAt']
        event3_message=serDetails['services'][0]['events'][3]['message']
        hcUrl  = urllib.request.urlopen(hc_endpoint+":"+hc_port+hc_path)
        result=hcUrl.read()




        #SerDict[serviceName]={"serviceName" : serviceName, "serviceStatus" : serviceStatus, "serviceDesiredCount" :serviceDesiredCount, "serviceRunningCount" : serviceRunningCount, "servicePendingCount" : servicePendingCount}
        SerDict[serviceName]={  
                            "serviceName" : serviceName, 
                            "serviceStatus" : serviceStatus, 
                            "serviceDesiredCount" :serviceDesiredCount, 
                            "serviceRunningCount" : serviceRunningCount, 
                            "servicePendingCount" : servicePendingCount, 
                            "healthCheck" : result,
                            "events" : [
                                {"Event_Time" : event0_time, "Message" : event0_message },
                                {"Event_Time" : event1_time, "Message" : event1_message },
                                {"Event_Time" : event2_time, "Message" : event2_message },
                                {"Event_Time" : event3_time, "Message" : event3_message },
                            ] 
                        }


    #data={"services" : SerDict}

    cInstances=ecs.list_container_instances(
    cluster='Blu-UAT-Mercury'
    )
    iarns=cInstances['containerInstanceArns']
    for j in iarns:
        cDetails = ecs.describe_container_instances(
            cluster='Blu-UAT-Mercury',
            containerInstances=[j]
        )
        InstanceID=cDetails['containerInstances'][0]['ec2InstanceId']
        InstanceStatus=cDetails['containerInstances'][0]['status']
        RunningTasksCount=cDetails['containerInstances'][0]['runningTasksCount']
        PendingTasksCount=cDetails['containerInstances'][0]['pendingTasksCount']
        ResourceTypeCPU=cDetails['containerInstances'][0]['remainingResources'][0]['name']
        remainingCpu=cDetails['containerInstances'][0]['remainingResources'][0]['integerValue']
        totalCpu=cDetails['containerInstances'][0]['registeredResources'][0]['integerValue']
        CpuUsagePerc=(totalCpu-remainingCpu)*100/totalCpu
        ResourceTypeMem=cDetails['containerInstances'][0]['remainingResources'][1]['name']
        remainingMem=cDetails['containerInstances'][0]['remainingResources'][1]['integerValue']
        totalMem=cDetails['containerInstances'][0]['registeredResources'][1]['integerValue']
        MemUsagePerc=(totalMem-remainingMem)*100/totalMem

        ConInsDict[InstanceID]={
                                "InstanceID" : InstanceID,
                                "InstanceStatus" : InstanceStatus,
                                "RunningTasksCount" : RunningTasksCount,
                                "PendingTasksCount" : PendingTasksCount,
                                "Resources" : [
                                                    {"ResourceType" :ResourceTypeCPU, "remaining" : remainingCpu, "total" : totalCpu, "Usage" :CpuUsagePerc },
                                                    {"ResourceType" :ResourceTypeMem, "remaining" : remainingMem, "total" : totalMem, "Usage" :MemUsagePerc },
                                                ]   
                                }
    context = {
    "services" : SerDict,
    "cInstances" : ConInsDict
    }

    return render(request,'dashboard/index.html', context) 
