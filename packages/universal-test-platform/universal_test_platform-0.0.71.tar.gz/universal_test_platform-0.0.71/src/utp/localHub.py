import subprocess
import os
import time
import click
from utp.checkport import isPortUsed
from utp.getConfig import getConfig
from utp.utils import downloadFile
import shutil

name = '.cache/selenium-server-4.21.0.jar'

def runLocalHub():
      ip = getConfig().get("server","").strip()
      url = f'http://{ip}:4723/device-farm/apps/file-1719662775015.jar'
      
      if not os.path.isdir(".cache"):
            os.mkdir(".cache")
      
      if not os.path.isfile(name):
            temp = name+".download"
            if os.path.isfile(temp):
                  os.remove(temp)
            click.secho("Download requirement to .cache directory. Don't delete it")
            downloadFile(url,temp)
            shutil.move(temp, name)
      
      localHubIsRunning = isPortUsed(4444)
      if localHubIsRunning == True:
            click.secho("Hub already running", bg='black', fg='yellow')
            return None

            
      click.secho("running Hub Locally")
      
      handler= subprocess.Popen("java -jar "+ name + " standalone",
                          shell=True,
                          stdout=subprocess.DEVNULL,
                          stderr=subprocess.DEVNULL)
      time.sleep(10)
      click.secho("Start Hub and Node standalone", bg='black', fg='green')

      return handler
    
