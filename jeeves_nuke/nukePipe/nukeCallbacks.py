import nuke, os, errno, re, nukescripts, glob, time, sys, subprocess, traceback

#nuke.tprint('nuke callback functions'.upper())


############################################################################################################
# Callback functions                                                                                           
############################################################################################################

def filenameFix(filename):
    if sys.platform == 'darwin':
	filename = filename.replace('//bertie/bertie', '/Volumes/Bertie')
	filename = filename.replace('//resources/resources', '/Volumes/Resources')
	filename = filename.replace('/mnt/bertie', '/Volumes/Bertie')
	filename = filename.replace('/mnt/resources', '/Volumes/Resources')
    elif sys.platform == 'win32':
	filename = filename.replace('/Volumes/Bertie', '//bertie/bertie')
	filename = filename.replace('/Volumes/Resources', '//resources/resources')
	filename = filename.replace('/mnt/bertie', '//bertie/bertie')
	filename = filename.replace('/mnt/resources', '//resources/resources')
    elif sys.platform == 'linux2':
	filename = filename.replace('/Volumes/Bertie', '/mnt/bertie')
	filename = filename.replace('/Volumes/Resources', '/mnt/resources')
	filename = filename.replace('//bertie/bertie', '/mnt/bertie')
	filename = filename.replace('//resources/resources', '/mnt/resources')

    return filename

def findChangedKnob():
    knob = nuke.thisKnob()
    node = nuke.thisNode()
    if knob.name() == 'renderType':
	output_type = knob.value()
	if output_type == 'matte':
	    nuke.tprint ('matte selected')
	    output_path = '[value dirName]/[value renderType]/[value fileName]/[value fileName].%04d.tiff'
	    node['file'].setValue(output_path)
	    node['file_type'].setValue('tiff')
	    node['datatype'].setValue('8')
	    node['colorspace'].setValue('srgb')
	    node['channels'].setValue('alpha')
	elif output_type in ['slapcomp', 'prerender', 'cleanup']:
	    output_path = "[value dirName]/[value renderType]/[value fileName]/[value fileName].%04d.dpx"
	    node['file'].setValue(output_path)
	    node['file_type'].setValue('dpx')
	    node['colorspace'].setValue('linear')
	    node['datatype'].setValue('10')
	    node['channels'].setValue('rgb')

def onAutoSave(filename):

  ## ignore untiled autosave
  if nuke.root().name() == 'Root':
    return filename

  fileNo = 0
  files = getAutoSaveFiles(filename)

  if len(files) > 0 :
    lastFile = files[-1]
    # get the last file number

    if len(lastFile) > 0:
      try:
        fileNo = int(lastFile[-1:])
      except:
        pass

      fileNo = fileNo + 1

  if ( fileNo > 9 ):
    fileNo = 0

  if ( fileNo != 0 ):
    filename = filename + str(fileNo)

  return filename

def onAutoSaveRestore(filename):

  files = getAutoSaveFiles(filename)

  if len(files) > 0:
    filename = files[-1]

  return filename

def onAutoSaveDelete(filename):

  ## only delete untiled autosave
  if nuke.root().name() == 'Root':
    return filename

  # return None here to not delete auto save file
  return None

  
def getAutoSaveFiles(filename):
  date_file_list = []
  files = glob.glob(filename + '[1-9]')
  files.extend( glob.glob(filename) )

  for file in files:
      # retrieves the stats for the current file as a tuple
      # (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime)
      # the tuple element mtime at index 8 is the last-modified-date
      stats = os.stat(file)
      # create tuple (year yyyy, month(1-12), day(1-31), hour(0-23), minute(0-59), second(0-59),
      # weekday(0-6, 0 is monday), Julian day(1-366), daylight flag(-1,0 or 1)) from seconds since epoch
      # note:  this tuple can be sorted properly by date and time
      lastmod_date = time.localtime(stats[8])
      #print image_file, lastmod_date   # test
      # create list of tuples ready for sorting by date
      date_file_tuple = lastmod_date, file
      date_file_list.append(date_file_tuple)
   
  date_file_list.sort()
  return [ filename for _, filename in date_file_list ]

def createWriteDir():
    print 'WRITE CALLBACK FUNCTION'
    file = nuke.filename(nuke.thisNode())
    dir = os.path.dirname( file )
    osdir = nuke.callbacks.filenameFilter( dir )
    # cope with the directory existing already by ignoring that exception
    try:
        os.makedirs( osdir )
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise

#currently not being used
def checkScriptName():
    if not re.search( r'[vV]\d+', nuke.root().name() ):
        raise NameError, 'Please include a version number and save script again.'



