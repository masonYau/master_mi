#!/usr/bin/env python
# coding: utf-8

# # Master MI Import
# ## Data Import Dependency
# **Incoming Doc Registry**<br>
# Depends on:
# <ul>
# <li>QV Files</li>
# </ul>
#
# **Stage 1**<br>
# Depends on:
# <ul>
# <li>QV Files</li>
# <li>cdd_review_dt_wkly</li>
# <li>BAU Cust Info RM (CI to CIN)</li>
# </ul>
#
# **MGCSM CM List**<br>
# Depends on:
# <ul>
# <li>horis_mg</li>
# </ul>
#

# # Hyperlink

# [Start of Import Data](#Import_Data)

# # Import Necessary Package
#
# The cell below is for import necessary package to run the file.

# In[1]:


import pandas as pd
import numpy as np
import time
import datetime as DT
# from datetime import datetime
import os
from master_mi_config import as_datetime, get_section
pd.set_option('display.max_columns', None)

_IMPORT_CONFIG = get_section("import")


# In[2]:


pd.__version__
# np.__version__


# # Set Files' Name to Variables
# <a id='import_file_path'></a>

# In[3]:


T90BBRM_File = _IMPORT_CONFIG["T90BBRM_File"]
IMIS_File = _IMPORT_CONFIG["IMIS_File"]
RMAnaInfo_File = _IMPORT_CONFIG["RMAnaInfo_File"]
CSEM_USBL_File = _IMPORT_CONFIG["CSEM_USBL_File"]

S1_Report_Raw_File = _IMPORT_CONFIG["S1_Report_Raw_File"]
CurtArr_File = _IMPORT_CONFIG["CurtArr_File"]
RMInfo_File = _IMPORT_CONFIG["RMInfo_File"]

#TriTgr_File = './Auto Trigger log sheet_20250728.xlsx'

AccClose_File = _IMPORT_CONFIG["AccClose_File"]
OffCRTAPP_File = _IMPORT_CONFIG["OffCRTAPP_File"]
QCAdj_File = _IMPORT_CONFIG["QCAdj_File"]
MSC_File = _IMPORT_CONFIG["MSC_File"]

MGCSM_File = _IMPORT_CONFIG["MGCSM_File"]

MstGrp_File = _IMPORT_CONFIG["MstGrp_File"]

RAM_FileName = _IMPORT_CONFIG["RAM_FileName"]
HR01_File = _IMPORT_CONFIG["HR01_File"]
SCC_File = _IMPORT_CONFIG["SCC_File"]

KPI_File = _IMPORT_CONFIG["KPI_File"]
SMS_File = _IMPORT_CONFIG["SMS_File"]

####### T0 Date Checking for KYC Ops CM （no need to change)#######
KYCOpsCM_StartDate = as_datetime(_IMPORT_CONFIG["KYCOpsCM_StartDate"])
KYCOpsCM_EndDate = as_datetime(_IMPORT_CONFIG["KYCOpsCM_EndDate"]) ####### To be updated after confirm no KYC CM #######

####### Please this field to last day #######
MICutOffDate = as_datetime(_IMPORT_CONFIG["MICutOffDate"])


# In[4]:


# GPRM_Name = pd.Series(['JOHN C DENG', 'KERRY H M HUNG'])

# CMTkr_FileIndex = {'AlexKFLi' : 'Alex K F LI',
#                   'ConiCTLeung' : 'Coni C T LEUNG',
#                   'GalieKYLee' : 'Galie K Y LEE',
#                   'HelenHLLeung' : 'Helen H L LEUNG',
#                   'JohnGXLong' : 'John G X LONG',
#                   'KarlKWMan' : 'Karl K W MAN',
#                   'LoritaVCChan' : 'Lorita V C CHAN',
#                   'MarcoYOChung' : 'Marco Y O CHUNG',
#                   'MaryLNCheung' : 'Mary L N CHEUNG',
#                   'PeggyCYFan' : 'Peggy C Y FAN',
#                   'RubyQYChen' : 'Ruby Q Y CHEN'}


# # List of Functions
# All the function must be run at least one time before importing data.<br>
# Specific functions' descriptions are as below:-

# ## TimeSpent(start, stop)
# The function is for displaying time spent in a proper format (i.e. in sec, min or hour).

# In[5]:


def TimeSpent(start, stop):
    Dt = stop - start
    Dts = stop - start
    title = 'Time Spent (sec):\t%.3f'

    if Dt > 60:
        Dt = Dt / 60
        title = 'Time Spent (min):\t%.3f'
    elif Dt > 60:
        Dt = Dt / 60
        title = 'Time Spent (hour):\t%.3f'

    print(title % Dt)

    return Dts


# ## ProcessDSFile
# ### List of Input
# **DWS**: DataFrame of Data Source<br>
# **InColS**: (Default: _Empty_) Index Column of Data Source for import, usually 'Customer ID' or 'CIN' or 'Customer Number'.<br>
# **SortField**: (Default: _Empty_) A Column Name to be sorted.<br>
# **asd**: (Default: _False_) Sorting order. Ascedning order if True.<br>
# **DateField**: (Default: _False_) Modify Column with Date to date data type.<br>
# ### Return
# The function will return sorted DataFrame and removed duplicated index.
#
#

# In[6]:


def ProcessDSFile(DWS, InCols='', SortField='', asd=False, DateField=False):

    DWS = DWS.replace('-', np.nan)
    iMax = DWS.shape[0]

    Ctr = 0
    if SortField == '':
        print('No Field was sorted.')
    else:
        #print(type(SortField))
        #print(type(asd))
        #print(type(DateField))
        if 'str' in str(type(SortField)) and 'bool' in str(type(asd)) and 'bool' in str(type(DateField)):
            Ctr = 0
        elif 'list' in str(type(SortField)) and 'list' in str(type(asd)) and 'list' in str(type(DateField)):
            Ctr = 1

            if (len(SortField) != len(asd)) or (len(SortField) != len(DateField)):
                print('Size')
                Ctr = -1

            for aVal in asd:
                if 'bool' in str(type(aVal)):
                    pass
                else:
                    print('asd')
                    Ctr = -1
            for aVal in DateField:
                if 'bool' in str(type(aVal)):
                    pass
                else:
                    print('DateField')
                    Ctr = -1

        else:
            #print('ABC')
            Ctr = -1

        if Ctr == -1:
            print('\'SortField\' & \'asd\' & \'DateField\' are not input properly.')
            return 0
    print('Import Type:\t%d' % Ctr)

    if InCols == '':
        pass
    else:

        print('Before remove NA in Index Column:\t' + str(DWS.shape))
        DWS = DWS.dropna(subset=[InCols])
        DWS = DWS.reset_index(drop=True)
        print('After remove NA in Index Column:\t' + str(DWS.shape))

    iMax = DWS.shape[0]
    for aCol in DWS.columns.tolist():
        #print(aCol)
        if 'Date' in str(aCol):
            #print('%s is a Column with Date.' % aCol)
            for i in range(0, iMax):
                #print(i)
                if 'datetime.time' in str(type(DWS.loc[i, aCol])) :
                    DWS.loc[i, aCol] = np.nan
            #print(aCol)
            DWS[aCol] = pd.to_datetime(DWS[aCol])



    if SortField == '':
        print('No Field was sorted.')
    else:

        DWS = DWS.sort_values(by=SortField, ascending=asd)

        #if Ctr == 0:
        #    DWS = DWS.sort_values(by=SortField, ascending=asd)
        #elif Ctr == 1:
        #    for j in range(len(SortField)-1, -1, -1):
        #        DWS = DWS.sort_values(by=SortField[j], ascending=asd[j])

        #return DWS

    if 'list' in str(type(InCols)):

        for aInCol in InCols:
            if aInCol == '':
                print('No Column was checked duplication.')
                #return DWS
            else:
                #DWS = DWS.dropna(subset=[InCols])
                Sel = np.logical_not(DWS.duplicated(subset=aInCol, keep='last').tolist())
                DWS = DWS[Sel]
                print('Removed Duplicated record for Column \'%s\'' % aInCol)
            pass



    elif 'str' in str(type(InCols)):
        if InCols == '':
            print('No Column was checked duplication.')
            #return DWS
        else:
            #DWS = DWS.dropna(subset=[InCols])
            Sel = np.logical_not(DWS.duplicated(subset=InCols, keep='last').tolist())
            DWS = DWS[Sel]
            #print('hi')
            print('Removed Duplicated record for Column \'%s\'' % InCols)
            pass
    else:
        print('No Column was checked duplication.')

    return DWS


# ## GetReqCol
# ### List of Input
# **MIWS**: DataFrame of Master MI<br>
# **DWS**: DataFrame of Data Source<br>
# **ImType**: String for column mapping during import, for example 'QVOpen', 'CM2', etc<br>
# **InColM**: Index Column of Master MI for import, usually 'Customer ID' or 'CIN'<br>
# **InColS**: Index Column of Data Source for import, usually 'Customer ID' or 'CIN' or 'Customer Number'<br>
# <br>
# ### Return
# The function will return a tuple of 2 arrays.<br>
# The 1st array is the list of column, including Index Column, of Master MI for receiving data.<br>
# The 2nd array is the list of column, including Index Column,of Data Source for receiving data.<br>
# (i.e. ([InColM, ColM_1, ColM_2, ...], [InColS, ColS_1, ColS_2, ...])

# In[7]:


def GetReqCol(MIWS, DWS, ImType="", InColM="", InColS=""):

    ReqColM = []
    ReqColS = []
    #print(str(type(InCol)))

    if InColM == "":
        ReqColM = []
        #ReqColS = []
    elif 'str' in str(type(InColM)):
        if InColM == "":
            ReqColM = []
            #ReqColS = []
        else:
            ReqColM.append(InColM)  #['CIN']
            #ReqColS.append(InCol)
    else:
        print('Invalid arg of InColM.')
        return 0


    if InColS == "":
        #ReqColM = []
        ReqColS = []
    elif 'str' in str(type(InColS)):
        if InColS == "":
            #ReqColM = []
            ReqColS = []
        else:
            #ReqColM.append(InCol)
            ReqColS.append(InColS) #['Customer Number']
    else:
        print('Invalid arg of InColS.')
        return 0
    #print(ReqCol)
    SCol = MIWS.columns.tolist()
    DCol = DWS.columns.tolist()
    if ImType == '':
        for aCol in DCol:
            if aCol in SCol:
                ReqColM.append(aCol)
                ReqColS.append(aCol)
    else:
        for aCol in DCol:

            tmP = str(ImType + '-' + aCol)

            if tmP in SCol:

                ReqColM.append(tmP)
                ReqColS.append(aCol)

    return ReqColM, ReqColS


# ## Adjust QV staff

# In[8]:


# staff_list_path = './staff list adjust_20230616.xlsx'
# staff_list = pd.read_excel(staff_list_path)
# staff_list = staff_list.loc[:,['Staff ID','Start Date','End Date']]
# staff_list['Staff ID'] = staff_list['Staff ID'].astype('str')

# path = os.getcwd()
# Files = os.listdir(path)
# QVType = ''
# QVF = ['QVOpen', 'QVQC', 'QVClosedAPP', 'QVClosedCAN', 'QVEsc', 'QVQA']


# In[9]:


# def adjust_qvfile(aFile, staff_id, handle_date):
#     QV_ = pd.read_excel('./' + aFile)
#     print(QV_.shape[0])
#     QV_[staff_id] = QV_[staff_id].astype('str')

#     QV_del = pd.merge(QV_, staff_list, how='left',left_on=[staff_id],right_on=['Staff ID'])
#     QV_del = QV_del.loc[(QV_del['Staff ID'] != None)&(QV_del[handle_date] != '-'),:]
#     QV_del[handle_date] = pd.to_datetime(pd.to_datetime(QV_del[handle_date]).dt.date)

#     QV_del['del_ind'] = 0

#     QV_del.loc[(QV_del['Staff ID'] != None)&(QV_del[handle_date] >= QV_del['Start Date'])&(QV_del[handle_date] <= QV_del['End Date']),['del_ind']] = 1

#     QV_final = QV_.drop(QV_del[(QV_del.del_ind == 1) ].index)
#     print(QV_final.shape[0])
#     return QV_final


# In[10]:


# for aFile in Files:
#     if aFile[:2].upper() == 'QV':
#         for i in range(0, len(QVF)):
#             if QVF[i].upper() in aFile.upper():
#                 if QVF[i] == 'QVQC':

#                     QV_ = pd.read_excel('./' + aFile)
#                     print(QV_.shape[0])
#                     QV_['Latest QC Completed by'] = QV_['Latest QC Completed by'].astype('str')

#                     QV_del = pd.merge(QV_, staff_list, how='left',left_on=['Latest QC Completed by'],right_on=['Staff ID'])

#                     QV_del['Latest QC Completion Date'] = pd.to_datetime(pd.to_datetime(QV_del['Latest QC Completion Date']).dt.date)

#                     QV_del['del_ind'] = 0

#                     QV_del.loc[(QV_del['Staff ID'] != None)&(QV_del['Latest QC Completion Date'] >= QV_del['Start Date'])&(QV_del['Latest QC Completion Date'] <= QV_del['End Date']),['del_ind']] = 1

#                     QVQC_final = QV_.drop(QV_del[(QV_del.del_ind == 1) ].index)
#                     print(QVQC_final.shape[0])
#                     QVQC_final.to_excel('./' + aFile )
#                     print('delete:\t%s' % aFile)

#                 elif QVF[i] == 'QVClosedCAN':
#                     QVClosedCAN_final = adjust_qvfile(aFile,staff_id ='Review ID',handle_date = 'Approval/Cancel Date')

#                     QVClosedCAN_final.to_excel('./' + aFile )
#                     print('delete:\t%s' % aFile)

#                 elif QVF[i] == 'QVQA':
#                     QV_ = pd.read_excel('./' + aFile)
#                     print(QV_.shape[0])
#                     QV_['Latest QA Completed by'] = QV_['Latest QA Completed by'].astype('str')

#                     QV_del = pd.merge(QV_, staff_list, how='left',left_on=['Latest QA Completed by'],right_on=['Staff ID'])

#                     QV_del['Latest QA Completion Date'] = pd.to_datetime(pd.to_datetime(QV_del['Latest QA Completion Date']).dt.date)

#                     QV_del['del_ind'] = 0

#                     QV_del.loc[(QV_del['Staff ID'] != None)&(QV_del['Latest QA Completion Date'] >= QV_del['Start Date'])&(QV_del['Latest QA Completion Date'] <= QV_del['End Date']),['del_ind']] = 1

#                     QVQA_final = QV_.drop(QV_del[(QV_del.del_ind == 1) ].index)
# #                     print(QV_final.shape[0])
#                     QVQA_final.to_excel('./' + aFile )
#                     print('delete:\t%s' % aFile)

#                 elif QVF[i] == 'QVOpen':
#                     QVOpen_final = adjust_qvfile(aFile,staff_id ='Latest DC Finalised by ID',handle_date = 'Latest DC Finalised Date')

#                     QVOpen_final.to_excel('./' + aFile )
#                     print('delete:\t%s' % aFile)

#                 elif QVF[i] == 'QVClosedAPP':
#                     QVClosedAPP_ = pd.read_excel('./' + aFile)
#                     print(aFile)

#                     QVClosedAPP_['Latest DC Finalised by ID'] = QVClosedAPP_['Latest DC Finalised by ID'].astype('str')
#                     QVClosedAPP_del = pd.merge(QVClosedAPP_, staff_list, how='left',left_on=['Latest DC Finalised by ID'],right_on=['Staff ID'])

#                     QVClosedAPP_del_1 = QVClosedAPP_del.loc[(QVClosedAPP_del['Latest DC Finalised by ID'] != '-'),:]
#                     QVClosedAPP_del_2 = QVClosedAPP_del.loc[(QVClosedAPP_del['Latest DC Finalised by ID'] == '-'),:]

#                     QVClosedAPP_del_1['Latest DC Finalised Date'] = pd.to_datetime(pd.to_datetime(QVClosedAPP_del_1['Latest DC Finalised Date']).dt.date)

#                     QVClosedAPP_del_1.loc[(QVClosedAPP_del_1['Staff ID'] != None)&(QVClosedAPP_del_1['Latest DC Finalised Date'] >= QVClosedAPP_del_1['Start Date'])&(QVClosedAPP_del_1['Latest DC Finalised Date'] <= QVClosedAPP_del_1['End Date']),['Review Reason']] = 'New to Bank'

#                     QVClosedAPP_del_1 = QVClosedAPP_del_1.drop(['Staff ID','Start Date','End Date'], axis=1)
#                     QVClosedAPP_del_2 = QVClosedAPP_del_2.drop(['Staff ID','Start Date','End Date'], axis=1)

#                     QVClosedAPP_final = pd.concat([QVClosedAPP_del_1,QVClosedAPP_del_2])

#                     QVClosedAPP_final.to_excel('./' + aFile )

#                     print('adjust:\t%s' % aFile)




