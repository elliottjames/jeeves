import nuke, os, sys, re, nukescripts
import jeeves_gui

nuke.tprint('STARTING NUKE MENU.PY''\n')

############################################################################################################
# Jeeves menu dictionary                                                                                          
############################################################################################################

nukeDict = {}
suffix = ('gizmo', 'py', 'tcl', 'dylib')

for filepath in nuke.pluginPath():
    menuName=os.path.split(filepath)[1]
    if menuName.startswith('menu.'):
        if not menuName == 'menu.ICONS':
            if not len(os.listdir(filepath)) == 0:
                menuName = menuName.split('menu.')[-1]
                nukeDict[menuName] = []
                for scripts in os.listdir(filepath):
                    if not scripts.startswith('.'):
                        if scripts.endswith(suffix):
                            nukeDict[menuName].append((os.path.splitext(scripts)[0], scripts))
            
############################################################################################################
# Add Menus                                                                                             
############################################################################################################

nukeMenu = nuke.menu('Nuke')
jeevesMenu = nukeMenu.addMenu('JEEVES')

jeevesMenu.addCommand('Connect to Jeeves', 'reload(jeeves_gui.jeevesNukeGui);jeeves_gui.jeevesNukeGui.run()', icon='unit.png' )
jeevesMenu.addSeparator()
jeevesMenu.addCommand("Submit to Farm", 'reload(nukeUtils.submitDeadline);nukeUtils.submitDeadline.main()', "", icon='deadline.png') 
jeevesMenu.addSeparator()
jeevesMenu.addCommand('Save', 'reload(nukePipe.jeevesSave);nukePipe.jeevesSave.saveVersion()', icon='Yellow.png' )
jeevesMenu.addCommand('Read', 'reload(nukePipe.jeevesRead);nukePipe.jeevesRead.nukeRead()', icon='Purple.png')
jeevesMenu.addCommand( 'Write', 'reload(nukePipe.jeevesOutput);nukePipe.jeevesWrite.outputWrite()', icon='Blue.png')
jeevesMenu.addSeparator()

pluginsMenu = jeevesMenu.addMenu('GIZMOS', icon='unit.png')

pyMenu = jeevesMenu.addMenu('SCRIPTS', icon='unit.png')
pyMenu.addCommand('Create Cam from EXR', 'reload(nukeUtils.createExrCamVray.createExrCamVray())')
pyMenu.addSeparator()
pyMenu.addCommand('Reveal Filesystem', 'reload(nukeUtils.utils);nukeUtils.utils.reveal()')
pyMenu.addCommand('Check Licenses', 'reload(nukeUtils.webBrowser);nukeUtils.webBrowser.run()')
pyMenu.addCommand('Reload Reads', 'reload(nukeUtils.utils);nukeUtils.utils.refreshReads()')
pyMenu.addCommand('Swapout Z', 'reload(nukeUtils.utils);nukeUtils.utils.swapoutz()')
pyMenu.addCommand('Find Missing Reads', 'reload(nukeUtils.utils):nukeUtils.utils.missingFrames()')

#Add menus and scripts from nukeDict

for every in nukeDict:
    subMenus = pluginsMenu.addMenu(every)
    for each in nukeDict[every]:
        cmd = each[0]
        subMenus.addCommand(cmd, 'nuke.createNode' + '("' + cmd + '")')

############################################################################################################
# Jeeves dependant things                                                                               
############################################################################################################

if fullsetup:
    m = nuke.menu( 'Nuke' ).findItem('JEEVES/Connect to Jeeves')
    m.setEnabled( False )
    nuke.addFavoriteDir('job_dir', os.path.join(jeeves_core.jobsRoot, os.getenv('JOB')))
    nuke.addFavoriteDir('script_dir', os.path.join(jeeves_core.jobsRoot, os.getenv('JOB'), 'vfx', 'nuke', os.getenv('SHOT'), 'scripts', jeevesStatic.user))
    nuke.addFavoriteDir('plates_dir', os.path.join(jeeves_core.jobsRoot, os.getenv('JOB'), 'vfx', 'nuke', os.getenv('SHOT'), 'plates'))
    nuke.addFavoriteDir('assets', os.path.join(jeeves_core.jobsRoot, os.getenv('JOB'), 'vfx', 'assets'))
    nuke.addFavoriteDir('3d_renders', os.path.join(jeeves_core.jobsRoot, os.getenv('JOB'), 'vfx', '3d', os.getenv('SHOT'), 'Render_Pictures'))
    nuke.addFavoriteDir('grade_dir', os.path.join(jeeves_core.jobsRoot, os.getenv('JOB'), 'grade'))
    nuke.addFavoriteDir('media_dir', os.path.join(jeeves_core.jobsRoot, os.getenv('JOB'), 'media_imports'))
else:
    turnoff = ["JEEVES/Save","JEEVES/Write", "JEEVES/Read"]
    for each in turnoff:
        m = nuke.menu( 'Nuke' ).findItem(each)
        m.setEnabled( False )

nuke.tprint ('\n''FINSHED NUKE MENU.PY''\n')
