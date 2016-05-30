import os, argparse, string, re, sys, glob
from time import time

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

def createFolders():
  try:
    os.mkdir(RegDir)
  except:
    pass

  try:
    os.mkdir(TempDir)
  except:
    pass

  try:
    os.mkdir(resDir)
  except:
    pass

def getCaseDir(case):

    if case < 10:
        caseDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Cases003-298_data/Case00'+str(case)+'/IntraopImages/'
    elif 9 < case < 100:
        caseDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Cases003-298_data/Case0'+str(case)+'/IntraopImages/'
    elif 99 < case:
        caseDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Cases003-298_data/Case'+str(case)+'/IntraopImages/'

    return caseDir

def getRegDir(case):

    if case < 10:
        regDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Transforms_Pelvis/Case00'+str(case)+'/IntraopImages/'
    elif 9 < case < 100:
        regDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Transforms_Pelvis/Case0'+str(case)+'/IntraopImages/'
    elif 99 < case:
        regDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Transforms_Pelvis/Case'+str(case)+'/IntraopImages/'

    return regDir

def getTransformDir(case):

    if case < 10:
        transformDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Transforms_Pelvis/Case00'+str(case)
    elif 9 < case < 100:
        transformDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Transforms_Pelvis/Case0'+str(case)
    elif 99 < case:
        transformDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Transforms_Pelvis/Case'+str(case)

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

def getListOfCaseIDs(numberOfCases):

  listOfCaseIDs = []

  for case in range(numberOfCases):
    if case < 10:
        caseDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Cases003-298_data/Case00'+str(case)+'/IntraopImages/'
        print caseDir
        if os.path.isdir(str(caseDir)):
             listOfCaseIDs.append(case)
    elif 9 < case < 100:
        caseDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Cases003-298_data/Case0'+str(case)+'/IntraopImages/'
        print caseDir
        if os.path.isdir(str(caseDir)):
             listOfCaseIDs.append(case)
    elif 99 < case:
        caseDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Cases003-298_data/Case'+str(case)+'/IntraopImages/'
        print caseDir
        if os.path.isdir(str(caseDir)):
             listOfCaseIDs.append(case)

  return listOfCaseIDs

def getTempDir(case):

    if case < 10:
        tempDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Masks_Pelvis/Case00'+str(case)
    elif 9 < case < 100:
        tempDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Masks_Pelvis/Case0'+str(case)
    elif 99 < case:
        tempDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Masks_Pelvis/Case'+str(case)

    return tempDir

def getResDir(case):

    if case < 10:
        ResDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Images_Pelvis/Case00'+str(case)
    elif 9 < case < 100:
        ResDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Images_Pelvis/Case0'+str(case)
    elif 99 < case:
        ResDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Images_Pelvis/Case'+str(case)

    return ResDir

def getMotionDir(case):

    if case < 10:
        motionDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/motion_Pelvis/Case00'+str(case)
    elif 9 < case < 100:
        motionDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/motion_Pelvis/Case0'+str(case)
    elif 99 < case:
        motionDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/motion_Pelvis/Case'+str(case)

    return motionDir

def createCentroid(mask,result):

  import SimpleITK as sitk

  # get centroid
  mask=sitk.ReadImage(mask)
  stats = sitk.LabelShapeStatisticsImageFilter()
  stats.Execute(mask)
  labels=stats.GetLabels()
  print stats.GetCentroid(labels[0])

  # write fiducial

  cmd = 'touch '+str(result)
  f = open(str(result), 'w')
  f.write(str(stats.GetCentroid(labels[0])))

def transformFiducialsBRAINS(fidIn,tfmIn,fidOut):
  CMD='/Users/peterbehringer/MyProjects/BRAINSTools/BRAINSTools-build/bin/BRAINSConstellationLandmarksTransform -i '+fidIn+' -t '+tfmIn+' -o '+fidOut
  print 'about to run : '+CMD

  ret = os.system(CMD)
  if ret:
   exit()

