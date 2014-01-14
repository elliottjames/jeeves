import nuke, os, errno, re, nukescripts, glob, time, sys, jeeves_core

def reveal():
    path = os.path.join(jeeves_core.jobsRoot, os.getenv('JOB'), 'vfx', 'nuke', os.getenv('SHOT'), os.getenv('SCENEROOT'), os.getenv('TASK'))
    if sys.platform == 'win32':
	os.startfile(path)
    if sys.platform == 'linux2':
	os.system('nautilus "%s"' % path)
    if sys.platform == 'darwin':
	os.system('open "%s"' % path)


############################################################################################################
# Custom python menu items and other misc                                                                                 
############################################################################################################

def freshLables():
    for each in nuke.allNodes():
        if each.Class() == 'Write':
            name = each.name()
            if 'Jeeves_Write' in name:
		each['reload'].execute()

def refreshReads():
    allNodes = nuke.allNodes()
    for readNode in allNodes:
        if readNode.Class() == 'Read':
            readNode.knob('reload').execute()
            nuke.tprint ('%s is refreshed' % readNode.knob('file').value())
        else:
            pass

def refreshWrites():
    print 'refresh writes'
    for each in nuke.allNodes():
        if each.Class() == 'Write':
            name = each.name()
            if 'Output Write' in name:
		each['file'].setValue('[string trimright [string trimright [file tail [value root.name]] .nk] _thread0]')
		print 'refreshed write, woop!'

def printReads():
    for fileNode in nuke.allNodes():
        if fileNode.Class() == 'Read':
            print (fileNode['file'].value())

def findClass():
    nuke.message('this node is a ' + nuke.selectedNode().Class() + ' node, quite simple really ')

def swapoutz():
    for s in nuke.allNodes('Read'):
        filepath = s['file'].value()
        if filepath.startswith('Z:/'):
            keep = filepath.split('Z:/')[1]
            newpath = '//bertie/bertie/' + keep
            s['file'].setValue(newpath)
            s['reload'].execute()
    
############################################################################################################
# 3rd party script - find missing reads / multi node tweaker                                                                                 
############################################################################################################

def missingFrames():
    missingFiles = []
    completeFileName = ""
    
    # first check if a node is selected and if so if it is a read node
    selectedNodes = nuke.selectedNodes()
    
    # either nothing or too much is selected
    if (len(selectedNodes) != 1):
        nuke.message("This only works if you select one Read node!")
        return "Fail"
    
    nodeType = selectedNodes[0].Class()
    
    if (nodeType != "Read"):
        nuke.message("This only works if you select one Read node!")
        return "Fail"
    
    #now we are sure one read node is selected, so go on.
    
    readNode = selectedNodes[0]
    
    fileNameLong = readNode.knob("file").value()
    startFrame = readNode.knob("first").value()
    endFrame = readNode.knob("last").value()
    
    # split the long file name with path to its subsections 
    splitFileNameLong = os.path.split(fileNameLong)
    fileNameShort = splitFileNameLong[1]
    pathName = splitFileNameLong[0]
    splitFileName = fileNameShort.split(".")
    
    if (len(splitFileName) != 3):
        nuke.message("File does not have the format name.number.ext.\nSearch the missing frames yourself :)")
        return "Fail"
    
    fileName = splitFileName[0]
    filePaddingOrg = splitFileName[1]
    filePaddingLength = len((filePaddingOrg) % 0)
    fileExtension = splitFileName[2]
    print filePaddingLength
    
    # now with all that given information search for missing files in the sequence 
    for i in range(startFrame, endFrame+1):
        print 'frame : ', i
        # first build the string of the padded frameNumbers
        frameNumber = str(i) 
    
        while(len(frameNumber) < filePaddingLength):
            frameNumber = "0" + frameNumber
    
            completeFileName = pathName + "/" + fileName + "." + frameNumber + "." + fileExtension

        if not os.path.isfile(completeFileName):
            missingFiles.append(i)
            
    if(len(missingFiles) == 0):
        nuke.message("No file seems to be missing")
        return
    
    print missingFiles
    cleanedUpMissingFiles = cleanUpList(missingFiles)
    print cleanedUpMissingFiles
    
    nuke.message("In the frame range: " + str(startFrame) + "-" + str(endFrame) + "\nThe following files are missing:\n\n" + cleanedUpMissingFiles)
    
    return

## from a sequencial array create a readable list which is returned

def cleanUpList(missingFrames):
    cleanMissingFrames = []
    missingFramesNice = ""
    dirtySize = 0
    minV = 0
    maxV = 0
    
    dirtySize = len(missingFrames)
    
    minV = missingFrames[0]
    maxV = missingFrames[0]
    
    for i in range(dirtySize):
        if (missingFrames[i] == (maxV+1)):
            #as long as the frames are in sequence, update the maxV value
            maxV = missingFrames[i]
        else:
            #if not in sequence, set the values
            cleanMissingFrames.append(minV)
            cleanMissingFrames.append(maxV)
            minV = maxV = missingFrames[i];
    
        if (i == (dirtySize-1)):
            #write the values if the list is at the end
            cleanMissingFrames.append(minV)
            cleanMissingFrames.append(maxV)
    
    for i in range(2,len(cleanMissingFrames),2):
        # create the formated output of the frames in the window for the user to shorten the list
        if(cleanMissingFrames[i] == cleanMissingFrames[i+1]):
            missingFramesNice += (str)(cleanMissingFrames[i]) + ", "
        else:
            missingFramesNice += (str)(cleanMissingFrames[i]) + "-" + (str)(cleanMissingFrames[i+1]) + ", "

    return missingFramesNice

def multiNodeTweaker():

    test = 0
    origFileName = None
    replaceInFileName = None
    booleanCheckBox = None
    chanVal = 'rgb rgba alpha depth'
    cspace = 'default linear sRGB rec709 Cineon Gamma1.8 Gamma2.2 Panalog REDlog ViperLog REDSpace'
    sn = nuke.selectedNodes()

# first checkpoint - is anything selected?
    if (len(sn) == 0):
        nuke.message("Select one or more Read or Write nodes")
        return

# second checkpoint - I will work only on valid node classes
    for i in sn:
        print i.Class() 
        if not i.Class() in ['Read' , 'Write']:
            nuke.message("No Read or Write nodes selected.")
            return

    o = nuke.Panel("Multi Node Tweaker")
    o.addSingleLineInput('Find:', origFileName)
    o.addSingleLineInput('Replace:', replaceInFileName)
    o.addEnumerationPulldown('Color Space',cspace)
    o.addButton("Cancel")
    o.addButton("Ok")

# If selected nodes are of Write class, add parameter to mess with the channels
    for i in sn:
        if i.Class() == 'Write':
            test = 1
    if test == 1:
        o.addEnumerationPulldown('Channels:',chanVal)

    o.show()

# grab new values
    origFileName = o.value("Find:")
    replaceInFileName = o.value("Replace:")
    cspace = o.value("Color Space")
    chanVal = o.value("Channels:")

    for n in sn:
        filename = n['file'].value()
        newFileName = filename.replace(origFileName,replaceInFileName)
        n.knob('file').setValue(newFileName)
        n.knob('colorspace').setValue(cspace)
        if n.Class() == 'Write':
                n.knob('channels').setValue(chanVal)