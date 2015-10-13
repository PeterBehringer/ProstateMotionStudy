import SimpleITK as sitk
import sys, os, glob, string

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

def getMovingImageID(IntraDir):
    movingImageID = []
    # returns list of Image ID's for case with dir intradir
    if os.path.isdir(IntraDir):
      listDir = os.listdir(IntraDir)
      for i in range(len(listDir)):
          if 'CoverProstate' in listDir[i]:
              movingImageID.append(int(string.split(listDir[i],'-')[0]))
    else:
      print 'there is no path like: '+str(IntraDir)
    return movingImageID

listOfCaseIDs = getListOfCaseIDs(300)
ignoreCaseIDs = [4,5,7,8,52,60,69,72,101,142,150,269,275,278,280,281,282,285,286,287,293]
listOfCaseIDs=list(set(listOfCaseIDs) - set(ignoreCaseIDs))


for case in listOfCaseIDs:

  labelList = []
  movingImageID = getMovingImageID(getCaseDir(case))
  print 'case = '+str(case)
  IntraDir = getCaseDir(case)
  fileList = os.listdir(IntraDir)

  for file in fileList:
      if 'label' in file:
          labelList.append(file)
      if 'TG' in file:
          labelList.append(file)

  # invert labels

  for label in labelList:

      inputLabel = sitk.ReadImage(IntraDir+'/'+str(label))
      outputLabel = IntraDir+'/'+str(label[:-5])+'-Pelvis.nrrd'

      changeFilter = sitk.ChangeLabelImageFilter()
      changeMap = sitk.DoubleDoubleMap()

      # get the label value

      stats = sitk.LabelShapeStatisticsImageFilter()
      stats.Execute(inputLabel)
      labels=stats.GetLabels()
      label = labels[0]

      changeMap[0] = 1
      changeMap[int(label)] = 0

      changedLabel = changeFilter.Execute(inputLabel, changeMap)
      sitk.WriteImage(changedLabel, outputLabel, True)

  print(str(case)+' done')