def transformFiducialsPelvis(needleImageIds,ResDir,case):

    for nid in needleImageIds:
      bsplineTfm=None
      nidStr=str(nid)
      fixedImage = IntraDir+'/'+nidStr+'-Needle.nrrd'

      # check if there is a matching TG
      initTfm = IntraDir+nidStr+'-init.h5'

      if os.path.isfile(initTfm):
          bsplineTfm = initTfm
      else:
          transformDir = getTransformDir(case)+'/IntraopImages'
          bsplineTfm = transformDir+'/'+nidStr+'-IntraIntra-Rigid-Attempt1.h5'


      #print ('bsplineTfm'+str(bsplineTfm))

      if not os.path.isfile(bsplineTfm):
        bsplineTfm = transformDir+'/'+nidStr+'-IntraIntra-Rigid-Attempt2.h5'
        if not os.path.isfile(bsplineTfm):
            print 'Failed to find ANY transform!'
            exit()

      #resampled = ResDir+'/'+nidStr+'-Pelvis-RigidRegistered-centroid.fcsv'
      try:
          os.makedirs(centroidDir+'/Case'+str(case)+'/')
      except:
          pass

      fid3='/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/targets_Pelvis/Case'+str(case)+'/centroid_label.fcsv'
      #fid4='/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/targets/Case'+str(case)+'/midgland_inferior.fcsv'
      #fid5='/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/targets/Case'+str(case)+'/midgland_left.fcsv'
      #fid6='/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/targets/Case'+str(case)+'/midgland_right.fcsv'
      #fid7='/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/targets/Case'+str(case)+'/midgland_superior.fcsv'

      listOfTargetsToBeTransformed = ['centroid_label']

      for i in range(0,len(listOfTargetsToBeTransformed)):

          resampled = centroidDir+'/Case'+str(case)+'/'+str(nidStr)+'-RigidRegistered-'+str(listOfTargetsToBeTransformed[i])+'.fcsv'
          fidList = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/targets_Pelvis/Case'+str(case)+'/'+str(listOfTargetsToBeTransformed[i])+'.fcsv'

          transformFiducialsSlicer(fiducialsIn=fidList,transform=bsplineTfm,fiducialsOut=resampled)

          i+=1

    print ('transformed fiducials for case '+str(case) +'!')
    print '\n'
    print '\n'
    print '\n'
    print '\n'
    print '\n'

def transformFiducialsSlicer(fiducialsIn, transform, fiducialsOut):
      ### done in Slicer!
      fidLogic = slicer.modules.markups.logic()
      tfmLogic = slicer.modules.transforms.logic()
      fidId = fidLogic.LoadMarkupsFiducials(fiducialsIn, 'na')
      print 'Fiducials loaded:',fidId
      fid = slicer.mrmlScene.GetNodeByID(fidId)
      tfm = tfmLogic.AddTransform(transform, slicer.mrmlScene)
      fid.SetAndObserveTransformNodeID(tfm.GetID())
      tfmLogic.hardenTransform(fid)

      fidStorage = fid.GetStorageNode()
      fidStorage.SetFileName(fiducialsOut)
      fidStorage.WriteData(fid)

def createMotionSummary(case,motionDir,centroidDir,needleImageIDs,listOfColumns):

    try:
      os.makedirs(motionDir)
    except:
      pass

    listOfTargetsToBeTransformed = ['centroid_label']


    for i in range(0,len(listOfTargetsToBeTransformed)):


        #print 'DIR = '+str(motionDir+'/motionsummary_'+str(listOfTargetsToBeTransformed[i])+'.txt')
        dir = motionDir+'/motionsummary_'+str(listOfTargetsToBeTransformed[i])+'.txt'
        cmd='touch '+ str(dir)
        #print dir
        os.system(cmd)

        f = open(dir, 'w')
        #f.write('case,nid,nidTime-initialTime,nidPosition[0]-initialPosition[0],nidPosition[1]-initialPosition[1],nidPosition[2]-initialPosition[2]')
        summary=[]
        for nid in needleImageIds:


          nidTime = ReadNeedleTime(case,nid)
          initialTime = ReadInitialTime(case)

          #print nidTime

          resampled = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/targets_transformed_Pelvis/Case'+str(case)+\
                      '/'+str(nid)+'-RigidRegistered-'+str(listOfTargetsToBeTransformed[i])+'.fcsv'

          initialPosition = ReadInitialFiducial('/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/targets_Pelvis/Case'+str(case)+'/'+str(listOfTargetsToBeTransformed[i])+'.fcsv')

          nidPosition = ReadRigidFiducial(resampled)

          #print case,',',nid,',',nidTime-initialTime,',',abs(nidPosition[0]-initialPosition[0]),', ',abs(nidPosition[1]-initialPosition[1]),', ',abs(nidPosition[2]-initialPosition[2])
          #print 'nidPosition[0]'+str(nidPosition[0])
          #print 'initialPosition[0]'+str(initialPosition[0])

          summary.append([case,nid,nidTime-initialTime,nidPosition[0]-initialPosition[0],nidPosition[1]-initialPosition[1],nidPosition[2]-initialPosition[2]])
          f.write(str(case)+','+str(nid)+','+str(nidTime-initialTime)+','+str(nidPosition[0]-initialPosition[0])+','+str(nidPosition[1]-initialPosition[1])+','+str(nidPosition[2]-initialPosition[2]))
          f.write('\n')
          x = nidPosition[0]-initialPosition[0]
          y = nidPosition[1]-initialPosition[1]
          z = nidPosition[2]-initialPosition[2]

          appendToExcelColumn(listOfTargetsToBeTransformed[i],x,y,z,list_of_columns)

          #print nidTime-initialTime

        """
        f.write("\n"+"_____________________________________")
        #print '_______'
        #print summary

        avgX = 0
        avgY = 0
        avgZ = 0

        for i in range(0,len(needleImageIds)):
          avgX =avgX+summary[i][3]
          avgY =avgY+summary[i][4]
          avgZ =avgZ+summary[i][5]

        avgX=avgX/len(needleImageIds)
        avgY=avgY/len(needleImageIds)
        avgZ=avgZ/len(needleImageIds)

        #print avgX
        #print avgY
        #print avgZ

        f.write("\n"+str(case)+', '+str(avgX)+', '+str(avgY) + ', ' +str(avgZ))
        """
