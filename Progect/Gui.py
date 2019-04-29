import tkinter as tk
import os
import json
from tkinter import ttk
from tkinter import *
import threading
from tkinter import messagebox,Tk,Label,Button
import UpdateVersion
import run_tests
import services_func


class GUI(tk.Frame):
        
    def __init__(self,root):
        tk.Frame.__init__(self,root)
        self.read_config()
        self.root = root
        self.initialize()

    

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
        global test_prop
        filelist=configuration['file_list']
        ignore_files=configuration['ignore_files']
        s3_properties=configuration['s3_properties']
        main_prop=configuration['main_prop']
        sql_properties=configuration['sql_properties']
        log_path=main_prop['log_path']
        test_prop=configuration['tests_properties']

    def initialize(self):
        #label
        self.label=Label(self.root,text="Update Version",bg="red",fg="white")
        self.label_update_folder=Label(self.root,text="Do you want to run sql scripts with the version ?",bg="blue",fg="white")
        self.label_done=Label(self.root,text="Finish Update Version",bg="green",fg="white")
        #entry
        self.version_name=Text(self.root,height=2,width=70)
        #checkbox
        self.var=IntVar()
        self.var2=IntVar()
        self.checkbox=Checkbutton(self.root,text="run sql files",variable=self.var)
        self.checkbox1=Checkbutton(self.root,text="check gnt&get_ad",variable=self.var2)
        #button
        self.button1 = Button(self.root,text="Submit",fg="red",command=lambda:self.retrieve_input(self.version_name,self.var,self.var2))
        self.frame=Frame(self.root,width=1600,height=1500)
        self.label.grid(row=0)
        self.version_name.grid(row=1)
        self.label_update_folder.grid(row=3)
        self.checkbox.grid(row=4)
        self.checkbox1.grid(row=5)
        self.button1.grid(row=6)
        self.processing_bar = ttk.Progressbar(self.root, orient='horizontal', mode='indeterminate')
        self.processing_bar.grid(row=7, column=0, columnspan=1, sticky='EWNS')
        # Launch the loop once the window is loaded



    def retrieve_input(self,version_name,var,var2):
            self.processing_bar.start(interval=10)
            #self.button1.config(state="disable")
            version_key=version_name.get("1.0","end-1c")
            run_sql=bool(var.get())
            run_tests=bool(var2.get())
            try:
                global thread
                thread=threading.Thread(target=self.update_version_all,args=(version_key,run_sql,run_tests))
                thread.daemon=True
                thread.start()
            except Exception as error:
                messagebox.showinfo('Info', error)
                root.destroy()
                root.quit()


    # The main function will stop iis service-so bin folder could be updated
    # if service name mentiond in config.json this service will be stoped
    # create backup for current bin folder in case something will be wrong
    # execute s3 functions to download and extract version 
    # if user chose to run sql files which came with the new version, this function will execute it
    def update_version_all(self,version_key,run_sql,run_tests):
        main_class=UpdateVersion.MainProgram(run_sql,version_key)
        main_class.s3_all_actions()
        services=services_func.Services(log_path)
        services.stop_iis()
        print ('Stop IIS')
        if not main_prop['services_to_stop'] =="":
            services.service_stop(main_prop['services_to_stop'])
        if not main_prop['process_to_stop'] =="":
            services.process_stop(main_prop['process_to_stop'])
        main_class.create_backup_for_bin()
        if(run_sql):
            print ('Start run sql files ')
            main_class.run_sql_scripts()
        main_class.update_version(version_key)
        services.start_iis()
        print ('Start IIS')
        if not main_prop['services_to_stop'] =="":
            services.service_start(main_prop['services_to_stop'])
            print ('Start service {}',main_prop['services_to_stop'])
        self.processing_bar.stop()
        print ('Done Update Version!')
        self.button1.config(state="normal")
        if(run_tests):
            gnt=self.check_gnt()
            get_ad=self.check_getad()
            if(not gnt):
                messagebox.showinfo('Info', 'gnt is not working ,please check!')
            else:
                if(not get_ad):
                    messagebox.showinfo('Info', 'get-ad is not working ,please check!')   
                else:
                    messagebox.showinfo('Info', 'gnt and get-ad working fine,process complete!')


        root.destroy()
        root.quit()


    def check_gnt(self):
        test_class=run_tests.tests(test_prop['gnt_url'],test_prop['getad_url'])
        gnt=test_class.check_gnt()
        return gnt

    def check_getad(self):
        test_class=run_tests.tests(test_prop['gnt_url'],test_prop['getad_url'])
        get_ad=test_class.check_get_ad()
        return get_ad


root=tk.Tk()
GUI(root)

root.mainloop()


