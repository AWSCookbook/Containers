#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_aws_cookbook_608.cdk_aws_cookbook_608_stack import CdkAwsCookbook608Stack


app = cdk.App()
CdkAwsCookbook608Stack(app, "cdk-aws-cookbook-608")

app.synth()
