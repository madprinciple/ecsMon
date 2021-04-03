import boto3
ecs = boto3.client('ecs')
cInstances=ecs.list_container_instances(
    cluster='Blu-UAT-Mercury'
)
iarns=cInstances['containerInstanceArns']
for i in iarns:
    print(i)
    cDetails = ecs.describe_container_instances(
        cluster='Blu-UAT-Mercury',
        containerInstances=[i]
    )
    #print(cDetails)
    print("Instance ID:", cDetails['containerInstances'][0]['ec2InstanceId'])
    print("Status:", cDetails['containerInstances'][0]['status'])
    print("Running Tasks Count:", cDetails['containerInstances'][0]['runningTasksCount'])
    print("Pending Tasks Count:", cDetails['containerInstances'][0]['pendingTasksCount'])
    print()
    print("ResourceType: ",cDetails['containerInstances'][0]['remainingResources'][0]['name'])
    remainingCpu=cDetails['containerInstances'][0]['remainingResources'][0]['integerValue']
    totalCpu=cDetails['containerInstances'][0]['registeredResources'][0]['integerValue']
    usage=(totalCpu-remainingCpu)*100/totalCpu
    print('Remaining Cpu: ', remainingCpu)
    print('Total Cpu: ', totalCpu)
    print('CPU Usage: ',str(usage)+'%')

    print()
    print("ResourceType: ",cDetails['containerInstances'][0]['remainingResources'][1]['name'])
    remainingMem=cDetails['containerInstances'][0]['remainingResources'][1]['integerValue']
    totalMem=cDetails['containerInstances'][0]['registeredResources'][1]['integerValue']
    usage=(totalMem-remainingMem)*100/totalMem
    print('Remaining Mem: ', remainingMem)
    print('Total Mem: ', totalMem)
    print('Mem Usage: ',str(usage)+'%')
