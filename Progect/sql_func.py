import pyodbc 
from glob import iglob
import logging
import os

class SQL_Server:

 
    def __init__(self,ip,folder_script_path,DB_user,DB_password,DB_name,log_path):
        logging.basicConfig(filename=log_path, level=logging.WARNING)
        self.ip=ip
        logging.warn('initialize Sql_Server class with this IP:{}'.format(self.ip))
        print ('initialize Sql_Server class with this IP:{}'.format(self.ip))
        self.folder_script_path=folder_script_path
        logging.warn('initialize Sql_Server class with this folder script path:{}'.format(self.folder_script_path))
        print ('initialize Sql_Server class with this folder script path:{}'.format(self.folder_script_path))
        self.DB_user=DB_user
        logging.warn('initialize Sql_Server class with DB_user:{}'.format(self.DB_user))
        print ('initialize Sql_Server class with DB_user:{}'.format(self.DB_user))
        self.DB_password=DB_password
        logging.warn('initialize Sql_Server class with this DB password:{}'.format(self.DB_password))
        print ('initialize Sql_Server class with this DB password:{}'.format(self.DB_password))
        self.DB_name=DB_name
        logging.warn('initialize Sql_Server class with this DB name:{}'.format(self.DB_name))
        print ('initialize Sql_Server class with this DB name:{}'.format(self.DB_name))
        


    def run_sql_file(self,script_name):
        con = pyodbc.connect('Trusted_Connection=yes', driver = '{ODBC Driver 13 for SQL Server}',server =self.ip, database = self.DB_name,user=self.DB_user,password=self.DB_password)
        try:
            cursor = con.cursor()
            logging.warn('connected to the DB :{}'.format(self.DB_name))
            print ('connected to the DB :{}'.format(self.DB_name))
            sql_file_path=os.path.join(self.folder_script_path,script_name)
            #open sql script file
            f = open(sql_file_path)
            full_sql = f.read() 
            #execute
            cursor.execute(full_sql)
            #close connection
            cursor.close()
            del cursor
            con.close()
            logging.warn('run sql script successfully :{} '.format(sql_file_path))
            print ('run sql script successfully :{} '.format(sql_file_path))
        except:
            logging.warn('faild connect to DB')
        

    def execute_sql_files(self):
        for name in os.listdir(self.folder_script_path):
                if name.endswith('.sql'):
                    logging.warn('found this sql file{}'.format(name))
                    print ('found this sql file{}'.format(name))
                    self.run_sql_file(name)

