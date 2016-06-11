import os,parser
#import slicer

def humanSort(l):
  """ Sort the given list in the way that humans expect.
      Conributed by Yanling Liu
  """
  convert = lambda text: int(text) if text.isdigit() else text
  alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
  l.sort( key=alphanum_key )

def getCaseDir(case):

    if case < 10:
        caseDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Cases003-298_data/Case00'+str(case)+'/IntraopImages/'
    elif 9 < case < 100:
        caseDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Cases003-298_data/Case0'+str(case)+'/IntraopImages/'
    elif 99 < case:
        caseDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Cases003-298_data/Case'+str(case)+'/IntraopImages/'

    return caseDir

def getListOfCaseIDs(numberOfCases):

  listOfCaseIDs = []

  for case in range(numberOfCases):
    if case < 10:
        caseDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Cases003-298_data/Case00'+str(case)+'/IntraopImages/'
        #print caseDir
        if os.path.isdir(str(caseDir)):
             listOfCaseIDs.append(case)
    elif 9 < case < 100:
        caseDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Cases003-298_data/Case0'+str(case)+'/IntraopImages/'
        #print caseDir
        if os.path.isdir(str(caseDir)):
             listOfCaseIDs.append(case)
    elif 99 < case:
        caseDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Cases003-298_data/Case'+str(case)+'/IntraopImages/'
        #print caseDir
        if os.path.isdir(str(caseDir)):
             listOfCaseIDs.append(case)

  return listOfCaseIDs

#listOfCaseIDs = getListOfCaseIDs(300)
#ignoreCaseIDs = [4,5,7,8,52,60,69,72,101,142]
#alreadyGotThose = range(0,197)
#listOfCaseIDs=list(set(listOfCaseIDs) - set(ignoreCaseIDs))
#listOfCaseIDs=list(set(listOfCaseIDs) - set(alreadyGotThose))
#listOfCaseIDs = sorted(listOfCaseIDs)

numberOfCases = 300
listOfCaseIDs = []
ignoreCaseIDs = [4,5,7,8,52,60,69,72,101,142]

pelvisRegProbs = [18,23,28,29,32,33,40,42,43,46,47,66,67,76,80,81,83,91,97,99,107,108,112,114,115,
                  118,119,127,146,150,151,153,164,168,185,186,189,202,214,219,228,245,246,253,256,
                  262,268,272,273,290,295]

ignoreCaseIDsFromLackOfData = [10,49,80,81,117,121,123,134,135,137,138,141,146,150,177,212,213,218,227,241,254,255,266,289,290]


# get list of cases
listOfCaseIDs = getListOfCaseIDs(numberOfCases)

# ignore cases
listOfCaseIDs=list(set(listOfCaseIDs) - set(ignoreCaseIDs))
#listOfCaseIDs=list(set(listOfCaseIDs) - set(pelvisRegProbs))
listOfCaseIDs=list(set(listOfCaseIDs) - set(ignoreCaseIDsFromLackOfData))

print listOfCaseIDs
print listOfCaseIDs

#listOfCaseIDs = [268,270,271]

def getNeedleImageIDs(IntraDir):
    needleImageIds = []
    # returns list of Image ID's for case with dir intradirw
    if os.path.isdir(IntraDir):
      listDir = os.listdir(IntraDir)
      for i in range(len(listDir)):
          if 'Needle' in listDir[i]:
              needleImageIds.append(int(string.split(listDir[i],'-')[0]))
      needleImageIds.sort()
    else:
      print 'there is no path like: '+str(IntraDir)
    return needleImageIds


# this script is launched inside slicer.
# open python terminal, type:
# execfile ('/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/scripts/makeSnapshots.py')
# to launch it. Also, make sure that VisAIRe is installed as a module and open!


for case in listOfCaseIDs:

    print 'NEW CASE ******************************************************'
    print 'CASE : '+str(case)
    # initialize widget
    #parent = slicer
    #slicer.modules.VisAIReInstance.__init__(parent)

    # get configdir
    configdir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/configs/Case'+str(case)+'_VisAIRe.ini'

    # open VisAIRe with config dir
    slicer.modules.VisAIReWidget.initFromFile('/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/configs/Case'+str(case)+'_VisAIRe.ini')

    # hit "make snapshots"
    slicer.modules.VisAIReWidget.onMakeSnapshots()


import sys, glob, string, os, re

# read all snapshot files
# for each case key, sort the files
# take pairs that have the same needle id, coombine into gif

inputDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/snapshots/'
outputDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/GIFs/'

inputFiles = glob.glob(inputDir+'/*png')

for case in listOfCaseIDs:

  print '***********************'
  print 'new case !! Case : '+str(case)
  imagesForCase = [x for x in inputFiles if os.path.split(x)[1].startswith('Case'+str(case)+'_')]
  print imagesForCase
  humanSort(imagesForCase)
  # list should look like fixed_for_needle_i, registered_for_needle_i, ...,
  # moving

  IntraDir = getCaseDir(case)
  print 'IntraDir : '+str(IntraDir)

  needleImageIds = []
  needleImageIds=getNeedleImageIDs(IntraDir)

  print '*****************************************************'
  print needleImageIds


  for n in range(len(needleImageIds)):

    print 'images for case ::::'
    print imagesForCase
    print 'n : '
    print n
    print 'len(needleImageIDs'
    print len(needleImageIds)


    fixedFileName = os.path.split(imagesForCase[n*2])[1]
    registeredFileName = os.path.split(imagesForCase[n*2+1])[1]
    movingFileName = os.path.split(imagesForCase[-1])[1]

    print "fixedFileName     : "+fixedFileName
    print "registeredFileName     : "+registeredFileName
    print "movingFileName        : "+movingFileName

    needleId = fixedFileName.split('_')[1]

    print ('needleID: '+str(needleId))

    fixed = imagesForCase[n*2]
    registered = imagesForCase[n*2+1]
    moving = imagesForCase[-1]

    fixedGif = '/tmp/'+fixedFileName.split('.')[0]+'.gif'
    movingGif = '/tmp/'+movingFileName.split('.')[0]+'.gif'
    registeredGif = '/tmp/'+registeredFileName.split('.')[0]+'.gif'

    os.system('sips -s format gif '+fixed+' --out /tmp')
    os.system('sips -s format gif '+moving+' --out /tmp')
    os.system('sips -s format gif '+registered+' --out /tmp')

    print 'current case '+str(case)
    print 'current needleImageIds[n] '+str(needleImageIds[n])

    beforeRegistration = outputDir+'/Case'+str(case)+'_'+str(needleImageIds[n])+'_before.gif'
    afterRegistration = outputDir+'/Case'+str(case)+'_'+str(needleImageIds[n])+'_after.gif'

    os.system('gifsicle --delay=100 --loop '+fixedGif+' '+movingGif+' > '+beforeRegistration)
    os.system('gifsicle --delay=100 --loop '+fixedGif+' '+registeredGif+' > '+afterRegistration)


  print 'CASE '+str(case)+' THROUGH!'
