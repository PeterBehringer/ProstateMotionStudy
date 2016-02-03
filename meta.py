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

        if os.path.isdir(str(caseDir)):
             listOfCaseIDs.append(case)
    elif 9 < case < 100:
        caseDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Cases003-298_data/Case0'+str(case)+'/IntraopImages/'

        if os.path.isdir(str(caseDir)):
             listOfCaseIDs.append(case)
    elif 99 < case:
        caseDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Cases003-298_data/Case'+str(case)+'/IntraopImages/'

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

def createMotionSummary(case,motionDir,centroidDir,needleImageIDs,listOfColumns):

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


    """
    for nid in needleImageIds:

        nidTime = ReadNeedleTime(case,nid)
        initialTime = ReadInitialTime(case)
        passedTime = str(nidTime - initialTime)

        #print ReadInitialTime(case)
        #print nidTime
        #print passedTime

    """

    for i in range(0,len(listOfTargetsToBeTransformed)):
        #print 'DIR = '+str(motionDir+'/motionsummary_'+str(listOfTargetsToBeTransformed[i])+'.txt')
        dir = motionDir+'/motionsummary_'+str(listOfTargetsToBeTransformed[i])+'.txt'
        cmd='touch '+ str(dir)
        #print dir
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

          #print case,',',nid,',',nidTime-initialTime,',',abs(nidPosition[0]-initialPosition[0]),', ',abs(nidPosition[1]-initialPosition[1]),', ',abs(nidPosition[2]-initialPosition[2])
          #print 'nidPosition[0]'+str(nidPosition[0])
          #print 'initialPosition[0]'+str(initialPosition[0])

          summary.append([case,nid,nidTime-initialTime,abs(nidPosition[0]-initialPosition[0]),abs(nidPosition[1]-initialPosition[1]),abs(nidPosition[2]-initialPosition[2])])
          f.write("\n"+str(case)+','+str(nid)+','+str(nidTime-initialTime)+','+str(abs(nidPosition[0]-initialPosition[0]))+', '+str(abs(nidPosition[1]-initialPosition[1]))+', '+str(abs(nidPosition[2]-initialPosition[2])))

          x = abs(nidPosition[0]-initialPosition[0])
          y = abs(nidPosition[1]-initialPosition[1])
          z = abs(nidPosition[2]-initialPosition[2])

          appendToExcelColumn(listOfTargetsToBeTransformed[i],x,y,z,list_of_columns)

          #print nidTime-initialTime
          print


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

def createMotionSummary2(case,motionDir,centroidDir,needleImageIDs,listOfColumns):

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


    """
    for nid in needleImageIds:

        nidTime = ReadNeedleTime(case,nid)
        initialTime = ReadInitialTime(case)
        passedTime = str(nidTime - initialTime)

        #print ReadInitialTime(case)
        #print nidTime
        #print passedTime

    """

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

          resampled = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/targets_transformed/Case'+str(case)+\
                      '/'+str(nid)+'-BSplineRegistered-'+str(listOfTargetsToBeTransformed[i])+'.fcsv'

          initialPosition = ReadInitialFiducial('/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/targets/Case'+str(case)+'/'+str(listOfTargetsToBeTransformed[i])+'.fcsv')

          nidPosition = ReadFiducial(resampled)

          #print case,',',nid,',',nidTime-initialTime,',',abs(nidPosition[0]-initialPosition[0]),', ',abs(nidPosition[1]-initialPosition[1]),', ',abs(nidPosition[2]-initialPosition[2])
          #print 'nidPosition[0]'+str(nidPosition[0])
          #print 'initialPosition[0]'+str(initialPosition[0])

          summary.append([case,nid,nidTime-initialTime,abs(nidPosition[0]-initialPosition[0]),abs(nidPosition[1]-initialPosition[1]),abs(nidPosition[2]-initialPosition[2])])
          f.write(str(case)+','+str(nid)+','+str(nidTime-initialTime)+','+str(abs(nidPosition[0]-initialPosition[0]))+','+str(abs(nidPosition[1]-initialPosition[1]))+','+str(abs(nidPosition[2]-initialPosition[2])))
          f.write('\n')
          x = abs(nidPosition[0]-initialPosition[0])
          y = abs(nidPosition[1]-initialPosition[1])
          z = abs(nidPosition[2]-initialPosition[2])

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
        return 'excel_column_APEX_x'
    if index == 1:
        return 'excel_column_APEX_y'
    if index == 2:
        return 'excel_column_APEX_z'
    if index == 3:
        return 'excel_column_BASE_x'
    if index == 4:
        return 'excel_column_BASE_y'
    if index == 5:
        return 'excel_column_BASE_z'
    if index == 6:
        return 'excel_column_LABEL_x'
    if index == 7:
        return 'excel_column_LABEL_y'
    if index == 8:
        return 'excel_column_LABEL_z'   
    if index == 9:
        return 'excel_column_INFERIOR_x'
    if index == 10:
        return 'excel_column_INFERIOR_y'
    if index == 11:
        return 'excel_column_INFERIOR_z'
    if index == 12:
        return 'excel_column_LEFT_x'
    if index == 13:
        return 'excel_column_LEFT_y'
    if index == 14:
        return 'excel_column_LEFT_z'
    if index == 15:
        return 'excel_column_RIGHT_x'
    if index == 16:
        return 'excel_column_RIGHT_y'
    if index == 17:
        return 'excel_column_RIGHT_z'
    if index == 18:
        return 'excel_column_SUPERIOR_x'
    if index == 19:
        return 'excel_column_SUPERIOR_y'
    if index == 20:
        return 'excel_column_SUPERIOR_z'
    
