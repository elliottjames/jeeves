import os, sys, jeeves_core

def findJob():
    if os.getenv('JOB'):
        return True
    else:
        return False

def get_initial():
    initial = {'elliott' : 'es',
               'unitadmin' : 'un'
               }
    
    if jeeves_core.user in initial:
        return initial[jeeves_core.user]