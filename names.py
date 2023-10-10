
import json
import os

from settings import basepath

def readnames(flname):
    with open(flname, 'r') as infl:
        names = json.load(infl)
    return names

def writenames(flname):
    with open(flname,'w') as outfl:
        json.dump(names, outfl)
    return f'written {flname}'