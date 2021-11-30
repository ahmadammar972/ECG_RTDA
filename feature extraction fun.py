# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 15:35:38 2021

@author: 100840150
"""
import json
import neurokit2 as nk
import pandas as pd
import numpy as np

def conv(data):
    data=data[0]['value']
    
    for key, value in  data.items():
        pass
    res=[]
    for i in value:
        s=i.split(',')
        s=s[1:-1]
        res.extend([float(j) for j in s])
        
    data=np.array(res)
    return data

def ecg_feature_extraction(data):
    data=conv(data)
    """this function take the ecg data as colum and return P Wave	R Interval	ST Segment	
        QRS Complex	 T Wave and	QT Interval.	
        ref :https://nurse.org/articles/how-to-read-an-ECG-or-EKG-electrocardiogram/
        input data json / output data json         '{"p_wave":[ p_wave],"pr_interval":[ pr],"qt_interval":[ qt],"t_wave":[ t_wave],"st_interval":[ st],"qrs":[ qrs]}'"""
    

    sample_rate=450

    signals, info = nk.ecg_process( data, sampling_rate=sample_rate)

        #calculate p_wave  = p start - p end / sample rate
        # ms=s*1000
    pi=signals['ECG_P_Onsets'][signals['ECG_P_Onsets'] == 1].index[0]
    pe=signals['ECG_P_Offsets'][signals['ECG_P_Offsets'] == 1].index[0]
    p_wave=(pe-pi)/sample_rate
        
        # pr pr interval start of p -start of r /sample rate
    ri=signals['ECG_R_Onsets'][signals['ECG_R_Onsets'] == 1].index[0]
    pr=(ri-pi)/ sample_rate
      
        # qt interval end of p - end of t /sample rate
    te= signals['ECG_T_Offsets'][ signals['ECG_T_Offsets'] == 1].index[0]
    qt=(te-pe)/ sample_rate
        
        #t wave =  t start - t end / sample rate
    ti= signals['ECG_T_Onsets'][ signals['ECG_T_Onsets'] == 1].index[0]  
    t_wave=(te-ti)/ sample_rate  
        
        #ST end of r - start of t /sample rate
    re= signals['ECG_R_Offsets'][ signals['ECG_R_Offsets'] == 1].index[0]
    st=(ti-re)/ sample_rate
        
        #qrs end of p  - end of r /sample rate
    qrs=(re-pe)/ sample_rate

    dic={"p_wave":[ p_wave],"pr_interval":[ pr],"qt_interval":[ qt],"t_wave":[ t_wave],"st_interval":[ st],"qrs":[ qrs]}
    json_object = json.dumps(dic)
    return json_object

############################################3
#test code#

import pandas as pd
data=pd.read_csv('https://raw.githubusercontent.com/Badr1600/ksql_ecg_udf_function/main/ecg_data_sample_1.csv',header=None)
############################################
with open('messages_ECG_ROW_DATA_AGGREGATED_1.json', 'r') as myfile:
    data=json.load(myfile)
    
r=ecg_feature_extraction(data)