def appendToExcelColumn(targetToBeTransformed,x,y,z,listOfColumns):

        excel_column_APEX_x = listOfColumns[0]
        excel_column_APEX_y = listOfColumns[1]
        excel_column_APEX_z = listOfColumns[2]
        excel_column_BASE_x = listOfColumns[3]
        excel_column_BASE_y = listOfColumns[4]
        excel_column_BASE_z = listOfColumns[5]
        excel_column_LABEL_x = listOfColumns[6]
        excel_column_LABEL_y = listOfColumns[7]
        excel_column_LABEL_z = listOfColumns[8]
        excel_column_INFERIOR_x = listOfColumns[9]
        excel_column_INFERIOR_y = listOfColumns[10]
        excel_column_INFERIOR_z = listOfColumns[11]
        excel_column_LEFT_x = listOfColumns[12]
        excel_column_LEFT_y = listOfColumns[13]
        excel_column_LEFT_z = listOfColumns[14]
        excel_column_RIGHT_x = listOfColumns[15]
        excel_column_RIGHT_y = listOfColumns[16]
        excel_column_RIGHT_z = listOfColumns[17]
        excel_column_SUPERIOR_x = listOfColumns[18]
        excel_column_SUPERIOR_y = listOfColumns[19]
        excel_column_SUPERIOR_z = listOfColumns[20]


        if targetToBeTransformed == 'centroid_apex':
            excel_column_APEX_x.append(x)
            excel_column_APEX_y.append(y)
            excel_column_APEX_z.append(z)
        if targetToBeTransformed == 'centroid_base':
            excel_column_BASE_x.append(x)
            excel_column_BASE_y.append(y)
            excel_column_BASE_z.append(z)
        if targetToBeTransformed == 'centroid_label':
            excel_column_LABEL_x.append(x)
            excel_column_LABEL_y.append(y)
            excel_column_LABEL_z.append(z)
        if targetToBeTransformed == 'midgland_inferior':
            excel_column_INFERIOR_x.append(x)
            excel_column_INFERIOR_y.append(y)
            excel_column_INFERIOR_z.append(z)
        if targetToBeTransformed == 'midgland_right':
            excel_column_RIGHT_x.append(x)
            excel_column_RIGHT_y.append(y)
            excel_column_RIGHT_z.append(z)
        if targetToBeTransformed == 'midgland_left':
            excel_column_LEFT_x.append(x)
            excel_column_LEFT_y.append(y)
            excel_column_LEFT_z.append(z)
        if targetToBeTransformed == 'midgland_superior':
            excel_column_SUPERIOR_x.append(x)
            excel_column_SUPERIOR_y.append(y)
            excel_column_SUPERIOR_z.append(z)

