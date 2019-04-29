import urllib.request
import pdb
import shutil
import logging
import datetime
import os
import sys
import time
from distutils.dir_util import copy_tree
import json
import S3_func
import sql_func


class MainProgram:



    
    #  initialisation

    def read_config(self):
        fileDir = os.path.dirname(os.path.abspath(__file__))
        sys.path.append(fileDir)
        configFile=os.path.join(fileDir,'config.json')
        configuration=json.loads(open(configFile).read())
        global filelist
        global log_path
        global ignore_files
        global main_prop
        global s3_properties
        global sql_properties
        filelist=configuration['file_list']
        ignore_files=configuration['ignore_files']
        s3_properties=configuration['s3_properties']
        main_prop=configuration['main_prop']
        sql_properties=configuration['sql_properties']
        log_path=main_prop['log_path']
        #ignore = shutil.ignore_patterns('ConnectionStrings','ServiceModel.Client','Web.config','SessionState')
 
        
    def __init__(self,run_sql,version_key):

        self.read_config()
        if os.path.exists(log_path):
            os.remove(log_path)
        logging.basicConfig(filename=log_path, level=logging.DEBUG)
        self.run_sql=run_sql
        logging.warn('run sql value from the gui is:{}'.format(self.run_sql))
        print ('run sql value from the gui is:{}'.format(self.run_sql))
        self.version_key=version_key
        logging.warn('version key which recived from the gui id : {}'.format(self.version_key))
        print ('version key which recived from the gui id : {}'.format(self.version_key))


    def s3_all_actions(self):
        s3=S3_func.S3(main_prop['copy_from_folder'],s3_properties['zip_name'],s3_properties['bucket_name'],self.version_key,log_path)
        s3.main()
    

        
    def run_sql_scripts(self):
        sql=sql_func.SQL_Server(sql_properties['server_ip'],main_prop['copy_from_folder'],sql_properties['user'],sql_properties['password'],sql_properties['DB_name'],log_path)
        sql.execute_sql_files()
    
    def update_version(self,version_desc):
        version_file=os.path.abspath(os.path.join(main_prop['version_folder_path'], 'version.txt'))
        with open(version_file,'w+') as f:
            f.write(version_desc)
            f.close
        for folder in filelist:
            #bin
            target_dir=os.path.abspath(os.path.join(main_prop['version_folder_path'], folder))
            self.create_folder_if_not_exist(target_dir)
            #new version
            source_dir=os.path.abspath(os.path.join(main_prop['copy_from_folder'],folder))
            if os.path.exists(source_dir):
                for subfolder in os.listdir(source_dir):
                    config=self.verify_file_not_config(subfolder)
                    #if file is not config file and we can delete it
                    if not config:
                        self.replace_item(subfolder,target_dir,source_dir)
            else:
                logging.warn('Please notice that you mention the folder you want to copy from new version correctly:, this folder not exist in new version {}'.format(source_dir))
                raise ValueError('folder is not exist in the new varsion')

    def create_backup_for_bin(self):
        #the backup folder -A combination of the folder from the configuration file and the current date and time
        backup_path=os.path.join(main_prop['backup_bin'], datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        copy_tree(main_prop['version_folder_path'],backup_path)
        logging.warn('create backup folder with last version with in this path: {}'.format(backup_path))
        print ('create backup folder with last version with in this path: {}'.format(backup_path))


    def get_subfolders_list(self,dir_path):
        root=dir_path
        dirlist = [ item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item)) ]
        return dirlist

# This function gets file name
# checking if the file name contains ignore files name from config file
    def verify_file_not_config(self,filename):
        for i in ignore_files:
            if i in filename:
                logging.warn('should not delete this file : {}'.format(filename))
                #this file should not be delete
                return True
        #this file should be deleted
        logging.warn('should delete this file : {}'.format(filename))
        return False
        

    def create_folder_if_not_exist(self,path):
        if not os.path.exists(path):
            os.makedirs(path)

# This function get copy from folder and copy to folder and iten(folder/file)
# check if the item is a file or folder
# copy the item from the copy from folder to the copy to folder
# if there is a file in 
    def replace_item (self,subfolder,target_dir,source_dir):
        #bin folder
        target_file_path=os.path.abspath(os.path.join(target_dir,subfolder))
        logging.warn('start copy file : {}'.format(target_file_path))
        print ('start copy file : {}'.format(target_file_path))
        #new version
        source_file_path=os.path.abspath(os.path.join(source_dir,subfolder))
        logging.warn('start copy file : {}'.format(source_file_path))
        if os.path.exists(target_file_path):
            try:
                os.remove(target_file_path)
                shutil.copyfile(source_file_path,target_file_path)
            except:
                try:
                    shutil.rmtree(target_file_path)
                    shutil.copytree(source_file_path,target_file_path)
                except Exception as e:
                    logging.warn('something went wrong with copy this item {}'.format(target_file_path))
                    raise ValueError('folder is not exist in the new varsion')    
        #if the file/folder does not exist in the bin folder
        else:
            try:
                    shutil.copyfile(source_file_path,target_file_path)
            except:
                try:
                    shutil.copytree(source_file_path,target_file_path)
                except Exception as e:
                    logging.warn('something went wrong with copy this item  {} with this error {}'.format(target_file_path,e))
                    raise ValueError('something went wrong with copy this item  {} with this error {}'.format(target_file_path,e))    
            
    



# The main function will stop iis service-so bin folder could be updated
# if service name mentiond in config.json this service will be stoped
# create backup for current bin folder in case something will be wrong
# execute s3 functions to download and extract version 
# if user chose to run sql files which came with the new version, this function will execute it
#    def update_version_all(self):
#        self.s3_all_actions()
#        services=services_func.Services(log_path)
#        services.stop_iis()
#        if not main_prop['services_to_stop'] =="":
#            services.service_stop(main_prop['services_to_stop'])
#        self.create_backup_for_bin()
#        self.s3_all_actions()
#        if(self.run_sql):
#            self.run_sql_scripts()
#        self.update_version()
#        services.start_iis()
#        if not main_prop['services_to_stop'] =="":
#            services.service_start(main_prop['services_to_stop'])
#        logging.warn('Done Update Version!')
#        print ('Done Update Version!')


#liron=MainProgram(True,"sdfgdfgdfg")









