r'''
# CMS Plone Chart for CDK8S

This chart provides a library to bootstrap a Plone deployment on a Kubernetes cluster using the [CDK8S](https://cdk8s.io) framework.

It provides

* backend (with `plone.volto` or Classic-UI)
* frontend (Plone-Volto, a ReactJS based user interface)
* varnish (optional)

## Usage

TODO

## Development

Clone the repository and install the dependencies:

```bash
yarn install
```

Then run the following command to run the test:

```bash
npx projen test
```

### WIP Checklist:

Each step need to be implemented with tests!

* [ ] Start Backend

  * [x] deployment
  * [x] service
  * [x] pdb
  * [ ] init container running plone-site-create
  * [x] lifecycle checks (readiness, liveness)
  * [x] generic way to inject sidecars
* [ ] Start Frontend

  * [x] deployment
  * [x] service
  * [x] pdb
  * [ ] lifecycle checks (readiness, liveness)
  * [ ] depend on ready/live backend (needed?)
  * [x] generic way to inject sidecars
* [ ] Start Varnish

  * [ ] deployment

    * [ ] do not depend on backend/front end to be  up, but configure to deliver from cache if possible.
  * [ ] service
  * [ ] pdb
  * [ ] lifecycle checks (readiness, liveness)
  * [ ] generic way to inject sidecars
  * find a way to purge caches. based on kitconcept varnish purger? needs
* [ ] Other Languages

  * [x] Check Python distribution
  * [ ] Check Java distribution
  * [ ] Check Go distribution
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

import cdk8s_plus_24 as _cdk8s_plus_24_d27940f9
import constructs as _constructs_77d1e7e8


class Plone(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk8s-plone.Plone",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        backend: typing.Optional[typing.Union["PloneBaseOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        frontend: typing.Optional[typing.Union["PloneBaseOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        image_pull_secrets: typing.Optional[typing.Sequence[builtins.str]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param backend: 
        :param frontend: 
        :param image_pull_secrets: 
        :param version: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce73be75e5c875694e2ea2deee9168aaf43047f7f3277915e5366215ac6ead0b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = PloneOptions(
            backend=backend,
            frontend=frontend,
            image_pull_secrets=image_pull_secrets,
            version=version,
        )

        jsii.create(self.__class__, self, [scope, id, options])

    @builtins.property
    @jsii.member(jsii_name="backendServiceName")
    def backend_service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backendServiceName"))

    @builtins.property
    @jsii.member(jsii_name="frontendServiceName")
    def frontend_service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "frontendServiceName"))


@jsii.data_type(
    jsii_type="cdk8s-plone.PloneBaseOptions",
    jsii_struct_bases=[],
    name_mapping={
        "environment": "environment",
        "image": "image",
        "image_pull_policy": "imagePullPolicy",
        "limit_cpu": "limitCpu",
        "limit_memory": "limitMemory",
        "max_unavailable": "maxUnavailable",
        "min_available": "minAvailable",
        "replicas": "replicas",
    },
)
class PloneBaseOptions:
    def __init__(
        self,
        *,
        environment: typing.Optional[_cdk8s_plus_24_d27940f9.Env] = None,
        image: typing.Optional[builtins.str] = None,
        image_pull_policy: typing.Optional[builtins.str] = None,
        limit_cpu: typing.Optional[jsii.Number] = None,
        limit_memory: typing.Optional[builtins.str] = None,
        max_unavailable: typing.Optional[typing.Union[builtins.str, jsii.Number]] = None,
        min_available: typing.Optional[typing.Union[builtins.str, jsii.Number]] = None,
        replicas: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param environment: 
        :param image: 
        :param image_pull_policy: 
        :param limit_cpu: 
        :param limit_memory: 
        :param max_unavailable: 
        :param min_available: 
        :param replicas: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98a3f897f3c97ce421ed9e373138d6f4217da3acb1acea15ecf79f12b7e83dc6)
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument image_pull_policy", value=image_pull_policy, expected_type=type_hints["image_pull_policy"])
            check_type(argname="argument limit_cpu", value=limit_cpu, expected_type=type_hints["limit_cpu"])
            check_type(argname="argument limit_memory", value=limit_memory, expected_type=type_hints["limit_memory"])
            check_type(argname="argument max_unavailable", value=max_unavailable, expected_type=type_hints["max_unavailable"])
            check_type(argname="argument min_available", value=min_available, expected_type=type_hints["min_available"])
            check_type(argname="argument replicas", value=replicas, expected_type=type_hints["replicas"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if environment is not None:
            self._values["environment"] = environment
        if image is not None:
            self._values["image"] = image
        if image_pull_policy is not None:
            self._values["image_pull_policy"] = image_pull_policy
        if limit_cpu is not None:
            self._values["limit_cpu"] = limit_cpu
        if limit_memory is not None:
            self._values["limit_memory"] = limit_memory
        if max_unavailable is not None:
            self._values["max_unavailable"] = max_unavailable
        if min_available is not None:
            self._values["min_available"] = min_available
        if replicas is not None:
            self._values["replicas"] = replicas

    @builtins.property
    def environment(self) -> typing.Optional[_cdk8s_plus_24_d27940f9.Env]:
        result = self._values.get("environment")
        return typing.cast(typing.Optional[_cdk8s_plus_24_d27940f9.Env], result)

    @builtins.property
    def image(self) -> typing.Optional[builtins.str]:
        result = self._values.get("image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_pull_policy(self) -> typing.Optional[builtins.str]:
        result = self._values.get("image_pull_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def limit_cpu(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("limit_cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def limit_memory(self) -> typing.Optional[builtins.str]:
        result = self._values.get("limit_memory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_unavailable(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, jsii.Number]]:
        result = self._values.get("max_unavailable")
        return typing.cast(typing.Optional[typing.Union[builtins.str, jsii.Number]], result)

    @builtins.property
    def min_available(self) -> typing.Optional[typing.Union[builtins.str, jsii.Number]]:
        result = self._values.get("min_available")
        return typing.cast(typing.Optional[typing.Union[builtins.str, jsii.Number]], result)

    @builtins.property
    def replicas(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("replicas")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PloneBaseOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk8s-plone.PloneOptions",
    jsii_struct_bases=[],
    name_mapping={
        "backend": "backend",
        "frontend": "frontend",
        "image_pull_secrets": "imagePullSecrets",
        "version": "version",
    },
)
class PloneOptions:
    def __init__(
        self,
        *,
        backend: typing.Optional[typing.Union[PloneBaseOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        frontend: typing.Optional[typing.Union[PloneBaseOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        image_pull_secrets: typing.Optional[typing.Sequence[builtins.str]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param backend: 
        :param frontend: 
        :param image_pull_secrets: 
        :param version: 
        '''
        if isinstance(backend, dict):
            backend = PloneBaseOptions(**backend)
        if isinstance(frontend, dict):
            frontend = PloneBaseOptions(**frontend)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11a7bf251c7d7108ebec61b6990d415bfd470d183d1663a37ef781641ec299d6)
            check_type(argname="argument backend", value=backend, expected_type=type_hints["backend"])
            check_type(argname="argument frontend", value=frontend, expected_type=type_hints["frontend"])
            check_type(argname="argument image_pull_secrets", value=image_pull_secrets, expected_type=type_hints["image_pull_secrets"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if backend is not None:
            self._values["backend"] = backend
        if frontend is not None:
            self._values["frontend"] = frontend
        if image_pull_secrets is not None:
            self._values["image_pull_secrets"] = image_pull_secrets
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def backend(self) -> typing.Optional[PloneBaseOptions]:
        result = self._values.get("backend")
        return typing.cast(typing.Optional[PloneBaseOptions], result)

    @builtins.property
    def frontend(self) -> typing.Optional[PloneBaseOptions]:
        result = self._values.get("frontend")
        return typing.cast(typing.Optional[PloneBaseOptions], result)

    @builtins.property
    def image_pull_secrets(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("image_pull_secrets")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PloneOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Plone",
    "PloneBaseOptions",
    "PloneOptions",
]

publication.publish()

def _typecheckingstub__ce73be75e5c875694e2ea2deee9168aaf43047f7f3277915e5366215ac6ead0b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    backend: typing.Optional[typing.Union[PloneBaseOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    frontend: typing.Optional[typing.Union[PloneBaseOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    image_pull_secrets: typing.Optional[typing.Sequence[builtins.str]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98a3f897f3c97ce421ed9e373138d6f4217da3acb1acea15ecf79f12b7e83dc6(
    *,
    environment: typing.Optional[_cdk8s_plus_24_d27940f9.Env] = None,
    image: typing.Optional[builtins.str] = None,
    image_pull_policy: typing.Optional[builtins.str] = None,
    limit_cpu: typing.Optional[jsii.Number] = None,
    limit_memory: typing.Optional[builtins.str] = None,
    max_unavailable: typing.Optional[typing.Union[builtins.str, jsii.Number]] = None,
    min_available: typing.Optional[typing.Union[builtins.str, jsii.Number]] = None,
    replicas: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11a7bf251c7d7108ebec61b6990d415bfd470d183d1663a37ef781641ec299d6(
    *,
    backend: typing.Optional[typing.Union[PloneBaseOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    frontend: typing.Optional[typing.Union[PloneBaseOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    image_pull_secrets: typing.Optional[typing.Sequence[builtins.str]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