def createListOfColumns():

    list_of_columns = []

    excel_column_APEX_x = []
    excel_column_APEX_y = []
    excel_column_APEX_z = []

    excel_column_BASE_x = []
    excel_column_BASE_y = []
    excel_column_BASE_z = []

    excel_column_LABEL_x = []
    excel_column_LABEL_y = []
    excel_column_LABEL_z = []

    excel_column_INFERIOR_x = []
    excel_column_INFERIOR_y = []
    excel_column_INFERIOR_z = []

    excel_column_LEFT_x = []
    excel_column_LEFT_y = []
    excel_column_LEFT_z = []

    excel_column_RIGHT_x = []
    excel_column_RIGHT_y = []
    excel_column_RIGHT_z = []

    excel_column_SUPERIOR_x = []
    excel_column_SUPERIOR_y = []
    excel_column_SUPERIOR_z = []


    list_of_columns.append(excel_column_APEX_x)
    list_of_columns.append(excel_column_APEX_y)
    list_of_columns.append(excel_column_APEX_z)
    list_of_columns.append(excel_column_BASE_x)
    list_of_columns.append(excel_column_BASE_y)
    list_of_columns.append(excel_column_BASE_z)
    list_of_columns.append(excel_column_LABEL_x)
    list_of_columns.append(excel_column_LABEL_y)
    list_of_columns.append(excel_column_LABEL_z)
    list_of_columns.append(excel_column_INFERIOR_x)
    list_of_columns.append(excel_column_INFERIOR_y)
    list_of_columns.append(excel_column_INFERIOR_z)
    list_of_columns.append(excel_column_LEFT_x)
    list_of_columns.append(excel_column_LEFT_y)
    list_of_columns.append(excel_column_LEFT_z)
    list_of_columns.append(excel_column_RIGHT_x)
    list_of_columns.append(excel_column_RIGHT_y)
    list_of_columns.append(excel_column_RIGHT_z)
    list_of_columns.append(excel_column_SUPERIOR_x)
    list_of_columns.append(excel_column_SUPERIOR_y)
    list_of_columns.append(excel_column_SUPERIOR_z)

    return list_of_columns

def printListOfColumns(list_of_columns):

    for motionList in range(len(list_of_columns)):
        print 'list = '+str(getNameOfList(motionList))
        for i in range(len(list_of_columns[motionList])):
            print list_of_columns[motionList][i]

def ReadInitialFiducial(dir):

    f = open(dir, 'r')
    l = f.read()
    i = l.split(',')
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
  IntraDir = getCaseDir(case)
  movingImageID = getMovingImageID(IntraDir)
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

        listOfTargetsToBeTransformed = ['centroid_apex',
                                        'centroid_base',
                                        'centroid_label',
                                        'midgland_inferior',
                                        'midgland_left',
                                        'midgland_right',
                                        'midgland_superior']


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
      cf.set('RegisteredData','Image'+nidStr,os.path.join(os.path.abspath(ResDir),nidStr+'-BSpline_resampled.nrrd'))
      # TODO: add transformations
      tfmFile1 = RegDir+'/'+nidStr+'-IntraIntra-BSpline-Attempt1.h5'
      tfmFile2 = RegDir+'/'+nidStr+'-IntraIntra-BSpline-Attempt2.h5'

      print tfmFile1
      print tfmFile2

      if os.path.exists(tfmFile1):
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

def getProdureTimeInSeconds(case):

   lastNeedleTime = 0
   needleImageIds = getNeedleImageIDs(getCaseDir(case))

   for nid in needleImageIds:
     lastNeedleTime = ReadNeedleTime(case,nid)

   procedureTimeInSeconds = lastNeedleTime - ReadInitialTime(case)
   return procedureTimeInSeconds

def plotProcedureTime(listOfCaseIDs):

    import matplotlib.pyplot as plt

    procedureTimesInSeconds = []
    procedureTimesInMinutes = []

    for case in listOfCaseIDs:
        print 'current case : '+str(case)
        procedureTimesInSeconds.append(getProdureTimeInSeconds(case))

    print 'procedureTimesInSeconds'
    print procedureTimesInSeconds

    for i in range(0,len(procedureTimesInSeconds)):
        procedureTimesInMinutes.append(procedureTimesInSeconds[i]/60)

    #print procedureTimesInMinutes

    plt.figure(2)
    plt.plot(listOfCaseIDs,procedureTimesInMinutes,'bo')
    rect = plt.figure(2)
    rect.set_facecolor('white')
    plt.xlabel('case')
    plt.ylabel('procedure time in minutes')
    plt.show()

