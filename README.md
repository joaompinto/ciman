# CIMAN

**C**ontainer **I**mage **MAN**ager

![PyPI - License](https://img.shields.io/pypi/l/ciman)
![PyPI](https://img.shields.io/pypi/v/ciman)
![PyPI - Downloads](https://img.shields.io/pypi/dm/ciman)

## About

This package provides a **C**ontainer **I**mage **MAN**agement Python library and command line utility

##

|  | ciman | docker | podman
| --- |:-----------:|:---:|:---:|
| Rootless install | :heavy_check_mark: | :x: |
| Remote image info | :heavy_check_mark: | :x: |
| Remote image history | :heavy_check_mark: | :x: |



## Requirements
Python 3.6+


## Install

```bash
pip install ciman
```

To use "run"
```bash
mkdir -p ~/.ciman/bin
curl -L https://github.com/proot-me/proot/releases/download/v5.3.0/proot-v5.3.0-x86_64-static -o ~/.ciman/bin/proot
```

## How to use (command ine tool)
```bash
# show info for the bash image on github
ciman info bash

# show info for the bash image from the microsoft registry
ciman info mcr.microsoft.com/dotnet/samples

# show tags for an image
ciman tags mcr.microsoft.com/dotnet/samples

```

## Environment variables

- DOCKER_REGISTRY: name of the docker registry to use for images names not containing a registry prefix (default: registry-1.docker.io)
- SSL_CERT_FILE: load CA certificate from the specified file instead of the default location
