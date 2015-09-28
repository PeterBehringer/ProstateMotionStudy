import os, argparse, string, re, sys, glob
import ConfigParser as conf
from time import time

parser = argparse.ArgumentParser(description="Prepare configuration file for Slicer VisAIRe module")
parser.add_argument('case',help='case to be processed')
parser.add_argument('IntraDir',help='IntraDir to be processed')
parser.add_argument('RegDir',help='RegDir to be processed')
parser.add_argument('ResDir',help='ResDir to be processed')


args = parser.parse_args()
case = args.case
IntraDir = args.IntraDir
RegDir = args.RegDir
ResDir = args.ResDir

ResDir='/Users/peterbehringer/MyStudies/Verification/Case'+case
IntraDir = '/Users/peterbehringer/MyStudies/Data/Case'+case+'/IntraopImages'
RegDir='/Users/peterbehringer/MyStudies/Data/Case'+case+'/Slicer4registration'
ResDir='/Users/peterbehringer/MyStudies/Verification/Case'+case
try:
  os.system('mkdir '+ResDir)
except:
  pass
SegDir='/Users/peterbehringer/MyStudies/Segmentations-Cases11-50/Case'+case+'-ManualSegmentations'


#   list all needle image ids first
needleImageIds = []
segImageIds = []
needleImages = glob.glob(IntraDir+'/[0-9]*nrrd')
for ni in needleImages:
  fname = string.split(ni,'/')[-1]
  #if string.find(fname,'TG') == -1:
  # keep only those images that look like 10.nrrd
  if re.match('\d+\.nrrd',fname):
    needleImageIds.append(int(string.split(fname,'.')[0]))
    #if os.path.exists(IntraDir+'/'+int(needleImageIds[-1])+'-label.nrrd'):
    #  segImageIds.append(needleImageIds[-1])
needleImageIds.sort()


cf = conf.SafeConfigParser()
cf.optionxform = str
cfFileName = '/Users/peterbehringer/MyStudies/Verification/Case'+case+'_VisAIRe.ini'
try:
  cmd = ('touch '+str(cfFileName))
  os.system(cmd)
except:
  pass

cfFile = open(cfFileName,'w')

# moving image/mask will always be the same
movingImage = IntraDir+'/CoverProstate.nrrd'
segImage = SegDir+'/CoverProstate-label.nrrd'

cf.add_section('MovingData')
cf.set('MovingData','ImagesPath',IntraDir)
cf.set('MovingData','SegmentationsPath',SegDir)
cf.set('MovingData','Image',os.path.abspath(movingImage))
cf.set('MovingData','Segmentation',os.path.abspath(segImage))

cf.add_section('FixedData')
cf.set('FixedData','ImagesPath',IntraDir)

for nid in needleImageIds:
  nidStr=str(nid)
  cf.set('FixedData','Image'+nidStr,os.path.join(os.path.abspath(IntraDir),nidStr+'.nrrd'))

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
cf.set('Info','CaseName','BxCase'+case)

cf.write(cfFile)
cfFile.close()

print 'Config file saved as ',cfFileName
