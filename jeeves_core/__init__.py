print 'IMPORTING JEEVES CORE __init__.py'

import sys, os
import getVars
import setVars
import searchJob
import make

if sys.platform == 'darwin':
    jobsRoot = '/Volumes/Bertie/Jobs'
    resourcesRoot = '/Volumes/Resources'
    user = os.getenv('USER')
    
elif sys.platform == 'win32':
    jobsRoot = r'\\bertie\bertie\Jobs'
    
elif sys.platform == 'linux2':
    jobsRoot = '/mnt/bertie/Jobs'
