import os, argparse, string, re, sys, glob
from time import time

def getNeedleImageIDs(IntraDir,needleImageIDs):
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
        regDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Transforms/Case00'+str(case)+'/IntraopImages/'
    elif 9 < case < 100:
        regDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Transforms/Case0'+str(case)+'/IntraopImages/'
    elif 99 < case:
        regDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Transforms/Case'+str(case)+'/IntraopImages/'

    return regDir

def getTransformDir(case):

    if case < 10:
        transformDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Transforms/Case00'+str(case)
    elif 9 < case < 100:
        transformDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Transforms/Case0'+str(case)
    elif 99 < case:
        transformDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Transforms/Case'+str(case)

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
        tempDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Masks/Case00'+str(case)
    elif 9 < case < 100:
        tempDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Masks/Case0'+str(case)
    elif 99 < case:
        tempDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Masks/Case'+str(case)

    return tempDir

def getResDir(case):

    if case < 10:
        ResDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Images/Case00'+str(case)
    elif 9 < case < 100:
        ResDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Images/Case0'+str(case)
    elif 99 < case:
        ResDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Images/Case'+str(case)

    return ResDir

def getMotionDir(case):

    if case < 10:
        motionDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/motion/Case00'+str(case)
    elif 9 < case < 100:
        motionDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/motion/Case0'+str(case)
    elif 99 < case:
        motionDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/motion/Case'+str(case)

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
  #print 'about to run : '+CMD

  ret = os.system(CMD)
  if ret:
   exit()

def transformFiducials(needleImageIds,ResDir,case):

    for nid in needleImageIds:
      bsplineTfm=None
      nidStr=str(nid)
      fixedImage = IntraDir+'/'+nidStr+'-Needle.nrrd'

      # check if there is a matching TG
      transformDir = getTransformDir(case)+'/IntraopImages'
      bsplineTfm = transformDir+'/'+nidStr+'-IntraIntra-BSpline-Attempt2.h5'
      #print ('bsplineTfm'+str(bsplineTfm))
      if not os.path.isfile(bsplineTfm):
        #print ('went here')
        bsplineTfm = transformDir+'/'+nidStr+'-IntraIntra-BSpline-Attempt1.h5'
        #print ('bsplineTfm '+str(bsplineTfm))
      if not os.path.isfile(bsplineTfm):
        print 'Failed to find ANY transform!'
        exit()

      # TODO: choose if targets or centroids should be registered and saved

      #resampled = ResDir+'/'+nidStr+'-Pelvis-RigidRegistered-centroid.fcsv'
      try:
          os.makedirs(centroidDir+'/Case'+str(case)+'/')
      except:
          pass

      fid1='/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/targets/Case'+str(case)+'/centroid_apex.fcsv'
      fid2='/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/targets/Case'+str(case)+'/centroid_base.fcsv'
      fid3='/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/targets/Case'+str(case)+'/centroid_label.fcsv'
      fid4='/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/targets/Case'+str(case)+'/midgland_inferior.fcsv'
      fid5='/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/targets/Case'+str(case)+'/midgland_left.fcsv'
      fid6='/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/targets/Case'+str(case)+'/midgland_right.fcsv'
      fid7='/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/targets/Case'+str(case)+'/midgland_superior.fcsv'

      listOfTargetsToBeTransformed = ['centroid_apex',
                                      'centroid_base',
                                      'centroid_label',
                                      'midgland_inferior',
                                      'midgland_left',
                                      'midgland_right',
                                      'midgland_superior']

      for i in range(0,len(listOfTargetsToBeTransformed)):

          resampled = centroidDir+'/Case'+str(case)+'/'+str(nidStr)+'-BSplineRegistered-'+str(listOfTargetsToBeTransformed[i])+'.fcsv'
          fidList = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/targets/Case'+str(case)+'/'+str(listOfTargetsToBeTransformed[i])+'.fcsv'

          transformFiducialsBRAINS(fidIn=fidList,tfmIn=bsplineTfm,fidOut=resampled)

          i+=1

    print ('transformed fiducials for case '+str(case) +'!')

