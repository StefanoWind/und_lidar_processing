# -*- coding: utf-8 -*-
'''
Processor of UND lidars through LIDARGO

Inputs (both hard-coded and available as command line inputs in this order):
    sdate [%Y-%m-%d]: start date in UTC
    edate [%Y-%m-%d]: end date in UTC
    delete [bool]: whether to delete raw data
    path_config: path to general config file
    mode [str]: serial or parallel
'''
import os
cd=os.path.dirname(__file__)
import sys
import traceback
import warnings
import lidargo as lg
from datetime import datetime
import yaml
from multiprocessing import Pool
import logging
import re
import glob

warnings.filterwarnings('ignore')

#%% Inputs

#users inputs
if len(sys.argv)==1:
    sdate='2022-04-13' #start date
    edate='2022-04-14' #end date
    delete=False #delete raw files?
    path_config=os.path.join(cd,'configs/config_und.yaml') #config path
    mode='serial'
else:
    sdate=sys.argv[1] #start date
    edate=sys.argv[2]  #end date
    delete=sys.argv[3]=="True" #delete raw files?
    path_config=sys.argv[4]#config path
    mode=sys.argv[5]
    
#%% Initalization

#configs
with open(path_config, 'r') as fid:
    config = yaml.safe_load(fid)

#initialize main logger
logfile_main=os.path.join(cd,'log',datetime.strftime(datetime.now(), '%Y%m%d.%H%M%S'))+'_errors.log'
os.makedirs('log',exist_ok=True)

#%% Functions
def format_file(file,save_path,delete,config,logfile_main):
    try:
        logfile=os.path.join(cd,'log',os.path.basename(file).replace('hpl','log'))
        lproc = lg.Format(file, config=config['path_config_format'], verbose=True,logfile=logfile)
        lproc.process_scan(replace=False, save_file=True,save_path=save_path_raw)
        
        if delete:
            os.remove(file)
            
    except:
        with open(logfile_main, 'a') as lf:
            lf.write(f"{datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')} - ERROR - Error formatting file {os.path.basename(file)}: \n")
            traceback.print_exc(file=lf)
            lf.write('\n --------------------------------- \n')
            
def standardize_file(file,save_path_stand,config,logfile_main,sdate,edate):
    date=re.search(r'\d{8}.\d{6}',file).group(0)[:8]
    if datetime.strptime(date,'%Y%m%d')>=datetime.strptime(sdate,'%Y-%m-%d') and datetime.strptime(date,'%Y%m%d')<=datetime.strptime(edate,'%Y-%m-%d'):
        try:
            logfile=os.path.join(cd,'log',os.path.basename(file).replace('nc','log'))
            lproc = lg.Standardize(file, config=config['path_config_stand'], verbose=True,logfile=logfile)
            lproc.process_scan(replace=False, save_file=True, save_path=save_path_stand)
        except:
            with open(logfile_main, 'a') as lf:
                lf.write(f"{datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')} - ERROR - Error standardizing file {os.path.basename(file)}: \n")
                traceback.print_exc(file=lf)
                lf.write('\n --------------------------------- \n')

#%% Main
for channel in config['channels']:
    
    #format all files
    files=glob.glob(os.path.join(config['path_data'],channel,'*hpl'))
    save_path_raw=os.path.join(config['path_data'],channel.replace('raw','00'))
    if mode=='serial':
        for f in files:
            format_file(f,save_path_raw,delete,config,logfile_main)
    elif mode=='parallel':
        args = [(files[i],save_path_raw,delete, config,logfile_main) for i in range(len(files))]
        with Pool() as pool:
            pool.starmap(format_file, args)
    else:
        raise BaseException(f"{mode} is not a valid processing mode (must be serial or parallel)")
        
             
    #standardize all files within date range
    files=glob.glob(os.path.join(config['path_data'],channel.replace('raw','a0'),'*.nc'))
    save_path_stand=os.path.join(config['path_data'],channel.replace('raw','b0'))
    if mode=='serial':
        for f in files:
              standardize_file(f,save_path_stand,config,logfile_main,sdate,edate)
    elif mode=='parallel':
        args = [(files[i],save_path_stand, config,logfile_main,sdate,edate) for i in range(len(files))]
        with Pool() as pool:
            pool.starmap(standardize_file, args)
    else:
        raise BaseException(f"{mode} is not a valid processing mode (must be serial or parallel)")
          

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
        
