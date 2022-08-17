## DEPLOYMENT OF FREE PBX (PRIVATE BRANCH EXCHANGE) IN AWS EC2 INSTANCE USING PYTHON 
 A `private branch exchange` (PBX) is a telephone system within an enterprise that switches calls between users on local lines, while enabling all users to share a certain number of external phone lines. 
### REQUIREMENTS
 - you are **required** to install Command Line Interface (AWS CLI) version 2 on supported operating systems.
 - install boto3 - which is the Amazon Web Services (AWS) Software Development Kit (SDK) for Python, which allows Python developers to write software that makes use of services like Amazon S3 and Amazon EC2.
### CONFIGURATIONS WITH AWS EC2
To set up your AWS CLI use the ```aws configure```  command. When you enter this command, the AWS CLI prompts you for four pieces of information such as your;
- Access key ID
- Secret access key
- AWS Region.
After this is done and you have signedin in the AWS console in a specified or any region, you can starting creating your _aws ec2 instance_ but before that, you first need to create the `vpc`, `subnet`,`internet gate way`, `route table`.  After that is done you can now create the `ec2 instance`.
####  USING PYTHON ENVIRONMENT TO CREATE AN EC2 INSTANCE
- First thing we import boto3 - this is the module that is going to identify or define key functions of boto3 in python. If not imported the python script will fail to identify key functions of the boto3.
- Second we create a variable that is going to store the session and assign it to boto3 and call the session function that stores configuration state and allows you to create service clients and resources as shown below;

```import boto3```

```sess = boto3.session.Session()```
```res = sess.resource('ec2')```
####  CREATING A VIRTUAL PRIVATE CLOUD (VPC)
 To create a virtual private cloud, we need to create a variable named vpc and assign it to the aws resource so that it can access the parameter which is the `cidrblock` and give it any `internet protocol`(IP). After this is done we call the vpc variable and connect to a wait_untill method that will waite for the vpc-id to be available and once available it should print the vpc-id. 

```vpc = res.create_vpc(CidrBlock ='13.0.0.0/16')```
```vpc.wait_until_available()```

```print(vpc.id)```.
###   CREATING THE INTERNET GATE WAY
**NOTE**.
- In order to create the internet-gate-way id we need to attach the vpc id to the internet gateway we are creating.
- First thing we create a variable that will store the internet gate way id and call the aws resource function that will enable us to create the internet gate way once that is done, we  attach the vpc id to the internet gateway we are creating and pass the attribute of the internet gate way and assign its value to the varible that is going to store the internet gate way id and print it.

```ig = res.create_internet_gateway()```
```vpc.attach_internet_gateway(```
    ```InternetGatewayId = ig.id```
   ```)```

```print(ig.id)```
### CREATING THE ROUTE TABLE
 VPCs has an implicit router, and you use route tables to control where network traffic is directed. Each route in a table specifies a destination and a target. The destination for the route is 0.0.0.0/0, which represents all IPv4 addresses. The target is the internet gateway that's attached to your VPC.

```route_table = vpc.create_route_table()```
```route_table.create_route(```
    ```DestinationCidrBlock = "0.0.0.0/0",```
    ```GatewayId = ig.id)```
```print(route_table.id)```
### CREATING A SUBNET 
 Create a variable that will store the subnet id and is connected to the create subnet method that has the cidrblock attribute and is assigned to another ip address and also another variable that is going to store the vpc id then print the subnet id.  
```subnet = res.create_subnet(```
    ```CidrBlock = "13.0.1.0/24",```
   ```VpcId = vpc.id)```
   
```print(subnet.id)```                  
                 
```route_table.associate_with_subnet(SubnetId=subnet.id)```
### CREATING  SECURITY GROUPS
You can have a security group variable for storing the group id and a security group for use in a VPC and for attaching the ingresss with the same variable name and also give it the cidrip that is all open(0.0.0.0/0) or asigned to all zeros and internet protocol  to be used, you can't have two security groups for use in EC2-instance with the same name or two security groups for use in a VPC with the same name.

 **NOTE**
- You need to create security groups also attach the security groups to the ingress which carries to attributes in the ip CidrBlock and the ip protocol to be used, failure to this it will not create the public IP.

 ```sec_group = res.create_security_group(```
    ```GroupName = "FreePBX_Group",```
     ```Description = "For the freePBX",```
     ```VpcId=vpc.id```
    ```)```
                        
```sec_group.authorize_ingress(```
    ```CidrIp = '0.0.0.0/0',```
    ```IpProtocol = "-1"```
    ```)```

```print(sec_group.id)```
 
### CREATING AN EC2 INSTANCE 
Create an ec2 variable that is going to store the instance and asign it to the boto3 resouce module method and in the parenthesis pass the string ec2.

```ec2 = boto3.resource('ec2')```

 ###  CREATE THE FILE TO STORE THE KEY LOCALLY
Create the varible that is going to store the private key in a file and in the parenthesis pass the key name created and put the extention needed for you either; .rta, .pem or anyother for us we are using the .pem extention.

 ```outfile = open('PBXAccessKey.pem','w')```

 ### CALLING THE BOTO3 EC2 FUNCTION TO CREATE A KEY PAIR
 Create a variable that is going to store the key pair and call the ec2 function to create it and in the parenthesis the keyname attritube should be assigned to a string with the key name.

```key_pair = ec2.create_key_pair(KeyName = 'PBXAccessKey')```

 ### CAPTURING THE KEY AND STORING IT IN A FILE 
 Create a variable that is going to store the string of the key pair material and write it to the file created that is going to be storing the private key.

```KeyPairOut = str(```
    ```key_pair.key_material```
```)```

```outfile.write(```
    ```KeyPairOut```
```)```

```print("Key Pair PBXAccessKey.pem successfully created")```
### LAUNCHING AN EC2 INSTANCE
To deploy free pbx into an instance go to the marketpalce in the aws console and search for free pbx then go on community free pbxs and  select or copy any ami image id for the free pbx. After this is done create a variable that will store an instance and assign it to the aws resource to create an insatnce in the parenthesis pass image id of the free pbx, the instance type it contains or any other, the key name , maxcount and mincount to have values of one because an instance should be created once.

```inst = res.create_instances(ImageId = 'ami-082cf60e3c339f4eb',```
        ```InstanceType ='t3.micro',```
       ```KeyName = 'PBXAccessKey',```
        ```MaxCount = 1,```
        ```MinCount = 1,```

        ```NetworkInterfaces = [{'SubnetId':subnet.id,```
                ```'DeviceIndex':0,````
                ```'AssociatePublicIpAddress': True,```
                ```'Groups':[sec_group.group_id]}]```
                ```)```

```inst[0].wait_until_running()```

```print(inst[0])```

```print("EC2 instance successfully created with using VPC, Subnets, InternetGateway, SecurityGroup ")```
 ### CONNECTING AN EC2 INSTANCE
 To connect an Amazon Linux instance, use  following command to set the lacation of the key ```ssh -i``` and the name of the keypair created. The name of the operating system we are using which should appear ```ubuntu ec2-user@52.87.168.235```
 ### SETTING UP FREE PBX
