import nuke, os, errno, re, nukescripts, glob, time, sys

def test():
    nuke.tprint('TEST TEST A TEST')
    
def threedRead():
    nuke.tprint('3d read')

def nukeRead():
    print('nuke read')
    
def updateRead():
    nuke.tprint('update read')
#    
#    
#############################################################################################################
## Read functions                                                                                    
#############################################################################################################
#def nukeRead():
#    readType = 'nuke'
#    jeevesRead('nuke')
#
#def threedRead():
#    readType = '3d'
#    jeevesRead('3d')
#
#def findTypes(path):
#    global types
#    types = []
#    typesToIgnore = ('tmp','.DS_Store')
#    for each in os.listdir(path):
#	if not each in typesToIgnore:
#	    types.append(each)
#    return types
#
#def jeevesRead(readType):
#    if readType == '3d':
#	global path
#	path = os.path.join( jeevesStatic.jobsRoot, os.getenv('JOB'), 'vfx', '3d', os.getenv('SHOT'), 'Render_Pictures' )
#    if readType == 'nuke':
#	global path
#	path = os.path.join( jeevesStatic.jobsRoot, os.getenv('JOB'), 'vfx', 'nuke', os.getenv('SHOT'), 'plates', 'output' )
#    
#    # lets generate the global types list - for nuke this will be the types of renders ('matte', 'slapcomp') etc but
#    # for 3d, it'll be the render versions (sh_001_somerenders_es_v01, sh_001_somerenders_es_v02)
#    
#    findTypes(path)
#    
#    global jeevesReadNode
#    jeevesReadNode = nuke.createNode( 'Read' ) 
#    
#    if readType == 'nuke':
#	count = 1
#	while nuke.exists('Nuke_Read ' + str(count)):
#	    count += 1
#	jeevesReadNode.knob('name').setValue('Nuke_Read ' + str(count))
#	
#	tabKnob = nuke.Tab_Knob( 'Jeeves Nuke Read', 'Jeeves Nuke Read' )
#	jeevesReadNode.addKnob(tabKnob)
#	
#	typeKnob = nuke.Enumeration_Knob( 'versionType', 'type', types )
#	updateKnob = nuke.PyScript_Knob( 'update', 'update' )
#	versionKnob = nuke.Enumeration_Knob( '_version', 'version', [] )
#	loadKnob = nuke.PyScript_Knob( 'load', 'load' )
#	
#	jeevesReadNode.addKnob(typeKnob)
#	jeevesReadNode.addKnob(updateKnob)
#	jeevesReadNode.addKnob(versionKnob)
#	jeevesReadNode.addKnob(loadKnob)
#	
#	# bind the buttons to functions
#	updateKnob.setValue( "jeevesNukeModules.updateVersionKnob()" )
#	loadKnob.setValue( 'jeevesNukeModules.loadScript()' )
#	
#	# now we need to populate the version knob
#	updateVersionKnob()
#    
#    if readType == '3d':
#	count = 1
#	while nuke.exists('3d_Read ' + str(count)):
#	    count += 1
#	jeevesReadNode.knob('name').setValue('3d_Read ' + str(count))
#	
#	tabKnob = nuke.Tab_Knob( 'Jeeves 3d Read', 'Jeeves 3d Read' )
#	jeevesReadNode.addKnob(tabKnob)
#	
#	versionKnob = nuke.Enumeration_Knob( '_version', 'version', types )
#	findLayers = nuke.PyScript_Knob( 'findLayers', 'find layers' )
#	layerKnob = nuke.Enumeration_Knob( '_layer', 'layer', [])
#	loadKnob = nuke.PyScript_Knob( 'load', 'load' )
#	
#	jeevesReadNode.addKnob(versionKnob)
#	jeevesReadNode.addKnob(findLayers)
#	jeevesReadNode.addKnob(layerKnob)
#	jeevesReadNode.addKnob(loadKnob)
#	
#	# bind the buttons to functions
#	loadKnob.setValue( 'jeevesNukeModules.loadScript()' )
#
#def loadScript():
#    n = nuke.thisNode()
#    path, range = n['_version'].value().split()
#    first, last = range.split('-')
#    n['file'].setValue( path )
#    n['first'].setValue( int(first) )
#    n['last'].setValue( int(last) )
#
#def updateVersionKnob():
#    print 'updateVersionKnob'
#    node = nuke.thisNode()
#    knob = nuke.thisKnob()
#    
#    versionDict = getVersions()
#    
#    jeevesReadNode['_version'].setValues( sorted(versionDict[ jeevesReadNode['versionType'].value() ], reverse=True) )
#    jeevesReadNode['_version'].setValue(0)
#    
#    # RUN ONLY IF THE TYPE KNOB CHANGES OR IF THE NODE PANEL IS OPENED
#    if not knob or knob.name() in [ 'versionType', 'showPanel' ]:
#        # GET THE VERSION DICTIONARY
#        versionDict = getVersions()
#        # POPULATE THE VERSION KNOB WITH THE VERSIONS REQUESTED THROUGH THE TYPE KNOB
#        jeevesReadNode['_version'].setValues( sorted(versionDict[ jeevesReadNode['versionType'].value() ], reverse=True) )
#        # SET THE A VALUE TO THE FIRST ITEM IN THE LIST
#        jeevesReadNode['_version'].setValue(0)
#
#def getVersions():
#    print 'getVersions'    
#    # INITIALISE THE DICTIONARY WE WILL RETURN AT THE END OF THE FUNCTION
#    versionDict = {}
#    # GET THE DIRECTORY BASED ON THE CURRENT SHOT ENVIRONMENT
#    shotDir = os.path.join( jeevesStatic.jobsRoot, os.getenv('JOB'), 'vfx', 'nuke', os.getenv('SHOT'), 'plates', 'output' )
#    # LOOP THROUGH THE FOLDERS INSIDE THE SHOT DIRECTORY AND COLLECT THE IMAGE SEQUENCES THEY CONTAIN
#    for t in types:
#        versionDict[t] = [] # THIS WILL HOLD THE FOUND SEQUENCES
#        typeDir = os.path.join( shotDir, t ) # GET THE CURRENT DIRECTORY PATH
#        for d in os.listdir( typeDir ): # LOOP THROUGH IT'S CONTENTS
#            path = os.path.join( typeDir, d)
#            if os.path.isdir( path ): # LOOP THROUGH SUB DIRECTORIES
#                versionDict[t].append( getFileSeq( path ) ) # RUN THE getFileSeq() FUNCTION AND APPEND IT'S OUTPUT TO THE LIST
#    #print versionDict
#    return versionDict
#
#def getFileSeq( dirPath ):
#    print 'getFileSeq'
#    '''Return file sequence with same name as the parent directory. Very loose example!!'''
#    dirName = os.path.basename( dirPath )
#    # COLLECT ALL FILES IN THE DIRECTORY THAT HVE THE SAME NAME AS THE DIRECTORY
#    files = glob.glob( os.path.join( dirPath, '%s.*.*' % dirName ) )
#    files.sort()
##    for each in files:
##	print each, files.index(each)
#    
#    # GRAB THE RIGHT MOST DIGIT IN THE FIRST FRAME'S FILE NAME
#    firstString = re.findall( r'\d+', files[0] )[-1]
#    # GET THE PADDING FROM THE AMOUNT OF DIGITS
#    padding = len( firstString )
#    # CREATE PADDING STRING FRO SEQUENCE NOTATION
#    paddingString = '%02s' % padding
#    # CONVERT TO INTEGER
#    first = int( firstString )
#    # GET LAST FRAME
#    last = int( re.findall( r'\d+', files[-1] )[-1] )
#    # GET EXTENSION
#    ext = os.path.splitext( files[0] )[-1]
#    # BUILD SEQUENCE NOTATION
#    fileName = '%s.%%%sd%s %s-%s' % ( dirName, str(padding).zfill(2), ext, first, last )
#    # RETURN FULL PATH AS SEQUENCE NOTATION
#    #print os.path.join( dirPath, fileName )	
#    return os.path.join( dirPath, fileName )	
#
#def updateRead():
#    pass