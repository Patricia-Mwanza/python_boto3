import boto3

sess = boto3.session.Session()
res = sess.resource('ec2')

#-------------------Create-VPC---------------------------

vpc = res.create_vpc(CidrBlock ='13.0.0.0/16')
vpc.create_tags(Tags = [
        {
            'Key': 'Name',
            'Value': 'hackers'
        },
    ])
vpc.wait_until_available()

print(vpc.id)


#------InternetGatewayId---------------------

ig = res.create_internet_gateway()
vpc.attach_internet_gateway(
    InternetGatewayId = ig.id
    )

print(ig.id)

#-------------RouteTable---------------------

route_table = vpc.create_route_table()
route_table.create_route(
    DestinationCidrBlock = "0.0.0.0/0",
    GatewayId = ig.id)

print(route_table.id)

#--------------------Create-Subnets---------------------------

subnet = res.create_subnet(
    CidrBlock = "13.0.1.0/24",
    VpcId = vpc.id)

print(subnet.id)                  
                      

route_table.associate_with_subnet(SubnetId=subnet.id)

#------------------Create-SecurityGroup---------------------------

sec_group = res.create_security_group(
    GroupName = "Better_Work",
     Description = "For _Better_work",
     VpcId=vpc.id
     )
                        
sec_group.authorize_ingress(
    CidrIp = '0.0.0.0/0',
    IpProtocol = "-1"
    )

print(sec_group.id)

#--------------------Create-Ec2-Instance---------------------------

ec2 = boto3.resource('ec2')

# create a file to store the key locally

outfile = open('Try_Key.pem','w')

# call the boto ec2 function to create a key pair

key_pair = ec2.create_key_pair(KeyName = 'Try_Key')

# capture the key and store it in a file

KeyPairOut = str(
    key_pair.key_material
    )

outfile.write(
    KeyPairOut
    )

print("Key Pair Try_Key.pem successfully created")

inst = res.create_instances(ImageId = 'ami-0a244485e2e4ffd03',
        InstanceType ='t2.micro',
        KeyName = 'Try_Key',
        MaxCount = 1,
        MinCount = 1,

        NetworkInterfaces = [{'SubnetId':subnet.id,
                'DeviceIndex':0,
                'AssociatePublicIpAddress': True,
                'Groups':[sec_group.group_id]}]
                )

inst[0].wait_until_running()
print(inst[0])
print("EC2 instance successfully created with using VPC, Subnets, InternetGateway, SecurityGroup ")
#----------------------Complete-----------------------------