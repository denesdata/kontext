import pandas as pd, numpy as np, json

def point_redflags(points):
    redflags_points=['Puncte']
    for redflag in redflags_points:
        if redflag in points:
            return False
    return True
        
def point_clean1(point):
    return point.replace('○','O').replace('I','H').replace('J','H').replace('×','')\
            .replace('–','').replace('1','O').replace('—','').replace('?','H')

def points_cleaner(points):
    points=str(points)
    hansoku=0
    encho=False
    if '∆' in points:
        hansoku=1
        points=points.replace('∆','')
    if '▲' in points:
        hansoku=1
        points=points.replace('▲','')
    if 'E' in points:
        encho=True
        points=points.replace('E','')
    if '(Ht)' in points:
        hansoku=1
        points=points.replace('(Ht)','')
    if '(victorie)' in points:
        points=points.replace('(victorie)','OO')
    if '?' in points:
        points=points.replace('?','')
    points=points.strip()
    if len(points)>2:
        print(points,'error')
    elif len(points)>1:
        point1=points[0]
        point2=points[1]
    elif len(points)>0:
        point1=points[0]
        point2=''
    else:
        point1=''
        point2=''
    point1=point_clean1(point1)
    point2=point_clean1(point2)
    return point1,point2,len(points),hansoku,encho

def match_cleaner(year,match):
    kind,phase='Unknown','Unknown'
    if '#' in match:
        stage0=match.split('#')[0].lower()
        stage1=match.split('#')[1]
        if 'pool' in stage1: 
            phase='Pool'
        if 'Pool' in stage1: 
            phase='Pool'
        elif 'prel' in stage1: 
            phase='Prelim.'
        elif 'Prel' in stage1: 
            phase='Prelim.'
        elif 'layoff' in stage1: 
            phase='Prelim.'
        elif '- F' in stage1: 
            phase='Finals'
        elif 'F -' in stage1: 
            phase='Finals'
        elif 'Final' in stage1: 
            phase='Finals'
        elif 'SF' in stage1: 
            phase='Finals'
        elif 'QF' in stage1: 
            phase='Finals'
        elif 'A'==stage1: phase='Pool'
        elif 'B'==stage1: phase='Pool'
        elif 'C'==stage1: phase='Pool'
        elif 'D'==stage1: phase='Pool'
        elif 'E'==stage1: phase='Pool'
        elif 'F'==stage1: phase='Pool'
        elif 'G'==stage1: phase='Pool'
        elif 'H'==stage1: phase='Pool'
        elif 'I'==stage1: phase='Pool'
        elif 'J'==stage1: phase='Pool'
        elif 'K'==stage1: phase='Pool'
        elif 'L'==stage1: phase='Pool'
        elif 'M'==stage1: phase='Pool'
        elif 'N'==stage1: phase='Pool'
        elif 'O'==stage1: phase='Pool'
        elif 'P'==stage1: phase='Pool'
        elif 'Q'==stage1: phase='Pool'
        elif 'R'==stage1: phase='Pool'
        elif 'S'==stage1: phase='Pool'
        elif 'T'==stage1: phase='Pool'
        
        if 'IS' in stage1:
            kind="Senior's Individual"
        elif 'IF' in stage1:
            kind="Women's Individual"
        elif 'IM' in stage1:
            kind="Men's Individual"
        elif 'IC' in stage1:
            kind="Children's Individual"
        elif 'IJ' in stage1:
            kind="Junior's Individual"
        elif 'EJ' in stage1:
            kind="Junior's Team"
        elif 'EF' in stage1:
            kind="Men's Team"
        elif 'ES' in stage1:
            kind="Senior's Team"
            
        if 'individual masculin.' in stage0:
            kind="Men's Individual"
        if 'echipe.' in stage0:
            kind="Mixed Team"
        if 'individual juniori' in stage0:
            kind="Junior's Team"
        if 'individual feminin' in stage0:
            kind="Junior's Team"
        if 'individual veterani' in stage0:
            kind="Senior's Team"
        if 'male team' in stage0:
            kind="Men's Team"
        if 'junior 1 individual' in stage0:
            kind="Junior's Individual"
        if 'junior 2 individual' in stage0:
            kind="Junior's Individual"
        
    elif match=='F':
        kind="Women's Individual"
    elif match=='M':
        kind="Men's Individual"
    elif match=='J':
        kind="Junior's Individual"
    elif match=='SF_s':
        kind="Women's Individual"
    elif match=='SM_s':
        kind="Men's Individual"
    elif match=='J_s':
        kind="Junior's Individual"
    
    if kind=='Unknown':
        category='Unknown'
        teams='Unknown'
    else:
        category=kind.split(' ')[0][:-2]
        teams=kind.split(' ')[1]
    if year<2014: 
        category=category.replace('Senior','Men')
    if year in [2018]: 
        category=category.replace('Senior','Men')
    return category,teams,phase

def outcome_cleaner(outcome):
    if outcome=='E': return True
    else: return False
    
def outcome_from_points(aka,shiro):
    if aka==shiro: return 'X',0
    elif aka>shiro: return 'A',str(aka-shiro)
    else: return 'S',str(shiro-aka)
    
    