import os
import sys
import shutil as sh
import datetime as dt
from time import sleep
from regex import search

# CLI argument
default_yes = False

# costants
USER = 'diebbo'
DOWLOAD_DIRECTORY = 'Downloads'
PATH_TO_UNI = 'Documents/obsidian/Note uni di Diebbo/Secondo Anno'

def handle_file(file, dest):
   _in = input('move to ' + dest + ': ' + file + ' - Continue? [y/n]') 
   if _in == 'n':
      raise Exception('file skipped')

def move_to(files, dest_path, name, prefixes, destinations, is_recursive = True):
   for file in files:
      if not default_yes:
         try:
            handle_file(file, name)
         except Exception as e:
            print(str(e))
            continue

      dest = ''
      for prefix in prefixes:
         if prefix in file[:3]:
            file_no_prefix = file.replace(f'{prefix}-', '')
            dest = destinations[prefix]
            break
      
      if dest == '':
         raise Exception('directory not found, for file ' + file)

      # finding sub-directory
      file_in_subdir = find_subdir(file_no_prefix, f'{dest_path}/{dest}')

      # move file
      move_path = f'{dest_path}/{dest}/{file_in_subdir}'
      print(f'file moved to {move_path}')
      sh.move(f'/home/{USER}/{DOWLOAD_DIRECTORY}/{file}', move_path)

def find_subdir(file_name, path):
   # finding sub-directory
   os.chdir(path)
   subdirs = os.listdir('.')
   if '-' in file_name:
      file_subdir = file_name.split('-')[0]
   
      if file_subdir in subdirs:
         file_name = file_name.replace(f'{file_subdir}-', '')
         file_name = find_subdir(file_name, f'{path}/{file_subdir}')
         file_name = f'{file_subdir}/{file_name}'
      else:
         print('WARN: subdirectory not found ' + file_subdir + ' in ' + file_name + ', was it intended?!')
         # raise Exception('subdirectory not found' + file_subdir + 'in' + file)
   
   return file_name

def convert_xopp(path, is_recursive = True):
   # get all files in xopp_path
   files = os.listdir(path)

   for file in files:
      if '.xopp' in file and '.' != file[0]:
         file_pdf = file.replace('.xopp', '.pdf')
         try:
            print(f'converting file: {file}')
            os.chdir(path)
            os.system(f'xournalpp -p {file_pdf} {file}')
         except Exception as e:
            Exception('error while converting file: ' + file + ', err: ' + str(e))
   
      if is_recursive:
         if os.path.isdir(f'{path}/{file}'):
            convert_xopp(f'{path}/{file}')


def main():
   user = USER # str(input('insert user name:' ))
    
   # getting the parameters
   for arg in sys.argv:
      if '-y' in arg:
         default_yes = True

   # dowload directory
   os.chdir(f'/home/{user}/{DOWLOAD_DIRECTORY}')
   
   # get all files in dowload directory
   dowload_files = os.listdir('.')
   
   # prefixes
   uni_prefixes = ['ott', 'lin', 'sis', 'cal', 'ret']
   sys_prefixes = ['doc', 'pic', 'vid', 'mus', 'tem', 'pub', 'dow']
   
   # destinations
   uni_destinations = {
      'ott': 'Ottimizzazione Combinatoria',
      'lin': 'Linguaggi di Programmazione',
      'sis': 'Sistemi Operativi',
      'cal': 'Calcolo Numerico',
      'ret': 'Reti di Calcolatori'
      }
   sys_destinations = {
      'doc': 'Documents',
      'pic': 'Pictures',
      'vid': 'Videos',
      'mus': 'Music',
      'tmp': 'tmp',
      'pub': 'Public',
      'dow': 'Downloads'
      }

   # regexes
   uni_regex = r'(ott|lin|sis|cal|ret)(-\S+)+\.[a-zA-Z]+'
   file_sys_regex = r'(doc|pic|vid|mus|tmp|pub|dow)(-\S+)+\.[a-zA-Z]+'

   # filter
   uni_files = [file for file in dowload_files if search(uni_regex, file)]
   file_sys_files = [file for file in dowload_files if search(file_sys_regex, file)]

   # move files
   try:
      move_to(uni_files, f'/home/{user}/{PATH_TO_UNI}', 'uni', uni_prefixes, uni_destinations)
      move_to(file_sys_files, f'/home/{user}/', 'file system', sys_prefixes, sys_destinations)
   except Exception as e:
      print('error while moving files. err: ' + str(e))
      exit(1)

   # wait for new files
   try:
      # recursive search
      is_recursive = default_yes if default_yes else bool(input('recursive search? [y/n]') == 'y')
      
      # convert .xopp to .pdf
      convert_xopp(f'/home/{user}/{PATH_TO_UNI}', is_recursive)
      
   except Exception as e:
      print('error while converting files. err: ' + str(e))
      exit(1)

   
if __name__ == "__main__":
   main()
