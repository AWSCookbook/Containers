#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_aws_cookbook_606.cdk_aws_cookbook_606_stack import CdkAwsCookbook606Stack


app = cdk.App()
CdkAwsCookbook606Stack(app, "cdk-aws-cookbook-606")

app.synth()
