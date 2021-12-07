#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_aws_cookbook_605.cdk_aws_cookbook_605_stack import CdkAwsCookbook605Stack


app = cdk.App()
CdkAwsCookbook605Stack(app, "cdk-aws-cookbook-605")

app.synth()
