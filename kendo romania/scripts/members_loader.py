import pandas as pd, numpy as np, json
import clubs_loader

nyears=8
    
def get_members(path):
    members=pd.read_excel(path,header=[1])
    members=members[[231,                         'Nr. EKF',
                                  'Club',                      'Unnamed: 3',
                                'Numele',                       'Prenumele',
                                   'Gen',                   'Data naşterii',
                                  '1 kyu','practică',
                                 '1 dan',                           '2 dan',
                                 '3 dan',                           '4 dan',
                                 '5 dan',                           '6 dan',
                                 '7 dan',                           '8 dan',
                                    151,
                                     152,                           '152.1',
                                     175,                               179,
                                     197,214,'231.1']]
    members.columns=list(members.columns[:-nyears])+list(range(2019-nyears,2019))
    return members

def get_transfer(name,tf,verbose=False):
    if tf==[]:
        return tf
    else:
        to_blank=[' ','(',')','Transfer:','?','/']
        to_replace={'Hungary':'HUN'}
        to_year={'Gușu Rebeca':'2010'}

        def get_tf_clubs(z):
            for t in range(len(to_blank)):
                z=z.replace(to_blank[t],'')
            for t in to_replace:
                z=z.replace(t,to_replace[t])
            if ('=>') in z:
                from_to=z.find('=>')
                to_return={'from':z[from_to-3:from_to],'to':z[from_to+2:from_to+5],'time':z[-4:]}
                if verbose:
                    to_return['orig']=z
            else:
                print('error with transfer',z,)
                to_return=z

            ##check years
            #infer year from wrong note order
            if '20' not in to_return['time']:
                if '20' in z:
                    to_return['time']=z[z.find('20'):z.find('20')+4]
            #if still not inferred, then manual fix
            if '20' not in to_return['time']:
                to_return['time']=to_year[name]
            to_return['time']=int(to_return['time'])
            return to_return

        transfers=str(tf).split('\n')
        tfr=[]
        for i in transfers:
            if not i in ('','nan'):
                tfr.append(get_tf_clubs(i))
        return sorted(tfr, key=lambda k: k['time'])

def cleaner(members):
    data={}
    replace_active={'Activ':'Active','Inactiv':'Inactive','Free':'Inactive','AS':'Abroad',
                    'Transferat':'Abroad','Decedat':'Inactive'}
    active_redflags=['Deleted']
    for i in members.T.iteritems():
        active=i[1][231]
        if active not in active_redflags:
            grades=i[1][['1 kyu','1 dan','2 dan','3 dan','4 dan','5 dan',
                         '6 dan','7 dan','8 dan']].replace('x',pd.NaT).dropna()
            grades0=i[1][['1 dan','2 dan','3 dan','4 dan','5 dan',
                          '6 dan','7 dan','8 dan']].replace('x',pd.NaT).dropna()
            df=pd.DataFrame(grades0)
            df.columns=['dan']
            df=df.reset_index().set_index('dan').sort_index()
            dummy={}
            grades=pd.to_datetime(grades.astype(str))
            active=replace_active[active]
            if len(grades)>0:
                mingrade=grades.min().year
                maxgrade=grades.max().year
            else:
                mingrade=2016 #default starting year
                maxgrade=2016
            if active=='Active':
                maxyear=2019 #default active max year
            else:
                maxyear=min(maxgrade+4,2019) #default active years grace period, if unknown

            dummy['name']=i[1]['Numele']+' '+i[1]['Prenumele']
            dummy['birth']=str(i[1]['Data naşterii'])[:10]
            dummy['gen']=i[1]['Gen']
            dummy['ekf']=i[1]['Nr. EKF']
            club=i[1]['Club']
            dummy['transfer']=get_transfer(dummy['name'],i[1]['Unnamed: 3'])

            for year in range(mingrade,maxyear):

                if year==maxyear-1:
                    dummy['active']=active
                else:
                    dummy['active']='Active'
                #get year from exams
                dummy['dan']=len(df[:str
                                    (year)])
                #get active from member list
                for j in i[1][-nyears:].index:
                    if year==j:
                        if i[1][-nyears:][j]=='Da':
                            dummy['active']=active
                        else:
                            dummy['active']='Inactive'
                #get club from transfers
                clubs=clubs_loader.get_club_by_year(dummy['transfer'],club,year,mingrade,maxyear)
                clubs=clubs[:1] #remove this step to double count. this limits to first club in transfer years
                for j in range(len(clubs)):
                    iclub=clubs_loader.replacer(clubs[j])
                    dummy['club']=iclub
                    dummy['age']=year-1-pd.to_datetime(dummy['birth']).year
                    data=clubs_loader.add_to_club(data,iclub,year,dummy.copy())

    all_data=[]

    for club in data:
        for year in data[club]:
            df=pd.DataFrame(data[club][year])
            df['year']=year
            df['club']=club
            df=df.drop('transfer',axis=1)
            all_data.append(df)

    return pd.concat(all_data).reset_index(drop=True)