def createMotionSummary(case,motionDir,centroidDir,needleImageIDs):

    try:
      os.makedirs(motionDir)
    except:
      pass

    listOfTargetsToBeTransformed = ['centroid_apex',
                                    'centroid_base',
                                    'centroid_label',
                                    'midgland_inferior',
                                    'midgland_left',
                                    'midgland_right',
                                    'midgland_superior']

    for i in range(0,len(listOfTargetsToBeTransformed)):
        #print 'DIR = '+str(motionDir+'/motionsummary_'+str(listOfTargetsToBeTransformed[i])+'.txt')
        dir = motionDir+'/motionsummary_'+str(listOfTargetsToBeTransformed[i])+'.txt'
        cmd='touch '+ str(dir)
        print dir
        os.system(cmd)

        f = open(dir, 'w')
        f.write('case,nid,nidTime-initialTime,nidPosition[0]-initialPosition[0],nidPosition[1]-initialPosition[1],nidPosition[2]-initialPosition[2]')
        summary=[]
        for nid in needleImageIds:


          nidTime = ReadNeedleTime(case,nid)
          initialTime = ReadInitialTime(case)

          #print nidTime

          resampled = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/targets_transformed/Case'+str(case)+\
                      '/'+str(nid)+'-BSplineRegistered-'+str(listOfTargetsToBeTransformed[i])+'.fcsv'

          initialPosition = ReadInitialFiducial('/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/targets/Case'+str(case)+'/'+str(listOfTargetsToBeTransformed[i])+'.fcsv')

          nidPosition = ReadFiducial(resampled)

          print case,',',nid,',',nidTime-initialTime,',',abs(nidPosition[0]-initialPosition[0]),', ',abs(nidPosition[1]-initialPosition[1]),', ',abs(nidPosition[2]-initialPosition[2])
          #print 'nidPosition[0]'+str(nidPosition[0])
          #print 'initialPosition[0]'+str(initialPosition[0])

          summary.append([case,nid,nidTime-initialTime,abs(nidPosition[0]-initialPosition[0]),abs(nidPosition[1]-initialPosition[1]),abs(nidPosition[2]-initialPosition[2])])
          f.write("\n"+str(case)+','+str(nid)+','+str(nidTime-initialTime)+','+str(abs(nidPosition[0]-initialPosition[0]))+', '+str(abs(nidPosition[1]-initialPosition[1]))+', '+str(abs(nidPosition[2]-initialPosition[2])))


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

def createOverallFiducialSummary():


    summary=[]
    for case in listOfCaseIDs:

        motionDir=('/Users/peterbehringer/MyStudies/Verification/Case'+str(case)+'/summary_glandMotion.txt')
        print motionDir
        f=open(pathToFile,'r')
        for line in f:
          last=line
        splitted=last.split(',')
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


registrationCmd = "/Applications/Slicer.app/Contents/lib/Slicer-4.4/cli-modules/BRAINSFit"
resamplingCmd = "/Applications/Slicer.app/Contents/lib/Slicer-4.4/cli-modules/BRAINSResample"

# depedencies:
# - python anaconda for h5py
# - simpleitk

# dirs
CaseDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Cases003-298_data/'
RegDir='/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Transforms/'
TempDir='/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Masks'
latestRigidTfm = '/Users/peterbehringer/MyStudies/InitialTransforms/Identity.h5'
centroidDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/targets_transformed'

numberOfCases = 300
listOfCaseIDs = []
ignoreCaseIDs = [4,5,7,8,52,60,69,72,101,142,150,269,275,278,280,281,282,285,286,287,293]

# get list of cases
listOfCaseIDs = getListOfCaseIDs(numberOfCases)

# ignore cases
listOfCaseIDs=list(set(listOfCaseIDs) - set(ignoreCaseIDs))
#print listOfCaseIDs

# testing:
#listOfCaseIDs = [10,11,12,13]

createFolders()

################################
# RUN prostate motion calculation

# register case

for case in listOfCaseIDs:
  print 'execute meta.py for case '+str(case)

  caseDir=getCaseDir(case)
  transformDir=getTransformDir(case)
  regDir=getRegDir(case)
  tempDir=getTempDir(case)
  resDir = getResDir(case)
  IntraDir = caseDir
  motionDir = getMotionDir(case)

  needleImageIds = []
  needleImageIds = getNeedleImageIDs(IntraDir,needleImageIds)


  """

  # 1. registerCase.py
  cmd = ('python registerCase.py '+str(case)+' '+str(caseDir)+' '+str(regDir)+' '+str(tempDir))
  print ('about to run : '+cmd)
  os.system(cmd)


  # 2. resampleCase.py
  cmd = ('python resampleCase.py '+str(case)+' '+str(regDir)+' '+str(IntraDir)+' '+str(resDir))
  print ('about to run : '+cmd)
  os.system(cmd)


  # 4. transformCentroids
  transformFiducials(needleImageIds,resDir,case)
  """


  # 5. createMotionSummary
  #createMotionSummary(case,motionDir,centroidDir,needleImageIds)



  """
  # 3. MakeConfig.py
  cmd = ('python MakeConfig.py '+str(case))
  print ('about to run : '+cmd)
  #os.system(cmd)
  """



createOverallFiducialSummary(listOfCaseIDs,motionDir)