#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_aws_cookbook_607.cdk_aws_cookbook_607_stack import CdkAwsCookbook607Stack


app = cdk.App()
CdkAwsCookbook607Stack(app, "cdk-aws-cookbook-607")

app.synth()
