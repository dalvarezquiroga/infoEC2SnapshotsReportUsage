# Report information about Snapshots, Volumes, AMIS...

![Cost](/assets/aws-cost.jpg)


We want reduce costs in our AWS account. Normally in DEVs accounts we have a lot of AMIs, Snapshots, Volumes that users forget to delete and it doesn't remove automatically when you destroy an EC2 Instance.

This small script help you to identify them to take some action.

Your boss Finance will appreciate it ;-)


# Technologies we’ll use:

*  AWS API (EC2)
*  Python3.9


```bash
https://linuxhostsupport.com/blog/how-to-install-python-3-9-on-ubuntu-20-04/ (Google)
```

# Pre-requisites:
```bash
pip3 intall boto3
```

# Deploy:

```bash
AWS_PROFILE=XXX python3 infoEC2SnapshotsReportUsage.py
```

![Yes](/assets/PlanetaSimios.gif)


# Testing

If everything is working well, we will see a new Excel in your same location:

```bash
AWS_PROFILE=sso-nvoperations-pu python3 py
Excel File going to be created --> Status-EC2-ENVIRONMENT-14-Mar.xlsx
Workbook closed
```

![Result](/assets/result.png)

# Licence

Apache

# Information

More info --> 

https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_snapshots

https://gist.github.com/nicbor/14987b2a382a384fd6299f6a76def099

https://www.tutorialspoint.com/How-do-we-use-re-finditer-method-in-Python-regular-expression

https://interactivechaos.com/en/python/function/remultiline

https://www.programiz.com/python-programming/methods/built-in/enumerate

David Álvarez Quiroga
