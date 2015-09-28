import os, argparse, string, re, sys, glob
from time import time


def BFResample(reference,moving,tfm,output,interp='Linear'):
  CMD = resamplingCmd+' --referenceVolume '+reference+' --inputVolume '+moving+' --outputVolume '+output+' --warpTransform '+tfm
  CMD = CMD + ' --interpolationMode '+interp
  ret = os.system(CMD)
  if ret:
    exit()

def IsBSplineTfmValid(tfm):
  import h5py
  f=h5py.File(tfm,'r')
  transformType=f["TransformGroup/2/TransformType"]
  type=transformType[:]
  typeStr=str(type)
  if 'BSplineTransform' in typeStr:
    return True

def getMovingImageID(IntraDir,movingImageID):
    # returns list of Image ID's for case with dir intradir
    if os.path.isdir(IntraDir):
      listDir = os.listdir(IntraDir)
      for i in range(len(listDir)):
          if 'CoverProstate' in listDir[i]:
              movingImageID.append(int(string.split(listDir[i],'-')[0]))
    else:
      print 'there is no path like: '+str(IntraDir)
    return movingImageID

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

caselist = [38,43,52,60,69,72]
for case in caselist:

    IntraDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Cases003-298_data/Case0'+str(case)+'/IntraopImages/'


    #   list all needle image ids first
    needleImageIds = []
    needleImageIds = getNeedleImageIDs(IntraDir,needleImageIds)
    print needleImageIds

    for nid in needleImageIds:

     # grab file
        timeStampDir = '/Users/peterbehringer/MyStudies/Data/cases11-50_Data/Data/Case'+str(case)+'/NeedleConfirmation/'+str(nid)+'/timestamp'
        destDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Cases003-298_data/Case0'+str(case)+'/IntraopImages/'+str(nid)+'.timestamp'
        if os.path.isfile(timeStampDir):
          print timeStampDir
          import shutil
          shutil.copy2(timeStampDir, destDir)
          print 'successfully copied timestamp '+str(timeStampDir)+' to '+str(destDir)

        else:
          print 'count not found '+str(timeStampDir)
          exit()