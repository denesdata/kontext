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
                        match[j]=filename+'#'+str(i[1][column_keys[j]+shift])
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