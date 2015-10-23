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

def getMovingImageID(IntraDir):
    movingImageID = []
    # returns list of Image ID's for case with dir intradir
    if os.path.isdir(IntraDir):
      listDir = os.listdir(IntraDir)
      #print 'HERE'
      #print listDir
      for i in range(len(listDir)):
          if 'CoverProstate' in listDir[i]:
              movingImageID.append(int(string.split(listDir[i],'-')[0]))
    else:
      print 'there is no path like: '+str(IntraDir)
    return movingImageID

def getLabelVolumeInL(label,image):

  import SimpleITK as sitk

  label = sitk.ReadImage(label)
  image = sitk.ReadImage(image)

  stats = sitk.LabelShapeStatisticsImageFilter()
  stats.Execute(label)
  labelID=stats.GetLabels()[0]
  #print labelID

  pixelcount = stats.GetNumberOfPixels(labelID)

  volume = pixelcount * (image.GetSpacing()[0] * image.GetSpacing()[1] * image.GetSpacing()[2])
  #print( """Computed volume is {vl} mm^3""".format( vl=volume ))

  # to liter: 1mm^3 = 0.000001 L
  volume = volume * 0.000001
  volume = volume * 1000

  return volume


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

count = 0
count2 = 0
count3 = 0
numberOfCases = 0

excel_column_CASE = []
excel_column_NEEDLEIMAGE = []

prostate_volumes = []


listOfCaseIDs = getListOfCaseIDs(300)
ignoreCaseIDs = [4,5,7,8,52,60,69,72,101,142,150,269,275,278,280,281,282,285,286,287,293]
listOfCaseIDs=list(set(listOfCaseIDs) - set(ignoreCaseIDs))

#listOfCaseIDs = [214]

for case in listOfCaseIDs:


    #print 'case = '+str(case)
    tag = 0
    caseDir = getCaseDir(case)
    nids =  getNeedleImageIDs(caseDir)

    #### CHECK IF NEEDLE SERIES IS SHORT AND COVER-PROSTATE IMAGE IS MISSING

    #print getNeedleImageIDs(caseDir)

    if os.path.exists(caseDir):
        list = os.listdir(caseDir)

        county = 0
        for items in list:
            #print items
            if 'CoverProstate' in items:
                county = county + 1

            if county == 2:
                print 'found a double CoverProstate case, its : '+str(case)


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


    #### COUNT !

    for needleImgs in nids:
        count2 += 1

        #print case
        #print needleImgs

        excel_column_CASE.append(case)
        excel_column_NEEDLEIMAGE.append(needleImgs)

    ####

    ####
    # CHECK FOR USELESS TG

    firstNeedleImage = nids[0]


    #if os.path.exists(caseDir+str(firstNeedleImage)+'-TG.nrrd'):
        #print "case "+str(case)+' uses a TG'


    fileList = os.listdir(caseDir)
    for file in fileList:
        if 'Pelvis-Pelvis' in file:
            print 'found pelvis pelvis file, its '+str(file)
            os.remove(caseDir+'/'+str(file))
    ####




    ####
    # CHECK FOR TG

    firstNeedleImage = nids[0]


    #if os.path.exists(caseDir+str(firstNeedleImage)+'-TG.nrrd'):
        #print "case "+str(case)+' uses a TG'


    fileList = os.listdir(caseDir)
    for file in fileList:
        if 'TG' in file:
            if 'Pelvis' not in file:
              count3 = count3 + 1
              # print 'found a tg, its '+str(file)

    ####



    # GET PROSTATE SIZE in ml
    #for needleImgs in nids:

    movingImageID = getMovingImageID(caseDir)
    image = caseDir+str(movingImageID[0])+'-CoverProstate.nrrd'
    label = caseDir+str(movingImageID[0])+'-label.nrrd'
    size_in_mL = getLabelVolumeInL(label,image)

    #print size_in_mL
    prostate_volumes.append(size_in_mL)

    fileList = os.listdir(caseDir)
    for file in fileList:
        if 'TG' in file:
            if 'Pelvis' not in file:
              count3 = count3 + 1
              # print 'found a tg, its '+str(file)

    ####




    ####
    """
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

    # CHECK IF CONFIGS WERE CREATED

    configDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/configs'
    cfFileName = configDir+'/Case'+str(case)+'_VisAIRe.ini'

    if not os.path.exists(cfFileName):
        print 'config file is missing for case '+str(case)


    """
    numberOfCases = numberOfCases + 1


print prostate_volumes

for i in range(0,len(prostate_volumes)):
    print prostate_volumes[i]



"""
print '____________________________________'
print ' no segmentation in '+str(count)+' cases'

print '____________________________________'
print 'there are '+str(numberOfCases)+' cases in total'

print '____________________________________'
print 'there are '+str(count2)+' needle images in total'

print '____________________________________'
print str(count3)+' manual segmentations were needed'
"""