# ## ImportData
# ### List of Input
# **MIWS**: DataFrame of Master MI<br>
# **DWS**: DataFrame of Data Source<br>
# **ImType**: (Default: _Empty_) String for column mapping during import, for example 'QVOpen', 'CM2', etc<br>
# **InColM**: (Default: _Empty_) Index Column of Master MI for import, usually 'Customer ID' or 'CIN'<br>
# **InColS**: (Default: _Empty_) Index Column of Data Source for import, usually 'Customer ID' or 'CIN' or 'Customer Number'<br>
# **ImMethod**: (Default: _0_) '0' means the only one file sources; '1' means the are more than 1 file sources. For example, QV Files are data sources with only one file source. But, CM Tracker is data source with more than 1 file sources.<br> For <font color='green'>Import CM Tracker</font>, this argument must be set to <font color='green'>'1'</font>. Otherwise, the entire columns will be replacd by each input for each files.<br>
# Suggest to set to _False_ all the time to avoid uncertainty due to pass by value or pass by reference.<br>
# **MapCol**: (Default: _Empty_) A tuple with 2 arrays. Each arrays define the index column (as the first element), and the 1-1 column mapping. The 1st array is the columns of Master MI while the 2ndis the columns of Data Source. For example (['CIN', 'XXX', 'YYY'], ['Customer Number', 'AAA', 'BBB']), 'XXX' and 'YYY' will be mapped by 'AAA' and 'BBB' respectively with 'CIN' and 'Customer Number' as mapping key. <br> This will override the prvious input under **ImType**, **InColM** & **InCols**.<br>
#
# ### Return
# The function will return a tuple of 2 arrays.<br>
# 1st elemet of the tuple is a DataFrame with data imported from DWS.<br>
# 2nd elemet of the tuple is a List of imported columns' name in MIWS.<br>
#
# (A copy of MIWS is made before importing, i.e. MIWS is a pass by value variable.)<br>
# ### Remarks
# This function works with **GetReqCol** function.<br>
# <br>
# Please pay attention to the parameter **MapCol**.<br>
# Since **MapCol** is a tuple of array, reference is passed, instead of value, to the ImportData Function.<br>
# As such, setting this parameter to _(aList, aList)_, where aList is an array, may cause run time error.<br>
# Try using _(aList, aList.copy())_ as **.copy()** is a function to duplicate an array instead of
#
#

# In[11]:


def ImportData(MIWS, DWS, ImType='', InColM='', InColS='', ImMethod=0, MapCol=''):

    #MapCol: Tuple of 2 array with equal dimension ([InColM, ColM_1, ColM_2, ...], [InColS, ColS_1, ColS_2, ...])


    MIWS_C = MIWS.copy(deep=True)

    DWS_C = DWS.copy(deep=True)
    #print("Pt-01")
    if MapCol == '':

        ReqColM, ReqColS = GetReqCol(MIWS_C, DWS_C, ImType, InColM, InColS)

    else:

        if not 'tuple' in str(type(MapCol)):

            print('Invalid Input for MapCol. Tuple of 2 arrays with same size is required.(Error:1)')
            return 0
        elif len(MapCol) != 2:
            print('Invalid Input for MapCol. Tuple of 2 arrays with same size is required.(Error:2)')
            return 0
        elif len(MapCol[0]) != len(MapCol[1]):

            print('Invalid Input for MapCol. Tuple of 2 arrays with same size is required.(Error:3)')
            return 0

        ReqColM = MapCol[0]
        ReqColS = MapCol[1]

        InColM = ReqColM[0]
        InColS = ReqColS[0]


#    if np.array(ReqColM[0]) == np.array(ReqColS[0]):
#        print('Column Matched!')
#    else:
#        print('Column Not Matched!')

    ExtM = MIWS_C[ReqColM]
    ExtS = DWS_C[ReqColS]

#    print('No of column:')
#    print(len(ExtM.columns.tolist()))
#    print(len(ExtS.columns.tolist()))

    #print("Pt-02")
    if InColM != '':
        #print('Be4 ReqColS:')
        #print((ReqColS))
        ExtM = ExtM.set_index(InColM)
        #print('Mid ReqColS:')
        #print((ReqColS))
        ReqColM.remove(InColM)
        #print('After ReqColS:')
        #print((ReqColS))
        #print(ExtM)


    #print("#############################################")
    if InColS != '':
        #print('Be4 ReqColS:')
        #print((ReqColS))
        ExtS = ExtS.set_index(InColS)
        ReqColS.remove(InColS)
        #print('No of column:')
        #print(len(ExtS.columns.tolist()))
        #print('After ReqColS:')
        #print((ReqColS))
        tmP = []
        if ImType != '':
            for i in ReqColS:
                tmP.append(ImType + '-' + i)
            ExtS.columns = tmP
            ReqColS = ExtS.columns.tolist()
    #print("Pt-03")
    if ImMethod:
        #Multi
        if MapCol == '':
            SelIndex = ExtM.index.intersection(ExtS.index)
            #print(ReqColS)


            #### For Debug
            for aaCol in ReqColM:
#                print(aaCol)
               ExtM.loc[SelIndex, aaCol] = ExtS.loc[SelIndex, aaCol]

            ####
            ExtM.loc[SelIndex, ReqColM] = ExtS.loc[SelIndex, ReqColS]

            if InColM != '':
                    MIWS_C = MIWS_C.set_index(InColM)
            SelIndex = MIWS_C.index.intersection(ExtM.index)
            MIWS_C.loc[SelIndex, ReqColM] = ExtM.loc[SelIndex, ReqColM]
        else:

            SelIndex = ExtM.index.intersection(ExtS.index)

            #for ik in range(0, len(ReqColM)):
            #    print(str(ReqColM[ik]) + '\t' + str(ExtS.columns.tolist()[ik]) + '\t' + str(ExtM.columns.tolist()[ik]))

            #print(ExtM.index.name, ExtS.index.name)
            ExtS.columns = ReqColM

            ExtM.loc[SelIndex, ReqColM] = ExtS.loc[SelIndex, ReqColM]

            if InColM != '':
                    MIWS_C = MIWS_C.set_index(InColM)
            SelIndex = MIWS_C.index.intersection(ExtM.index)


            MIWS_C.loc[SelIndex, ReqColM] = ExtM.loc[SelIndex, ReqColM]
    else:
        #One (Default)
        #print("Pt-04")
        if MapCol == '':
            #print("Pt-04a")
            ExtM = ExtM.merge(ExtS, how='left', left_index=True, right_index=True)
            ColList = ExtM.columns.tolist()
            for aCol in ColList:
                if '_x' in aCol:
                    ExtM = ExtM.drop(aCol, axis=1)
            ColList = ExtM.columns.tolist()
            for i in range(0, len(ColList)):
                if '_y' in ColList[i]:
                    ColList[i] = ColList[i][:len(ColList[i])-2]
            ExtM.columns = ColList
            if InColM != '':
                MIWS_C = MIWS_C.set_index(InColM)
            SelIndex = MIWS_C.index.intersection(ExtM.index)

            MIWS_C.loc[SelIndex, ReqColM] = ExtM.loc[SelIndex, ReqColM]

        else:
            #print('Hello')
            #print("Pt-04b")
            ExtM = ExtM.merge(ExtS, how='left', left_index=True, right_index=True)
            ColList = ExtM.columns.tolist()

            chk0001 = 0

            for aCol in ColList:
                if '_x' in aCol:
                    ExtM = ExtM.drop(aCol, axis=1)
                    chk0001 = 1
            ColList = ExtM.columns.tolist()
            for i in range(0, len(ColList)):
                if '_y' in ColList[i]:
                    ColList[i] = ColList[i][:len(ColList[i])-2]
                    chk0001 = 1

            if chk0001 == 0:
                for aCol in ColList:
                    if aCol in ReqColM:
                        ExtM = ExtM.drop(aCol, axis=1)

            ColList = ExtM.columns.tolist()
            #print(ReqColM)
            #print("####")
#             print(ExtM.columns)
            ExtM.columns = ReqColM
#             print(MIWS_C.head())
            if InColM != '':
                MIWS_C = MIWS_C.set_index(InColM)
            SelIndex = MIWS_C.index.intersection(ExtM.index)

            MIWS_C.loc[SelIndex, ReqColM] = ExtM.loc[SelIndex, ReqColM]
    #return 0
    #print('*********************************')
    #print(MIWS_C.head())
    #print("Pt-05")
    if InColM != '':
        MIWS_C = MIWS_C.reset_index()
    #return MIWS_C
    return MIWS_C, ReqColM


# ## FixColumnSeq
# To ensure the Columns of DataFrame of Master MI is starting with "Customer ID" then "CIN".

# In[12]:


def FixColumnSeq(MIWs01):
    MIColList = MIWs01.columns.tolist()
    if MIColList[0] == 'MI Seq':
        MIColList.remove('MI Seq')
        MIColList.append('MI Seq')

    MIColList.remove('CIN')
    MIColList.remove('Customer ID')
    MIColList.remove('Old / Dummy CID')
    MIColList.insert(0, 'Old / Dummy CID')
    MIColList.insert(0, 'CIN')
    MIColList.insert(0, 'Customer ID')


    #else:
    #    MIColList.remove('CIN')
    #    MIColList.remove('Customer ID')
    #
    #    MIColList.insert(0, 'Customer ID')
    #    MIColList.insert(0, 'CIN')
    #    MIWs01 = MIWs01.loc[:, MIColList]
    MIWs01 = MIWs01.loc[:, MIColList]
    return MIWs01


# ## Merge_MI_MIOID
# ### List of Input
# **MIWS01**: DataFrame of Master MI<br>
# **MIWs01_OldCI**: DataFrame of Data Source<br>
# **deBug**: (Default: _0_) If 1, debug message will be shown.<br>
# **MapCol**: (Default: _Empty_) A list of Column names in MIWS01.<br>
# If it is empty, the function will fill all the columns in MIWS01 to find any columns with empty value then filled by values based on Old Customer ID when available.<br>
# If it is not empty, the function will fill all the elements in MapCol in MIWS01 and locate ID with all columns are empty value then filled by values based on Old Customer ID when available.<br>
#
# ### Return
# The function will return a DataFrame.<br>
#
# (A copy of MIWS is made before importing, i.e. MIWS is a pass by value variable.)<br>
# ### Remarks
# This function works with **GetReqCol** function.
#
#

# In[ ]:


def Merge_MI_MIOID(MIWs01, MIWs01_OldCI, deBug=0, MapCol=''):

    aCopy = MIWs01.copy(deep=True)
    #MapCol.remove('MI Seq')
    if 'MI Seq' in MapCol:
        MapCol.remove('MI Seq')

    Title = aCopy.columns.tolist()

    Title.remove('MI Seq')

    NList = ['Customer ID', 'Old / Dummy CID', 'CIN', 'Customer Name']

    for aNList in NList:
        if aNList in Title:
            Title.remove(aNList)

    if MapCol == '':
        for aTit in Title:
            if deBug:
                print('Processing:\t' + str(aTit))
                print(aCopy)
            aID = aCopy['MI Seq'][aCopy[aTit].isnull()].tolist()
            FID = MIWs01_OldCI['MI Seq'].isin(aID)
            Chk01 = np.logical_not(MIWs01_OldCI[aTit][FID].isnull())
            if deBug:
                print(np.sum(Chk01))
            if np.sum(Chk01) == 0:
                if deBug:
                    print('\tNo Data for\t' + str(aTit))
                continue
            else:
                if deBug:
                    print('\tWith Data to be re-imported.')


            if np.sum(FID) > 0:
                if deBug:
                    print('\t' + str(np.sum(FID)) + ' Record(s) located.')
                Slic = MIWs01_OldCI[FID]
                aCopy = ImportData(aCopy, Slic, ImMethod=1, MapCol=(['MI Seq', aTit], ['MI Seq', aTit]))[0]
            else:
                if deBug:
                    print('\tNo Record located.')
                return MIWs01
    else:
        FID = []
        for i in range(0, len(MapCol)):
            aTit = MapCol[i]
            if deBug:
                print('Processing:\t' + str(aTit))
            aID = aCopy['MI Seq'][aCopy[aTit].isnull()].tolist()
            FID.append(aID)
        UID = set(FID[0])

        for i in range(0, len(FID)):
            UID = UID & set(FID[i])

        UID = list(UID)
        if deBug:
            print('UID:')
            print(UID)
        if len(UID) == 0:
            if deBug:
                print('\tNo Record located.')
            return MIWs01

        FID = MIWs01_OldCI['MI Seq'].isin(UID)
        if deBug:
            print('FID:')
            print(np.sum(FID))
            print(FID)

        if np.sum(FID) > 0:
            if deBug:
                print('No of record:\t' + str(len(UID)))
            Slic = MIWs01_OldCI[FID]
            MapCol.insert(0, 'MI Seq')
            aMapCol01 = MapCol.copy()
            aMapCol02 = MapCol.copy()
            aCopy = ImportData(aCopy, Slic, ImMethod=1, MapCol=(aMapCol01, aMapCol02))[0]
        else:
            if deBug:
                print('\tNo Record located.')
            return MIWs01

    return aCopy


# ## CheckDF
# ### List of Input
# **Mst_C**: DataFrame of Master MI with data imported by VBA.<br>
# **MIWs01_C**: DataFrame of Master MI with data imported by Python.<br>
# **IDCol**: Name of Index Column.<br>
# **ImportedCol**: List of Imported Column by using Python.<br>
# **allCol**: (Default: _False_) If True, display all the columns' checking, else only Columns with error are displayed.<br>
#
#
# ### Return
# Return a DataFrame of Index records showing which columns has discrepancy.<br>
#

# In[14]:


def CheckDF(Mst_C, MIWs01_C, IDCol, ImportedCol, allCol=False):
    D1 = pd.DataFrame()
    D1[IDCol] = Mst_C[IDCol]
    ImportedCol = list(set(ImportedCol))
    ImportedCol.sort()
    for aCol in ImportedCol:
        Sel = CheckCol(Mst_C, MIWs01_C, aCol, allCol=False)

        D1[aCol] = Sel
        pass
    return D1


def CheckCol(Mst_C, MIWs01_C, aCol, allCol=False):
    vVal = np.array(Mst_C[aCol].values)
    pVal = np.array(MIWs01_C[aCol].values)
    Sel = vVal != pVal
    nc = np.sum(Sel)
    if nc > 0 or allCol:
        print('Checking:\t%s\t%d' % (aCol, nc))
    return Sel

## Code for Checking Score ##
def CheckScoreCol(Mst01, MIWs02, Col, iCol):
    #Col = "QVQC-Initial Quality Score"
    #iCol = ['CIN']

    #print(MIWs02[Err[Col]][Col])
    #print(Mst01[Err[Col]][Col])

    S01 = MIWs02[Err[Col]][Col].values
    S02 = Mst01[Err[Col]][Col].values

    SD = S01 - S02
    #print(SD)

    CS = SD > 0.0000001

    print("No fo error after adjustng for truncation error:\t%d" % np.sum(CS))

#print(MIWs02['QVClosedCAN-Approval/Cancel Date'][MIWs02['CIN'] == 4579112])
#print(Mst01['QVClosedCAN-Approval/Cancel Date'][Mst01['CIN'] == 4579112])



# ## JoinOSDoc & ModifyDocReg
# For Incoming Doc Registry only
#

# In[15]:


def JoinOSDoc(DocList):
    FullList = []
    for aDoc in DocList:

        if aDoc != "":

            tmpList = aDoc.split(";#")
            for tmP in tmpList:

                if tmP in FullList:

                    pass
                else:
                    FullList.append(tmP)
                    pass
                pass
            pass
        pass
    return (";#").join(FullList)

def ModifyDocReg(IRD, CRTAppDate):
    #IRD = IRD.sort_values(by=["CIN", "Document Receive Date"])
    #print(IRD.shape)
    #CRTAppDate['QVClosedAPP-Approval/Cancel Date'] = CRTAppDate['QVClosedAPP-Approval/Cancel Date'].dt.date
    IRD["Document Receive Date"] = IRD["Document Receive Date"].dt.date
    ColTitle = IRD.columns.tolist()
#    CINs = IRD['CIN'].drop_duplicates().tolist()
#    for aCol in ColTitle:
#        if 'Document Type - ' in aCol:
#            IRD[aCol] = IRD[aCol].fillna("")


    IRD['Keep'] = False

    for i in range(0, IRD.shape[0]):
        #print('ID:\t%d' % i)
        aCIN = IRD.loc[i]['CIN']
        #print(aCIN)
        Sel00 = CRTAppDate['CIN'] == aCIN
        #print(np.sum(Sel00))
        #print(CRTAppDate.loc[Sel00, 'QVClosedAPP-Approval/Cancel Date'].values[0])
        if np.sum(Sel00) > 0:
            #print(CRTAppDate.loc[Sel00, 'QVClosedAPP-Approval/Cancel Date'].values[0])
            #print(IRD.loc[i]["Document Receive Date"])
            #print(CRTAppDate.loc[Sel00, 'QVClosedAPP-Approval/Cancel Date'].values[0])
            if CRTAppDate.loc[Sel00, 'QVClosedAPP-Approval/Cancel Date'].values[0] < IRD.loc[i]["Document Receive Date"]:
                #print('Be4:')
                #print(IRD.loc[i, 'Keep'])
                IRD.loc[i, 'Keep'] = True
                #print('After:')
                #print(IRD.loc[i, 'Keep'])
                pass
            #elif:
                #pass
            pass
        else:
            IRD.loc[i, 'Keep'] = True
        pass

    #print(IRD)
    IRD = IRD[IRD['Keep'].tolist()]
    #print(IRD)
    CINs = IRD['CIN'].drop_duplicates().tolist()
    IRD_Fin = IRD.copy(deep=True)
    IRD_Fin = IRD_Fin.drop_duplicates(subset='CIN', keep='last')
    for aCIN in CINs:
        Sel01 = IRD['CIN'] == aCIN
        tmpPD = IRD[Sel01].copy(deep=True)
        for aCol in ColTitle:
            if 'Document Type - ' in aCol:
                DocList = tmpPD[aCol].fillna("").tolist()
                DocList = JoinOSDoc(DocList)
                Sel02 = IRD_Fin['CIN'] == aCIN
                IRD_Fin.loc[Sel02, aCol] = DocList
                pass
            pass
        pass
    return IRD_Fin


# ## ImportStage1Report
# For Import Stage 1 Report

# In[16]:


