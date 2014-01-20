import jeeves_core, os, glob

def searchJob(searchtext):
    # returns list
    searchtext = searchtext.lower()
    joblist = []
    
    for each in os.listdir(jeeves_core.jobsRoot):
        if searchtext in each.lower():
            if each[0] not in '._':
                joblist.append(each)
    
    if joblist == []:
        return None
    
    else:
        if len(joblist):
            # we'll take the fist one we get
            job = joblist[0]

        # check for new job struct
        if not os.path.isdir(os.path.join(jeeves_core.jobsRoot, job, 'vfx', '3d')):
            print 'old job struct'
        else:
            return job

def searchShot(job):
    # returns list
    #were just picking 3d cos its easy
    mayaroot = os.path.join(jeeves_core.jobsRoot, job, 'vfx', '3d')
    shotlist = []
    
    for each in os.listdir(mayaroot):
        if each.startswith('sh_'):
            shotlist.append(each)
    
    if shotlist:
        return sorted(shotlist)

def searchMyNukeScripts(job, shot, user):
    # returns list
    suffix = ('.nk')
    scriptpath = os.path.join(jeeves_core.jobsRoot, job, 'vfx', 'nuke', shot, 'scripts', user )
    
    if not os.path.isdir(scriptpath):
        return ['NEW.NK']
    
    scriptlist = [script for script in os.listdir(scriptpath)
         if script.endswith(suffix)]
    
    if scriptlist:
        scriptlist.sort(key=lambda s: os.path.getmtime(os.path.join(scriptpath, s)), reverse=True)
        scriptlist.append('NEW.NK')
        return scriptlist

def searchAllNukeScripts(job, shot):
    # returns list
    scriptpath = os.path.join(jeeves_core.jobsRoot, job, 'vfx', 'nuke', shot, 'scripts')
    scriptlist = []

    for users in os.listdir(scriptpath):
        if os.path.isdir(os.path.join(scriptpath, users)):
            for scripts in os.listdir(os.path.join(scriptpath, users)):
                if scripts.endswith('.nk'):
                    nkfile = os.path.join(users, scripts)
                    scriptlist.append(nkfile)
    
    scriptlist.sort(key=lambda nkfile: os.path.getmtime(os.path.join(scriptpath, nkfile)), reverse=True)
    
    if scriptlist:
        return scriptlist

def searchNukeFullpath(job, shot, user, script):
    #returns string
    fullpath = os.path.join(jeeves_core.jobsRoot, job, 'vfx', 'nuke', shot, 'scripts', user, script )
    return fullpath

def searchForShot(job, shot):
    shotpath = os.path.join(jeeves_core.jobsRoot, job, 'vfx', 'nuke', shot)
    if os.path.isdir(shotpath):
        return False
    else:
        return True
        