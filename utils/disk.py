import os, yaml
from string import Template

def load_hashtags(path):
    return open(path, 'r').read().splitlines()

def load_template(path):
    temp = open(path, 'r').read()
    return Template(temp)

def load_config(path):
    with path.open() as f:
        return yaml.safe_load(f)


