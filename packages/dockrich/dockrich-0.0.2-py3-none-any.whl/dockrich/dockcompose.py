import subprocess
from rich.console import Console
from rich.table import Table
import shlex
from time import sleep
from rich import print
import json

def load_json(filename):
    with open(filename,'r') as file:
        data = json.load(file)
    return data
