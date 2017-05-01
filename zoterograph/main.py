from selenium import webdriver
from threading import Thread
import SimpleHTTPServer
import SocketServer
import json
import time
from pyzotero import zotero
import sys

class networkobj:
  def __init__(self):
    self.network={}
    self.network["nodes"]=[]
    self.network["links"]=[]
    
  def add_node(self,name,group):
    self.network["nodes"].append({"name":name,"group":group})
  def add_link(self,source,target,weight):
    self.network["links"].append({"source":source,"target":target,"weight":weight})
    
  def to_json(self,filename='graphFile.json'):
    with open(filename,'w') as outfile:
      json.dump(self.network,outfile)



def launch_ff(url):
  time.sleep(0.5)
  driver = webdriver.Firefox()
  driver.get(url)

if __name__=='__main__':
  userid = raw_input("Enter your Zotero user ID number: ")
  apikey = raw_input("Enter your Zotero api key: ")
  zot = zotero.Zotero(int(userid), 'user', str(apikey))
  items = zot.top(limit=5)
  nw=networkobj()
  for i in range(5):
    nw.add_node(items[i]['data']['title'],1)
  nw.to_json()
  
  
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
    
  background = Thread(target=launch_ff,args=("http://127.0.0.1:"+str(PORT),))
  background.start()
  httpd.serve_forever()
