import os

def setJob(job):
    os.environ['JOB'] = job
    print 'SET JOB VAR TO : ', os.getenv('JOB')

def setShot(shot):
    os.environ['SHOT'] = shot
    print 'SET SHOT VAR TO : ', os.getenv('SHOT')

def setScript(script):
    os.environ['SCRIPT'] = script
    print 'SET SCRIPT VAR TO : ', os.getenv('SCRIPT')

def setFullpath(fullpath):
    os.environ['FULLPATH'] = fullpath
    print 'SET FULLPATH VAR TO : ', os.getenv('FULLPATH')

def blankVars():
    os.environ['JOB'] = ''
    os.environ['SHOT'] = ''
    os.environ['SCRIPT'] = ''
    os.environ['FULLPATH'] = ''
    
    