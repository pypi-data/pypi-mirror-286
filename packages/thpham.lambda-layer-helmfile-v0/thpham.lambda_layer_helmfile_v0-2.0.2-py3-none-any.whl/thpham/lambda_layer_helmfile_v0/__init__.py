r'''
# Lambda Layer with Helmfile

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

This module exports a single class called `HelmfileLayer` which is a `lambda.LayerVersion` that
bundles the [`helm`](https://helm.sh/) and the
[`helmfile`](https://helmfile.readthedocs.io/en/latest/) command line.

> * Helm Version: 3.15.3
> * Helmfile Version: 0.166.0

Usage:

```python
// HelmfileLayer bundles the 'helm' and 'helmfile' command lines
import { HelmfileLayer } from '@thkpham/lambda-layer-helmfile-v0';
import * as lambda from 'aws-cdk-lib/aws-lambda';

declare const fn: lambda.Function;
const helmfile = new HelmfileLayer(this, 'HelmfileLayer');
fn.addLayers(helmfile);
```

`helm` will be installed under `/opt/helm/helm` and `helmfile` will be installed under `/opt/helmfile/helmfile`.
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import constructs as _constructs_77d1e7e8


class HelmfileLayer(
    _aws_cdk_aws_lambda_ceddda9d.LayerVersion,
    metaclass=jsii.JSIIMeta,
    jsii_type="@thkpham/lambda-layer-helmfile-v0.HelmfileLayer",
):
    '''A CDK Asset construct that contains ``kubectl`` and ``helm``.'''

    def __init__(self, scope: _constructs_77d1e7e8.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__330d4bb433562ff0a26d72c30238635458e605a529107e0e1ab6ecd6b192f29a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [scope, id])


__all__ = [
    "HelmfileLayer",
]

publication.publish()

def _typecheckingstub__330d4bb433562ff0a26d72c30238635458e605a529107e0e1ab6ecd6b192f29a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
