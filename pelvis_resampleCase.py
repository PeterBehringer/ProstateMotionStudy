import os, argparse, string, re, sys, glob
from time import time

resamplingCmd = "/Applications/Slicer.app/Contents/lib/Slicer-4.4/cli-modules/BRAINSResample"

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

parser = argparse.ArgumentParser(description="Run various registration experiments for a given case number")
parser.add_argument('case',help='case to be processed')
parser.add_argument('regdir',help='regdir')
parser.add_argument('IntraDir',help='IntraDir')
parser.add_argument('ResDir',help='ResDir')

args = parser.parse_args()

case = args.case
RegDir = args.regdir
IntraDir = args.IntraDir
ResDir = args.ResDir


try:
  os.mkdir(ResDir)
except:
  pass


#   list all needle image ids first
needleImageIds = []

needleImageIds = getNeedleImageIDs(IntraDir,needleImageIds)
# moving image/mask will always be the same
movingImage = IntraDir+'/CoverProstate.nrrd'

movingImageID=[]
movingImageID=getMovingImageID(IntraDir,movingImageID)
movingImage = IntraDir+'/'+str(movingImageID[0])+'-CoverProstate.nrrd'
if not os.path.isfile(movingImage):
    print 'coud not find moving image : '+str(movingImage)


# take latest croverprostate
movingMask = IntraDir+'/'+str(movingImageID[len(movingImageID)-1])+'-label.nrrd'
if not os.path.isfile(movingMask):
    print 'coud not find moving image : '+str(movingMask)



for nid in needleImageIds:
  bsplineTfm=None

  nidStr=str(nid)

  fixedImage = IntraDir+'/'+nidStr+'-Needle.nrrd'

  print 'regDir'
  print RegDir
  # check if there is a matching TG

  bsplineTfm = RegDir+'/'+nidStr+'-IntraIntra-Rigid-Attempt1.h5'

  initTfm = IntraDir+nidStr+"-init.h5"

  if os.path.isfile(initTfm):
    bsplineTfm = initTfm
  else:
    bsplineTfm = RegDir+'/'+nidStr+'-IntraIntra-Rigid-Attempt1.h5'


  print ' directory '
  print str(bsplineTfm)

  if not os.path.isfile(bsplineTfm):
    bsplineTfm = RegDir+'/'+nidStr+'-IntraIntra-Rigid-Attempt2.h5'
  if not os.path.isfile(bsplineTfm):
    print 'Failed to find ANY transform!'


  resampled = ResDir+'/'+nidStr+'-Rigid_resampled.nrrd'
  """
  if not IsBSplineTfmValid(bsplineTfm):
    print 'BSpline transform is not valid! Will skip needle image ',nid
    continue
  """

  BFResample(reference=fixedImage,moving=movingImage,tfm=bsplineTfm,output=resampled)