def ImportStage1Report(MITemp_Copy, S1_Report_Ext, StaffList):
    start = time.time()
    #print(StaffList.columns.tolist())
    if not 'Employee Number' in StaffList.columns.tolist():
        StaffList['Employee Number'] = StaffList.index
        StaffList = StaffList.reset_index(drop=True)

    ImportedS1Col = ['S1 Report Date', 'Overall_Status_S1', 'T0 CM Name', 'T0 CM Team Head', 'T0',
                    'T30 Rmdr Letter date (Actual)', 'T60 Rmdr Letter date (Actual)', 'GWIS_Number',
                    'KYCI Curt Letter issue date (Actual)', 'S1 Remark', 'S1 Review Type', 'Activities','Acceleration Case actual T0 date','Actual Review team(After CM assignment)']

    S1RDate = []
    S1Seg = []
    S1Team = []
    S1T0CMName = []
    S1T0CMTH = []
    S1T0CMStaffID = []
    S1Act = []
    S1GWIS = []
    S1MstStatus = []
    S1T0Date = []
    S1T30ActDate =[]
    S1T60ActDate =[]
    S1KYCIActDate =[]
    S1Remark = []
    S1Type = []
    S1AccelerationT0Date = []
    S1CMTeam = []

    checkID = ['X1630071']
    checkID = ['']

    iCount = 0

    for index, row in MITemp_Copy.iterrows():
        #print('Customer ID:\t%s\t%s'% (index, row['Old / Dummy CID']))
        S1R_Sub = S1_Report_Ext[S1_Report_Ext['Customer_ID_S1'].isin([index])]
        #print('No of S1 Record:\t%d' % S1R_Sub.shape[0])
        if row['Old / Dummy CID'] != '':
            Sel = S1_Report_Ext['Customer_ID_S1'].isin([row['Old / Dummy CID']])
            #print('No of old ID record:\t%d' % np.sum(Sel))
            if np.sum(Sel) > 0:
                S1R_Sub02 = S1_Report_Ext[Sel]
                #print(index)
                #print(row['Old / Dummy CID'])
                S1R_Sub = S1R_Sub.append(S1R_Sub02)
                S1R_Sub = S1R_Sub.sort_values(by=['Date_of_Report_S1'], ascending=True)
                #print(S1R_Sub)
    #    if index in checkID:
    #        print('No of S1 Record:\t%d' % S1R_Sub.shape[0])

        TmpS1Statuscode = 0

        StrOverallStatusS1 = '00'
        StrS1Remark = ""
        StrT0IssueDate = ""
        StrActivities = ""
        StrCMTeam = ""
        TmpS1ReportDate = 0
        TmpCMAssignDate = 0
        TmpT0IssueDate = 0
        TmpT30RmdLttrDate = 0
        TmpT60RmdLttrDate = 0
        TmpCurtLttrDate = 0

        TmpAccelerationT0Date = ""

        CanCode = ''
        OldCanCode = ''

        StrCMID = 0
        StrCMName_Tmp = ''
        StrCMTH = ''
        S1ReviewType = ''

        StrCMBSegment = ''
        StrGWISNo = ''
        StrCusName = ''

        Condcheck = False
        T0Record = False

        if S1R_Sub.shape[0] > 0:

            for sub_i, sub_Row in S1R_Sub.iterrows():

                #Condcheck = False
                #T0Record = False

                if sub_Row['S1 Master Status'] != '':

                    TmpS1Statuscode = int(sub_Row['S1 Master Status'][:2])
                    if TmpS1Statuscode == 40:
                        T0Record = True
                    #try:
                    #    TmpS1Statuscode = int(sub_Row['S1 Master Status'][:2])
                    #except TypeError:
                    #    print(sub_i)
                    #    print(index)
                    #    print(sub_Row['S1 Master Status'])

                else:
                    TmpS1Statuscode = 0
                #print('%s\t%d' % (sub_Row['S1 Master Status'], (TmpS1Statuscode)))

                OldCanCode = CanCode

                if sub_Row['Cancellation Code'] != '':
                    #print(CanCode)
                    CanCode = sub_Row['Cancellation Code'][:5]
                else:
                    CanCode = 0

                if index in checkID:
                    print("S1-01")
                    print(StrOverallStatusS1)
                    print(TmpS1Statuscode)

                #if (int(StrOverallStatusS1[:2]) <= TmpS1Statuscode) and ((CanCode != '008-1')):
                if (int(StrOverallStatusS1[:2]) <= TmpS1Statuscode):
                    #TmpS1Statuscode = int(sub_Row['S1 Master Status'][:2])

                    if (CanCode != '008-1') or (int(StrOverallStatusS1[:2]) == 0) or (CanCode == OldCanCode) :
                        StrOverallStatusS1 = sub_Row['S1 Master Status']
                        StrS1Remark = sub_Row['Remark_S1']
                        StrCMID = sub_Row['Case_Manager_Staff_ID_S1']
                        StrCMName_Tmp = sub_Row['Case_Manager_Email_S1']
                        StrCMTH = sub_Row['Case_Manager_Team_Head']
                        #StrActivities = sub_Row['Activities_S1']
                        S1ReviewType = sub_Row['Type']

                        StrCMBSegment = sub_Row['CMB_Segment_S1']
                        StrGWISNo = sub_Row['GWIS_Number_S1']
                        StrCusName = sub_Row['Customer_Name']
                        StrCMTeam = sub_Row['Actual Review team(After CM assignment)']

                        StrActivities = sub_Row['Activities_S1']

                        #TmpAccelerationT0Date = sub_Row['Date_of_T+0_Issue_S1']


                        if TmpS1Statuscode == 40:
                        #if (not pd.isnull(sub_Row['Date_of_T+0_Issue_S1'])):
                        #if (sub_Row['S1 Master Status'] == '40 - T0 initiated'):

                            #if sub_Row['Acceleration Case actual T0 date'] != '':
                                #TmpT0IssueDate = sub_Row['Acceleration Case actual T0 date']
                            if ('Annual' not in sub_Row['Activities_S1']) and (sub_Row['CRT initiated date'] != ''):
                                TmpT0IssueDate = sub_Row['CRT initiated date']
                            else:
                                TmpT0IssueDate = sub_Row['Date_of_T+0_Issue_S1']
                        else:
                            TmpT0IssueDate = sub_Row['Date_of_T+0_Issue_S1']

                        if sub_Row['Acceleration Case actual T0 date'] != '':
                            TmpAccelerationT0Date = sub_Row['Acceleration Case actual T0 date']
                        else:
                            TmpAccelerationT0Date = ''

                        if (sub_Row['Date_of_Report_S1'] != ''):
                            TmpS1ReportDate = sub_Row['Date_of_Report_S1']

                        if (sub_Row['Date_of_T30_Physical_Letter (ACTUAL)'] != ''):
                            TmpT30RmdLttrDate = sub_Row['Date_of_T30_Physical_Letter (ACTUAL)']

                        if (sub_Row['Date_of_T60_Physical_Letter (ACTUAL)'] != ''):
                            TmpT60RmdLttrDate = sub_Row['Date_of_T60_Physical_Letter (ACTUAL)']

                        if (sub_Row['KYCI Curtailment Letter Issue Date (ACTUAL)'] != ''):
                            TmpCurtLttrDate = sub_Row['KYCI Curtailment Letter Issue Date (ACTUAL)']
                        pass



                else:

                    Condcheck = ((TmpS1Statuscode > 32) or (TmpS1Statuscode < 30))

                    #if index in checkID:

                    #    print(Condcheck)

                    Condcheck = Condcheck and TmpS1Statuscode > 0
                    #if index in checkID:
                    #    print(Condcheck)
                    #    print(pd.isnull(row['QVClosedAPP-Approval/Cancel Date']))
                    #    print(row['Last KYC Date'])



                    LastKYCDate = DT.datetime(2015, 1, 1, 0, 0)
                    CancelDate = DT.datetime(2015, 1, 1, 0, 0)

                    if (not pd.isnull(row['QVClosedCAN-Approval/Cancel Date'])):
                        CancelDate = row['QVClosedCAN-Approval/Cancel Date']


                    if (not pd.isnull(row['QVClosedAPP-Approval/Cancel Date'])) and (not pd.isnull(row['Last KYC Date'])):

                        if row['QVClosedAPP-Approval/Cancel Date'] >= row['Last KYC Date']:
                            LastKYCDate = row['QVClosedAPP-Approval/Cancel Date']
    #                        if index in checkID:
    #                            print("A1")
                        else:
                            LastKYCDate = row['Last KYC Date']
    #                        if index in checkID:
    #                            print("A2")
                    elif (pd.isnull(row['QVClosedAPP-Approval/Cancel Date'])) and (pd.isnull(row['Last KYC Date'])):
                        LastKYCDate = DT.datetime(2015, 1, 1, 0, 0)
    #                    if index in checkID:
    #                        print("B")
                    elif (pd.isnull(row['QVClosedAPP-Approval/Cancel Date'])) and (not pd.isnull(row['Last KYC Date'])):
                        LastKYCDate = row['Last KYC Date']
    #                    if index in checkID:
    #                        print("C")
                    else:
                        LastKYCDate = row['QVClosedAPP-Approval/Cancel Date']
    #                    if index in checkID:
    #                        print("D")

#                     Condcheck = Condcheck and (sub_Row['Date_of_Report_S1'] > LastKYCDate)
    #                if index in checkID:
    #                    print('*****')
    #                    print(sub_Row['Date_of_Report_S1'] )
    #                    print(LastKYCDate)
    #                    print(Condcheck)
####                    if (LastKYCDate < TmpT0IssueDate):
####                        Condcheck = False

                    if (TmpS1ReportDate == sub_Row['Date_of_Report_S1']):
                        if ((StrOverallStatusS1[0] == '3') and (StrOverallStatusS1[:2] != '39')):
                            Condcheck = True
                        if (StrOverallStatusS1[0] == '4'):
                            Condcheck = False

                    # Only get 'to be start' status for case completed / cancelled
                    if LastKYCDate > TmpS1ReportDate or ((CancelDate > TmpS1ReportDate) and ('008-5' not in row['QVClosedCAN-Cancellation Comments'])):
                        pass
                    else:
                        if T0Record == False:
                            # Condcheck = True
                            pass
                        else:
                            Condcheck = False


                    if Condcheck:
                        StrOverallStatusS1 = sub_Row['S1 Master Status']
                        StrS1Remark = sub_Row['Remark_S1']
                        StrCMID = sub_Row['Case_Manager_Staff_ID_S1']
                        StrCMName_Tmp = sub_Row['Case_Manager_Email_S1']
                        StrCMTH = sub_Row['Case_Manager_Team_Head']
                        #StrActivities = sub_Row['Activities_S1']
                        S1ReviewType = sub_Row['Type']

                        StrCMBSegment = sub_Row['CMB_Segment_S1']
                        StrGWISNo = sub_Row['GWIS_Number_S1']
                        StrCusName = sub_Row['Customer_Name']
                        StrCMTeam = sub_Row['Actual Review team(After CM assignment)']

                        StrActivities = sub_Row['Activities_S1']

                        #TmpAccelerationT0Date = sub_Row['Date_of_T+0_Issue_S1']

    #                    if index in checkID:
    #                        print(sub_Row['Date_of_T+0_Issue_S1'])
                        if TmpS1Statuscode == 40:
                        #if (not pd.isnull(sub_Row['Date_of_T+0_Issue_S1'])):
                        #if (sub_Row['S1 Master Status'] == '40 - T0 initiated'):

                            #if sub_Row['Acceleration Case actual T0 date'] != '':
                                #TmpT0IssueDate = sub_Row['Acceleration Case actual T0 date']
                            if ('Annual' not in sub_Row['Activities_S1']) and (sub_Row['CRT initiated date'] != ''):
                                TmpT0IssueDate = sub_Row['CRT initiated date']
                            else:
                                TmpT0IssueDate = sub_Row['Date_of_T+0_Issue_S1']
                        else:
                            TmpT0IssueDate = sub_Row['Date_of_T+0_Issue_S1']

                        if sub_Row['Acceleration Case actual T0 date'] != '':
                            TmpAccelerationT0Date = sub_Row['Acceleration Case actual T0 date']
                        else:
                            TmpAccelerationT0Date = ''

                        if (sub_Row['Date_of_Report_S1'] != ''):
                            TmpS1ReportDate = sub_Row['Date_of_Report_S1']

                        if (sub_Row['Date_of_T30_Physical_Letter (ACTUAL)'] != ''):
                            TmpT30RmdLttrDate = sub_Row['Date_of_T30_Physical_Letter (ACTUAL)']

                        if (sub_Row['Date_of_T60_Physical_Letter (ACTUAL)'] != ''):
                            TmpT60RmdLttrDate = sub_Row['Date_of_T60_Physical_Letter (ACTUAL)']

                        if (sub_Row['KYCI Curtailment Letter Issue Date (ACTUAL)'] != ''):
                            TmpCurtLttrDate = sub_Row['KYCI Curtailment Letter Issue Date (ACTUAL)']
                    pass
                #if index in checkID:
                #    if len(index) < 8:
                #        print("Result:\t%s\t\t%s" % (index, StrOverallStatusS1))
                #    else:
                #        print("Result:\t%s\t%s" % (index, StrOverallStatusS1))

                pass

#                 if sub_Row['Customer_ID_S1'] == "C1388292":
#                     print (Condcheck)
#                     print (sub_Row['Customer_ID_S1'], sub_Row['Date_of_Report_S1'], sub_Row['Case_Manager_Email_S1'], sub_Row['Case_Manager_Team_Head'], sub_Row['Activities_S1'], sub_Row['S1 Master Status'], sub_Row['Date_of_T+0_Issue_S1'])
#                     print (LastKYCDate, CancelDate, TmpS1ReportDate, row['QVClosedCAN-Cancellation Comments'])
            #print("Result:\t%s\t\t%s" % (index, StrOverallStatusS1))
            if index in checkID:
                if len(index) < 8:
                    print("Result:\t%s\t\t%s" % (index, StrOverallStatusS1))
                else:
                    print("Result:\t%s\t%s" % (index, StrOverallStatusS1))


            # Import to Array first Master MI

        if StrOverallStatusS1 == '00':
            StrOverallStatusS1 = ''
            StrS1Remark = ''
            StrT0IssueDate = ''
            StrActivities = ''
            TmpS1ReportDate = ''
            TmpCMAssignDate = ''
            TmpT0IssueDate = ''
            TmpT30RmdLttrDate = ''
            TmpT60RmdLttrDate = ''
            TmpCurtLttrDate = ''
            TmpAccelerationT0Date = ''

            StrCMID = ''
            StrCMName_Tmp = ''
            StrCMTH = ''
            S1ReviewType = ''
            StrCMName = ''
            StrCMBSegment = ''
            StrGWISNo = ''
            StrCusName = ''
            StrCMTeam = ''
            pass
        else:
            #print((TmpT0IssueDate))
            #print(pd.isnull(TmpT0IssueDate))

#             if pd.isnull(TmpT0IssueDate):
#                 #print(index)
#                 maxID = S1R_Sub['Date_of_T+0_Issue_S1'].idxmax()
#                 #print(maxID)
#                 if not pd.isnull(maxID):
#                     if (StrCMID == '' or pd.isnull(StrCMID) or StrCMID == ' '):
#                         StrCMID = S1R_Sub.loc[maxID, 'Case_Manager_Staff_ID_S1']
#                         StrCMName_Tmp = S1R_Sub.loc[maxID, 'Case_Manager_Email_S1']
#                         StrCMTH = S1R_Sub.loc[maxID, 'Case_Manager_Team_Head']
#                     if S1R_Sub.loc[maxID, 'Acceleration Case actual T0 date'] != '' and S1R_Sub.loc[maxID, 'S1 Master Status'] == '40 - T0 initiated':
#                         TmpT0IssueDate = S1R_Sub.loc[maxID, 'Acceleration Case actual T0 date']
#                     elif ('Annual' not in S1R_Sub.loc[maxID, 'Activities_S1']) and (S1R_Sub.loc[maxID, 'CRT initiated date'] != ''):
#                         TmpT0IssueDate = S1R_Sub.loc[maxID, 'CRT initiated date']
#                     else:
#                         TmpT0IssueDate = S1R_Sub.loc[maxID, 'Date_of_T+0_Issue_S1']
#                     StrActivities = S1R_Sub.loc[maxID, 'Activities_S1']
#                     TmpT30RmdLttrDate = S1R_Sub.loc[maxID, 'Date_of_T30_Physical_Letter (ACTUAL)']
#                     TmpT60RmdLttrDate = S1R_Sub.loc[maxID, 'Date_of_T60_Physical_Letter (ACTUAL)']
#                     TmpCurtLttrDate = S1R_Sub.loc[maxID, 'KYCI Curtailment Letter Issue Date (ACTUAL)']
#                     S1ReviewType = S1R_Sub.loc[maxID, 'Type']
#                     StrGWISNo = S1R_Sub.loc[maxID, 'GWIS_Number_S1']
#                     #print(TmpT0IssueDate)
#                 #print('================================')
#                 pass

            #print(StrCMID)
            #print(type(StrCMID))
            #print(S1_Report_Ext['Customer_ID_S1'].tolist()[0])
            if (not pd.isnull(StrCMID)) :