def getLabelVolumeInMl(label,image):

  import SimpleITK as sitk

  label = sitk.ReadImage(label)
  image = sitk.ReadImage(image)

  stats = sitk.LabelShapeStatisticsImageFilter()
  stats.Execute(label)
  labelID=stats.GetLabels()[0]

  pixelcount = stats.GetNumberOfPixels(labelID)

  volume = pixelcount * (image.GetSpacing()[0] * image.GetSpacing()[1] * image.GetSpacing()[2])
  #print( """Computed volume is {vl} mm^3""".format( vl=volume ))

  # to liter: 1mm^3 = 0.000001 L
  volume = volume * 0.000001

  # to milliliter:
  volume = volume * 1000

  return volume

def getProstateVolumes(listOfCaseIDs):

    prostate_volumes = []

    for case in listOfCaseIDs:
        caseDir = getCaseDir(case)
        movingImageID = getMovingImageID(caseDir)
        image = caseDir+str(movingImageID[0])+'-CoverProstate.nrrd'
        label = caseDir+str(movingImageID[0])+'-label.nrrd'
        volume_in_mL = getLabelVolumeInMl(label,image)
        prostate_volumes.append(volume_in_mL)

    return prostate_volumes

def plotProstateVolumes(listOfCaseIDs):

    prostate_volumes = getProstateVolumes(listOfCaseIDs)

    import matplotlib.pyplot as plt

    plt.figure(1)
    plt.plot(listOfCaseIDs,prostate_volumes,'bo')
    rect = plt.figure(1)
    rect.set_facecolor('white')
    plt.xlabel('case')
    plt.ylabel('prostate volume in ml')
    plt.show()

def plotNumberOfNeedleImagesPerCase(listOfCaseIDs):

    number_of_needleImages_per_Case = []

    for case in listOfCaseIDs:

        number_of_needleImages = 0
        nids = getNeedleImageIDs(getCaseDir(case))

        for nid in nids:
            number_of_needleImages = number_of_needleImages + 1

        print number_of_needleImages
        number_of_needleImages_per_Case.append(number_of_needleImages)

    #print number_of_needleImages_per_Case

    import matplotlib.pyplot as plt

    plt.figure(3)
    plt.plot(listOfCaseIDs,number_of_needleImages_per_Case,'bo')
    rect = plt.figure(3)
    rect.set_facecolor('white')
    plt.xlabel('case')
    plt.ylabel('number of needle images')
    plt.show()

def plotNumberOfNeedleImagesPerCase_withColomns(listOfCaseIds):

    number_of_needleImages_per_Case = []

    for case in listOfCaseIDs:

        number_of_needleImages = 0
        nids = getNeedleImageIDs(getCaseDir(case))

        for nid in nids:
            number_of_needleImages = number_of_needleImages + 1

        #print number_of_needleImages
        number_of_needleImages_per_Case.append(number_of_needleImages)

    #print 'max'
    #print str(max(number_of_needleImages_per_Case))
    count = range(0,max(number_of_needleImages_per_Case)+1,1)

    for i in range(len(count)):
        count[i] = 0

    #print count
    for i in range(0,len(number_of_needleImages_per_Case)):
        needleImages = number_of_needleImages_per_Case[i]
        count[needleImages] += 1

    #print count



    xrange=range(0,31)
    print xrange
    print count


    import matplotlib.pyplot as plt

    plt.figure(7)
    plt.bar(xrange,count)
    rect = plt.figure(7)
    rect.set_facecolor('white')
    plt.xlabel('needle images')
    plt.ylabel('amount')
    plt.show()



