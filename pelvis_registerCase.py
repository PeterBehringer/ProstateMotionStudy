import os, argparse, string, re, sys, glob
from time import time

registrationCmd = "/Applications/Slicer.app/Contents/lib/Slicer-4.4/cli-modules/BRAINSFit"
resamplingCmd = "/Applications/Slicer.app/Contents/lib/Slicer-4.4/cli-modules/BRAINSResample"

def BFRegister(fixed=None,moving=None,fixedMask=None,movingMask=None,rigidTfm=None,affineTfm=None,bsplineTfm=None,initializer=None,log=None,initTfm=None,initialTfm=None):
  CMD=registrationCmd+" --fixedVolume "+fixed+" --movingVolume "+moving+" --numberOfThreads -1 --maskProcessingMode ROI"

  if fixedMask:
    CMD = CMD+" --fixedBinaryVolume "+fixedMask
  if movingMask:
    CMD = CMD+" --movingBinaryVolume "+movingMask
  if initializer:
    CMD = CMD+" "+initializer
  if initTfm:
    CMD = CMD+' --initialTransform '+initTfm
  if bsplineTfm:
    CMD = CMD+" --useROIBSpline --useBSpline --splineGridSize 3,3,3 --outputTransform "+bsplineTfm+" --useScaleVersor3D --useScaleSkewVersor3D --numberOfIterations 1500 --outputVolumePixelType float --backgroundFillValue 0 --interpolationMode Linear --minimumStepLength 0.005 --translationScale 5000 --reproportionScale 1 --skewScale 1 --fixedVolumeTimeIndex 0 --movingVolumeTimeIndex 0 --medianFilterSize 0,0,0 --ROIAutoDilateSize 0 --relaxationFactor 0.5 --maximumStepLength 0.2 --failureExitCode -1 --costFunctionConvergenceFactor 1.00E+09 --projectedGradientTolerance 1.0E-05 --maxBSplineDisplacement 0 --maximumNumberOfEvaluations 900 --maximumNumberOfCorrections 25  --removeIntensityOutliers 0 --ROIAutoClosingSize 9"
  if rigidTfm:
    CMD = CMD+" --useRigid --minimumStepLength 0.005"
  if rigidTfm and not bsplineTfm:
    CMD = CMD+" --outputTransform "+rigidTfm
  if affineTfm:
    CMD = CMD+" --useAffine --outputTransform "+affineTfm
  if fixedMask and movingMask and bsplineTfm and not initTfm:
    # B SPLINE TRANSFORM WITH MASKS
    CMD = CMD+' --initializeTransformMode useCenterOfROIAlign'
    # additional params here
    print ('went into additional params for bspline')
    CMD = CMD +' --samplingPercentage 0.002 --maskInferiorCutOffFromCenter 1000 --numberOfHistogramBins 50 --numberOfMatchPoints 10 --metricSamplingStrategy Random --costMetric MMI'
  if fixedMask and movingMask and rigidTfm and not bsplineTfm and not initTfm:
    # RIGID TRANSFORM WITH MASKS
    CMD = CMD+' --initializeTransformMode useCenterOfROIAlign'
    # additional params here
    print ('went into additional params for rigid1111')
  if fixedMask and movingMask and affineTfm and not bsplineTfm and not initTfm:
    # AFFINE TRANSFORM WITH MASKS
    CMD = CMD+' --initializeTransformMode useCenterOfROIAlign'
    # additional params here
    print ('went into additional params for affine')
  if initialTfm and not initializer:
    CMD = CMD+' --initialTransform '+initialTfm

  print "About to run ",CMD

  if log:
    CMD = CMD+" | tee "+log

  ret = os.system(CMD)
  if ret:
    exit()

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

def dilateMask(inputPATH,outputPATH):

  import SimpleITK as sitk

  image_input=sitk.ReadImage(inputPATH)

  grayscale_dilate_filter = sitk.GrayscaleDilateImageFilter()
  grayscale_dilate_filter.SetKernelRadius([12,12,0])
  grayscale_dilate_filter.SetKernelType(sitk.sitkBall)

  image_output = grayscale_dilate_filter.Execute(image_input)
  sitk.WriteImage(image_output,outputPATH)

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

