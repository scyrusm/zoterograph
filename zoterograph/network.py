#from selenium import webdriver
import webbrowser
from threading import Thread
import SimpleHTTPServer
import SocketServer
import json
import time
from pyzotero import zotero
import sys
import os

datapath=os.path.dirname(os.path.realpath(__file__))+"/../data/"
graphnumber=0
while 1==1:
  if os.path.isdir('./zgraph'+str(graphnumber)):
    graphnumber+=1
  else:
    os.system("mkdir zgraph"+str(graphnumber))
    os.system("cp "+datapath+"geckodriver zgraph"+str(graphnumber))
    os.system("cp "+datapath+"index.html zgraph"+str(graphnumber))
    break

class networkobj:
  def __init__(self):
    self.network={}
    self.network["nodes"]=[]
    self.network["links"]=[]
    self.authorlookup={}
    self.counter=0

  def process_entry(self,zoteroentry):
    name=zoteroentry['data']['title']
    group=1
    if {"name":name,"group":group} not in self.network["nodes"]:
      self.add_node(name,group)
      if u'creators' in zoteroentry['data'].keys():
        for creatordict in zoteroentry['data']['creators']:
          try:
            creator=creatordict['lastName']+creatordict['firstName']
          except:
            creator=creatordict['name']
          if creator not in self.authorlookup:
            self.authorlookup[creator]=[self.counter]
          else:
            for copaper in self.authorlookup[creator]:
              self.add_link(self.counter,copaper,1)
            self.authorlookup[creator].append(self.counter)
      self.counter+=1
    
  def add_node(self,name,group):
    self.network["nodes"].append({"name":name,"group":group})
  def add_link(self,source,target,weight):
    self.network["links"].append({"source":source,"target":target,"weight":weight})
    
  def to_json(self,filename='graphFile.json',directory='./'):
    with open(directory+filename,'w') as outfile:
      json.dump({"nodes":self.network["nodes"],"links":self.network["links"]},outfile,sort_keys=True,indent=4, separators=(',', ': '))
   


def launch_browser(url):
  time.sleep(0.5)
  webbrowser.get(using='google-chrome').open(url,new=2)  

def launch():
  if os.path.isfile('.zoterographcreds'):
    try:
      with open('.zoterographcreds','r') as creds:
        userid=creds.readline()
        apikey=creds.readline()
    except:
      userid = raw_input("Enter your Zotero user ID number: ")
      apikey = raw_input("Enter your Zotero api key: ")

  else:
    userid = raw_input("Enter your Zotero user ID number: ")
    apikey = raw_input("Enter your Zotero api key: ")
    while 1==1:
      saveprompt = raw_input("Would you like to save these credentials? (N/y)")
      if saveprompt in ["N","n",""]:
        break 
      elif saveprompt=="y":
        with open(".zoterographcreds","w") as creds:
          creds.write(userid+"\n")
          creds.write(apikey)
        break


  zot = zotero.Zotero(int(userid), 'user', str(apikey))
  items=[]
  bookmark=1
  pagesize=100
  while 1==1:
    block=zot.items(limit=pagesize,start=bookmark)
    if len(block)==0:
      break
    elif len(block)<pagesize:
      items+=block
      break
    elif len(block)==pagesize:
      items+=block
      bookmark+=pagesize
    else:
      raise("Somehow, the Zotero API has returned unexpected output")
#  items = zot.items(limit=5)
  nw=networkobj()
  for i in range(len(items)):
    #nw.add_node(items[i]['data']['title'],1)
    nw.process_entry(items[i])
  nw.to_json(directory="zgraph"+str(graphnumber)+"/")
  
  
  PORT=8000     
  SocketServer.TCPServer.allow_reuse_address=True
  Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
  while 1==1:
    try:
      httpd = SocketServer.TCPServer(("", PORT), Handler)
      break
    except:
      PORT+=1
  
  print("serving on port "+str(PORT))
  background = Thread(target=launch_browser,args=("http://127.0.0.1:"+str(PORT),))
  background.start()
  os.chdir('zgraph'+str(graphnumber))
  httpd.serve_forever()

