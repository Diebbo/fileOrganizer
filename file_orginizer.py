import os
import shutil as sh
import datetime as dt
from time import sleep
from regex import search

# costants
USER = 'diebbo'
DOWLOAD_DIRECTORY = 'Downloads'
PATH_TO_UNI = 'Documents/obsidian/Note uni di Diebbo/Secondo Anno'

def handle_file(file, dest):
   _in = input('move to ' + dest + ': ' + file + ' - Continue? [y/n]') 
   if _in == 'n':
      exit(1)

def move_to_uni(files):
   for file in files:
      handle_file(file, 'uni')

      # removing file prefix
      if(file.replace('ott-', '') != file):
         file_name = file.replace('ott-', '')
         dest = 'Ottimizzazione Combinatoria'
      elif(file.replace('ling-', '') != file):
         file_name = file.replace('lin-', '')
         dest = 'Linguaggi di Programmazione'
      elif(file.replace('so-', '') != file):
         file_name = file.replace('sis-', '')
         dest = 'Sistemi Operativi'
      elif(file.replace('cal-', '') != file):
         file_name = file.replace('cal-', '')
         dest = 'Calcolo Numerico'
      else:
         raise Exception('file not found' + file)

      # find subdirectory
      os.chdir(f'/home/{USER}/{PATH_TO_UNI}/{dest}')
      subdirs = os.listdir('.')
      file_subdir = file_name.split('-')[0]

      if file_subdir in subdirs:
         dest += '/' + file_subdir
         file_name = file_name.replace(f'{file_subdir}-', '')
      
      # move file
      sh.move(f'/home/{USER}/{DOWLOAD_DIRECTORY}/{file}', f'/home/{USER}/{PATH_TO_UNI}/{dest}/{file_name}')


def move_to_file_sys(files):
   for file in files:
      handle_file(file, 'file system')

      # get file prefix
      prefixes = ['doc', 'pic', 'vid', 'mus', 'tem', 'pub', 'dow']
      prefixes_location = {'doc': 'Documents', 'pic': 'Pictures', 'vid': 'Videos', 'mus': 'Music', 'tmp': 'tmp', 'pub': 'Public', 'dow': 'Downloads'}
      file_prefix  = file.split('-')[0]
      file_name = file.replace(f'{file_prefix}-', '')
      if file_prefix not in prefixes:
         raise Exception('directory not found, for file ' + file)

      # finding sub-directory
      os.chdir(f'/home/{USER}/{prefixes_location[file_prefix]}')
      subdirs = os.listdir('.')
      if '-' in file_name:
         file_subdir = file_name.split('-')[0]
      
         if file_subdir in subdirs:
            file_name = file_name.replace(f'{file_subdir}-', f'{file_subdir}/') # add subdirectory to file name (PATH)
         else:
            print('WARN: subdirectory not found' + file_subdir + 'in' + file+ 'was it intended?!')
            # raise Exception('subdirectory not found' + file_subdir + 'in' + file)

      # move file
      sh.move(f'/home/{USER}/{DOWLOAD_DIRECTORY}/{file}', f'/home/{USER}/{prefixes_location[file_prefix]}/{file_name}')

def main():
   user = USER # str(input('insert user name:' ))

   while True:
      # dowload directory
      os.chdir(f'/home/{user}/{DOWLOAD_DIRECTORY}')
      
      # get all files in dowload directory
      dowload_files = os.listdir('.')

      # regexes
      uni_regex = r'(ott|lin|sis|cal)(-\S+)+\.[a-zA-Z]+'
      file_sys_regex = r'(doc|pic|vid|mus|tmp|pub|dow)(-\S+)+\.[a-zA-Z]+'

      # filter
      uni_files = [file for file in dowload_files if search(uni_regex, file)]
      file_sys_files = [file for file in dowload_files if search(file_sys_regex, file)]

      # move files
      try:
         move_to_uni(uni_files)
         move_to_file_sys(file_sys_files)
      except Exception as e:
         print('error while moving files. err: ' + str(e))

      # wait for new files
      try:
         while dowload_files == os.listdir('.'):
            print('waiting for new files...')
            sleep(3)
            pass  
      except:
         print('Service stopped')
         exit(1)

   
if __name__ == "__main__":
   main()