parser = argparse.ArgumentParser(description="Run various registration experiments for a given case number")
parser.add_argument('case',help='case to be processed')
parser.add_argument('--needle',help='needle confirmation image to register')
parser.add_argument('intraDir',help='intraDir')
parser.add_argument('regDir',help='regDir')
parser.add_argument('tempDir',help='tempDir')

args = parser.parse_args()

case = args.case
needleReq = args.needle
IntraDir = args.intraDir
RegDir = args.regDir
TempDir = args.tempDir

try:
  os.makedirs(TempDir)
  os.makedirs(RegDir)
  os.makedirs(TempDir)
except:
  pass

# 1. run preop/intraop registration

# 2. for each needle image, run intraop/intraop registration using different
# registration modes

#   list all needle image ids first

needleImageIds = []
needleImageIds = getNeedleImageIDs(IntraDir,needleImageIds)
print needleImageIds


# moving image/mask will always be the same

movingImageID=[]
movingImageID=getMovingImageID(IntraDir,movingImageID)
movingImage = IntraDir+str(movingImageID[0])+'-CoverProstate.nrrd'
print 'movingImage = ' + str(movingImage)
if not os.path.isfile(movingImage):
    print 'coud not find moving image : '+str(movingImage)


# take latest croverprostate
movingMask = IntraDir+str(movingImageID[len(movingImageID)-1])+'-label-Pelvis.nrrd'
if not os.path.isfile(movingMask):
    print 'coud not find moving image : '+str(movingMask)


latestRigidTfm = '/Users/peterbehringer/MyStudies/InitialTransforms/Identity.h5'
latestMovingMask = movingMask

# try to read the registration log

if not os.path.isfile(str(RegDir+case+'_registration_times.log')):
    try:
      os.makedirs(str(RegDir+case))
    except:
      pass
    cmd = ('touch '+ str(RegDir+case+'_registration_times.log'))
    print cmd
    os.system(cmd)

regTimesLog = open(RegDir+case+'_registration_times.log','a+')


