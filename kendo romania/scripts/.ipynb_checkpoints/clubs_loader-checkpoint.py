import pandas as pd, numpy as np, json

def pretty(club):
    pretty_clubs={'ARA':'Arashi', 'BDS':'Budoshin', 'BSD':'Bushido', 'BTK':'Bushi Tokukai', 'BG':'Bulgaria',
              'CDO':'Coroan de Oțel', 'CRK':'Clubul Român de Kendo', 'HAR':'Hargita', 
              'ICH':'Ichimon', 'IKA':'Ikada','ISH':'Ishhin', 'IT':'Italy','HU':'Hungary','HUN':'Hungary',
              'KAS':'Kashi', 'KNS':'Kenshin', 'KYO':'Kyobukan', 'MC':'Macedonia',
              'SR':'Serbia', 'MN':'Montenegro', 'MOL':'Moldova', 'MUS':'Museido', 
              'RON':'Ronin-do', 'SAK':'Sakura', 'SAM':'Sam-sho','SAN':'Sankon', 'SBK':'Sobukan',
              'SON':'Sonkei', 'SR':'Serbia', 'TAI':'Taiken', 'TR':'Turkey','ACKIJ':'ACKIJ',
               'YUK':'Yu-kai','KAY':'Kaybukan'}
    if club in pretty_clubs: 
        return pretty_clubs[club]
    else:
        print ('Warning! Full name for',club,'not known..')
        return club

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
    