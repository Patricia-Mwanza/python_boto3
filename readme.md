# INSTALLING AND UPDATING THE AWS EC2 CLI

" you are required to install Command Line Interface (AWS CLI) on supported operating systems.
NOTE:
 That AWS CLI versions 1 and 2 use the same aws command name. If you have both versions installed, your computer uses the first one found in your search path. If you previously installed AWS CLI version 1, we recommend that you uninstall the older version and install new version which is AWS CLI version 2.'''

## CONFIGURATIONS WITH AWS EC2

""" to set up your AWS CLI use the aws configure is the fastest way to for installation. When you enter this command, the AWS CLI prompts you for four pieces of information such as your;

Access key ID

Secret access key

AWS Region

After this is done and you have signedin in the AWS CONSOLE you can starting creating your AWS EC2 INSTANCE but before that you FIRST need to create the VPC, SUBNET,INTERNET GATE WAY, ROUTE TABLE.  After that is done you can now create the EC2 INSTANCE."""

# 1. CREATE A VPC USING THE COMMAND BELOW

aws ec2 create-vpc --cidr-block 10.10.0.0/16

# 2. WE CREATE A SUBNET AND USE THE VPC ID CREATED INT THE OUT PUT AND UPDATE THE COMMANDS
'''using the command below'''

aws ec2 create-subnet --vpc-id vpc-2f09a348 --cidr-block 10.0.1.0/24

# 3. WE CREATE A SECOND SUBNET AND USE THE VPC ID IN THE OUTPUT AND UPDATE THE COMMANDS
'''Use the commands below;'''

aws ec2 create-subnet --vpc-id vpc-2f09a348 --cidr-block 10.0.0.0/24

# 4. Once the subnets are created, you can make one of the subnets a public subnet by attaching an internet gateway to your VPC, creating a custom route table, and configuring routing for the subnet to the internet gateway. below is the command of creating an internet gateway.

aws ec2 create-internet-gateway --query InternetGateway.InternetGatewayId --output text

'''when the above command is run it generate the internet gateway, like in the example code below'''

                    igw-1ff7a07b

# 5. ATTACH THE INTERNET GATE WAY TO VPC 
''' Use the following command to attach-internet-gateway command.'''
 
 aws ec2 attach-internet-gateway --vpc-id vpc-2f09a348 --internet-gateway-id igw-1ff7a07b

# 6. CREATE THE CUSTOM ROUTE TABLE FOR YOUR VPC
''' Using the following create-route-table command.'''

aws ec2 create-route-table --vpc-id vpc-2f09a348 --query RouteTable.RouteTableId --output text

'''This command returns the ID of the new route table. The following is an example.'''

                                      rtb-c1c8faa6

# 7. CREATE A ROUTE TABLE THAT POINTS TO ALL TRAFFIC(0.0.0.0/0) THE DESTINATION TO THE INTERNET GATE WAY 
'''Using the following create-route command.'''

 aws ec2 create-route --route-table-id rtb-c1c8faa6 --destination-cidr-block 0.0.0.0/0 --gateway-id igw-1ff7a07b

 # 8. (OPTIONAL) TO CONFIRM THAT YOUR ROUTE HAS BEEN CREATED AND IS ACTIVE
 ''' you can describe the route table using the following describe-route-tables command.'''

 aws ec2 describe-route-tables --route-table-id rtb-c1c8faa6

 # 9. ASSOCIATE EITHER WITH THE FIRST OR SECOND SUBNET WITH THE CUSTOM ROUTE TABLE 
 ''' Associate it using the associate-route-table command. This subnet is your public subnet.'''

 aws ec2 associate-route-table  --subnet-id subnet-b46032ec --route-table-id rtb-c1c8faa6

 # 10. (OPTIONAL) YOU CAN  MODIFY THE PUBLIC IP ADDRESSING BEHAVIOR OF YOUR SUBNET SO THAT SO THAT AN INSTANCE CAN BE LAUNCHED INTO THE SUBNET TO AUTOMATICALLY RECEIVE AN IP ADDRESS.
 ''' Using the following modify-subnet-attribute command. Otherwise, associate an Elastic IP address with your instance after launch so that the instance is reachable from the internet.'''

 aws ec2 modify-subnet-attribute --subnet-id subnet-b46032ec --map-public-ip-on-launch

 ##  LAUNCHE AN INSTANCE INTO YOUR SUBNET
 # 11.reate a key pair and use the --query option and the --output text option to pipe your private key directly into a file with the .pem extension.

 aws ec2 create-key-pair --key-name MyKeyPair --query "KeyMaterial" --output text > MyKeyPair.pem

 ou launch an Amazon Linux instance. If you use an SSH client on a Linux or Mac OS X operating system to connect to your instance, use the following command to set the permissions of your private key file so that only you can read it.

 chmod 400 MyKeyPair.pem

 # 12. Create a security group in your VPC using the create-security-group command

 aws ec2 create-security-group --group-name SSHAccess --description "Security group for SSH access" --vpc-id vpc-2f09a348

 '''NOTE:
        Add a rule that allows SSH access from anywhere using the authorize-security-group-ingress command.''''

        aws ec2 authorize-security-group-ingress --group-id sg-e1fb8c9a --protocol tcp --port 22 --cidr 0.0.0.0/0

# 13.Launch an instance into your public subnet, using the security group and key pair you've created. In the output, take note of the instance ID for your instance.

aws ec2 run-instances --image-id ami-a4827dc9 --count 1 --instance-type t2.micro --key-name MyKeyPair --security-group-ids sg-e1fb8c9a --subnet-id subnet-b46032ec

# 14. Your instance must be in the running state in order to connect to it. Use the following command to describe the state and IP address of your instance.

aws ec2 describe-instances --instance-id i-0146854b7443af453 --query "Reservations[*].Instances[*].{State:State.Name,Address:PublicIpAddress}"

# 15. When your instance is in the running state, you can connect to it using an SSH client on a Linux or Mac OS X computer by using the following command:

ssh -i "MyKeyPair.pem" ec2-user@52.87.168.235