for nid in needleImageIds:
  success = False
  rigidTfm = None
  affineTfm = None
  bsplineTfm = None
  attempt = ''

  nidStr=str(nid)

  fixedImage = IntraDir+nidStr+'-Needle.nrrd'

  log = RegDir+nidStr+'_registration.log'

  # check if there is a matching TG
  fixedMask = IntraDir+nidStr+'-TG-Pelvis.nrrd'
  #fixedMask = '/Users/peterbehringer/MyTesting/ProjectWeek15/Data/masks/15_15-Resampled-label.nrrd'
  #fixedMask = '/Users/peterbehringer/MyTesting/ProjectWeek15/Data/TempDir/15_15-Resampled-CoverProstate-TG.nrrd'
  #fixedMask2 = '/Users/peterbehringer/MyTesting/ProjectWeek15/Data/masks/15_12-Resampled-CoverProstate-TG_bigger_mask_without_cutting.nrrd'
  #fixedMask2 = '/Users/peterbehringer/MyTesting/ProjectWeek15/Data/masks/25_8-Resampled-CoverProstate-TG_bigger.nrrd'
  #fixedMask2 = '/Users/peterbehringer/MyTesting/ProjectWeek15/Data/TempDir/15_18-Dilated_Resampled-CoverProstate-TG.nrrd'


  if not os.path.isfile(fixedMask):
    bsplineTfm = RegDir+nidStr+'-IntraIntra-BSpline-Attempt1.h5'
    rigidTfm = RegDir+nidStr+'-IntraIntra-Rigid-Attempt1.h5'
    affineTfm = RegDir+nidStr+'-IntraIntra-Affine-Attempt1.h5'
    fixedMask = TempDir+'/'+str(case)+'_'+nidStr+'-Resampled-'+string.split(latestMovingMask,'/')[-1]
    fixedMask_dilated = TempDir+'/'+str(case)+'_'+nidStr+'-Dilated_Resampled-'+string.split(latestMovingMask,'/')[-1]
    print ('DEBUG: FIXED IMAGE')
    print fixedImage
    print ('DEBUG: LATEST MOVING MASK')
    print latestMovingMask
    print ('DEBUG: LATEST RIGID TFM')
    print latestRigidTfm
    print ('DEBUG: FIXED MASK')
    print fixedMask
    BFResample(reference=fixedImage,moving=latestMovingMask,tfm=latestRigidTfm,output=fixedMask,interp='NearestNeighbor')
    # since we have only one mask, we cannot use a smarter initialization procedure
    startTime = time()
    # rigid
    print IntraDir
    initTfm = IntraDir+nidStr+'-init.h5'

    if os.path.isfile(initTfm):
       BFRegister(fixed=fixedImage,moving=movingImage,fixedMask=fixedMask,rigidTfm=rigidTfm,log=log,initialTfm=latestRigidTfm,initTfm=initTfm)
    else:
       BFRegister(fixed=fixedImage,moving=movingImage,fixedMask=fixedMask,rigidTfm=rigidTfm,log=log,initialTfm=latestRigidTfm)

    # create bigger mask
    #dilateMask(fixedMask,fixedMask_dilated)

    # bspline
    #BFRegister(fixed=fixedImage,moving=movingImage,fixedMask=fixedMask_dilated,bsplineTfm=bsplineTfm,log=log,initialTfm=rigidTfm)
    print 'latest BSpline transform path in not else case: '+str(bsplineTfm)

    endTime = time()
    attempt='Attempt1'
  else:
    print 'mask case entered'

    print 'ENTERED MASK EXIST CASE'
    bsplineTfm = RegDir+'/'+nidStr+'-IntraIntra-BSpline-Attempt2.h5'
    rigidTfm = RegDir+'/'+nidStr+'-IntraIntra-Rigid-Attempt2.h5'
    affineTfm = RegDir+'/'+nidStr+'-IntraIntra-Affine-Attempt2.h5'
    initTfm = IntraDir+nidStr+'-init.h5'
    startTime = time()
    # rigid
    print ('fixed Mask = '+fixedMask)
    if os.path.isfile(initTfm):
       BFRegister(fixed=fixedImage,moving=movingImage,fixedMask=fixedMask,rigidTfm=rigidTfm,log=log,initialTfm=latestRigidTfm,initTfm=initTfm)
    else:
       BFRegister(fixed=fixedImage,moving=movingImage,fixedMask=fixedMask,rigidTfm=rigidTfm,log=log,initialTfm=latestRigidTfm)
    # affine
    # BFRegister(fixed=fixedImage,moving=movingImage,movingMask=movingMask,fixedMask=fixedMask,affineTfm=affineTfm,log=log)
    # bspline
    print 'latest BSpline transform path in else case BEFORE RUNNING the BSPLINE: '+str(bsplineTfm)
    #BFRegister(fixed=fixedImage,moving=movingImage,movingMask=movingMask,fixedMask=fixedMask,bsplineTfm=bsplineTfm,log=log,initialTfm=rigidTfm)
    # BFRegister(fixed=fixedImage,moving=movingImage,movingMask=movingMask,fixedMask=fixedMask,rigidTfm=rigidTfm,bsplineTfm=bsplineTfm,log=log,initTfm=initTfm)
    print 'latest BSpline transform path in else case: '+str(bsplineTfm)
    endTime = time()
    attempt='Attempt1'

  print ('DEBUG: latestRigidTfm')
  print rigidTfm
  if os.path.isfile(initTfm):
    latestRigidTfm = initTfm
  else:
    latestRigidTfm = rigidTfm
  """
  success = success or IsBSplineTfmValid(bsplineTfm)
  if not success:
    print 'Processing failed for needle image ',nid
    exit()
  """
  regTimesLog.write(str(case)+';'+str(nid)+';'+attempt+';'+str(endTime-startTime)+';')