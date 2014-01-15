print 'STARTING NUKE INIT.PY'

import nuke, os, sys, nukescripts
import jeeves_core, nukeUtils, nukePipe

# print jeeves_core.jobsRoot

global fullsetup

if jeeves_core.getVars.findJob():
    print ('JOB FOUND - FULL SETUP')
    fullsetup = True
else:
    print ('NO JOB FOUND - PARTIAL SETUP')
    fullsetup = False

############################################################################################################
# Callbacks - need to set them up here even if disabling later on                                                                                         
############################################################################################################

nuke.addBeforeRender(nukePipe.nukeCallbacks.createWriteDir)
nuke.addFilenameFilter(nukePipe.nukeCallbacks.filenameFix)
#nuke.addOnScriptLoad
    
if fullsetup:
    nuke.addAutoSaveFilter( nukePipe.nukeCallbacks.onAutoSave )
    nuke.addAutoSaveRestoreFilter( nukePipe.nukeCallbacks.onAutoSaveRestore )
    nuke.addAutoSaveDeleteFilter( nukePipe.nukeCallbacks.onAutoSaveDelete )
    nuke.addKnobChanged(nukePipe.nukeCallbacks.findChangedKnob, nodeClass='Write')
    #nuke.addOnUserCreate( nukePipe.nukeCallbacks.createVersionKnobs, nodeClass='Read' )
    #nuke.addKnobChanged( nukePipe.nukeCallbacks.updateVersionKnob, nodeClass='Read' )

#nuke.addOnScriptSave( nukePipe.nukeCallbacks.checkScriptName )

############################################################################################################
# Set the plugin paths and sys paths                                                                     
############################################################################################################

for root, dirs, files in os.walk(os.getenv('NUKE_PATH')):
    for folder in dirs:
        gizmodir = os.path.join(root, folder).replace('\\', '/')
        nuke.pluginAddPath(gizmodir)
        sys.path.append(gizmodir)


nuke.pluginAddPath(os.path.join(jeeves_core.resourcesRoot, 'vfx', 'jeeves', 'icons'))
############################################################################################################
# Defaults                                                                                      
############################################################################################################

s = nuke.root()
name  = s.name()
nuke.knobDefault('Root.fps', '25')
nuke.knobDefault('Root.format', 'HD')
nuke.knobDefault('Viewer.viewerProcess', 'sRGB')
nuke.knobDefault('Root.name', name)
nuke.knobDefault('Read.cached', '1')
#nuke.knobDefault('Read.postage_stamp', 'False')

print 'FINISHED NUKE INIT.PY'
