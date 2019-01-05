import pandas as pd
def save(data):
    print('Saving matches...')
    data['aka hansoku']=data['aka hansoku'].replace(0,'').replace(1,'Δ')
    data['shiro hansoku']=data['shiro hansoku'].replace(0,'').replace(1,'Δ')
    data.to_csv('../data/export/matches.csv')
    print('Saving players...')
    aka=data[[i for i in data.columns if 'shiro ' not in i]]
    aka.columns=[i.replace('aka ','') for i in aka.columns]
    aka['color']='aka'
    aka['opponent']=data['shiro name']
    aka=aka.reset_index()
    shiro=data[[i for i in data.columns if 'aka ' not in i]]
    shiro.columns=[i.replace('shiro ','') for i in shiro.columns]
    shiro['color']='shiro'
    shiro['opponent']=data['aka name']
    shiro=shiro.reset_index()
    extended_matches=pd.concat([aka,shiro],axis=0).reset_index(drop=True)
    extended_matches.to_csv('../data/export/extended_matches.csv')
    print('Saving points...')
    p1=extended_matches[[i for i in extended_matches.columns if i!='point2']]
    p2=extended_matches[[i for i in extended_matches.columns if i!='point1']]
    p1.rename(columns={'point1':'point'}, inplace=True)
    p2.rename(columns={'point2':'point'}, inplace=True)
    extended_points=pd.concat([p1,p2],axis=0).reset_index(drop=True)
    extended_points.to_csv('../data/export/extended_points.csv')
    print('Saving shinpan...')
    shu=extended_points[[i for i in extended_points.columns if 'fukushin' not in i]]
    shu.columns=[i.replace('shushin','shinpan') for i in shu.columns]
    fk1=extended_points[[i for i in extended_points.columns if 'shushin' not in i and 'fukushin2' not in i]]
    fk1.columns=[i.replace('fukushin1','shinpan') for i in fk1.columns]
    fk2=extended_points[[i for i in extended_points.columns if 'shushin' not in i and 'fukushin1' not in i]]
    fk2.columns=[i.replace('fukushin2','shinpan') for i in fk2.columns]
    extended_shinpan=pd.concat([shu,fk1,fk2],axis=0).reset_index(drop=True)
    extended_shinpan.to_csv('../data/export/extended_shinpan.csv')