#             if (not np.isnan(StrCMID)) :
#                 print(StrCMID)
                try:
                    SelCMName = (StaffList['Employee Number'] == StrCMID)
                except:
                    SelCMName = (StaffList['Employee Number'] == int(StrCMID))
                if np.sum(SelCMName) > 0:
                    #print(index)
                    #print(StaffList['Employee Name'][SelCMName].tolist()[0])
                    StrCMName = StaffList['Employee Name'][SelCMName].tolist()[0]
                elif StrCMName_Tmp != '':
                    StrCMName = StrCMName_Tmp
                else:
                    StrCMName = ''
            else:
                StrCMName = ''

            pass

        S1RDate.append(TmpS1ReportDate)
        #S1Seg = []
        #S1Team = []
        S1T0CMName.append(StrCMName)
        S1T0CMStaffID.append(StrCMID)
        S1T0CMTH.append(StrCMTH)
        S1Act.append(StrActivities)
        S1GWIS.append(StrGWISNo)
        S1MstStatus.append(StrOverallStatusS1)
        S1T0Date.append(TmpT0IssueDate)
        S1T30ActDate.append(TmpT30RmdLttrDate)
        S1T60ActDate.append(TmpT60RmdLttrDate)
        S1KYCIActDate.append(TmpCurtLttrDate)
        S1Remark.append(StrS1Remark)
        S1Type.append(S1ReviewType)
        S1AccelerationT0Date.append(TmpAccelerationT0Date)
        S1CMTeam.append(StrCMTeam)





        iCount += 1
        #print(iCount)
        #print(len(S1RDate))
        if len(S1RDate) != iCount:
            print(index)


        #print(S1R_Sub)
        #if iCount > 100:
        #    break
        pass

    MITemp_Copy['S1 Report Date'] = S1RDate
    MITemp_Copy['T0 CM Name'] = S1T0CMName
    MITemp_Copy['T0 CM Team Head'] = S1T0CMTH
    MITemp_Copy['Activities'] = S1Act
    MITemp_Copy['GWIS_Number'] = S1GWIS
    MITemp_Copy['T0'] = S1T0Date
    MITemp_Copy['T30 Rmdr Letter date (Actual)'] = S1T30ActDate
    MITemp_Copy['T60 Rmdr Letter date (Actual)'] = S1T60ActDate
    MITemp_Copy['KYCI Curt Letter issue date (Actual)'] = S1KYCIActDate
    MITemp_Copy['S1 Remark'] = S1Remark
    MITemp_Copy['S1 Review Type'] = S1Type
    MITemp_Copy['Overall_Status_S1'] = S1MstStatus
    MITemp_Copy['Acceleration T0 Date'] = S1AccelerationT0Date
    MITemp_Copy['S1 CM Team'] = S1CMTeam

    print('Completed %d cases.' % iCount)
    stop = time.time()
    TimeSpent(start, stop)
    return MITemp_Copy.reset_index()



# # Import List of CIN & Customer ID from Master MI

# The Code below is for Importing Customer ID, CIN and Old Customer ID into Memory.<br>
# MIWsR is the Dataframe.
#
# MIWs01 is a copy of MIWsR.<br>
# We work on MIWs01 instead of MIWsR.<br>
# In case of re-work, we can use the below code:<br>
# **MIWs01 = MIWsR.copy(deep = True)**<br>
# Instead of reloading from the file to save time as it takes a few minutes to Importing the Excel File.<br>
# <br>
# <font color='brown'>_GS CDD FullList Master template.xlsx_</font> is an **Empty** Master MI file which contain a full list of Customer ID, CIN and Old Customer ID and all the necessary column fields (without value) for import.

# In[17]:


