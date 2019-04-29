import sys
import configparser
sys.path.append("C:\\Users\\liron.b\\AppData\\Local\\Continuum\\anaconda3")
sys.path.append("C:\\Users\\liron.b\\AppData\\Local\\Continuum\\anaconda3\\lib")
print(sys.path)
import boto3
print(sys.path)
import logging
import zipfile
import os
import shutil


class S3:




    def __init__(self,folder,file_name,bucket,s3_version_path,log_path):
        logging.basicConfig(filename=log_path, level=logging.DEBUG)
        #get from config
        #example : c:\Copy\server
        self.local_folder=folder
        logging.warn('initialize S3 class with this local folder name:{}'.format(self.local_folder))
        #get from config
        #example : liron.zip
        self.local_file_name=file_name
        logging.warn('initialize S3 class with this local local file name:{}'.format(self.local_file_name))
        self.full_local_path=os.path.join(self.local_folder,self.local_file_name)
        #get from config
        #example : "artimedia-versions"
        self.bucket=bucket
        logging.warn('initialize S3 class with this bucket:{}'.format(self.bucket))
        #get it from label
        #example : 'Server/141.0.0/141.0.0_09-04-2018-11-59-release.zip'
        self.s3_version=s3_version_path
        logging.warn('initialize S3 class with this s3_version:{}'.format(self.s3_version))



    def verify_folder(self):
        ##if the folder is already exist
        if  os.path.exists(self.local_folder):
            logging.warn('This folder: {} which we copy from is already exist'.format(self.local_folder))
            print ('This folder: {} which we copy from is already exist'.format(self.local_folder))
            #if the folder is not empty
            if (os.listdir(self.local_folder)):
                for the_file in os.listdir(self.local_folder):
                    file_path = os.path.join(self.local_folder, the_file)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        logging.warn('failed to remove this file: {} with this exception: {}'.format(file_path,e))
                        print ('failed to remove this file: {} with this exception: {}'.format(file_path,e))
            else:
                logging.warn('the copy from folder is already exist and its empty')
        else:
            os.makedirs(self.local_folder)
            logging.warn('created new folder :{}'.format(self.local_folder))
            

    def downloads3 (self):
        logging.debug("liron")
        s3 = boto3.resource('s3')
        try:
            s3.Bucket(self.bucket).download_file(self.s3_version,self.full_local_path)
            logging.warn("download new version to this local path:{}".format(self.full_local_path))
            print ("download new version to this local path:{}".format(self.full_local_path))
        except Exception as e:
            logging.warn("got exception: {}".format(e))
            logging.warn("The object does not exist in s3, please check again")
            raise


    def extract_zip (self):
        zip_ref = zipfile.ZipFile(self.full_local_path, 'r')
        zip_ref.extractall(self.local_folder)
        logging.warn('extract this zip :{}'.format(self.full_local_path))
        print ('extract this zip :{}'.format(self.full_local_path))
        zip_ref.close()


    def main(self):
        self.verify_folder()
        self.downloads3()
        self.extract_zip()
