import os,string

# this script checks, if there are missing segmentations and if the case is useful regarding its length
def getTransformDir(case):

    if case < 10:
        transformDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Transforms/Case00'+str(case)+'/IntraopImages/'
    elif 9 < case < 100:
        transformDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Transforms/Case0'+str(case)+'/IntraopImages/'
    elif 99 < case:
        transformDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Transforms/Case'+str(case)+'/IntraopImages/'

    return transformDir

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

def getNeedleImageIDs(IntraDir):
    needleImageIds = []
    # returns list of Image ID's for case with dir intradir
    if os.path.isdir(IntraDir):
      listDir = os.listdir(IntraDir)
      for i in range(len(listDir)):
          if 'Needle' in listDir[i]:
              needleImageIds.append(int(string.split(listDir[i],'-')[0]))
      needleImageIds.sort()
    else:
      print 'there is no path like: '+str(IntraDir)
    return needleImageIds


print 'list of cases with no segmentation: '
print '____________________________________'
count = 0

listOfCaseIDs = getListOfCaseIDs(300)
ignoreCaseIDs = [4,5,7,8,52,60,69,72,101,142,150,275,278,280,281,282,285,286,287]
listOfCaseIDs=list(set(listOfCaseIDs) - set(ignoreCaseIDs))



for case in listOfCaseIDs:
    tag = 0
    caseDir = getCaseDir(case)
    nids =  getNeedleImageIDs(caseDir)

    #### CHECK IF NEEDLE SERIES IS SHORT AND COVER-PROSTATE IMAGE IS MISSING

    #print getNeedleImageIDs(caseDir)
    """
    if os.path.exists(caseDir):
        list = os.listdir(caseDir)

        if len(list) < 10:
            print 'case '+str(case)+' is short!'

        for f in range(len(list)):
            if not any("CoverProstate" in s for s in list):
              print 'COVER PROSTATE IS MISSING '+str(case)
              count += 1
              break
    """
    ####

    ####
    # CHECK FOR TG

    firstNeedleImage = nids[0]
    if os.path.exists(caseDir+str(firstNeedleImage)+'-TG.nrrd'):
        print "case "+str(case)+' uses a TG'
    ####


    ####
    # CHECK IF TRANSFORMS ARE EXISTING FOR EACH NEEDLE CONFIRMATION IMAGE
    transDir = getTransformDir(case)
    for i in range(0,len(nids)):
        #print nids
        listDir = os.listdir(transDir)
        #print listDir
        if not any (str(nids[i])+'-' in s for s in listDir):
            print "TRANSFORM "+str(nids[i])+' IN CASE '+str(case)+' IS MISSING'
            tag = 1

    if tag == 1:

         print '____________________'
         print "\n"
         tag = 0
    ####

"""
print '____________________________________'
print ' no segmentation in '+str(count)+' cases'
"""