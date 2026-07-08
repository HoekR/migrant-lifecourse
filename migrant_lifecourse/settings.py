import os
import json

# change locations to reflect your situation

basepath = './data'
namesfile = os.path.join(basepath,'names.json')
excelfilename = os.path.join(basepath, "Lifecourses NA tentoonstelling.xlsx")

schemes = {'nama':'NAMA', 
           'ngas':'NGAS', 
           'ex-servicemen': 'empire-and-allied-ex-servicemen-scheme-1948-1955',
           'youth program':'working-holiday-scheme',
           'visa 457': 'working-holiday-scheme',
           'working holiday': 'working-holiday-scheme'}