def calculateMaxMotionPerCase2DForCentroid(case):

    import string
    dir = getMotionDir(case)
    file = dir+'/motionsummary_centroid_label.txt'
    f = open(file, 'rb')

    maxMotionX = 0.0
    maxMotionY = 0.0
    maxMotionZ = 0.0

    xPositions = []
    yPositions = []
    zPositions = []


    # read x,y,z motion positions
    for line in f:
        line = line.rstrip('\n')
        splitted=string.split(str(line),',')
        xPositions.append(splitted[3])
        yPositions.append(splitted[4])
        zPositions.append(splitted[5])

    print 'x positions '
    for i in range(0,len(xPositions)):
        print xPositions[i]

    print 'y positions '
    for i in range(0,len(yPositions)):
        print yPositions[i]

    print 'z positions '
    for i in range(0,len(zPositions)):
        print zPositions[i]

    for nid in range(0,len(getNeedleImageIDs(getCaseDir(case)))-1):

      if abs(maxMotionX) < abs(float(xPositions[nid+1])-float(xPositions[nid])):
          maxMotionX = float(xPositions[nid+1])-float(xPositions[nid])

      if abs(maxMotionY) < abs(float(yPositions[nid+1])-float(yPositions[nid])):
          maxMotionY = float(yPositions[nid+1])-float(yPositions[nid])

      if abs(maxMotionZ) < abs(float(zPositions[nid+1])-float(zPositions[nid])):
          maxMotionZ = float(zPositions[nid+1])-float(zPositions[nid])


    print 'maxMotionX : '+str(maxMotionX)
    print 'maxMotionY : '+str(maxMotionY)
    print 'maxMotionZ : '+str(maxMotionZ)

    return maxMotionX,maxMotionY,maxMotionZ

def calculate2DXYMotionForTimePoint(case,nid):

    # this function calculates euclidean distance of the centroid between the needle image t(nid) and the t(nid-1) image

    import string
    dir = getMotionDir(case)
    file = dir+'/motionsummary_centroid_label.txt'
    f = open(file, 'rb')

    xPositions = []
    yPositions = []


    # read x,y,z motion positions
    for line in f:
        line = line.rstrip('\n')
        splitted=string.split(str(line),',')
        xPositions.append(splitted[3])
        yPositions.append(splitted[4])

    print 'x positions : '
    print xPositions

    print 'y positions : '
    print yPositions


    if nid == getNeedleImageIDs(getCaseDir(case))[0]:

        print 'if case entered'

        [x_1,y_1,z_1] = ReadInitialFiducial('/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/targets/Case'+str(case)+'/centroid_label.fcsv')
        x_2 = xPositions[0]
        y_2 = yPositions[0]

        print 'nid : '+str(nid)
        print 'x_1 :' +str(x_1)
        print 'y_1 :' +str(y_1)
        print 'x_2 :' +str(x_2)
        print 'y_2 :' +str(y_2)
        print 'distance : '+str(getEuclidian2D(float(x_1),float(y_1),float(x_2),float(y_2)))

        return getEuclidian2D(float(x_1),float(y_1),float(x_2),float(y_2))

    else:

        print 'nid : '+str(nid)

        print 'array_position x1 : ' +str(int(getArrayPosFromNid(case,nid))-1)
        print 'array_position x2 : ' +str(int(getArrayPosFromNid(case,nid)))

        x_1 = xPositions[int(getArrayPosFromNid(case,nid))-1]
        y_1 = yPositions[int(getArrayPosFromNid(case,nid))-1]
        x_2 = xPositions[int(getArrayPosFromNid(case,nid))]
        y_2 = yPositions[int(getArrayPosFromNid(case,nid))]

        print 'x_1 :' +str(x_1)
        print 'y_1 :' +str(y_1)
        print 'x_2 :' +str(x_2)
        print 'y_2 :' +str(y_2)
        print 'distance : '+str(getEuclidian2D(float(x_1),float(y_1),float(x_2),float(y_2)))


        return getEuclidian2D(float(x_1),float(y_1),float(x_2),float(y_2))

    print 'something went wrong with calculate2DXYMotionForTimePoint'