def getNameOfList(index):
    
    if index == 0:
        return 'excel_column_LABEL_x'
    if index == 1:
        return 'excel_column_LABEL_y'
    if index == 2:
        return 'excel_column_LABEL_z'

    
def appendToExcelColumn(targetToBeTransformed,x,y,z,listOfColumns):


        excel_column_LABEL_x = listOfColumns[0]
        excel_column_LABEL_y = listOfColumns[1]
        excel_column_LABEL_z = listOfColumns[2]




        if targetToBeTransformed == 'centroid_label':
            excel_column_LABEL_x.append(x)
            excel_column_LABEL_y.append(y)
            excel_column_LABEL_z.append(z)


def createListOfColumns():

    list_of_columns = []

    excel_column_LABEL_x = []
    excel_column_LABEL_y = []
    excel_column_LABEL_z = []


    list_of_columns.append(excel_column_LABEL_x)
    list_of_columns.append(excel_column_LABEL_y)
    list_of_columns.append(excel_column_LABEL_z)

    return list_of_columns

def printListOfColumns(list_of_columns):

    for motionList in range(len(list_of_columns)):
        print 'list = '+str(getNameOfList(motionList))
        for i in range(len(list_of_columns[motionList])):
            print list_of_columns[motionList][i]

def ReadInitialFiducial(dir):

    f = open(dir, 'r')
    l = f.read()
    #print l
    i = l.split(',')
    #print i
    #print 'i[1]'
    #print [float(i[1])]
    #print 'i[2]'
    #print [float(i[2])]
    #print 'i[3]'
    #print [float(i[3])]
    return [float(i[1]),float(i[2]),float(i[3])]

def ReadFiducial(fname):

    #print 'fname',fname
    f = open(fname, 'r')
    # ignore line 1-8
    l = f.readlines()[8:]
    #print 'l = ',str(l)
    number_of_fids=len(l)
    #print ('amount of fids : '+str(number_of_fids))
    import string
    splitted=string.split(str(l),',')
    #print 'splitted = '+str(splitted)
    #print splitted[1]
    #print splitted[2]
    #print splitted[3]
    """
    chunks=[splitted[x:x+6] for x in xrange(0, number_of_fids*6, 6)]
    fiducials=[]
    for i in range(0,1):
        # print ('fiducialPoint = '+str(chunks[i][1:4]))
        fiducials.append(chunks[i][1:4])
    """
    return [float(splitted[1]),float(splitted[2]),float(splitted[3])]

def ReadRigidFiducial(fname):

    f = open(fname, 'r')
    # ignore line 1-8
    l = f.readlines()[3:]
    #print 'l = ',str(l)
    number_of_fids=len(l)
    #print ('amount of fids : '+str(number_of_fids))
    import string
    splitted=string.split(str(l),',')
    #print 'splitted = '+str(splitted)
    #print splitted[1]
    #print splitted[2]
    #print splitted[3]
    """
    chunks=[splitted[x:x+6] for x in xrange(0, number_of_fids*6, 6)]
    fiducials=[]
    for i in range(0,1):
        # print ('fiducialPoint = '+str(chunks[i][1:4]))
        fiducials.append(chunks[i][1:4])
    """
    return [float(splitted[1]),float(splitted[2]),float(splitted[3])]