if __name__ == "__main__":
    start = time.time()


    MstTmp = pd.ExcelFile('./GS CDD FullList Master template.xlsx')
    MIWsR = pd.read_excel(MstTmp, sheet_name='GS CDD Fulllist')
    TriggerCode = pd.read_excel(MstTmp, sheetname='Info02-TriggerEventList')['Trigger Event Code'].dropna().tolist()
    StaffList = pd.read_excel(MstTmp, sheetname='info04-Staffs List')
    StaffList_c = StaffList.copy(deep=True)
    StaffList_c1 = StaffList.copy(deep=True)
    #MIWsR = pd.read_excel(io='./GS CDD FullList Master template.xlsx', sheetname='')


    MIWs01 = MIWsR.copy(deep = True)

    ImportedList = []
    stop = time.time()
    #stop - start
    TimeSpent(start, stop)


    # # Check Duplicate Customer ID and CIN

    # In[18]:


    VC_CID = MIWsR['Customer ID'].value_counts()
    SelDuCID = VC_CID > 1

    if np.sum(SelDuCID) > 0:
        print('Duplicated Customer ID record were found!')
        print(VC_CID[SelDuCID])

    else:
        print('No Duplicated Customer ID!')

    print('\n')

    VC_CID = MIWsR['CIN'].value_counts()
    SelDuCID = VC_CID > 1

    if np.sum(SelDuCID) > 0:
        print('Duplicated CIN record were found!')
        print(VC_CID[SelDuCID])
    else:
        print('No Duplicated CIN!')


    # ## Treatment on importing data based on old Customer ID
    #
    # The code below is for creating another Dataframe **MIWs01_OldCI**.<br>
    # MIWs01_OldCI is for importing data based on old Customer ID.<br>
    # If data needs to be imported based on old Customer ID, the record will be imported to MIWs01_OldCI first.<br>
    # After that, data in MIWs01_OldCI will be transferred to MIWs01 at final step.<br>
    # <br>
    # If you want to reset the DataFrame, please also run this code.

    # In[19]:


    MIWs01 = MIWsR.copy(deep = True)
    MIWs01['MI Seq'] = MIWs01.index
    MIWs01_OldCI = MIWs01.copy(deep = True)
    Sel01 = np.logical_not(MIWs01_OldCI['Old / Dummy CID'].isnull())
    if np.sum(Sel01) > 0:
        Sel02 = MIWs01_OldCI['Old / Dummy CID'] != 'both CI and CIN are dummy inf.'
        Sel = np.logical_and(Sel01, Sel02)
        MIWs01_OldCI = MIWs01_OldCI[Sel]


    # The below is for checking the Old CI record is match with MIWs01.

    # In[20]:


    OID_ID = MIWs01_OldCI.index.tolist()
    t01 = MIWs01.iloc[OID_ID]['Customer ID'].tolist()
    t02 = MIWs01_OldCI['Customer ID'].tolist()
    fc = 0
    nfc = 0
    for a in t01:
        if a in t02:
            fc += 1
            pass
        else:
            nfc += 1
            print(a + ' is not found.')

    if nfc > 0 :
        print("Please check Old Customer ID.")
        print('%d record unmatched.' % nfc)
    else:
        print('Checked %d cases.' % fc)
        print('No unmatched record.')

    wError = 0


    # # For Reset all input to default

    # In[21]:


    MIWs01 = MIWsR.copy(deep = True)
    ImportedList = []
    MIWs01 = MIWsR.copy(deep = True)
    MIWs01['MI Seq'] = MIWs01.index
    MIWs01_OldCI = MIWs01.copy(deep = True)
    Sel01 = np.logical_not(MIWs01_OldCI['Old / Dummy CID'].isnull())
    if np.sum(Sel01) > 0:
        Sel02 = MIWs01_OldCI['Old / Dummy CID'] != 'both CI and CIN are dummy inf.'
        Sel = np.logical_and(Sel01, Sel02)
        MIWs01_OldCI = MIWs01_OldCI[Sel]
    OID_ID = MIWs01_OldCI.index.tolist()
    t01 = MIWs01.iloc[OID_ID]['Customer ID'].tolist()
    t02 = MIWs01_OldCI['Customer ID'].tolist()
    fc = 0
    nfc = 0

    StaffList = StaffList_c.copy(deep=True)

    for a in t01:
        if a in t02:
            fc += 1
            pass
        else:
            nfc += 1
            print(a + ' is not found.')

    if nfc > 0 :
        print("Please check Old Customer ID.")
        print('%d record unmatched.' % nfc)
    else:
        print('Checked %d cases.' % fc)
        print('No unmatched record.')

    wError = 0


    # <a id='Import_Data'></a>
    # # Import Data Source for Master MI Update
    #
    # ## Introduction
    #
    # The follpowing sections are for Importing different data soruce from different file to Master MI DataFrame.<br>
    # As usual, not all the record can be captured by Customer ID but with old Customer ID.<br>
    # (For those based on CIN will not have this problem.)<br>
    # So, the following code will also import data based on Old Customer ID and merge with Master MI based on current Customer ID.<br>
    # At the same time, the imported value will be changed to the correct format or value for some kind of record.<br>
    # <br>
    # User can run specifc code for specific data import.

    # # Import CM Trackers
    # Please update the file name (in brown) for the code below in the following cell.<br>
    #
    # ImMethod must be <font color='red'>1</font> when using ImportData.

    # [Return to Import File Path](#import_file_path)

    # [Jump to Export Result](#export_result)

    # In[22]:


    # %%time

    # path = os.getcwd()
    # Files = os.listdir(path)
    # CMTkrs = []
    # ColumnsToDrop = ['CM2-T90 Letter Issue Arrangement', 'CM2-T90 Letter - Not issue Remarks']
    # for aFile in Files:

    #     if aFile[-5:] == '.xlsx' or aFile[-5:] == '.xlsm':

    #         if 'CM_Tracker_' in aFile:
    #             print("This is a CM Tracker:\t" + aFile)
    #             tmpDF = pd.read_excel('./' + aFile, sheetname='GSCDD CMTracker')
    #             tmpDF['T0'] = pd.to_datetime(tmpDF['T0'], errors='coerce')
    #             tmpDF = tmpDF.sort_values(by=['T0'], ascending=False)
    #             tmpDF =  tmpDF.drop_duplicates(subset='Customer ID', keep='first')
    #             tmpColumnList = tmpDF.columns.tolist()

    #             for aCol in ColumnsToDrop:
    #                 if aCol in tmpColumnList:
    #                     tmpDF = tmpDF.drop(aCol, axis=1)
    #                 else:
    #                     if 'DATE' in aCol.upper():
    #                         tmpDF[aCol] = pd.to_datetime(tmpDF[aCol], errors='coerce')
    #                     elif 'All Doc Received'.upper() in aCol.upper():
    #                         tmpDF[aCol] = tmpDF[aCol].replace(0, False)
    #                         tmpDF[aCol] = tmpDF[aCol].replace(1, True)
    #                         tmpDF[aCol] = tmpDF[aCol].astype('bool')
    #             tmpDF['CM Team Head'] = CMTkr_FileIndex[aFile.split('_')[2].split('-')[0].split('.')[0]]
    #             CMTkrs.append(tmpDF)
    #             CMTkrs[len(CMTkrs) -1].name = aFile


    #         else:
    #             print("Skipped:\t%s" % aFile)

    #     else:
    #         print("This is not an Excel File:\t" + aFile)
    # print('\nLoaded %d CM Tracker to Memory.\n' % len(CMTkrs))


    # In[23]:


    # %%time
    # ####### Update Using Customer ID

    # for aCMTrk in CMTkrs:
    #     print('Importing:\t%s' % aCMTrk.name)
    #     MIWs01_OldCI, LTitle = ImportData(MIWs01_OldCI, aCMTrk, ImType='CM2', InColM='Old / Dummy CID', InColS='Customer ID', ImMethod=1)
    #     MIWs01  = ImportData(MIWs01, aCMTrk, ImType='CM2', InColM='Customer ID', InColS='Customer ID', ImMethod=1)[0]
    #     MIWs01 = Merge_MI_MIOID(MIWs01, MIWs01_OldCI, 0, LTitle)
    #     ImportedList += LTitle
    # ImportedList = list(set(ImportedList))


    # In[24]:


    # for aCol in ImportedList:
    #     if aCol != 'MI Seq':
    #         print(aCol)
    #         if 'DATE' in aCol.upper():
    #             MIWs01[aCol] = pd.to_datetime(MIWs01[aCol], errors='coerce')
    # #         elif 'DAYS' in aCol.upper():
    # #             MIWs01[aCol] = MIWs01[aCol].astype('str').str.strip().astype('int', errors='ignore')
    #         else:
    #             MIWs01[aCol] = MIWs01[aCol].astype('str').str.strip()


    # In[25]:


    ####### Update Using CIN


    #for aCMTrk in CMTkrs:
    #    print('Importing:\t%s' % aCMTrk.name)
    #    #MIWs01_OldCI, LTitle = ImportData(MIWs01_OldCI, aCMTrk, ImType='CM2', InColM='Old / Dummy CID', InColS='Customer ID', ImMethod=1)
    #    MIWs01, LTitle = ImportData(MIWs01, aCMTrk, ImType='CM2', InColM='CIN', InColS='CIN', ImMethod=1)
    #    ImportedList += LTitle
    #    ImportedList = list(set(ImportedList))

    #print('\nImported for:')
    #print(LTitle)
    #print('\nImported CM Trackers to Master MI.')


    # ## Import "Tri-TgrTriage Status" & "Tri-TgrTriage Completion Date"
    # Please update the file name (in brown) for the code below in the following cell.<br>
    # TriTgr = pd.read_excel(io='./<font color='brown'>Auto Trigger log sheet_19 Aug 2019.xlsx</font>')<br>
    # <br>
    # Please noted that the record is carries forward.<br>
    # <br>
    # To import <font color='brown'>Auto Trigger log sheet.xlsx</font>, please set **Update_TgrTriage** to <font color='red'>1</font>.<br>
    # To not import <font color='brown'>Auto Trigger log sheet.xlsx</font>, please set **Update_TgrTriage** to <font color='red'>0</font>.<br>

    # [Return to Import File Path](#import_file_path)

    # [Jump to Export Result](#export_result)

    # In[26]:


    # # Update_TgrTriage = 0
    # Update_TgrTriage = 1

    # if Update_TgrTriage:
    #     start = time.time()

    #     TriTgr = pd.read_excel(io=TriTgr_File)
    #     TriTgr = TriTgr[['Customer_CIN', 'Customer_ID', 'Customer_Name', 'CMB_Segment', 'Date from QV', 'TgrTriage Status', 'TgrTriage Completion Date']]

    #     TriTgr = ProcessDSFile(TriTgr, InCols='Customer_ID', SortField='Date from QV', DateField=True, asd=True)

    #     MIWs01, LTitle = ImportData(MIWs01, TriTgr, ImMethod=1, ImType="Tri", InColM='Customer ID', InColS='Customer_ID')
    #     MIWs01_OldCI, LTitle = ImportData(MIWs01_OldCI, TriTgr, ImMethod=1, ImType="Tri", InColM='Customer ID', InColS='Customer_ID')

    #     ImportedList += LTitle
    #     print('Imported for:')
    #     print(LTitle)
    #     print('\n')
    #     print('Merging Old Record.')
    #     MIWs01 = Merge_MI_MIOID(MIWs01, MIWs01_OldCI, 0, LTitle)

    #     print('\nImported Tri-Tgr Triage information to Master MI.')
    #     stop = time.time()
    #     TimeSpent(start, stop)


    # ## Import "Media Sensitive Customers (MSC)"

    # [Return to Import File Path](#import_file_path)

    # [Jump to Export Result](#export_result)

    # In[27]:


    # get_ipython().run_cell_magic('time', '', "\nMSC = pd.read_excel(MSC_File)\n\n\nSelCustID = MIWs01['Customer ID'].isin(MSC['Customer ID'])\nSel = SelCustID\n# SelCIN = MIWs01['CIN'].isin(MSC['CIN'])\n# Sel = SelCustID | SelCIN\nMIWs01['Media Sensitive Customers (MSC)'] = Sel\nLTitle = ['Media Sensitive Customers (MSC)']\nImportedList += LTitle\nprint('Imported for:')\nprint(LTitle)\nprint('\\n')\n\n\nprint('Imported Media Sensitive Customers (MSC).')\n")
    MSC = pd.read_excel(MSC_File)
    SelCustID = MIWs01['Customer ID'].isin(MSC['Customer ID'])
    Sel = SelCustID
    # SelCIN = MIWs01['CIN'].isin(MSC['CIN'])
    # Sel = SelCustID | SelCIN
    MIWs01['Media Sensitive Customers (MSC)'] = Sel
    LTitle = ['Media Sensitive Customers (MSC)']
    ImportedList += LTitle
    print('Imported for:')
    print(LTitle)
    print('\n')
    print('Imported Media Sensitive Customers (MSC).')


    # # Import BBRM T90 Decision and Remarks
    # Please update the file name (in brown) for the code below in the following cell.<br>
    # T90BBRM = pd.read_excel(io='./<font color='brown'>T90-Import-2019-05-16.xlsx</font>')<br>
    # This Step is tp be done after Importing CM Tracker, no matter using VBA or Python.<br>
    # ImMethod must be <font color='red'>1</font> when using ImportData.

    # [Return to Import File Path](#import_file_path)

    # [Jump to Export Result](#export_result)

    # In[28]:


    start = time.time()

    T90Col = ['CIN', 'Segment', 'CM2-T90 Letter Issue Arrangement', 'CM2-T90 Letter - Not issue Remarks']
    #T90Col = ['CIN', 'Segment', 'RM-T90 Letter Issue Arrangement', 'RM-T90 Letter - Not issue Remarks']
    T90BBRM = pd.read_excel(io=T90BBRM_File)
    T90BBRM = T90BBRM[T90Col]
    T90BBRM = ProcessDSFile(T90BBRM, InCols='CIN')
    #T90BBRM = T90BBRM[T90BBRM['Segment'] == 'BBRM']
    T90Col = ['CIN', 'CM2-T90 Letter Issue Arrangement', 'CM2-T90 Letter - Not issue Remarks']
    #T90Col = ['CIN', 'RM-T90 Letter Issue Arrangement', 'RM-T90 Letter - Not issue Remarks']

    MIWs01, LTitle = ImportData(MIWs01, T90BBRM, ImMethod=1, MapCol=(T90Col, T90Col.copy()))
    ImportedList += LTitle
    MIWs01['T90 All Doc Received Input Date'] = MIWs01['T90 All Doc Received Input Date'].fillna('')
    MIWs01['RMTH OTLM Input Date'] = MIWs01['RMTH OTLM Input Date'].fillna('')

    SelInT90 = MIWs01['CIN'].isin(T90BBRM['CIN'])
    SelAllDocRec01 = MIWs01['CM2-T90 Letter Issue Arrangement'].str.upper().str.contains('ALL DOC REC', na=False)
    SelAllDocRec02 = MIWs01['CM2-T90 Letter Issue Arrangement'].str.upper().str.contains('ALL DOCUMENT RECEIVED', na=False)
    SelAllDocRec = np.logical_or(SelAllDocRec01, SelAllDocRec02)
    SelOTLM = MIWs01['CM2-T90 Letter Issue Arrangement'].str.upper().str.contains('21 - NO - DO NOT ISSUE: ONE-TIME-LINE-MANAGER EXTENSION GRANTED|OTLM OBTAINED', na=False) | MIWs01['CM2-T90 Letter Issue Arrangement'].str.upper().str.contains('27 - NO - ET CASE DO NOT ISSUE: ONE-TIME-LINE-MANAGER EXTENSION GRANTED', na=False) | MIWs01['CM2-T90 Letter Issue Arrangement'].str.upper().str.contains('26 - YES - ET CASE ISSUE T60 LETTER ONE-TIME-LINE-MANAGER EXTENSION GRANTED', na=False)


    Sel = np.logical_and(SelInT90, SelAllDocRec)
    #MIWs01['T90 All Doc Received Input Date'] = ''

    MIWs01['T90 All Doc Received Input Date'][Sel] = MICutOffDate

    Sel = np.logical_and(SelInT90, SelOTLM)
    #MIWs01['RMTH OTLM Input Date'] = ''

    MIWs01['RMTH OTLM Input Date'][Sel] = MICutOffDate
    ImportedList += ['RMTH OTLM Input Date']
    ImportedList += ['T90 All Doc Received Input Date']

    #MIWs01 = Merge_MI_MIOID(MIWs01, MIWs01_OldCI, 0, LTitle)
    print('Imported for:')
    print(LTitle)
    print('\nImported BBRM T90 decision and remarks to Master MI.')
    stop = time.time()
    TimeSpent(start, stop)


    # # Import RAM File _ Medium List
    # Please update the file name (in brown) for the code below in the following cell.<br>
    # RAMMst = pd.read_excel(io='./<font color='brown'>Medium List 202409.xlsx</font>')

    # [Return to Import File Path](#import_file_path)

    # [Jump to Export Result](#export_result)

    # In[29]:


    # get_ipython().run_cell_magic('time', '', "RAMMst = pd.read_excel(io=RAM_FileName)\n\nMIWs01_OldCI, LTitle = ImportData(MIWs01_OldCI, RAMMst, ImMethod=0, ImType='RAM')\nMIWs01 = ImportData(MIWs01, RAMMst, InColM='Customer ID', InColS='Real customer Id', ImMethod=0, ImType='RAM')[0]\nImportedList += LTitle\nprint('Imported for:')\nprint(LTitle)\nprint('\\n')\nprint('Merging Old Record.')\nMIWs01 = Merge_MI_MIOID(MIWs01, MIWs01_OldCI, 0, LTitle)\n")
    RAMMst = pd.read_excel(io=RAM_FileName)
    MIWs01_OldCI, LTitle = ImportData(MIWs01_OldCI, RAMMst, ImMethod=0, ImType='RAM')
    MIWs01 = ImportData(MIWs01, RAMMst, InColM='Customer ID', InColS='Real customer Id', ImMethod=0, ImType='RAM')[0]
    ImportedList += LTitle
    print('Imported for:')
    print(LTitle)
    print('\n')
    print('Merging Old Record.')
    MIWs01 = Merge_MI_MIOID(MIWs01, MIWs01_OldCI, 0, LTitle)


    # ## Import RM Analytic Team
    # Please update the file name (in brown) for the code below in the following cell.<br>
    # RMAnaInfo = pd.read_excel(io='./<font color='brown'>cdd_review_dt_wkly_20190426.xlsx</font>')

    # [Return to Import File Path](#import_file_path)

    # [Jump to Export Result](#export_result)

    # In[30]:


    #Checked, ok

    start = time.time()

    # RMAnaInfo = pd.read_excel(io=RMAnaInfo_File)
    RMAnaInfo = pd.read_csv(RMAnaInfo_File, encoding='iso-8859-1')
    RMAnaInfo_Col = RMAnaInfo.columns.tolist()

    if 'FCC_RISK_RATING' in RMAnaInfo_Col:
        RMAnaInfo = RMAnaInfo.sort_values(by=['FCC_RISK_RATING'])
    RMAnaInfo = RMAnaInfo.drop_duplicates(subset =["REAL_CUST_ID_1"], keep='first')

    # RMAnaInfo['cdd_review_dt'] = pd.to_datetime(RMAnaInfo['cdd_review_dt'], format='%d-%b-%y')
    RMAnaInfo['cdd_review_dt'] = pd.to_datetime(RMAnaInfo['cdd_review_dt'], format='%d%b%Y')

    #RMAnaInfo = ProcessDSFile(RMAnaInfo, InCols='REAL_CUST_ID_1')
    print('Imported data source to memory')

    MIWs01_OldCI, LTitle = ImportData(MIWs01_OldCI, RMAnaInfo, ImMethod=0, MapCol=(['Old / Dummy CID', 'Analytics Team', 'Analytics Sub Team', 'Last KYC Date'],
                                                          ['REAL_CUST_ID_1', 'TEAM', 'SUB_TEAM', 'cdd_review_dt']))
    MIWs01 = ImportData(MIWs01, RMAnaInfo, ImMethod=0, MapCol=(['Customer ID', 'Analytics Team', 'Analytics Sub Team', 'Last KYC Date'],
                                                          ['REAL_CUST_ID_1', 'TEAM', 'SUB_TEAM', 'cdd_review_dt']))[0]
    ImportedList += LTitle
    print('Imported for:')
    print(LTitle)
    print('\n')
    print('Merging Old Record.')
    MIWs01 = Merge_MI_MIOID(MIWs01, MIWs01_OldCI, 0, LTitle)


    Sel01 = np.logical_not(MIWs01['Analytics Sub Team'].isnull())
    ListV = MIWs01[Sel01]['Analytics Sub Team'].tolist()
    MIWs01.loc[Sel01, 'RM Sub Team'] = ListV

    Sel02 = np.logical_and(np.logical_not(MIWs01['Analytics Team'].isnull()), MIWs01['Analytics Sub Team'].isnull())
    ListV = MIWs01[Sel02]['Analytics Team'].tolist()
    MIWs01.loc[Sel02, 'RM Sub Team'] = ListV


    Sel01 = np.logical_not(MIWs01_OldCI['Analytics Sub Team'].isnull())
    ListV = MIWs01_OldCI[Sel01]['Analytics Sub Team'].tolist()
    MIWs01_OldCI.loc[Sel01, 'RM Sub Team'] = ListV
    ImportedList += ['RM Sub Team']

    Sel02 = np.logical_and(np.logical_not(MIWs01_OldCI['Analytics Team'].isnull()), MIWs01_OldCI['Analytics Sub Team'].isnull())
    ListV = MIWs01_OldCI[Sel02]['Analytics Team'].tolist()
    MIWs01_OldCI.loc[Sel02, 'RM Sub Team'] = ListV

    MIWs01_OldCI['RM Sub Team'] = MIWs01_OldCI['RM Sub Team'].replace({'SVS':'PSE'}, regex=True)
    print('Imported RM Analytic Info to Master MI.')


    MIWs01['RM Sub Team'] = MIWs01['RM Sub Team'].replace({'SVS':'PSE'}, regex=True)
    stop = time.time()
    #stop - start
    TimeSpent(start, stop)


    # ## Import CSEM & USBL
    # Please update the file name (in brown) for the code below in the following cell.<br>
    # CSEM_USBL = pd.read_excel(io='./<font color='brown'>cdd_cds_wkly_20190426.xlsx</font>')
    #

    # [Return to Import File Path](#import_file_path)

    # [Jump to Export Result](#export_result)

    # In[31]:


    start = time.time()
    # CSEM_USBL = pd.read_excel(io=CSEM_USBL_File)
    CSEM_USBL = pd.read_csv(CSEM_USBL_File, encoding='iso-8859-1')

    CSEM_USBL['CDS_REC_REPT_DT_CSEM'] = pd.to_datetime(CSEM_USBL['CDS_REC_REPT_DT_CSEM'], format='%d-%b-%y')
    CSEM_USBL['CDS_REC_REPT_DT_USBL'] = pd.to_datetime(CSEM_USBL['CDS_REC_REPT_DT_USBL'], format='%d-%b-%y')

    # CSEM_USBL['CDS_REC_REPT_DT_CSEM'] = pd.to_datetime(CSEM_USBL['CDS_REC_REPT_DT_CSEM'], format='%d%b%Y')
    # CSEM_USBL['CDS_REC_REPT_DT_USBL'] = pd.to_datetime(CSEM_USBL['CDS_REC_REPT_DT_USBL'], format='%d%b%Y')


    print('Imported data source to memory')
    MIWs01_OldCI, LTitle = ImportData(MIWs01_OldCI, CSEM_USBL, ImType='CDS', InColM='Old / Dummy CID', InColS='REAL_CUST_ID_1', ImMethod=0, MapCol='')
    MIWs01 = ImportData(MIWs01, CSEM_USBL, ImType='CDS', InColM='Customer ID', InColS='REAL_CUST_ID_1', ImMethod=0, MapCol='')[0]
    ImportedList += LTitle
    print('Imported for:')
    print(LTitle)
    print('\n')
    print('Merging Old Record.')
    MIWs01 = Merge_MI_MIOID(MIWs01, MIWs01_OldCI, 0, LTitle)


    print('Imported CSEM & USBL to Master MI.')
    stop = time.time()
    #stop - start
    TimeSpent(start, stop)


    # ## Import High Risk & SCC
    # Please update the file name (in brown) for the code below in the following cell.<br>
    # HR01 =  pd.read_excel(io='./<font color='brown'>HR List Apr2019.xlsx</font>')<br>
    # SCC  = pd.read_excel(io='./<font color='brown'>SCC List Apr2019.xlsx</font>')<br>
    # <br>
    # Since CIN is the key for the mapping, no need to update DataFrame for Old Customer ID.

    # [Return to Import File Path](#import_file_path)

    # [Jump to Export Result](#export_result)

    # In[32]:


    start = time.time()
    HR01 =  pd.read_excel(HR01_File,'Sheet1')
    #HR02 =  pd.read_excel(io='./HR List Dec2018 RAM1.3.xlsx')
    SCC  = pd.read_excel(SCC_File, 'Sheet1')
    #OKYCE = pd.read_excel(io='./OKYC Eligible Base 2018.xlsx')

    # if 'SCCS' in SCC.columns.tolist():
    #     SCC = SCC[SCC['SCCS'] == 'SCCS']
    #     print('Removed record without \'SCCS\' flag in SCC file source.')
    #     pass



    print('Imported data source to memory')
    MIWs01, LTitle = ImportData(MIWs01, HR01, MapCol=(['Customer ID', 'HR1.4-HighRisk Indicator (RAM 1.4)'],['Real customer Id', 'Segment']))
    MIWs01.loc[np.logical_not(MIWs01['HR1.4-HighRisk Indicator (RAM 1.4)'].isnull().tolist()), 'HR1.4-HighRisk Indicator (RAM 1.4)'] = 'H'
    MIWs01.loc[np.logical_not(MIWs01['HR1.4-HighRisk Indicator (RAM 1.4)'].isnull().tolist()), 'SCC / HighRisk Indicator (RAM 1.4)'] = 'H'
    ImportedList += LTitle
    print('Imported for:')
    print(LTitle)
    print('\n')
    print('Imported HR to Master MI.')
    MIWs01, LTitle = ImportData(MIWs01, SCC, MapCol=(['CIN', 'SCC-SCC','SCC-SCCS CDS Load Date'],['CIN','Risk Rating','Latest OBS KYC Date']))
    MIWs01.loc[np.logical_not(MIWs01['SCC-SCC'].isnull().tolist()), 'SCC-SCC'] = 'SCC'
    #MIWs01.loc[np.logical_not(MIWs01['SCC-SCC'].isnull().tolist()), 'SCC / HighRisk Indicator (RAM 1.4)'] = 'SCC'
    ImportedList += LTitle
    print('Imported for:')
    print(LTitle)
    print('\n')
    print('Imported SCC to Master MI.')
    stop = time.time()
    #stop - start
    TimeSpent(start, stop)


    # ## Import QV Adjustment Information
    #
    #

    # [Return to Import File Path](#import_file_path)

    # [Jump to Export Result](#export_result)

    # In[33]:


    start = time.time()

    QCAdj = pd.read_excel(io=QCAdj_File)

    #QCAdj['CIN'] = QCAdj['CIN'].str.strip()
    #QCAdj['CIN'] = pd.to_numeric(QCAdj['CIN'])
    #QCAdj['Total Marks Deducted For RDC due to KYC Ops Error']

    print('Imported data source to memory')
    #MIWs01_OldCI, LTitle = ImportData(MIWs01_OldCI, AccClose, ImType='ACClosure', InColM='Old / Dummy CID', InColS='Customer ID', ImMethod=0, MapCol='')
    MIWs01, LTitle = ImportData(MIWs01, QCAdj, ImType='QVQCWF', InColM='CIN', InColS='CIN', ImMethod=0, MapCol='')
    ImportedList += LTitle
    print('Imported for:')
    print(LTitle)
    print('\n')
    #print('Merging Old Record.')
    #MIWs01 = Merge_MI_MIOID(MIWs01, MIWs01_OldCI, 0, LTitle)


    print('Imported QV Adjustment Information to Master MI.')
    stop = time.time()
    #stop - start
    TimeSpent(start, stop)


    # ## Import Account Closure Information
    # Please update the file name (in brown) for the code below in the following cell.<br>
    # AccClose = pd.read_excel(io='./<font color='brown'>AccountMonitorTemplate - Ac Closed list.xlsx</font>')

    # [Return to Import File Path](#import_file_path)

    # [Jump to Export Result](#export_result)

    # In[34]:


    start = time.time()
    AccClose = pd.read_excel(io=AccClose_File)
    print('Imported data source to memory')
    #MIWs01_OldCI, LTitle = ImportData(MIWs01_OldCI, AccClose, ImType='ACClosure', InColM='Old / Dummy CID', InColS='Customer ID', ImMethod=0, MapCol='')
    MIWs01, LTitle = ImportData(MIWs01, AccClose, ImType='ACClosure', InColM='Customer ID', InColS='Customer ID', ImMethod=0, MapCol='')
    ImportedList += LTitle
    print('Imported for:')
    print(LTitle)
    print('\n')
    #print('Merging Old Record.')
    #MIWs01 = Merge_MI_MIOID(MIWs01, MIWs01_OldCI, 0, LTitle)


    print('Imported Acc Close Info to Master MI.')
    stop = time.time()
    #stop - start
    TimeSpent(start, stop)


    # ## Import Curtailment MI
    # Please update the file name (in brown) for the code below in the following cell.<br>
    # CurtArr = pd.read_excel(io='./<font color='brown'>Master List of Payment Curtailment-2019.4.26.xlsx</font>', sheetname='Masterlist-GSCDD', header=1)

    # [Return to Import File Path](#import_file_path)

    # [Jump to Export Result](#export_result)

    # In[35]:


    start = time.time()
    CurtArr = pd.read_excel(io=CurtArr_File, sheetname='Masterlist-GSCDD', header=1)
    print('Imported data source to memory')
    MIWs01_OldCI, LTitle = ImportData(MIWs01_OldCI, CurtArr, ImType='CUR', InColM='Old / Dummy CID', InColS='Real Cust ID', ImMethod=0, MapCol='')
    MIWs01 = ImportData(MIWs01, CurtArr, ImType='CUR', InColM='Customer ID', InColS='Real Cust ID', ImMethod=0, MapCol='')[0]
    ImportedList += LTitle
    print('Imported for:')
    print(LTitle)
    print('\n')
    print('Merging Old Record.')
    MIWs01 = Merge_MI_MIOID(MIWs01, MIWs01_OldCI, 0, LTitle)


    print('Imported Curt MI to Master MI.')
    stop = time.time()
    #stop - start
    TimeSpent(start, stop)


    # ## Import OKYC Eligible Case (Suspended)
    # Please update the file name (in brown) for the code below in the following cell.<br>
    # OKYCE = pd.read_excel(io='./<font color='brown'>OKYC Eligible Base 2018.xlsx</font>')

    # [Return to Import File Path](#import_file_path)

    # [Jump to Export Result](#export_result)

    # In[36]:


    #start = time.time()
    #OKYCE = pd.read_excel(io='./OKYC Eligible Base 2018.xlsx')
    #print('Imported data source to memory')
    #MIWs01_OldCI, LTitle = ImportData(MIWs01_OldCI, OKYCE, ImMethod=0, MapCol=(['Old / Dummy CID', 'OKYC-OKYC Eligibility'],['CI number', 'OKYC Eligibility']))
    #MIWs01 = ImportData(MIWs01, OKYCE, ImMethod=0, MapCol=(['Customer ID', 'OKYC-OKYC Eligibility'],['CI number', 'OKYC Eligibility']))[0]
    #ImportedList += LTitle
    #print('Imported for:')
    #print(LTitle)
    #print('\n')
    #print('Merging Old Record.')
    #MIWs01 = Merge_MI_MIOID(MIWs01, MIWs01_OldCI, 0, LTitle)


    #print('Imported for Normal CI.')

    #stop = time.time()
    #print('Imported OKYC Data Soruce to Master MI.')
    #TimeSpent(start, stop)


    # ## Import Off CRT Approval Info
    #

    # [Return to Import File Path](#import_file_path)

    # [Jump to Export Result](#export_result)

    # In[37]:


    start = time.time()
    OffCRT = pd.read_excel(io=OffCRTAPP_File)

    MIWs01, LTitle = ImportData(MIWs01, OffCRT, ImType='MAPR', InColM='Customer ID', InColS='Customer ID', ImMethod=0, MapCol='')

    ImportedList += LTitle
    print('Imported for:')
    print(LTitle)
    print('\n')
    stop = time.time()
    print('Imported Off CRT to Master MI.')
    TimeSpent(start, stop)


    # ## Import IMIS Group Information
    # Please update the file name (in brown) for the code below in the following cell.<br>
    # IMIS = ProcessDSFile(pd.read_excel(io='./<font color='brown'>IMIS_File = 'BBRM IMIS GROUP-202004.xlsx'</font>'), InCols='Real Customer ID 1')

    # [Return to Import File Path](#import_file_path)

    # [Jump to Export Result](#export_result)

    # In[38]:


    start = time.time()
    IMIS = pd.read_excel(io=IMIS_File)
    IMIS = IMIS.dropna(subset=['Group Name'])
    IMIS = ProcessDSFile(IMIS, InCols='Real customer id')


    MIWs01, LTitle = ImportData(MIWs01, IMIS, ImMethod=0, MapCol=(['Customer ID', 'IMISGroupNo', 'IMIS Group Name'], ['Real customer id', 'IMIS Group No', 'Group Name']))

    MIWs01_OldCI, LTitle = ImportData(MIWs01_OldCI, IMIS, ImMethod=0, MapCol=(['Customer ID', 'IMISGroupNo', 'IMIS Group Name'], ['Real customer id', 'IMIS Group No', 'Group Name']))
    MIWs01 = ImportData(MIWs01, IMIS, ImMethod=0, MapCol=(['Customer ID', 'IMISGroupNo', 'IMIS Group Name'], ['Real customer id', 'IMIS Group No', 'Group Name']))[0]
    ImportedList += LTitle
    print('Imported for:')
    print(LTitle)
    print('\n')
    print('Merging Old Record.')
    MIWs01 = Merge_MI_MIOID(MIWs01, MIWs01_OldCI, 0, LTitle)

    ImportedList += LTitle
    print('Imported for:')
    print(LTitle)
    print('\n')
    stop = time.time()
    print('Imported IMIS Info Master MI.')
    TimeSpent(start, stop)


    # ## Import BAU Cust Info RM & Relationship ID
    # Please update the file name (in brown) for the code below in the following cell.<br>
    # RMInfo = ProcessDSFile(pd.read_excel(io='./<font color='brown'>BAU Cust Info RM (CI to CIN) 20181228.xlsx</font>'), InCols='Real Customer ID 1')

    # [Return to Import File Path](#import_file_path)

    # [Jump to Export Result](#export_result)

    # In[39]:


    # get_ipython().run_cell_magic('time', '', "start = time.time()\nRMInfo = pd.read_excel(io=RMInfo_File)\nRMInfo['VirtualKey'] = RMInfo['Real Customer ID 1'] + '-' + RMInfo['Internal Customer Number (CIN)'].astype(str)\n\n# RMInfo = ProcessDSFile(RMInfo, InCols='Internal Customer Number (CIN)')\n# RMInfo = ProcessDSFile(RMInfo, InCols='Real Customer ID 1')\nMIWs01['VirtualKey'] = MIWs01['Customer ID'] + '-' + MIWs01['CIN'].astype(str)\n\n\nRMInfo['Relationship Manager Team Name'].fillna(RMInfo['CIBM/COB/BUB team'],inplace=True)\nRMInfo['CIBM/COB/BUB team']=RMInfo['Relationship Manager Team Name']\n\n\nMIWs01, LTitle = ImportData(MIWs01, RMInfo, ImMethod=0, MapCol=(['VirtualKey', 'Customer Name', 'RM Name', 'RM Staff ID', 'RM Team Group', 'RelationshipID', 'RelationshipID Group Name', 'Company email Address'], ['VirtualKey', 'Customer Full Name', 'Relationship Manager Name', 'Relationship Manager Staff ID', 'CIBM/COB/BUB team', 'Relationship ID', 'FINMIS Group Name', 'Company Internet Address']))\n# MIWs01, LTitle = ImportData(MIWs01, RMInfo, ImMethod=0, MapCol=(['VirtualKey', 'Customer Name', 'RM Name', 'RM Staff ID', 'RM Team Group', 'RelationshipID', 'RelationshipID Group Name'], ['VirtualKey', 'Customer Full Name', 'Relationship Manager Name', 'Relationship Manager Staff ID', 'CIBM/COB/BUB team', 'Relationship ID', 'FINMIS Group Name']))\n\n\nImportedList += LTitle\nprint('Imported for:')\nprint(LTitle)\nprint('\\n')\nstop = time.time()\nprint('Imported BAU Cust Info RM to Master MI.')\n\n\nTimeSpent(start, stop)\n")
    start = time.time()
    RMInfo = pd.read_excel(io=RMInfo_File)
    RMInfo['VirtualKey'] = RMInfo['Real Customer ID 1'] + '-' + RMInfo['Internal Customer Number (CIN)'].astype(str)
    # RMInfo = ProcessDSFile(RMInfo, InCols='Internal Customer Number (CIN)')
    # RMInfo = ProcessDSFile(RMInfo, InCols='Real Customer ID 1')
    MIWs01['VirtualKey'] = MIWs01['Customer ID'] + '-' + MIWs01['CIN'].astype(str)
    RMInfo['Relationship Manager Team Name'].fillna(RMInfo['CIBM/COB/BUB team'],inplace=True)
    RMInfo['CIBM/COB/BUB team']=RMInfo['Relationship Manager Team Name']
    MIWs01, LTitle = ImportData(MIWs01, RMInfo, ImMethod=0, MapCol=(['VirtualKey', 'Customer Name', 'RM Name', 'RM Staff ID', 'RM Team Group', 'RelationshipID', 'RelationshipID Group Name', 'Company email Address'], ['VirtualKey', 'Customer Full Name', 'Relationship Manager Name', 'Relationship Manager Staff ID', 'CIBM/COB/BUB team', 'Relationship ID', 'FINMIS Group Name', 'Company Internet Address']))
    # MIWs01, LTitle = ImportData(MIWs01, RMInfo, ImMethod=0, MapCol=(['VirtualKey', 'Customer Name', 'RM Name', 'RM Staff ID', 'RM Team Group', 'RelationshipID', 'RelationshipID Group Name'], ['VirtualKey', 'Customer Full Name', 'Relationship Manager Name', 'Relationship Manager Staff ID', 'CIBM/COB/BUB team', 'Relationship ID', 'FINMIS Group Name']))
    ImportedList += LTitle
    print('Imported for:')
    print(LTitle)
    print('\n')
    stop = time.time()
    print('Imported BAU Cust Info RM to Master MI.')
    TimeSpent(start, stop)


    # ## Import QVFiles
    # Auto Search all QVFiles in the folder. Please only keep necessary files in the folder.

    # [Return to Import File Path](#import_file_path)

    # [Jump to Export Result](#export_result)

    # In[40]:


    start = time.time()
    path = os.getcwd()
    Files = os.listdir(path)
    QVType = ''
    QVF = ['QVOpen', 'QVQC', 'QVClosedAPP', 'QVClosedCAN', 'QVEsc', 'QVQA']
    #QVF = ['QVClosedCAN']

    for aFile in Files:
        if aFile[:2].upper() == 'QV':
            for i in range(0, len(QVF)):
                if QVF[i].upper() in aFile.upper():
                    print('Importing:\t%s' % aFile)

                    if QVF[i] == 'QVQC':
                        #F01 = ['Latest QC Completion Date', 'Review ID']
                        #F02 = [True, True]
                        #F03 = [True, False]

                        ### Use below setting for QVQC ###
                        F01 = ['Latest QC Completion Date', 'Review ID']
                        F02 = [True, True]
                        F03 = [True, False]
                    elif QVF[i] == 'QVClosedCAN':

                        #QT = QVF[i].copy(deep=True)
                        #QVF[i] = QT[np.logical_not(QT['Approval/Cancel Date'] == '-')]
                        #QT['Approval/Cancel Date']

                        F01 = ['Approval/Cancel Date', 'Review ID']
                        F02 = [True, True]
                        F03 = [True, False]

                        #F01 = ['Review ID', 'Approval/Cancel Date']
                        #F02 = [True, True]
                        #F03 = [False, True]

                    elif QVF[i] == 'QVClosedAPP':
                         ### Use this setting for QVClosedAPP ###
                        F01 = 'Approval/Cancel Date'
                        F02 = True
                        F03 = True

                    elif QVF[i] == 'QVEsc' or QVF[i] == 'QVEscalation':

                        ### Use this setting for QVEsc ###

                        F01 = 'Escalation ID'
                        F02 = True
                        F03 = False
                    elif QVF[i] == 'QVOpen':

                        ### Use this setting for QVOpen ###

                        F01 = 'Review ID'
                        F02 = True
                        F03 = False

                    elif QVF[i] == 'QVQA':

                        F01 = 'Review ID'
                        F02 = True
                        F03 = False



                    QVS = pd.read_excel(io='./' + aFile)

                    if QVF[i] == 'QVOpen':
                        QVS['Latest level of Approval'] = QVS['Latest level of Approval'].replace('-', 0)


                    #QVO.append(QVS.copy(deep=True))
                    #QVO[len(QVO) - 1].name = aFile
                    QVS = ProcessDSFile(QVS, 'Customer Number', F01, F02, F03)
                    QVS.name = aFile
                    if 'QVClosedCAN' in QVS.name:
                        #print("Hihihihihihi")
                        #print(QVS.shape)
                        QVS = QVS[np.logical_not(QVS['Approval/Cancel Date'].isnull())]
                        #print(QVS.shape)
                    #QVOc.append(QVS.copy(deep=True))
                    #QVOc[len(QVOc) - 1].name = aFile


                    QVType = QVF[i]

                    MIWs01, LTitle = ImportData(MIWs01, QVS, ImType=QVType, InColM='CIN', InColS='Customer Number', ImMethod=0, MapCol='')
                    ImportedList += LTitle
                    print('Imported for:')
                    print(LTitle)
                    print('\n')

                    if 'QVClosedAPP' in QVType:
                        SelQV = QVS['Review Reason'] == 'New to Bank'
                        print(np.sum(SelQV))
                        QVSETB = QVS[np.logical_not(SelQV)]
                        QVSNTB = QVS[SelQV]

                        MIWs01, LTitle = ImportData(MIWs01, QVSETB, ImType=QVType, InColM='CIN', InColS='Customer Number', ImMethod=0, MapCol='')
                        ImportedList += LTitle
                        print('Imported for:')
                        print(LTitle)
                        print('\n')

                        MIWs01, LTitle = ImportData(MIWs01, QVSNTB, ImType='QVClosedNTBAPP', InColM='CIN', InColS='Customer Number', ImMethod=0, MapCol='')
                        ImportedList += LTitle
                        print('Imported for:')
                        print(LTitle)
                        print('\n')


                    else:
                        MIWs01, LTitle = ImportData(MIWs01, QVS, ImType=QVType, InColM='CIN', InColS='Customer Number', ImMethod=0, MapCol='')
                        ImportedList += LTitle
                        print('Imported for:')
                        print(LTitle)
                        print('\n')



    print('Imported QV Files to Master MI.\n')

    print('Starting Post Import adjustment...')

    Sel01 = MIWs01['QVOpen-Review ID'].isnull()
    MIWs01.loc[Sel01, 'QVOpen-Latest DC Finalised Date'] = MIWs01.loc[Sel01, 'QVClosedAPP-Latest DC Finalised Date']
    MIWs01.loc[Sel01, 'QVOpen-Latest DC Finalised by ID'] = MIWs01.loc[Sel01, 'QVClosedAPP-Latest DC Finalised by ID']

    #StaffList = pd.read_excel(io='./StaffList.xlsx')
    #StaffList['ID_to_Name'] = StaffList['Team'] + ' - ' + StaffList['Employee Name'].apply(lambda x: "" if x == 'NaN' else x)
    StaffList['ID_to_Name'] = " "
    Sel01 = StaffList['Employee Name'].isnull()
    StaffList.loc[Sel01, 'ID_to_Name'] = StaffList[Sel01]['Team'] + ' - '
    StaffList.loc[np.logical_not(Sel01), 'ID_to_Name'] = StaffList[np.logical_not(Sel01)]['Team'] + ' - ' + StaffList['Employee Name']
    StaffList = StaffList[['Employee Number', 'ID_to_Name']]
    StaffList = StaffList.set_index('Employee Number')

    UIDtoNameCol = ['QVOpen-Assigned to User', 'QVOpen-Latest DC Finalised by ID', 'QVOpen-User ID', 'QVQC-Initial DC Finalised by ID',
                    'QVQC-Latest QC Completed by', 'QVClosedAPP-Latest DC Finalised by ID',
                    'QVClosedCAN-Latest DC Finalised by ID']



    InVV = ['BPM', 'SYSTEM', 'CDDSS_GDMS_HK', 'No Mapping']
    for aCol in UIDtoNameCol:
        #print("Column:\t" + str(aCol))
        aSL = pd.to_numeric(MIWs01[aCol], downcast ='integer', errors='ignore')

        if aSL.dtype == 'object':
            for aInVV in InVV:
                Sel01 = MIWs01[aCol] == aInVV
                #MIWs01.loc[Sel01, aCol] = np.NaN
                MIWs01.loc[Sel01, aCol] = 0
            aSL = pd.to_numeric(MIWs01[aCol], downcast ='integer', errors='ignore')


        #print("***************************")
        if aSL.dtype == 'object':
            print('Please check for the value of field' + aCol)
        bSL = aSL.map(StaffList['ID_to_Name'])

        aIDSel = np.logical_not(aSL.isnull())
        bIDSel = bSL.isnull()
        IDSel = bIDSel & aIDSel

        bSL[IDSel] = aSL[IDSel]
        MIWs01.loc[:, aCol] = bSL

    #TriggerCode = pd.read_excel(io='./TriggerCode.xlsx')['Trigger Event Code'].dropna().tolist()
    #print(MIWs01['QVOpen-Trigger Description'].shape)
    TC = MIWs01['QVOpen-Trigger Description'].fillna("A")

    TC = TC.tolist()

    TTC = []
    for aTC in TriggerCode:

        if (aTC[0:2] != 'TE') & (aTC[0:2] != 'IT'):
            TriggerCode.remove(aTC)


    for aTC in TC:
        MTC = ""
        Ctr = 0
        #print(aTC)
        for aTCE in TriggerCode:

            if aTC.find(aTCE) > -1 :
                #print("\t"+aTCE)
                MTC = MTC + aTCE + ","
                Ctr = Ctr + 1
        TTC.append(MTC)

    #print(len(TTC))
    MIWs01.loc[:, 'QVOpen-Trigger Description'] = TTC



    print('Finished Post Import adjustment.\n')
    stop = time.time()

    TimeSpent(start, stop)


    # ## Code for Checking QV Files
    # To check if there is any QV data is not imported properly.<br>
    # The below 3 columns are calculated by formula in Master MI:<br>
    # - QVClosedAPP-Approval/Cancel Date > T0
    # - QVClosedAPP-Approval/Cancel Year-Month
    # - QVClosedCAN-Approval/Cancel Year-Month

    # [Return to Import File Path](#import_file_path)

    # [Jump to Export Result](#export_result)

    # In[41]:


    QVCheck = []
    for aCol in MIWs01.columns.tolist():
        for aQV in QVF:
            if aQV in aCol:
                QVCheck.append(aCol)
                pass
            pass
        pass
    QVCheck.remove("QVClosedAPP-Approval/Cancel Date > T0")
    QVCheck.remove("QVClosedAPP-Approval/Cancel Year-Month")
    QVCheck.remove("QVClosedCAN-Approval/Cancel Year-Month")
    QVCheck.remove("QVQCWF-Initial CRT Finalization Date")
    QVCheck.remove("QVQCWF-Total Marks Deducted For RDC due to KYC Ops Error")
    #if 'QVClosedNTBAPP-Approval/Cancel Date' in QVCheck:
    #    QVCheck.remove("QVClosedNTBAPP-Approval/Cancel Date")
    #if 'QVClosedNTBAPP-Last CDD Review Completion Date' in QVCheck:
    #    QVCheck.remove("QVClosedNTBAPP-Last CDD Review Completion Date")
    TRecord = MIWs01.shape[0]
    wError = 0
    for aCol in QVCheck:
        if np.sum(MIWs01[aCol].isnull()) >= TRecord:
            print('Please check the QVFiles with column:\t%s' % aCol)
            pass
        pass

    if wError == 0:
        print('QVFiles need to be checked but python will stll run no matter what')


    # ## Import Incoming Doc Register Data (Demised)
    # Please update the file name (in brown) for the code below in the following cell.<br>
    # IncomingDoc = pd.read_excel(io='./<font color='brown'>IncomingDocRegister20191002.xlsx</font>')

    # [Return to Import File Path](#import_file_path)

    # [Jump to Export Result](#export_result)

    # In[42]:


    # start = time.time()

    # CRTAppDate = MIWs01[['CIN', 'QVClosedAPP-Approval/Cancel Date']].dropna()
    # CRTAppDate['QVClosedAPP-Approval/Cancel Date'] = CRTAppDate['QVClosedAPP-Approval/Cancel Date'].dt.date

    # IncomingDoc = pd.read_excel(io=IncomingDoc_File)
    # #IncomingDoc = ProcessDSFile(IncomingDoc, 'CIN', 'Document Receive Date', True, True)
    # IncomingDoc = ModifyDocReg(IncomingDoc, CRTAppDate)

    # #print(IncomingDoc)
    # #print('Imported data source to memory')
    # MIWs01, LTitle = ImportData(MIWs01, IncomingDoc, ImType='IDR', InColM='CIN', InColS='CIN', ImMethod=0, MapCol='')
    # ImportedList += LTitle
    # print('Imported for:')
    # print(LTitle)
    # print('\n')

    # print('Imported Incoming Doc Register Data to Master MI.')
    # stop = time.time()
    # #stop - start
    # TimeSpent(start, stop)


    # ## Import Stage 1
    # Please update the file name (in brown) for the code below in the following cell.<br>
    # S1_Report_Raw = pd.read_excel('<font color='brown'>Stage 1 CDD Deployment-20200320.xlsx</font>')
    #

    # [Return to Import File Path](#import_file_path)

    # [Jump to Export Result](#export_result)

    # In[43]:


    start = time.time()

    S1_Report_Raw = pd.read_excel(S1_Report_Raw_File)
    stop = time.time()
    #stop - start
    TimeSpent(start, stop)


    # In[44]:


    start = time.time()

    S1_Report_Ext = S1_Report_Raw.copy(deep=True)
    S1_Report_Ext['Customer_ID_S1'] = S1_Report_Ext['Customer_ID_S1'].str.strip()
    S1_Report_Ext['Cancellation Code'] = S1_Report_Ext['Cancellation Code'].fillna('')
    S1_Report_Ext['Cancellation Code'] = S1_Report_Ext['Cancellation Code'].str.strip()
    S1_Report_Ext['S1 Master Status'] = S1_Report_Ext['S1 Master Status'].fillna('')
    S1_Report_Ext['S1 Master Status'] = S1_Report_Ext['S1 Master Status'].str.strip()
    S1_Report_Ext['CRT initiated date'] = S1_Report_Ext['CRT initiated date'].fillna('')
    #S1_Report_Ext['Date_of_T+0_Issue_S1'] = S1_Report_Ext['Date_of_T+0_Issue_S1'].fillna('')
    S1_Report_Ext['Acceleration Case actual T0 date'] = S1_Report_Ext['Acceleration Case actual T0 date'].fillna('')
    S1_Report_Ext['Actual Review team(After CM assignment)'] = S1_Report_Ext['Actual Review team(After CM assignment)'].str.strip()
    S1_Report_Ext = S1_Report_Ext.replace('Can will be cancelled, pls do not issue T0 letter', value = '')

    S1_Report_Ext = S1_Report_Ext.sort_values(by=['Date_of_Report_S1', 'S1 Master Status'], ascending=[True, False])

    MIWs01 = MIWs01.fillna('')
    MIWs01 = MIWs01.set_index('Customer ID')

    MIWs01['Last KYC Date'] = pd.to_datetime(MIWs01['Last KYC Date'])
    MIWs01['QVClosedAPP-Approval/Cancel Date'] = pd.to_datetime(MIWs01['QVClosedAPP-Approval/Cancel Date'])
    MIWs01['QVClosedCAN-Approval/Cancel Date'] = pd.to_datetime(MIWs01['QVClosedCAN-Approval/Cancel Date'])


    # In[ ]:


    #MITemp_Result = MIWs01[['Customer ID', 'CIN', 'Old / Dummy CID', 'S1 Report Date', 'Overall_Status_S1', 'T0 CM Name',
    #                             'T0 CM Team Head', 'T0',
    #                             'T30 Rmdr Letter date (Actual)', 'T60 Rmdr Letter date (Actual)', 'GWIS_Number',
    #                            'KYCI Curt Letter issue date (Actual)', 'S1 Remark', 'S1 Review Type', 'Activities']]
    #MITemp_Result.to_excel('S1_Imported.xlsx')


    # In[ ]:


    # get_ipython().run_cell_magic('time', '', "MIWs01 = ImportStage1Report(MIWs01, S1_Report_Ext, StaffList_c.copy(deep=True))\nLTitle = ['S1 Report Date', 'Overall_Status_S1', 'T0 CM Name',\n                             'T0 CM Team Head', 'T0',\n                             'T30 Rmdr Letter date (Actual)', 'T60 Rmdr Letter date (Actual)', 'GWIS_Number',\n                            'KYCI Curt Letter issue date (Actual)', 'S1 Remark', 'S1 Review Type', 'Activities', 'Acceleration T0 Date','S1 CM Team']\nImportedList += LTitle\n\nstop = time.time()\nTimeSpent(start, stop)\n")
    MIWs01 = ImportStage1Report(MIWs01, S1_Report_Ext, StaffList_c.copy(deep=True))
    LTitle = ['S1 Report Date', 'Overall_Status_S1', 'T0 CM Name',
                                 'T0 CM Team Head', 'T0',
                                 'T30 Rmdr Letter date (Actual)', 'T60 Rmdr Letter date (Actual)', 'GWIS_Number',
                                'KYCI Curt Letter issue date (Actual)', 'S1 Remark', 'S1 Review Type', 'Activities', 'Acceleration T0 Date','S1 CM Team']
    ImportedList += LTitle
    stop = time.time()
    TimeSpent(start, stop)


    # ## Get Missing Segment, Team, RM and RM Staff ID record from BoW / Stage 1

    # In[ ]:


    # %%time
    # BoW_FileRecord = pd.ExcelFile(BoW_File)
    # BoW_Record = pd.read_excel(BoW_FileRecord, sheetname='Details')


    # In[ ]:


    # SelSMEMass = MIWs01['RM Team Group'].str.upper().str.contains('MASS', na=False) & ((MIWs01['Team'] == '') | (MIWs01['Team'].isnull()))
    # # SelEmptyTeam = np.logical_or(MIWs01['Team'] == '', MIWs01['Team'].isnull())
    # # SelEmptySegment = np.logical_or(MIWs01['Segment'] == '', MIWs01['Segment'].isnull())
    # # SelT0 = MIWs01['T0'] > MICutOffDate - DT.timedelta(days=90)
    # SelT0 = MIWs01['T0'] > DT.datetime(2020, 9, 30, 0, 0)
    # print('Number of Case wihtout Segment or Team:\t%d' % np.sum(SelSMEMass & SelT0))


    # In[ ]:


    # SelSMEMass = MIWs01['RM Team Group'].str.upper().str.contains('MASS', na=False) & ((MIWs01['Segment'] == '') | (MIWs01['Segment'].isnull()))
    # # SelEmptyTeam = np.logical_or(MIWs01['Team'] == '', MIWs01['Team'].isnull())
    # # SelEmptySegment = np.logical_or(MIWs01['Segment'] == '', MIWs01['Segment'].isnull())
    # # SelT0 = MIWs01['T0'] > MICutOffDate - DT.timedelta(days=90)
    # SelT0 = MIWs01['T0'] > DT.datetime(2020, 9, 30, 0, 0)
    # print('Number of Case without Segment or Team:\t%d' % np.sum(SelSMEMass & SelT0))


    # In[ ]:


    # Cust_wo_Team = MIWs01.loc[SelSMEMass & SelT0, 'Customer ID']
    # Cust_wo_Team = list(Cust_wo_Team.values)


    # In[ ]:


    # MIWs01_Backup = MIWs01.copy(deep=True)


    # ### Code by using BoW

    # In[ ]:


    # %%time
    # nF = 0
    # # MIWs01 = MIWs01_Backup.copy(deep=True)
    # ImportedList += ['Segment', 'Team']
    # for aCust in Cust_wo_Team:
    #     SelCustMI = MIWs01['Customer ID'] == aCust
    #     SelCustBoW = BoW_Record['Real ID'] == aCust
    #     if np.sum(SelCustBoW) > 0:
    #         tmpSegment = BoW_Record.loc[SelCustBoW, 'Segment'].tolist()[0]
    #         tmpTeam = BoW_Record.loc[SelCustBoW, 'Team'].tolist()[0]
    #         tmpRM = BoW_Record.loc[SelCustBoW, 'RM'].tolist()[0]
    #         tmpRMID = BoW_Record.loc[SelCustBoW, 'RM Staff ID'].tolist()[0]

    #         MIWs01.loc[SelCustMI, 'Segment'] = tmpSegment
    #         MIWs01.loc[SelCustMI, 'Team'] = tmpTeam
    #         MIWs01.loc[SelCustMI, 'RM Name'] = tmpRM
    #         MIWs01.loc[SelCustMI, 'RM Staff ID'] = tmpRMID
    #         nF += 1
    # #         print('Done:\t%s' % (aCust, nF))
    #         print('Done:\t%s\t%s\t%s\t%s\t%s\t@\t%d' % (aCust, tmpSegment, tmpTeam, tmpRM, str(tmpRMID), nF))
    #         pass
    #     else:
    #         print('Not Found:\t%s' % aCust)


    # ### Code by using Stage 1

    # In[ ]:


    # %%time

    #ImportedList += ['Segment', 'Team']
    # # Cust_wo_Team = MIWs01[Sel]['Customer ID'].tolist()
    # S1Tmp = S1_Report_Raw.copy(deep=True)
    # S1Tmp['Customer_ID_S1'].fillna('')
    # S1Tmp['Date_of_T+0_Issue_S1'] = pd.to_datetime(S1Tmp['Date_of_T+0_Issue_S1'], errors='coerce')
    # S1Tmp = S1Tmp[S1Tmp['Date_of_T+0_Issue_S1'].notnull()]
    # S1Tmp = S1Tmp[S1Tmp['Date_of_T+0_Issue_S1'] > DT.datetime(2020, 9, 30, 0, 0)]

    # nF = 0

    # for aCust in Cust_wo_Team:
    # #     print(aCust)
    #     SelCustMI = MIWs01['Customer ID'] == aCust
    #     tmpT0 = MIWs01[SelCustMI]['T0'].tolist()[0]
    # #     print(tmpT0)

    #     SelS1CIN = S1Tmp['Customer_ID_S1'] == aCust
    #     SelS1T0 = S1Tmp['Date_of_T+0_Issue_S1'] == tmpT0
    #     SelS1 = SelS1CIN & SelS1T0
    # #     print(np.sum(SelS1))
    #     if np.sum(SelS1) > 0:
    #         tmpSegment = S1Tmp[SelS1]['CMB_Segment_S1'].tolist()[0]
    #         tmpTeam = S1Tmp[SelS1]['RM_Team_Group_S1'].tolist()[0]
    #         tmpRM = S1Tmp[SelS1]['CMB_Segment_S1'].tolist()[0]
    #         tmpRMID = S1Tmp[SelS1]['CMB_Segment_S1'].tolist()[0]
    #         nF += 1
    #         print('%s\t%s\t%s\t%s\t%s\t%s' % (aCust, str(tmpT0), tmpSegment, tmpTeam, tmpRM, tmpRMID ))
    #         MIWs01.loc[SelCustMI, 'Segment'] = tmpSegment
    #         MIWs01.loc[SelCustMI, 'RM Name'] = tmpRM
    #         MIWs01.loc[SelCustMI, 'RM Staff ID'] = tmpRMID
    #         if tmpTeam == 'COR' or len(tmpTeam) > 3:
    #             MIWs01.loc[SelCustMI, 'RM Team Group'] = tmpTeam
    #         else:
    #             MIWs01.loc[SelCustMI, 'Team'] = tmpTeam

    #     else:
    #         print('Not Found:\t%s' % aCust)
    #         pass
    # #     print('***********************************')




    # ## Code for Checking and Modifying QV Files Staff
    # ### After Stage 1 Import
    # Column Must be KYC Ops only:<br>
    # QVQC-Latest QC Completed by<br>
    # <br>
    # Column can be KYC Ops (Control by Cut-off Date):<br>
    # QVQC-Initial DC Finalised by ID<br>
    # QVOpen-Latest DC Finalised by ID<br>
    # QVOpen-Assigned to User<br>
    # QVOpen-Latest DC Finalised by ID<br>
    # QVOpen-User ID<br>
    # QVClosedAPP-Latest DC Finalised by ID<br>
    # QVClosedCAN-Latest DC Finalised by ID<br>

    # [Return to Import File Path](#import_file_path)

    # [Jump to Export Result](#export_result)

    # In[ ]:


    # Array2Update = ['QVQC-Initial DC Finalised by ID', 'QVOpen-Latest DC Finalised by ID',
    #                'QVOpen-Assigned to User', 'QVOpen-Latest DC Finalised by ID',
    #                'QVOpen-User ID', 'QVClosedAPP-Latest DC Finalised by ID',
    #                'QVClosedCAN-Latest DC Finalised by ID']

    # SelKYCOpsCM = MIWs01['T0'] >= KYCOpsCM_StartDate
    # SelKYCOpsCM = np.logical_and(SelKYCOpsCM, MIWs01['T0'] <= KYCOpsCM_EndDate)

    # for aCol in Array2Update:
    #     tmp = MIWs01[aCol]
    #     tmp[SelKYCOpsCM] = tmp[SelKYCOpsCM].str.replace(' / KYC Ops', '')
    #     tmp[np.logical_not(SelKYCOpsCM)] = tmp[np.logical_not(SelKYCOpsCM)].str.replace('CM / ', '')
    #     MIWs01[aCol] = tmp

    # MIWs01['QVQC-Latest QC Completed by'] = MIWs01['QVQC-Latest QC Completed by'].str.replace('CM / KYC Ops', 'KYC Ops')


    # In[ ]:


    # get_ipython().run_cell_magic('time', '', "Array2Update = ['QVQC-Initial DC Finalised by ID', 'QVOpen-Latest DC Finalised by ID',\n               'QVOpen-Assigned to User', 'QVOpen-Latest DC Finalised by ID',\n               'QVOpen-User ID', 'QVClosedAPP-Latest DC Finalised by ID',\n               'QVClosedCAN-Latest DC Finalised by ID']\n\nDateArray2Check = ['QVQC-Initial DC Finalised Date', 'QVOpen-Latest DC Finalised Date',\n                  'T0', 'QVOpen-Latest DC Finalised Date',\n                  'T0', 'QVClosedAPP-Latest DC Finalised Date',\n                  'QVClosedCAN-Latest DC Finalised Date']\n\nNTBStaff = ['Santie T T XIA', 'Karena J X DENG', 'Chris G M LIANG']\n\nStaffList_KYCOps = StaffList_c1[StaffList_c1['Team'].fillna('').str.contains('CM / KYC Ops')]\n\nfor i in range(0, len(Array2Update)):\n    aCol = Array2Update[i]\n    aDateCol = DateArray2Check[i]\n    tmp = MIWs01[aCol]\n    #     tmp[SelKYCOpsCM] = tmp[SelKYCOpsCM].str.replace(' / KYC Ops', '')\n    #     tmp[np.logical_not(SelKYCOpsCM)] = tmp[np.logical_not(SelKYCOpsCM)].str.replace('CM / ', '')\n    #     MIWs01[aCol] = tmp\n    tmpDate = pd.to_datetime(MIWs01[aDateCol].fillna(pd.NaT))\n    for aIndex, aRow in StaffList_KYCOps.iterrows():\n        KYCOpsCM_StartDate = aRow['Effective Date']\n#         print(KYCOpsCM_StartDate)\n#         print(aDateCol)\n#         print(aCol)\n        SelKYCOpsCMDate = np.logical_and(tmpDate >= KYCOpsCM_StartDate, tmpDate <= KYCOpsCM_EndDate)\n        SelKYCOpsCM = (MIWs01[aCol] == aRow['Team'] + ' - ' + aRow['Employee Name'])\n        SelinDate = SelKYCOpsCM & SelKYCOpsCMDate\n        tmp[SelinDate] = tmp[SelinDate].str.replace(' / KYC Ops', '')\n        SeloutDate = SelKYCOpsCM & ~SelKYCOpsCMDate\n        tmp[SeloutDate] = tmp[SeloutDate].str.replace('CM / ', '')\n        if aRow['Employee Name'] in NTBStaff:\n#             print(aRow['Employee Name'])\n            tmp[SeloutDate] = 'NTB - '\n    MIWs01[aCol] = tmp\n\nMIWs01['QVQC-Latest QC Completed by'] = MIWs01['QVQC-Latest QC Completed by'].str.replace('CM / KYC Ops', 'KYC Ops')\n\n")

    Array2Update = ['QVQC-Initial DC Finalised by ID', 'QVOpen-Latest DC Finalised by ID',
                   'QVOpen-Assigned to User', 'QVOpen-Latest DC Finalised by ID',
                   'QVOpen-User ID', 'QVClosedAPP-Latest DC Finalised by ID',
                   'QVClosedCAN-Latest DC Finalised by ID']
    DateArray2Check = ['QVQC-Initial DC Finalised Date', 'QVOpen-Latest DC Finalised Date',
                      'T0', 'QVOpen-Latest DC Finalised Date',
                      'T0', 'QVClosedAPP-Latest DC Finalised Date',
                      'QVClosedCAN-Latest DC Finalised Date']
    NTBStaff = ['Santie T T XIA', 'Karena J X DENG', 'Chris G M LIANG']
    StaffList_KYCOps = StaffList_c1[StaffList_c1['Team'].fillna('').str.contains('CM / KYC Ops')]
    for i in range(0, len(Array2Update)):
        aCol = Array2Update[i]
        aDateCol = DateArray2Check[i]
        tmp = MIWs01[aCol]
        #     tmp[SelKYCOpsCM] = tmp[SelKYCOpsCM].str.replace(' / KYC Ops', '')
        #     tmp[np.logical_not(SelKYCOpsCM)] = tmp[np.logical_not(SelKYCOpsCM)].str.replace('CM / ', '')
        #     MIWs01[aCol] = tmp
        tmpDate = pd.to_datetime(MIWs01[aDateCol].fillna(pd.NaT))
        for aIndex, aRow in StaffList_KYCOps.iterrows():
            KYCOpsCM_StartDate = aRow['Effective Date']
    #         print(KYCOpsCM_StartDate)
    #         print(aDateCol)
    #         print(aCol)
            SelKYCOpsCMDate = np.logical_and(tmpDate >= KYCOpsCM_StartDate, tmpDate <= KYCOpsCM_EndDate)
            SelKYCOpsCM = (MIWs01[aCol] == aRow['Team'] + ' - ' + aRow['Employee Name'])
            SelinDate = SelKYCOpsCM & SelKYCOpsCMDate
            tmp[SelinDate] = tmp[SelinDate].str.replace(' / KYC Ops', '')
            SeloutDate = SelKYCOpsCM & ~SelKYCOpsCMDate
            tmp[SeloutDate] = tmp[SeloutDate].str.replace('CM / ', '')
            if aRow['Employee Name'] in NTBStaff:
    #             print(aRow['Employee Name'])
                tmp[SeloutDate] = 'NTB - '
        MIWs01[aCol] = tmp
    MIWs01['QVQC-Latest QC Completed by'] = MIWs01['QVQC-Latest QC Completed by'].str.replace('CM / KYC Ops', 'KYC Ops')

    # In[ ]:


    # MIWs01['QVOpen-Latest DC Finalised Date'] = pd.to_datetime(MIWs01['QVOpen-Latest DC Finalised Date'], errors='coerce')
    # MIWs01['T0'] = pd.to_datetime(MIWs01['T0'], errors='coerce')
    # Sel01 = MIWs01['QVOpen-Latest DC Finalised Date'] < MIWs01['T0']
    # MIWs01.loc[Sel01, 'QVOpen-Latest DC Finalised Date'] = pd.NaT
    # MIWs01.loc[Sel01, 'QVOpen-Latest DC Finalised by ID'] = ''


    # ## Import Master Group and Master Group ID
    # Please update the file name (in brown) for the code below in the following cell.<br>
    # MstGrp = ProcessDSFile(pd.read_excel(io='./<font color='brown'>horis_MG_201903.xlsx</font>'), InCols='Real Customer ID 1')
    #
    # if "**Can't find workbook in OLE2 compound document**" error appeared, please save the file to an unprotected MS Excel file before import.

    # [Return to Import File Path](#import_file_path)
    #

    # [Jump to Export Result](#export_result)

    # In[ ]:


    start = time.time()
    MstGrp = pd.read_excel(io=MstGrp_File)
    MstGrp = ProcessDSFile(MstGrp, InCols='CIN')
    MstGrp = MstGrp[MstGrp['Master_Group_ID'] != 1514726659]
    MstGrp = MstGrp[MstGrp['Master_Group_ID'] != 1514726667]

    MIWs01, LTitle = ImportData(MIWs01, MstGrp, ImMethod=0, MapCol=(['CIN', 'MasterGroup ID', 'MasterGroup Name'], ['CIN', 'Master_Group_ID', 'Master_Group_Name']))
    ImportedList += LTitle
    print('Imported for:')
    print(LTitle)
    print('\n')
    stop = time.time()
    print('Imported Master Group and Master Group ID to Master MI.')
    TimeSpent(start, stop)


    # ## Import "MGCSM CM List" for Selected MG Case

    # [Return to Import File Path](#import_file_path)

    # [Jump to Export Result](#export_result)

    # In[ ]:


    # get_ipython().run_cell_magic('time', '', "MGCSM_CMList = pd.read_excel(MGCSM_File)\n\ntmpDF = MIWs01.merge(MGCSM_CMList[['Master Group ID', 'MG CM owner']], how='left', left_on='MasterGroup ID', right_on='Master Group ID')\n\nMIWs01['Selected MGs'] = tmpDF['MG CM owner']\nLTitle = ['Selected MGs']\nImportedList += LTitle\n\nprint('Imported for:')\nprint(LTitle)\n\nprint('Imported MGCSM CM List to Master MI.')\n")
    MGCSM_CMList = pd.read_excel(MGCSM_File)
    tmpDF = MIWs01.merge(MGCSM_CMList[['Master Group ID', 'MG CM owner']], how='left', left_on='MasterGroup ID', right_on='Master Group ID')
    MIWs01['Selected MGs'] = tmpDF['MG CM owner']
    LTitle = ['Selected MGs']
    ImportedList += LTitle
    print('Imported for:')
    print(LTitle)
    print('Imported MGCSM CM List to Master MI.')


    # # Import KPI7 Due Date

    # In[ ]:


    KPI =  pd.read_excel(KPI_File)

    print('Imported KPI duedate to Master MI.')
    KPI = KPI.loc[:, ['Customer Number','Overdue Date']].drop_duplicates()
    KPI.columns = ['CIN','KPI7 Due Date']
    #change data
    KPI.loc[KPI['KPI7 Due Date'] == '-', ['KPI7 Due Date']]  =  DT.datetime(1900, 1, 1, 0, 0)
    KPI['KPI7 Due Date'] = pd.to_datetime(KPI['KPI7 Due Date'] )
    #DROP DUPLICATES
    KPI_1 = KPI.drop_duplicates()
    KPI_1['rank_g'] = KPI_1.groupby(['CIN'])['KPI7 Due Date'].rank(ascending=False)
    KPI_final = KPI_1.loc[KPI_1['rank_g'] == 1, :].drop_duplicates()
    #KPI_2 = KPI.loc[KPI['Review Status'] == 'Approval Completed', :].drop_duplicates()
    #KPI_2 = KPI_2.loc[~KPI_2['CIN'].isin(KPI_1['CIN'].tolist()), :].drop_duplicates()

    #KPI_final = pd.concat([KPI_1,KPI_2]).drop(['rank_g','Review Status'],axis=1)

    MIWs01 = MIWs01.drop(['KPI7 Due Date'],axis = 1)
    MIWs01 = pd.merge(MIWs01,KPI_final, how='left',on='CIN' )

    ImportedList += ['KPI7 Due Date']


    # # Import Smart Serve Data

    # In[ ]:


    start = time.time()
    SMS = pd.read_excel(SMS_File)
    # SMS = ProcessDSFile(SMS, InCols='CIN')
    # SMS = SMS.sort_values(by='TASK MODIFIED DATE',ascending=False)


    SMS = ProcessDSFile(SMS, InCols='CIN', SortField='TASK MODIFIED DATE', DateField=True, asd=True)
    SMS['STATUS'] = SMS['STATUS'].fillna('')
    SMS = SMS.loc[SMS['BALANCE SHEET CODE']=='HBAP']
    SMS = SMS.loc[(SMS['STATUS'] != "ABANDONED") & (SMS['STATUS'] != "DRAFT") & (SMS['STATUS'] != "EXPIRED") & (SMS['STATUS'] != "INCOMPLETE_DRAFT") & (SMS['STATUS'] != "WITHDRAWN") & (SMS['STATUS'] != '') ]
    # SMS = SMS.drop_duplicates()


    # SMS.to_excel(r'C:\Users\43792723\Desktop\Python\SMS.xlsx')
    # MIWs01, LTitle = ImportData(MIWs01, SMS, ImMethod=1, ImType="SMS", InColM='CIN', InColS='CIN')

    MIWs01, LTitle = ImportData(MIWs01, SMS, ImMethod=0, MapCol=(['CIN', 'SS-Case Created Date', 'SS-Status'], ['CIN', 'CASE CREATED DATE','STATUS']))

    ImportedList += LTitle
    print('Imported for:')
    print(LTitle)
    print('\n')
    stop = time.time()
    print('Imported Smart Serve Create Date and Status to Master MI.')
    TimeSpent(start, stop)



    # # Export Result
    # After Importing, the Master MI will be exported to a MS Excel file.<br>
    # The file has 2 worksheets.<br>
    # The first worksheet is the Master MI with imported columns only.<br>
    # The second one is listing out which columns are imported.<br>
    # <br>
    # After exporting, please run the VBA subroutine "**CopyColumnFromMIPy**" for copying the data back to Master MI.
    #
    # <a id='export_result'></a>

    # [Return to Import File Path](#import_file_path)

    # In[ ]:


    MIWs01 = FixColumnSeq(MIWs01)


    # In[ ]:


    # get_ipython().run_cell_magic('time', '', 'if wError == 0:\n    start = time.time()\n\n    ####### Pre Export Adjustment #######\n#     SelGPTeam = MIWs01[\'RM Name\'].str.upper().isin(GPRM_Name)\n#     MIWs01.loc[SelGPTeam, \'RM Sub Team\'] = \'G&P\'\n#     MIWs01.loc[SelGPTeam, \'RM Team Group\'] = \'G&P\'\n#     MIWs01.loc[SelGPTeam, \'Segment\'] = \'CMB\'\n\n\n    MIWs01 = FixColumnSeq(MIWs01)\n    ImportedList = list(set(ImportedList))\n    ImportedList.sort()\n\n\n\n    ImportedList02 = ImportedList.copy()\n\n    print(\'All imported column(s):\')\n    print(ImportedList)\n    print(\'\\n\')\n    print(\'Exporting...\')\n    ImportedList02 = MIWs01.columns.tolist()[:3] + ImportedList02\n    DF2 = pd.DataFrame(data={\'Column Name\' : ImportedList})\n    MIWs02 = MIWs01[ImportedList02]\n\n    ###########\n    writer = pd.ExcelWriter(\'MI-\' + DT.datetime.now().strftime("%Y%m%d") + \'.xlsx\')\n    ###########\n\n    MIWs02.to_excel(writer,\'Master MI\')\n    DF2.to_excel(writer,\'Imported Columns\', index=False)\n    writer.save()\n    print(\'Done!\')\n    #MIWs01.to_excel(\'./MI-20190510.xlsx\', index=False)\n    stop = time.time()\n\n    TimeSpent(start, stop)\nelse:\n    print("Please ensure Data are imported properly.")\n')
    if wError == 0:
        start = time.time()
        ####### Pre Export Adjustment #######
    #     SelGPTeam = MIWs01['RM Name'].str.upper().isin(GPRM_Name)
    #     MIWs01.loc[SelGPTeam, 'RM Sub Team'] = 'G&P'
    #     MIWs01.loc[SelGPTeam, 'RM Team Group'] = 'G&P'
    #     MIWs01.loc[SelGPTeam, 'Segment'] = 'CMB'
        MIWs01 = FixColumnSeq(MIWs01)
        ImportedList = list(set(ImportedList))
        ImportedList.sort()
        ImportedList02 = ImportedList.copy()
        print('All imported column(s):')
        print(ImportedList)
        print('\n')
        print('Exporting...')
        ImportedList02 = MIWs01.columns.tolist()[:3] + ImportedList02
        DF2 = pd.DataFrame(data={'Column Name' : ImportedList})
        MIWs02 = MIWs01[ImportedList02]
        ###########
        writer = pd.ExcelWriter('MI-' + DT.datetime.now().strftime("%Y%m%d") + '.xlsx')
        ###########
        MIWs02.to_excel(writer,'Master MI')
        DF2.to_excel(writer,'Imported Columns', index=False)
        writer.save()
        print('Done!')
        #MIWs01.to_excel('./MI-20190510.xlsx', index=False)
        stop = time.time()
        TimeSpent(start, stop)
    else:
        print("Please ensure Data are imported properly.")


    # # Change Log
    #
    # **This file was updated on 15 Jun 2023.**<br>
    # Update code for Adjustment of QV staff
    #
    # **This file was updated on 22 Feb 2023.**<br>
    # Update code for label KPI 7
    #
    # **This file was updated on 29 Nov 2021.**<br>
    # Update Code for Checking QV Files.<br>
    #
    # **This file was updated on 29 Nov 2021.**<br>
    # Update code for new data source.<br>
    #
    # **This file was updated on 17 Jun 2021.**<br>
    # Update code for disbaling BoW related import.<br>
    #
    # **This file was updated on 15 Apr 2021.**<br>
    # Update code for MSC as file format changed.<br>
    #
    # **This file was updated on 3 Mar 2021.**<br>
    # Update code for new RM Segment for G&P.<br>
    #
    # **This file was updated on 26 Feb 2021.**<br>
    # Debug for NaN value in StaffList.<br>
    #
    # **This file was updated on 15 Feb 2021.**<br>
    # Update code for new RM Team G&P.<br>
    #
    # **This file was updated on 29 Jan 2021.**<br>
    # Update code for T90 Import Debug.<br>
    #
    # **This file was updated on 27 Jan 2021.**<br>
    # Update code for different KYC Ops CM Effective Date.<br>
    #
    # **This file was updated on 12 Jan 2021.**<br>
    # Update code for Off CRT Approval Record.<br>
    #
    # **This file was updated on 4 Jan 2021.**<br>
    # Update code on mapping Customer Name and relative information from Cognos.<br>
    #
    # **This file was updated on 10 Dec 2020.**<br>
    # Update code on Column "QVQC-Latest QC Completed by". (To remove "CM / ")<br>
    #
    # **This file was updated on 7 Dec 2020.**<br>
    # New Data Source RAM File for Medium Risk.<br>
    #
    # **This file was updated on 18 Nov 2020.**<br>
    # New Data Source MSC Client List.<br>
    #
    # **This file was updated on 12 Nov 2020.**<br>
    # To get S1 / BoW Segment and Team Record if no previous record.<br>
    #
    # **This file was updated on 8 Oct 2020.**<br>
    # Fine Tune S1 Import Logic.<br>
    # Updated Logic for Staff with role in KYC Ops and CM.<br>
    #
    # **This file was updated on 18 Aug 2020.**<br>
    # Fine Tune S1 Import Logic.<br>
    #
    # **This file was updated on 4 Aug 2020.**<br>
    # IDR was demised.<br>
    #
    # **This file was updated on 18 May 2020.**<br>
    # S1 Code is ready.<br>
    #
    # **This file was updated on 25 Apr 2020.**<br>
    # IMIS Group Information import is added.<br>
    #
    # **This file was updated on 14 Apr 2020.**<br>
    # Stage 1 import is added.<br>
    #
    # **This file was updated on 18 Dec 2019.**<br>
    # Add Code for Checking QV Files if the data are imported properly.<br>
    #
    # **This file was updated on 18 Dec 2019.**<br>
    # Add code for Relatioship ID import. And update SVS to PSE at Code Level.<br>
    #
    # **This file was updated on 11 Dec 2019.**<br>
    # Update Code for processing Incoming Doc Register for debug purpose.<br>
    #
    # **This file was updated on 5 Nov 2019.**<br>
    # Update Code for processing Incoming Doc Register.<br>
    #
    # **This file was updated on 4 Oct 2019.**<br>
    # Update Code Incoming Doc Register.<br>
    # Update Code for ProcessDSFile.<br>
    #
    # **This file was updated on 2 Sep 2019.**<br>
    # Update Code for import "T90".<br>
    #
    # **This file was updated on 28 Aug 2019.**<br>
    # Update Code for import "Tri-TgrTriage Status" & "Tri-TgrTriage Completion Date".<br>
    #
    # **This file was updated on 22 Aug 2019.**<br>
    # Debug for importing BAU Cust Info RM.<br>
    #
    # **This file was updated on 22 Aug 2019.**<br>
    # Update Code for import "Tri-TgrTriage Status" & "Tri-TgrTriage Completion Date" (Needs further Checking).<br>
    #
    # **This file was updated on 19 Aug 2019.**<br>
    # Update Code for import Customer Name.<br>
    #
    # **This file was updated on 1 Aug 2019.**<br>
    # Add code for QVQA import.<br>
    #
    # **This file was updated on 25 Jul 2019.**<br>
    # Add code for skipping some Master Group ID.<br>
    #
    # **This file was updated on 8 Jul 2019.**<br>
    # Add code for checking duplicate ID.<br>
    #
    # **This file was updated on 5 Jul 2019.**<br>
    # Further debug.<br>
    #
    # **This file was updated on 21 Jun 2019.**<br>
    # Updated code for importing SCC. To remove if there is non SCCS case on the SCC List.<br>
    #
    # **This file was updated on 10 Jun 2019.**<br>
    # Removed code for importing OKYC Eligiblity.<br>
    #
    # **This file was updated on 30 May 2019.**<br>
    # Change the logic of importing Acc Close info. Skipped import for old Customer ID.<br>
    #
    # **This file was updated on 24 May 2019.**<br>
    # Updated import GS CDD FullList Master template, as Staff List and Trigger code will be exported from Master MI at the sametime.<br>
    # Disable code for import CM Trackers. User can use "Run All".<br>
    # Updated some parameters for code for importing.<br>
    # Debug for QVOpen, treatment on "-" is done.<br>
    #
    # **This file was updated on 21 May 2019.**<br>
    # Added code for import Master Group and Master Group ID (for monthly update purpose).<br>
    #
    # **This file was updated on 20 May 2019.**<br>
    # Updated ProcessDSFile.<br>
    # Import QVEsc, QVOpen, QVQC, QVClosedAPP & QVClosedCAN Files are ready.<br>
    #
    # **This file was updated on 16 May 2019.**<br>
    # Import for T90 BBRM Decision and Remarks.<br>
    #
    # **This file was updated on 15 May 2019.**<br>
    # Import for QVFiles.<br>
    # (Tested QVEsc, QVOpen, QVQC, QVClosedAPP & QVClosedCAN.<br>
    # Add CheckDF function for easy comparing record imported by VBA.<br>
    #
    #
    # **This file was updated on 10 May 2019.**<br>
    # Add new variable _ImportedList_ for advising which columns are imported.<br>
    # Admended Export file, list of imported columns is saved in the same workbook.<br>
    # Add new example and remarks for ImportData.<br>
    # Updated Import sessions' output message.<br>
    #
    # **This file was updated on 6 May 2019.**<br>
    # Revised Merge Old Customer ID function.<br>
    # Revised Import function.<br>
    # Add code for import "BAU Cust Info RM (CI to CIN)".

    # In[ ]:




