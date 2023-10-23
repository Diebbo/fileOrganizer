import os
import shutil as sh
import datetime as dt
from time import sleep
from regex import search

# costants
USER = 'diebbo'
DOWLOAD_DIRECTORY = 'Downloads'
PATH_TO_UNI = 'Documents/obsidian/Note\ uni\ di\ Diebbo/Secondo\ anno'

def move_to_uni(files):
   for file in files:
      # removing file prefix
      if(file.replace('ott-', '') != file): 
         dest = 'Ottimizzazione\ Combinatoria'
      elif():
         ...
      
      
      sh.move(f'/home/{USER}/{DOWLOAD_DIRECTORY}/{file_name}', f'/home/{USER}/{PATH_TO_UNI}/{dest}/{file_name}')


def move_to_file_sys(files):
   _

def main():
   user = USER # str(input('insert user name:' ))

   # dowload directory
   os.chdir(f'/home/{user}/{DOWLOAD_DIRECTORY}')
   
   while True:
      # get all files in dowload directory
      dowload_files = os.listdir('.')

      # regexes
      uni_regex = r'(ott|ling|so|calc)(-\S+)+\.[a-zA-Z]+'
      file_sys_regex = r'(Documents|Pictures|Videos|Music|Templates|Public|Downoloads)(-\S+)+\.[a-zA-Z]+'

      # filter
      uni_files = [file for file in dowload_files if search(uni_regex, file)]
      file_sys_files = [file for file in dowload_files if search(file_sys_regex, file)]

      # move files
      move_to_uni(uni_files)
      move_to_file_sys(file_sys_files)

      # wait for new files
      while dowload_files == os.listdir('.'):
         sleep(2)
         pass

   



if __name__ == "__main__":
   main()
