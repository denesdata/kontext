import pandas as pd, numpy as np

def get_matches_from_list(filenames,sheetnames,column_keys,skiprows,shift=0):
    matches=[]
    if type(filenames)!=list:
        filenames=[filenames]
    if type(sheetnames)!=list:
        sheetnames=[sheetnames]
    for filename in filenames:
        for sheetname in sheetnames:
            df=pd.read_excel(filename,sheet_name=sheetname,skiprows=skiprows,header=None)
            df[column_keys['match_type']+shift]=df[column_keys['match_type']+shift].fillna(method='ffill')
            for i in df.T.iteritems():
                match={}
                for j in column_keys:
                    if type(column_keys[j])==dict:
                        match[j]={}
                        for k in column_keys[j]:
                            match[j][k]=i[1][column_keys[j][k]+shift]
                    elif j=='match_type':
                        match[j]=filename+'#'+sheetname+'$'+str(i[1][column_keys[j]+shift])
                    else:
                        match[j]=i[1][column_keys[j]+shift]
                matches.append(match)
    return matches

def get_matches_from_table(filename,sheetnames,skiprows,nrows=0,shift=0,drops=[]):
    matches=[]
    if type(sheetnames)!=list:
        sheetnames=[sheetnames]
    for sheetname in sheetnames:
        df=pd.read_excel(filename,sheet_name=sheetname,header=None,skiprows=skiprows)
        df=df[df.columns[shift:]].drop(drops,axis=1)
        df=df.reset_index(drop=True)
        df.columns=range(len(df.columns))
        if nrows>0:
            df=df.loc[:nrows]
        for i in range(len(df.index)//2):
            for j in range(1,len(df.index)//2+1):
                if i<(j-1):
                    match={'match_type':sheetname,'aka':{'name':df.loc[i*2][0],
                              'point1':df.loc[i*2+1][j*2],'point2':df.loc[i*2+1][j*2+1]},
                     'shiro':{'name':df.loc[(j-1)*2][0],
                              'point1':df.loc[(j-1)*2+1][(i+1)*2],'point2':df.loc[(j-1)*2+1][(i+1)*2+1]}}
                    matches.append(match)    
    return matches

def get_matches_from_table_oneliner(filename,sheetnames,skiprows,nrows=0,shift=0,point_shift=1,drops=[]):
    matches=[]
    if type(sheetnames)!=list:
        sheetnames=[sheetnames]
    for sheetname in sheetnames:
        df=pd.read_excel(filename,sheet_name=sheetname,header=None,skiprows=skiprows)
        df=df[df.columns[shift:]].drop(drops,axis=1)
        df=df.reset_index(drop=True)
        df.columns=range(len(df.columns))
        if nrows>0:
            df=df.loc[:nrows-1]
        for i in range(len(df.index)):
            for j in range(1,len(df.index)+1):
                if i<(j-1):
                    match={'match_type':sheetname,'aka':{'name':df.loc[i][0],
                              'point1':df.loc[i][j+point_shift]},
                     'shiro':{'name':df.loc[(j-1)][0],
                              'point1':df.loc[(j-1)][i+point_shift+1]}}
                    matches.append(match)    
    return matches

def get_matches(year,competition,stage=''):
    path='../data/raw/'+str(year)+'/'+str(competition)+'/'
    column_keys={'match_type':2,'aka':{'name':5,'hansoku':6,'point1':7,'point2':8,'point3':9},
                         'shiro':{'name':15,'hansoku':14,'point1':11,'point2':12,'point3':13},'outcome':10,
                         'shinpan':{'fukushin1':16,'shushin':17,'fukushin2':18}}
    column_keys_ns={'match_type':2,'aka':{'name':5,'hansoku':6,'point1':7,'point2':8,'point3':9},
                         'shiro':{'name':15,'hansoku':14,'point1':11,'point2':12,'point3':13},'outcome':10}
    column_keys_012_653_789={'match_type':0,'aka':{'name':1,'point1':2},
             'shiro':{'name':6,'point1':5},'outcome':3,
             'shinpan':{'fukushin1':7,'shushin':8,'fukushin2':9}}
    column_keys_012_543={'match_type':0,'aka':{'name':1,'point1':2},
             'shiro':{'name':5,'point1':4},'outcome':3}
    column_keys_013_654={'match_type':0,'aka':{'name':1,'point1':3},
             'shiro':{'name':6,'point1':5},'outcome':4}
    column_keys_2012_543={'match_type':20,'aka':{'name':1,'point1':2},
             'shiro':{'name':5,'point1':4},'outcome':3}
    column_keys_1512_543={'match_type':15,'aka':{'name':1,'point1':2},
             'shiro':{'name':5,'point1':4},'outcome':3}
    column_keys_612_543={'match_type':6,'aka':{'name':1,'point1':2},
             'shiro':{'name':5,'point1':4},'outcome':3}
    column_keys_312_543={'match_type':3,'aka':{'name':1,'point1':2},
             'shiro':{'name':5,'point1':4},'outcome':3}
    sheetname='List of matches'
    matches=[]
    
    if year==2018:
        if competition=='CR':
            filename=path+'CR25 - Public.xlsx'
            matches=matches+get_matches_from_list(filename,sheetname,column_keys,3,stage=stage)
        elif competition=='SL':
            filename=path+'Prezenta SL_WKC17.xlsx'
            sheetname=['F','M']
            matches=matches+get_matches_from_table(filename,sheetname,5,stage=stage)
        elif competition=='CN':
            filename=path+'Event management CN25.xlsx'
            sheetname='Shiai'
            column_keys['match_type']=3
            matches=matches+get_matches_from_list(filename,sheetname,column_keys,7,shift=-1,stage=stage)
    elif year==2017:
        if competition=='CN':
            categoriess=[['Individual masculin','Echipe'],
                        ['Individual juniori mici','Individual juniori mari','Individual feminin']]
            shifts=[0,-1]
            for i in range(len(categoriess)):
                categories=categoriess[i]
                shift=shifts[i]
                filename=[path+i+'.xlsx' for i in categories]
                matches=matches+get_matches_from_list(filename,sheetname,column_keys,3,shift=shift,stage=stage)
        elif competition=='CR':
            categoriess=[['Individual masculin'],
                        ['Individual juniori','Individual veterani','Individual feminin'],
                        ['Echipe']]
            shifts=[2,-1,0]
            for i in range(len(categoriess)):
                categories=categoriess[i]
                shift=shifts[i]
                filename=[path+i+'.xlsx' for i in categories]
                matches=matches+get_matches_from_list(filename,sheetname,column_keys_ns,3,shift=shift,stage=stage)
        elif competition=='SL':
            filename=path+'Prezenta.xlsx'
            sheetname=['F','M','J']
            matches=matches+get_matches_from_table(filename,sheetname,6,stage=stage)
    elif year==2016:
        if competition=='SL':
            filename=path+'Event management - stagiul 4.xlsx'
            sheetnames=[['F','M'],['J']]
            skiprows=[6,5]
            for i in range(len(sheetnames)):
                sheetname=sheetnames[i]
                skiprow=skiprows[i]
                matches=matches+get_matches_from_table(filename,sheetname,skiprow,stage=stage)
        elif competition=='CN':
            categoriess=[['Individual masculin'],
                        ['Echipe','Male team'],
                        ['Individual feminin','Junior 1 individual','Junior 2 individual']
                        ]
            shifts=[2,0,-1]
            for i in range(len(categoriess)):
                categories=categoriess[i]
                shift=shifts[i]
                filename=[path+i+'.xlsx' for i in categories]
                matches=matches+get_matches_from_list(filename,sheetname,column_keys_ns,3,shift=shift,stage=stage)
        elif competition=='CR':
            filename=path+'Event management_CR23.2016.xlsx'
            sheetnames=[['IF_m','IJ_m','IM_m','IS_m'],['EJ_m','ES_m']]
            skiprows=[4,6]
            for i in range(len(sheetnames)):
                sheetname=sheetnames[i]
                skiprow=skiprows[i]
                matches=matches+get_matches_from_list(filename,sheetname,column_keys_012_653_789,skiprow,stage=stage)
    elif year==2015:
        if competition=='SL':
            filename=path+'Event management - stagiul 5.xlsx'
            sheetname=['SF_s','SM_s']
            matches=matches+get_matches_from_table(filename,sheetname,6,stage=stage)
        elif competition=='CN':
            filename=path+'Event management_CN22.2015.xlsx'
            sheetnames=[['IF_m','IJ2_m','IM_m'],['E_m']]
            skiprows=[4,6]
            for i in range(len(sheetnames)):
                sheetname=sheetnames[i]
                skiprow=skiprows[i]
                matches=matches+get_matches_from_list(filename,sheetname,column_keys_012_653_789,skiprow,stage=stage)
        elif competition=='CR':
            filename=path+'Event management_CR22.2015.xlsx'
            #part 1
            sheetnames=[['IF_m','IS_m'],['IM_s'],['IM_s']]
            skiprows=[4,7,7]
            shifts=[0,19,29]
            cks=[column_keys_012_653_789,column_keys_012_543,column_keys_012_543,]
            for i in range(len(sheetnames)):
                sheetname=sheetnames[i]
                skiprow=skiprows[i]
                shift=shifts[i]
                ck=cks[i]
                matches=matches+get_matches_from_list(filename,sheetname,ck,skiprow,shift=shift,stage=stage)
            #part 2
            sheetnames=[['IJ1_s'],['IJ2_s'],['IJ2_s']]
            skiprows=[7,8,16]
            shifts=[1,12,12]
            nrowss=[9,8,8]
            for i in range(len(sheetnames)):
                sheetname=sheetnames[i]
                skiprow=skiprows[i]
                shift=shifts[i]
                nrows=nrowss[i]
                matches=matches+get_matches_from_table(filename,sheetname,skiprows=skiprow,
                                                     shift=shift,nrows=nrows,stage=stage)
    elif year==2014:
        if competition=='SL':
            filename=path+'Lista de participanti 6.xlsx'
            sheetname=['SF_s','SM_s','J_s']
            matches=matches+get_matches_from_table(filename,sheetname,6)
        elif competition=='CR':
            filename=path+'Event management_CR21.2014.xlsx'
            sheetnames=[['IC-10_m','IC_m','IJ_m','IS_m','IF_m'],['IM_s']]
            skiprows=[4,8]
            shifts=[0,8]
            cks=[column_keys_012_653_789,column_keys_012_543]
            for i in range(len(sheetnames)):
                sheetname=sheetnames[i]
                skiprow=skiprows[i]
                shift=shifts[i]
                ck=cks[i]
                matches=matches+get_matches_from_list(filename,sheetname,ck,skiprow,shift=shift,stage=stage)
        elif competition=='CN':
            filename=path+'Event management_CN21.2014 - v2.xlsx'
            #part 1
            sheetnames=[['IF_m'],['IM_s'],['IM_s']]
            shifts=[0,19,29]
            skiprows=[4,7,7]
            cks=[column_keys_012_653_789,column_keys_012_543,column_keys_012_543]
            for i in range(len(sheetnames)):
                sheetname=sheetnames[i]
                skiprow=skiprows[i]
                shift=shifts[i]
                ck=cks[i]
                matches=matches+get_matches_from_list(filename,sheetname,ck,skiprow,shift=shift,stage=stage)
            #part 2
            sheetnames=[['IJ1_s'],['IJ2_s'],['IJ2_s'],['IJ2_s']]
            skiprows=[7,8,14,20]
            shifts=[1,12,12,12]
            nrowss=[10,6,6,6]
            for i in range(len(sheetnames)):
                sheetname=sheetnames[i]
                skiprow=skiprows[i]
                shift=shifts[i]
                nrows=nrowss[i]
                matches=matches+get_matches_from_table(filename,sheetname,skiprows=skiprow,
                                                     shift=shift,nrows=nrows,stage=stage)
    elif year==2013:
        if competition=='CN':
            filename=path+'Event management_CN2013.xlsx'
            sheetname=['IS_m','IF_m','IC_m','IJ_m','E_m','IM_m']
            matches=matches+get_matches_from_list(filename,sheetname,column_keys_012_653_789,4,stage=stage)
        elif competition=='CR':
            filename=path+'Event management_CR2013.xlsx'
            sheetname=['IF_meciuri','IJ_meciuri','IM_meciuri']
            matches=matches+get_matches_from_list(filename,sheetname,column_keys_012_653_789,4,stage=stage)
        elif competition=='SL':
            #part 1
            filename=path+'Event management.xlsx'
            sheetname=['E_meciuri']
            matches=matches+get_matches_from_list(filename,sheetname,column_keys_012_653_789,4,stage=stage)            
            #part 2
            sheetnames=[['Schema feminin'],['Schema juniori']]
            nrowss=[14,12]
            for i in range(len(sheetnames)):
                sheetname=sheetnames[i]
                nrows=nrowss[i]
                matches=matches+get_matches_from_table(filename,sheetname,2,nrows=nrows,stage=stage)
    elif year==2012:
        if competition=='CN':
            filename=path+'Event management CN2012.xlsx'
            sheetname=['E_meciuri','IJ_meciuri','IF_meciuri','IM_meciuri']
            matches=matches+get_matches_from_list(filename,sheetname,column_keys_012_653_789,4,stage=stage)
        elif competition=='CR':
            filename=path+'2012.05.05-06 - CR - Cluj.xlsx'
            #part 1
            sheetnames=[['IC'],['IC'],['IJ'],['IJ'],['IJ'],['IJ'],['IJ'],['IF'],['IF']]
            skiprows=[12,18,14,19,24,30,35,13,18]
            shifts=[1,1,1,1,1,1,1,1,1]
            nrowss=[3,4,3,3,3,3,3,3,3]
            for i in range(len(sheetnames)):
                sheetname=sheetnames[i]
                skiprow=skiprows[i]
                shift=shifts[i]
                nrows=nrowss[i]
                matches=matches+get_matches_from_table_oneliner(filename,
                                            sheetname,skiprow,shift=shift,nrows=nrows,stage=stage)
            #part 2
            sheetnames=[['IF'],['IM'],['ES'],['ES'],['ES']]
            shifts=[0,6,-1,4,9]
            skiprows=[22,6,4,4,4]
            cks=[column_keys_013_654,column_keys_012_543,column_keys_2012_543,
                column_keys_2012_543,column_keys_2012_543]
            for i in range(len(sheetnames)):
                sheetname=sheetnames[i]
                skiprow=skiprows[i]
                shift=shifts[i]
                ck=cks[i]
                matches=matches+get_matches_from_list(filename,sheetname,ck,skiprow,shift=shift,stage=stage)
    elif year==2011:
        if competition=='CN':
            filename=path+'2011.11.26-27 - CN - Bucuresti_print.xlsx'
            #part 1
            sheetnames=[['IJ'],['IJ'],['IJ'],['IF'],['IF'],['IF']]
            skiprows=[13,18,23,13,18,23]
            shifts=[1,1,1,1,1,1]
            nrowss=[3,3,10,3,3,4]
            for i in range(len(sheetnames)):
                sheetname=sheetnames[i]
                skiprow=skiprows[i]
                shift=shifts[i]
                nrows=nrowss[i]
                matches=matches+get_matches_from_table_oneliner(filename,
                                            sheetname,skiprow,shift=shift,nrows=nrows,stage=stage)
            #part 2
            sheetnames=[['IF'],['IM'],['IM'],['E'],['E'],['E']]
            shifts=[0,5,11,17,23,29]
            skiprows=[28,6,6,5,5,5]
            cks=[column_keys_013_654,column_keys_012_543,column_keys_012_543,column_keys_012_543,
                 column_keys_012_543,column_keys_012_543]
            for i in range(len(sheetnames)):
                sheetname=sheetnames[i]
                skiprow=skiprows[i]
                shift=shifts[i]
                ck=cks[i]
                matches=matches+get_matches_from_list(filename,sheetname,ck,skiprow,shift=shift,stage=stage)
        elif competition=='CR':
            filename=path+'2011.04.16-17 - CR - Miercurea Ciuc.xlsx'
            #part 1
            sheetnames=[['ES'],['ES'],['ES'],['IM'],['IM'],['IF'],['EJ']]
            shifts=[-1,5,11,5,11,0,0]
            skiprows=[7,7,7,6,6,26,15]
            cks=[column_keys_612_543,column_keys_612_543,column_keys_612_543,column_keys_012_543,
                column_keys_012_543,column_keys_013_654,column_keys_012_543]
            for i in range(len(sheetnames)):
                sheetname=sheetnames[i]
                skiprow=skiprows[i]
                shift=shifts[i]
                ck=cks[i]
                matches=matches+get_matches_from_list(filename,sheetname,ck,skiprow,shift=shift,stage=stage)
            #part 2
            sheetnames=[['IF'],['IF'],['IJ'],['IJ'],['IJ'],['IC']]
            skiprows=[15,21,16,21,27,4]
            shifts=[1,1,1,1,1,0]
            nrowss=[4,4,3,4,3,4]
            for i in range(len(sheetnames)):
                sheetname=sheetnames[i]
                skiprow=skiprows[i]
                shift=shifts[i]
                nrows=nrowss[i]
                matches=matches+get_matches_from_table_oneliner(filename,
                                            sheetname,skiprow,shift=shift,nrows=nrows,stage=stage)
    elif year==2010:
        if competition=='CN':
            filename=path+'2010.11.27-28 - CN - Bucuresti.xlsx'
            #part 1
            sheetnames=[['IJ'],['IC'],['IC'],['IF'],['IF']]
            skiprows=[13,13,18,13,18]
            shifts=[1,1,1,1,1]
            nrowss=[5,3,3,3,3]
            for i in range(len(sheetnames)):
                sheetname=sheetnames[i]
                skiprow=skiprows[i]
                shift=shifts[i]
                nrows=nrowss[i]
                matches=matches+get_matches_from_table_oneliner(filename,
                                            sheetname,skiprow,shift=shift,nrows=nrows,stage=stage)
            #part 2
            sheetnames=[['IM'],['IM'],['E'],['E'],['E']]
            shifts=[6,12,-1,5,11]
            skiprows=[4,4,5,5,5]
            cks=[column_keys_012_543,column_keys_012_543,column_keys_2012_543,column_keys_1512_543,
                column_keys_1512_543,column_keys_1512_543]
            for i in range(len(sheetnames)):
                sheetname=sheetnames[i]
                skiprow=skiprows[i]
                shift=shifts[i]
                ck=cks[i]
                matches=matches+get_matches_from_list(filename,sheetname,ck,skiprow,shift=shift,stage=stage)
        elif competition=='CR':
            filename=path+'2010.03.27-28 - CR - Budeasa.xlsx'
            #part 1
            sheetnames=[['IM'],['IM'],['IF'],['EJ']]
            shifts=[5,11,0,0]
            skiprows=[6,6,26,15]
            cks=[column_keys_012_543,column_keys_012_543,column_keys_013_654,column_keys_012_543]
            for i in range(len(sheetnames)):
                sheetname=sheetnames[i]
                skiprow=skiprows[i]
                shift=shifts[i]
                ck=cks[i]
                matches=matches+get_matches_from_list(filename,sheetname,ck,skiprow,shift=shift,stage=stage)
            #part 2
            sheetnames=[['IF'],['IF'],['IJ'],['IJ'],['IJ'],['IC']]
            skiprows=[15,21,16,21,27,4]
            shifts=[1,1,1,1,1,0]
            nrowss=[4,4,3,4,3,4]
            for i in range(len(sheetnames)):
                sheetname=sheetnames[i]
                skiprow=skiprows[i]
                shift=shifts[i]
                nrows=nrowss[i]
                matches=matches+get_matches_from_table_oneliner(filename,
                                            sheetname,skiprow,shift=shift,nrows=nrows,stage=stage)
    elif year==2009:
        if competition=='CN':
            filename=path+'2009.11.28-29 - CN - Bucuresti.xlsx'
            #part 1
            sheetnames=[['IJ'],['IF']]
            skiprows=[4,12]
            shifts=[0,1]
            point_shifts=[1,0]
            nrowss=[4,5]
            for i in range(len(sheetnames)):
                sheetname=sheetnames[i]
                skiprow=skiprows[i]
                shift=shifts[i]
                point_shift=point_shifts[i]
                nrows=nrowss[i]
                matches=matches+get_matches_from_table_oneliner(filename,sheetname,skiprow,
                                        shift=shift,point_shift=point_shift,nrows=nrows,stage=stage)
            #part 2
            sheetnames=[['IM'],['IM'],['ES'],['ES'],['ES']]
            shifts=[5,11,-1,5,11]
            skiprows=[6,6,7,7,7]
            cks=[column_keys_012_543,column_keys_012_543,column_keys_312_543,column_keys_312_543,
                column_keys_312_543]
            for i in range(len(sheetnames)):
                sheetname=sheetnames[i]
                skiprow=skiprows[i]
                shift=shifts[i]
                ck=cks[i]
                matches=matches+get_matches_from_list(filename,sheetname,ck,skiprow,shift=shift,stage=stage)             
        elif competition=='CR':
            filename=path+'2009.04.04 - CR - Budeasa - print.xlsx'
            #part 1
            sheetnames=[['IM'],['IM'],['ES'],['ES']]
            shifts=[5,11,-1,5]
            skiprows=[6,6,8,8]
            cks=[column_keys_012_543,column_keys_012_543,column_keys_312_543,column_keys_312_543]
            for i in range(len(sheetnames)):
                sheetname=sheetnames[i]
                skiprow=skiprows[i]
                shift=shifts[i]
                ck=cks[i]
                matches=matches+get_matches_from_list(filename,sheetname,ck,skiprow,shift=shift,stage=stage)
            #part 2
            sheetnames=[['IJ'],['IF']]
            skiprows=[12,13]
            shifts=[1,1]
            point_shifts=[0,0]
            nrowss=[5,6]
            for i in range(len(sheetnames)):
                sheetname=sheetnames[i]
                skiprow=skiprows[i]
                shift=shifts[i]
                point_shift=point_shifts[i]
                nrows=nrowss[i]
                matches=matches+get_matches_from_table_oneliner(filename,sheetname,skiprow,
                                            point_shift=point_shift,shift=shift,nrows=nrows,stage=stage)
    elif year==1993:
        if competition=='CR':
            filename=path+'1993.07.24 - Cupa Romaniei_print.xlsx'
            #part 1
            #part 2
            sheetnames=[['IF']]
            skiprows=[11]
            shifts=[1]
            point_shifts=[1]
            nrowss=[4]
            for i in range(len(sheetnames)):
                sheetname=sheetnames[i]
                skiprow=skiprows[i]
                shift=shifts[i]
                point_shift=point_shifts[i]
                nrows=nrowss[i]
                matches=matches+get_matches_from_table_oneliner(filename,sheetname,skiprow,
                                            point_shift=point_shift,shift=shift,nrows=nrows,stage=stage)
    return matches