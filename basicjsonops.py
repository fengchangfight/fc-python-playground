#!/usr/local/bin/python2
import os
import json
from dbtool import Dbtool



def insertNlgData(fileName):
    db = Dbtool()
    with open('./intents/'+fileName,'r') as fh:
      js = json.load(fh)
      name = js['name']
      print(name)
      responses = js['responses']
      for r in responses:
          messages = r['messages']
          for m in messages:
              if m['lang']  == 'en':
                  lines = m['speech']
                  for l in lines:
                      print(l)
                      # insert into nlg data table name & l
                      db.insertNlg(name, l, 8, 2)
      print("=======")



files = os.listdir("./intents")
for f in files:
    if not "usersays"  in f:
        insertNlgData(f)
