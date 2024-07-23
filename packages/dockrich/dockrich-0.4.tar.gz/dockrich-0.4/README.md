# Dockrich

![GitHub stars](https://img.shields.io/github/stars/prasaanth2k/dockrich?style=social)
![GitHub issues](https://img.shields.io/github/issues/prasaanth2k/dockrich)
![GitHub license](https://img.shields.io/github/license/prasaanth2k/dockrich)

A tool to pretty print Docker command outputs.

## Installation

```bash
pip install dockrich
```

```python3

from dockrich.dockmanager import Dockermanager

DM = Dockermanager()

DM.list_container_ports()
DM.list_networks()
DM.list_true_without_none()
DM.run_container(imagename="kalilinux/kali-rolling",imagetag="latest",command="tail -f /dev/null")

```