def calculate2DXYMotionForTimePoint2(case,nid):

    # this function calculates euclidean distance of the centroid between the needle image t(nid) and the t(nid-1) image

    import string
    dir = getMotionDir(case)
    file = dir+'/motionsummary_centroid_label.txt'
    f = open(file, 'rb')

    xPositions = []
    yPositions = []


    # read x,y,z motion positions
    for line in f:
        line = line.rstrip('\n')
        splitted=string.split(str(line),',')
        xPositions.append(splitted[3])
        yPositions.append(splitted[4])

    print 'x positions : '
    print xPositions

    print 'y positions : '
    print yPositions


    if nid == getNeedleImageIDs(getCaseDir(case))[0]:

        print 'if case entered'

        [x_1,y_1,z_1] = ReadInitialFiducial('/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/targets/Case'+str(case)+'/centroid_label.fcsv')
        x_2 = xPositions[0]
        y_2 = yPositions[0]

        print 'nid : '+str(nid)
        print 'x_1 :' +str(x_1)
        print 'y_1 :' +str(y_1)
        print 'x_2 :' +str(x_2)
        print 'y_2 :' +str(y_2)
        print 'distance : '+str(getEuclidian2D(float(x_1),float(y_1),float(x_2),float(y_2)))

        #return getEuclidian2D(float(x_1),float(y_1),float(x_2),float(y_2))
        return 0.0

    else:

        print 'nid : '+str(nid)

        print 'array_position x1 : ' +str(int(getArrayPosFromNid(case,nid))-1)
        print 'array_position x2 : ' +str(int(getArrayPosFromNid(case,nid)))

        x_1 = xPositions[int(getArrayPosFromNid(case,nid))-1]
        y_1 = yPositions[int(getArrayPosFromNid(case,nid))-1]
        x_2 = xPositions[int(getArrayPosFromNid(case,nid))]
        y_2 = yPositions[int(getArrayPosFromNid(case,nid))]

        print 'x_1 :' +str(x_1)
        print 'y_1 :' +str(y_1)
        print 'x_2 :' +str(x_2)
        print 'y_2 :' +str(y_2)
        print 'distance : '+str(getEuclidian2D(float(x_1),float(y_1),float(x_2),float(y_2)))


        return getEuclidian2D(float(x_1),float(y_1),float(x_2),float(y_2))

    print 'something went wrong with calculate2DXYMotionForTimePoint'

def getArrayPosFromNid(case,nid):

  count = 0
  for i in getNeedleImageIDs(getCaseDir(case)):
      if i == nid:
          return count
      else:
          count = count+1


def plot2DMaxMotion(listOfCaseIDs):

    maxMotionX = []
    maxMotionY = []

    for case in listOfCaseIDs:
      x,y,z = calculateMaxMotionPerCase2DForCentroid(case)
      maxMotionX.append(x)
      maxMotionY.append(y)

    import matplotlib.pyplot as plt
    """
    plt.figure(5)
    plt.plot(maxMotionX,maxMotionY,'bo')
    rect = plt.figure(5)
    rect.set_facecolor('white')
    plt.xlabel('Left-Right Max Motion in mm')
    plt.ylabel('Up-Down Max Motion in mm')
    plt.show()
    """

    plt.figure(5)
    plt.hexbin(maxMotionX, maxMotionY, mincnt=1,gridsize=25,cmap=plt.cm.YlOrRd_r)
    rect = plt.figure(5)
    rect.set_facecolor('white')
    plt.xlim([-15,15])
    plt.ylim([-15,15])
    plt.xlabel('Left-Right Max Motion in mm')
    plt.ylabel('Up-Down Max Motion in mm')
    cb = plt.colorbar()
    plt.show()

def plotMotionAsAFunctionOfTime(listOfCaseIDs):


    # get x axis
    list_of_times_in_minutes = []
    list_of_distances = []

    for case in listOfCaseIDs:

      firstNeedleTime = float(ReadNeedleTime(case,getNeedleImageIDs(getCaseDir(case))[0]))
      # list_of_times_in_minutes.append(float(ReadInitialTime(case)-ReadInitialTime(case))) dont need x = 0
      for nid in getNeedleImageIDs(getCaseDir(case)):
        list_of_times_in_minutes.append(float(ReadNeedleTime(case,nid)-ReadInitialTime(case))/float(60.0))

      # get movement for timepoint t
      for nid in getNeedleImageIDs(getCaseDir(case)):
        list_of_distances.append(float(calculate2DXYMotionForTimePoint(case,nid)))


    print list_of_times_in_minutes
    print list_of_distances

    import matplotlib.pyplot as plt

    plt.figure(2)
    plt.plot(list_of_times_in_minutes,list_of_distances,'bo')
    rect = plt.figure(2)
    rect.set_facecolor('white')
    plt.xlabel('time in minutes')
    plt.ylabel('motion: euclidian 2D distance')
    plt.show()

