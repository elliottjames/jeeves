import nuke, os
from PySide.QtGui import *
from PySide.QtCore import *
from nukescripts import panels
import jeeves_core, nukePipe


#jeeves gui connect functions

def addshot(job, shot):
    print 'ADD SHOT - uitls'
    #given a job and a shot, check to see if one already exists, strip white space etc etc
    jeeves_core.make.add_shot(job, shot)

def enablemenus():
    turnon = ["JEEVES/Save","JEEVES/Write", "JEEVES/Read"]
    for each in turnon:
        m = nuke.menu( 'Nuke' ).findItem(each)
        m.setEnabled( True )
    
    m = nuke.menu( 'Nuke' ).findItem("JEEVES/Connect to Jeeves")
    #m.setEnabled( False )
    
    nuke.addAutoSaveFilter( nukePipe.nukeCallbacks.onAutoSave )
    nuke.addAutoSaveRestoreFilter( nukePipe.nukeCallbacks.onAutoSaveRestore )
    nuke.addAutoSaveDeleteFilter( nukePipe.nukeCallbacks.onAutoSaveDelete )
    nuke.addKnobChanged(nukePipe.nukeCallbacks.findChangedKnob, nodeClass='Write')
    
    nuke.addFavoriteDir('job_dir', os.path.join(jeeves_core.jobsRoot, os.getenv('JOB')))
    nuke.addFavoriteDir('script_dir', os.path.join(jeeves_core.jobsRoot, os.getenv('JOB'), 'vfx', 'nuke', os.getenv('SHOT'), 'scripts', jeeves_core.user))
    nuke.addFavoriteDir('plates_dir', os.path.join(jeeves_core.jobsRoot, os.getenv('JOB'), 'vfx', 'nuke', os.getenv('SHOT'), 'plates'))
    nuke.addFavoriteDir('assets', os.path.join(jeeves_core.jobsRoot, os.getenv('JOB'), 'vfx', 'assets'))
    nuke.addFavoriteDir('3d_renders', os.path.join(jeeves_core.jobsRoot, os.getenv('JOB'), 'vfx', '3d', os.getenv('SHOT'), 'Render_Pictures'))
    nuke.addFavoriteDir('grade_dir', os.path.join(jeeves_core.jobsRoot, os.getenv('JOB'), 'grade'))
    nuke.addFavoriteDir('media_dir', os.path.join(jeeves_core.jobsRoot, os.getenv('JOB'), 'media_imports'))
    

def changeShot(self, shot):
    print 'CHANGING SHOT'
    
    #clearout
    self.scriptscombo.clear()
    self.allscriptscombo.clear()
    self.shot = None
    self.user = None
    self.script = None
    
    self.job = self.jobsearch.displayText()
    self.user = jeeves_core.user
    self.shot = self.shotcombo.currentText()
    
    self.scriptlist = jeeves_core.searchJob.searchMyNukeScripts(self.job, self.shot, self.user)
    
    list(map(self.scriptscombo.addItem, self.scriptlist))
    
    self.allscriptlist = jeeves_core.searchJob.searchAllNukeScripts(self.job, self.shot)
    list(map(self.allscriptscombo.addItem, self.allscriptlist))

def findjob(self):
    print 'FINDING JOB'
    
    #clearout
    self.shotcombo.clear()
    self.scriptscombo.clear()
    self.allscriptscombo.clear()
    self.job = None
    self.shot = None
    self.user = None
    self.script = None
    
    #job
    searchtext = self.jobsearch.displayText()
    self.job = jeeves_core.searchJob.searchJob(searchtext)
    self.jobsearch.setText(self.job)
    
    #shots
    self.shotlist = jeeves_core.searchJob.searchShot(self.job)
    list(map(self.shotcombo.addItem, self.shotlist))
    
    #my scritps
    self.shot = self.shotcombo.currentText()
    self.user = jeeves_core.user
    self.scriptlist = jeeves_core.searchJob.searchMyNukeScripts(self.job, self.shot, self.user)
    list(map(self.scriptscombo.addItem, self.scriptlist))
    
    #all scripts
    self.allscriptlist = jeeves_core.searchJob.searchAllNukeScripts(self.job, self.shot)
    list(map(self.allscriptscombo.addItem, self.allscriptlist))