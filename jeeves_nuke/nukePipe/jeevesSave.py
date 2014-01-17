import nuke, os, errno, re, nukescripts, glob, time, sys, jeeves_core

def saveVersion():
    scriptsdir = os.path.join(jeeves_core.jobsRoot, os.getenv('JOB'), 'vfx', 'nuke', os.getenv('SHOT'), 'scripts',  jeeves_core.user)
    
    if os.path.isdir(scriptsdir):
	print 'dir exists'
    else:
	print 'need to create dir'
	jeeves_core.make.nuke_user(jeeves_core.user)
	print 'done'
    
    # strip white space from user input description
    description = nuke.getInput( 'script description', 'slapcomp' ).replace( ' ', '_' )

    job = os.environ['JOB'].rsplit('_', 1)[-1]
    
    fileSaved = False
    version = int(1)
    
    while not fileSaved:
	scriptName = '%s_%s_%s_v%02d.nk' % ( os.getenv('SHOT'), description, jeeves_core.getVars.get_initial(), version )
	fullPath = os.path.join( scriptsdir, scriptName )
        # if file exists, we version up
        if os.path.isfile(fullPath):
            version += 1
            continue
        # save the script
        nuke.scriptSaveAs( fullPath )
        fileSaved = True
    freshLables()

def freshLables():
    for each in nuke.allNodes():
        if each.Class() == 'Write':
            name = each.name()
            if 'Jeeves_Write' in name:
		each['reload'].execute()