def tm2sec(tm):
  try:
    hhmmss = string.split(tm,'.')[0]
  except:
    hhmmss = tm

  try:
    ssfrac = float('0.'+string.split(tm,'.')[1])
  except:
    ssfrac = 0.

  if len(hhmmss)==6: # HHMMSS
    sec = float(hhmmss[0:2])*60.*60.+float(hhmmss[2:4])*60.+float(hhmmss[4:6])
  elif len(hhmmss)==4: # HHMM
    sec = float(hhmmss[0:2])*60.*60.+float(hhmmss[2:4])*60.
  elif len(hhmmss)==2: # HH
    sec = float(hhmmss[0:2])*60.*60.

  sec = sec+ssfrac

  return sec

def ReadInitialTime(case):
  movingImageID = getMovingImageID(caseDir)
  file = IntraDir+str(movingImageID[0])+'.timestamp'
  f=open(file,'r')
  return tm2sec(f.read())

def ReadNeedleTime(case,nid):
  file=getCaseDir(case)+str(nid)+'.timestamp'
  f=open(file,'r')
  return tm2sec(f.read())

def createOverallFiducialSummary(listOfCaseIDs,motionDir):

    summary=[]
    for case in listOfCaseIDs:

        listOfTargetsToBeTransformed = ['centroid_label']

        for target in listOfTargetsToBeTransformed:
            print target
            fileDir = motionDir+'/motionsummary_' + target +'.txt'
            print fileDir



        f=open(fileDir,'r')
        # ignore line 1-8
        l = f.readlines()[2:len(fileDir)-2]
        print l
        for line in f:
          last=line
        splitted=last.split(',')
        print splitted

    """
    summary.append(splitted)

    print summary

    avgX=0
    avgY=0
    avgZ=0

    for i in range(0,len(summary)):
      avgX =avgX+float(summary[i][1])
      avgY =avgY+float(summary[i][2])
      print ('avgY = '+str(avgY))
      print ('case = '+str(i))
      avgZ =avgZ+float(summary[i][3])

    avgX=avgX/len(summary)
    avgY=avgY/len(summary)
    avgZ=avgZ/len(summary)

    print avgX
    print avgY
    print avgZ

    cmd=('touch /Users/peterbehringer/MyStudies/Verification/OverallSummary_glandMotion.txt')
    print ('about to run '+cmd)
    os.system(cmd)
    f = open('/Users/peterbehringer/MyStudies/Verification/OverallSummary_glandMotion.txt', 'w')
    f.write('Overall Summary created, showing [lastcase,averageMovement_x, averageMovement_y, averageMovement_z ')
    f.write("\n"+str(case)+', '+str(avgX)+', '+str(avgY) + ', ' +str(avgZ))
    """

