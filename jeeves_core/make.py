import jeeves_core, os

# will spin this off to xmlrpc server

def nuke_user(user):
    scriptsdir = os.path.join(jeeves_core.jobsRoot, os.getenv('JOB'), 'vfx', 'nuke', os.getenv('SHOT'), 'scripts', user)
    os.mkdir(scriptsdir)

def add_shot(job, shot):
    print 'ADDING SHOT'