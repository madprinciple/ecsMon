import boto3
import urllib.request
serviceName='No Services Runnung'
SerDict={}


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
    print("Service Name: ",serviceName)
    print("Service Status: ",serviceStatus)
    print("Pending Count: ",servicePendingCount)
    print("Running Count: ",serviceRunningCount)
    print("Desired Count: ",serviceDesiredCount)
    event0_time=serDetails['services'][0]['events'][0]['createdAt']
    event0_message=serDetails['services'][0]['events'][0]['message']
    event1_time=serDetails['services'][0]['events'][1]['createdAt']
    event1_message=serDetails['services'][0]['events'][1]['message']
    event2_time=serDetails['services'][0]['events'][2]['createdAt']
    event2_message=serDetails['services'][0]['events'][2]['message']
    SerDict[serviceName]={  
                            "serviceName" : serviceName, 
                            "serviceStatus" : serviceStatus, 
                            "serviceDesiredCount" :serviceDesiredCount, 
                            "serviceRunningCount" : serviceRunningCount, 
                            "servicePendingCount" : servicePendingCount, 
                            "events" : [
                                {"Event0_Time" : event0_time, "Message0" : event0_message },
                                {"Event1_Time" : event1_time, "Message1" : event1_message },
                                {"Event2_Time" : event2_time, "Message2" : event2_message },
                            ] 
                        }

    event0_time=serDetails['services'][0]['events'][0]['createdAt']
    event0_message=serDetails['services'][0]['events'][0]['message']
    print(event0_time, " ",event0_message )
    print(event1_time, " ",event1_message )
    print(event2_time, " ",event2_message )

print("")    
#print(SerDict['mercury']['events'])
print(SerDict)

hc_endpoint = 'https://console-sit2.blu.today'
hc_port = '443'
hc_path = '/1.0/health'

hcUrl  = urllib.request.urlopen(hc_endpoint+":"+hc_port+hc_path)
result=hcUrl.read()
print (result)