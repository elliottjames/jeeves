import jeeves_core, os

# will spin this off to xmlrpc server

def nuke_user(user):
    scriptsdir = os.path.join(jeeves_core.jobsRoot, job, 'vfx', 'nuke', os.getenv('SHOT'), 'scripts', user)
    os.mkdir(scriptsdir)

def add_shot(job, shot):
    nuke_shot = nukeShot(job, shot).replace('\\','/')
    soft_shot = softShot(job, shot).replace('\\','/')
    track_shot = trackShot(job, shot).replace('\\','/')

    #NUKE
    nuke_base = ['mkdir', '%s' % nuke_shot]
    nuke_plates = ['mkdir', '%s/plates' % nuke_shot]
    nuke_scripts = ['mkdir', '%s/scripts' % nuke_shot]
    nuke_plates_output = ['mkdir', '%s/plates/output' % nuke_shot]
    nuke_plates_input = ['mkdir', '%s/plates/input' % nuke_shot]
    
    #SOFT
    soft_base = ['cp', '-r', '%s' % '/mnt/resources/vfx/jeeves/vfx/softimage/softimage_project_default', '%s' %  soft_shot]
    soft_pictures = ['ln', '-s','%s' % os.path.join('/mnt/bertie/Jobs', job, 'vfx', 'assets', 'sourceimages').replace('\\','/'), '%s/Pictures' % soft_shot]
    soft_models = ['ln', '-s', '%s' % os.path.join('/mnt/bertie/Jobs', job, 'vfx', 'assets', 'models').replace('\\','/'), '%s/Models' % soft_shot]
 
    #TRACK
    track_base = ['mkdir', '%s' % track_shot]
    track_project = ['mkdir', '%s/project' % track_shot]
    track_data = ['mkdir', '%s/solve' % track_shot]

    #CHMOD
    chmod_dir = ['chmod', '-R', '777', '%s' % nuke_shot, '%s' % track_shot, '%s' % soft_shot, '%s'  % os.path.join('/mnt/bertie/Jobs', job, 'vfx', 'assets').replace('\\','/')]
    chgrp_dir = ['chgrp', '-R', 'games', '%s' % nuke_shot, '%s' % track_shot, '%s' % soft_shot, '%s' % os.path.join('/mnt/bertie/Jobs', job, 'vfx', 'assets').replace('\\','/')]
    chown_dir = ['chown', '-R', 'unitadmin', '%s' % nuke_shot, '%s' % track_shot, '%s' % soft_shot, '%s' % os.path.join('/mnt/bertie/Jobs', job, 'vfx', 'assets').replace('\\','/')]
            
    #COMMAND LIST
    cmd_list = [track_base, track_project, track_data, nuke_base, nuke_plates, nuke_plates_output, nuke_plates_input, nuke_scripts, soft_base, soft_pictures, soft_models, chmod_dir, chgrp_dir, chown_dir]
    
    for i in cmd_list:
        print i
    #
    #if not server.make_shot(cmd_list):
    #    return False
    #else:
    #    return True

def nukeShot(job, shot):
    nuke_shot = os.path.join('/mnt/bertie/Jobs', job, 'vfx', 'nuke', shot)
    return nuke_shot

def softShot(job, shot):
    soft_shot = os.path.join('/mnt/bertie/Jobs', job, 'vfx', '3d', shot)
    return soft_shot

def trackShot(job, shot):
    renders_shot = os.path.join('/mnt/bertie/Jobs', job, 'vfx', 'tracking', shot)
    return renders_shot 