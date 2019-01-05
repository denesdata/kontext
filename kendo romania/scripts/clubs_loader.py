import pandas as pd, numpy as np, json

pretty_clubs={'ARK':'Asociația Română de Kendo', 'ARA':'Arashi', 'BDS':'Budoshin', 'BSD':'Bushido', 'BTK':'Bushi Tokukai', 'BG':'Bulgaria','FDS':'Fudoshin','BE':'Belgium',
              'CDO':'Coroana de Oțel', 'CRK':'Clubul Român de Kendo', 'HAR':'Hargita', 
              'ICH':'Ichimon', 'IKA':'Ikada','ISH':'Ishhin', 'IT':'Italy','HU':'Hungary','HUN':'Hungary',
              'KAS':'Kashi', 'KNS':'Kenshin', 'KYO':'Kyobukan', 'MC':'Macedonia',
              'SR':'Serbia', 'MN':'Montenegro', 'MD':'Moldova','MOL':'Moldova', 'MUS':'Museido', 
              'RON':'Ronin-do', 'SAK':'Sakura', 'SAM':'Sam-sho','SAN':'Sankon', 'SBK':'Sobukan',
              'SON':'Sonkei', 'SR':'Serbia', 'TAI':'Taiken', 'TR':'Turkey','ACKIJ':'ACKIJ',
               'YUK':'Yu-kai','KAY':'Kaybukan','CNT':'Cantemir','XXX':'Unknown'}

club_equals={'MLD':'MOL/Md',
             'MOL':'MOL/Md',
             'IKD':'IKA',
             'HUN':'HUN/Hu',
             'BUL':'BUL/Bg',
             'TUR':'TUR/Tr',
             'MAC':'MAC/Mc',
             'MNE':'MNE/Mn',
             'SRB':'SRB/Sr',
             'ITA':'ITA/It',
             'ISS':'ISH',
             'Musso, Bg':'MUS/Bg',
             'Makoto, Sr':'MAK/Sr',
             'Szeged, Hu':'SZE/Hu'}
    
def pretty(club):
    if club in pretty_clubs: 
        return pretty_clubs[club]
    else:
        print ('Warning! Full name for',club,'not known..')
        return club
    
def pretty_cc(club, country):
    if country!='RO':
        return pretty(country)
    else: return pretty(club)
    
def club_cleaner(club,country='RO'):
    if club in club_equals:
        club=club_equals[club]
    if str(club)=='nan':
        club='XXX'
    if '/' in club:
        return club.split('/')[0],club.split('/')[1].upper()
    else:
        return club,country

def replacer(club):
    club_replacer={'':'KYO'}
    if club in club_replacer:
        return club_replacer[club]
    else:
        return club
    
def get_club_by_year(d,club,year,mingrade,maxyear):
    if d==[]:
        return [club]
    else:
        years={}
        transfer_years=[mingrade]+[i['time'] for i in d]+[maxyear]
        transfer_clubs=[d[0]['from']]+[i['to'] for i in d]
        for i in range(1,len(transfer_years)):
            for y in range(transfer_years[i-1],transfer_years[i]+1):
                if y not in years:years[y]=[]
                years[y].append(transfer_clubs[i-1])
        return years[year]
    
def add_to_club(data,club,year,d):
    if club not in data: data[club]={}
    if year not in data[club]:data[club][year]=[]
    data[club][year].append(d)
    return data

club_year_df=pd.read_excel('../data/manual/Gantt-club.xlsx')
club_year_df=club_year_df[['Cod', 'Nume organizație',             'Oraș',
                  'start',              'end',        'alternate']]
club_year_df=club_year_df[~np.isnan(club_year_df['start'])].set_index('Cod')
def club_year(club,country,year,xxx=True):
    if country=='RO':
        if club in club_year_df.index:
            df=club_year_df.loc[club]
            if xxx:
                if year<df['start']:
                    club='XXX'
                if year>df['end']:
                    club='XXX'
            if str(df['alternate'])!='nan':
                alternate=df['alternate'].split(',')
                if int(alternate[1])<=year<=int(alternate[2]):
                    return club,pretty_cc(alternate[0], country)
        else:
            for i in club_year_df['alternate'].dropna().iteritems():
                if club==i[1].split(',')[0]:
                    return club_year(i[0],country,year)
    return club,pretty_cc(club, country)
    