def plotMotionAsAFunctionOfTimeFromFirstNeedleImage(listOfCaseIDs):


    # get x axis
    list_of_times_in_minutes = []
    list_of_distances = []

    for case in listOfCaseIDs:

      firstNeedleTime = float(ReadNeedleTime(case,getNeedleImageIDs(getCaseDir(case))[0]))
      # list_of_times_in_minutes.append(float(ReadInitialTime(case)-ReadInitialTime(case))) dont need x = 0
      for nid in getNeedleImageIDs(getCaseDir(case)):
        list_of_times_in_minutes.append(float(ReadNeedleTime(case,nid)-ReadInitialTime(case))/float(60.0))

      # get movement for timepoint t
      for nid in getNeedleImageIDs(getCaseDir(case)):
        list_of_distances.append(float(calculate2DXYMotionForTimePoint2(case,nid)))


    print list_of_times_in_minutes
    print list_of_distances

    import matplotlib.pyplot as plt

    plt.figure(2)
    plt.plot(list_of_times_in_minutes,list_of_distances,'bo')
    rect = plt.figure(2)
    rect.set_facecolor('white')
    plt.xlabel('time in minutes')
    plt.ylabel('motion: euclidian 2D distance')
    plt.show()

def getEuclidian2D(x1,y1,x2,y2):
    import math
    return math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))

def printListOfProstateVolumes(listOfCaseIDs):

    prostate_volumes = []

    for case in listOfCaseIDs:

        # GET PROSTATE SIZE in ml
        nids = getNeedleImageIDs(getCaseDir(case))

        for needleImgs in nids:
            caseDir = getCaseDir(case)
            print ReadNeedleTime(case,needleImgs)-ReadInitialTime(case)
            """
            movingImageID = getMovingImageID(caseDir)
            image = caseDir+str(movingImageID[0])+'-CoverProstate.nrrd'
            label = caseDir+str(movingImageID[0])+'-label.nrrd'
            size_in_mL = getLabelVolumeInMl(label,image)
            prostate_volumes.append(size_in_mL)
            print size_in_mL
            """


def deleteOldTransforms(dir):
    if dir:
        cmd = ("rm -rfv "+str(dir)+"/*")
        os.system(cmd)

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
configDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/configs'

numberOfCases = 300
listOfCaseIDs = []
ignoreCaseIDs = [4,5,7,8,52,60,69,72,101,142]

procedureTimesInSeconds = []

# get list of cases
listOfCaseIDs = getListOfCaseIDs(numberOfCases)

# ignore cases
listOfCaseIDs=list(set(listOfCaseIDs) - set(ignoreCaseIDs))
listOfCaseIDs = sorted(listOfCaseIDs)
listOfCaseIDs = [124]

print listOfCaseIDs

# testing:


createFolders()
list_of_columns = createListOfColumns()


################################
# RUN prostate motion calculation

# 0. create motion tracker points.py
cmd = ('python createTrackers.py ')
print ('about to run : '+cmd)
#os.system(cmd)

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

  # 0. Delete old transforms
  deleteOldTransforms(regDir)

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

  # 5. create Config for verification and snapshots
  makeConfig(case,caseDir,needleImageIds,regDir,resDir)

  # 6. createMotionSummary
  createMotionSummary2(case,motionDir,centroidDir,needleImageIds,list_of_columns)


# 0. make snapshots and GIFs
#cmd = ('python makeSnapshots.py ')
#print ('about to run : '+cmd)
#os.system(cmd)

# 7. Print Prostate Volumes for Excel
#printListOfProstateVolumes(listOfCaseIDs)

# 7. print Motion for Excel
#printListOfColumns(list_of_columns)

# 9. print Pelvis Motion
#printPelvisMotion(listOfCaseIDs)


#### DO THE ANALYSIS

#plotProstateVolumes(listOfCaseIDs)

#plotProcedureTime(listOfCaseIDs)

#plotNumberOfNeedleImagesPerCase(listOfCaseIDs)

#plotNumberOfNeedleImagesPerCase_withColomns(listOfCaseIDs)

#plot2DMaxMotion(listOfCaseIDs)

#plotMotionAsAFunctionOfTime(listOfCaseIDs)

#plotMotionAsAFunctionOfTimeFromFirstNeedleImage(listOfCaseIDs)