def makeConfig(case,caseDir,needleImageIDs,RegDir,ResDir):

    import os, argparse, string, re, sys, glob
    import ConfigParser as conf
    from time import time


    # delete : SegDir='/Users/peterbehringer/MyStudies/Segmentations-Cases11-50/Case'+case+'-ManualSegmentations'


    cf = conf.SafeConfigParser()
    cf.optionxform = str
    cfFileName = configDir+'/Case'+str(case)+'_VisAIRe.ini'

    try:
      cmd = ('touch '+str(cfFileName))
      os.system(cmd)
    except:
      pass

    cfFile = open(cfFileName,'w')

    # moving image/mask will always be the same
    movingImageID = getMovingImageID(caseDir)
    movingImage = caseDir+str(movingImageID[0])+'-CoverProstate.nrrd'
    segImage = caseDir+str(movingImageID[0])+'-label.nrrd'


    cf.add_section('MovingData')
    cf.set('MovingData','ImagesPath',IntraDir)
    #cf.set('MovingData','SegmentationsPath',SegDir)
    cf.set('MovingData','Image',os.path.abspath(movingImage))
    cf.set('MovingData','Segmentation',os.path.abspath(segImage))

    cf.add_section('FixedData')
    cf.set('FixedData','ImagesPath',IntraDir)

    for nid in needleImageIds:
      nidStr=str(nid)
      cf.set('FixedData','Image'+nidStr,os.path.join(os.path.abspath(IntraDir),nidStr+'-Needle.nrrd'))

    cf.add_section('RegisteredData')
    cf.set('RegisteredData','ImagesPath',ResDir)
    cf.set('RegisteredData','TransformsDir',RegDir)

    for nid in needleImageIds:
      nidStr=str(nid)
      cf.set('RegisteredData','Image'+nidStr,os.path.join(os.path.abspath(ResDir),nidStr+'-Rigid_resampled.nrrd'))
      # TODO: add transformations
      tfmFileInit = IntraDir+nidStr+'-init.h5'
      tfmFile1 = RegDir+nidStr+'-IntraIntra-Rigid-Attempt1.h5'
      tfmFile2 = RegDir+nidStr+'-IntraIntra-Rigid-Attempt2.h5'

      print tfmFile1
      print tfmFile2
      print tfmFileInit

      if os.path.exists(tfmFileInit):
        print 'i am existing'
        cf.set('RegisteredData','Transform'+nidStr,os.path.abspath(tfmFileInit))
      elif os.path.exists(tfmFile1):
        cf.set('RegisteredData','Transform'+nidStr,os.path.abspath(tfmFile1))
      elif os.path.exists(tfmFile2):
        cf.set('RegisteredData','Transform'+nidStr,os.path.abspath(tfmFile2))
      else:
        assert False
      # add segmentations

    # assessment questions; format:
    #   comment; type=[binary,number];
    cf.add_section('Questions')
    cf.set('Questions','Question1','Did registration improve alignment?;binary;')
    cf.set('Questions','Question2','Is registered image of diagnostic quality?;binary;')
    cf.set('Questions','Question3','Quantitative assessment of mis-registration (if available);numeric;')


    cf.add_section('Info')
    cf.set('Info','CaseName','BxCase'+str(case))

    cf.write(cfFile)
    cfFile.close()

    print 'Config file saved as ',cfFileName

registrationCmd = "/Applications/Slicer.app/Contents/lib/Slicer-4.4/cli-modules/BRAINSFit"
resamplingCmd = "/Applications/Slicer.app/Contents/lib/Slicer-4.4/cli-modules/BRAINSResample"

# depedencies:
# - python anaconda for h5py
# - simpleitk
# - pylab ('pip install pylab' into terminal)


# dirs
CaseDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Cases003-298_data/'
RegDir='/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Transforms_Pelvis/'
TempDir='/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Masks_Pelvis'
latestRigidTfm = '/Users/peterbehringer/MyStudies/InitialTransforms/Identity.h5'
centroidDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/targets_transformed_Pelvis'
configDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/configs_Pelvis'

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

createFolders()
list_of_columns = createListOfColumns()
################################
# RUN prostate motion calculation


# 1. create pelvis labels.py
#cmd = 'python makePelvisMask.py '
#print ('about to run : '+cmd)
#os.system(cmd)

# 1. create Trackers.py
#cmd = 'python pelvis_createTrackers.py '
#print ('about to run : '+cmd)
#os.system(cmd)

# register case

for case in listOfCaseIDs:
  #print 'execute meta.py for case '+str(case)

  caseDir=getCaseDir(case)
  transformDir=getTransformDir(case)
  regDir=getRegDir(case)
  tempDir=getTempDir(case)
  resDir = getResDir(case)
  IntraDir = caseDir
  motionDir = getMotionDir(case)

  needleImageIds = []
  needleImageIds = getNeedleImageIDs(IntraDir)


  # 1. registerCase.py
  cmd = ('python pelvis_registerCase.py '+str(case)+' '+str(caseDir)+' '+str(regDir)+' '+str(tempDir))
  #print ('about to run : '+cmd)
  #os.system(cmd)

  # 2. resampleCase.py
  cmd = ('python pelvis_resampleCase.py '+str(case)+' '+str(regDir)+' '+str(IntraDir)+' '+str(resDir))
  #print ('about to run : '+cmd)
  #os.system(cmd)

  # 4. transformCentroids
  #transformFiducialsPelvis(needleImageIds,resDir,case)

  # 5. create Config for verification and snapshots
  #makeConfig(case,caseDir,needleImageIds,regDir,resDir)

  # 6. createMotionSummary
  #createMotionSummary(case,motionDir,centroidDir,needleImageIds,list_of_columns)


# 7. print Motion for Excel
#printListOfColumns(list_of_columns)

