import os, argparse, string, re, sys, glob
from time import time

def BFResample(reference,moving,tfm,output,interp='Linear'):
  CMD = 'Slicer3 --launch BRAINSResample --referenceVolume '+reference+' --inputVolume '+moving+' --outputVolume '+output+' --warpTransform '+tfm
  CMD = CMD + ' --interpolationMode '+interp
  ret = os.system(CMD)
  if ret:
    exit()

def IsBSplineTfmValid(tfm):
  f=open(tfm,'r')
  nTransforms = 0
  for l in f:
    if string.find(l,'# Transform') != -1:
      nTransforms = nTransforms+1
  return nTransforms == 2

def TransformFiducials(ref, mov, fidIn, tfmIn, fidOut):

 CMD="~/bitbucket/SlicerCLITools-build/TransformFiducialList --referenceimage "+ref+" --movingimage "+mov+" --fiducialsfile "+fidIn+" --inputtransform "+tfmIn+" --outputfile "+fidOut
 print CMD
  
 ret = os.system(CMD)
 if ret:
   exit()

 '''
 Case11/IntraopImages/10.nrrd --movingimage
 Case11/IntraopImages/CoverProstate.nrrd --fiducialsfile
 Case11/IntraopImages/CoverProstate-Centroid.fcsv --inputtransform
 Case11/Registration2attempts/10-IntraIntra-BSpline-Attempt1.tfm --outputfile
 Case11/Registration2attempts/10_CoverProstate-Centroid.fcsv
 '''
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

  dir='/Users/peterbehringer/MyStudies/Data/cases11-50_Data/Data/Case'+case+'/CoverProstate'
  subdir = os.listdir(dir)[0]
  print ('subdir = '+subdir)
  # kick out .DS_Store
  if "Store" in subdir:
    subdir=os.listdir(dir)[1]
  file=dir+'/'+subdir+'/timestamp'
  f=open(file,'r')
  return tm2sec(f.read())


def ReadNeedleTime(case,nid):
  file='/Users/peterbehringer/MyStudies/Data/cases11-50_Data/Data/Case'+case+'/NeedleConfirmation/'+str(nid)+'/timestamp'
  f=open(file,'r')
  return tm2sec(f.read())

def ReadFiducial(fname):

  if 'CoverProstate' in fname:
    # andriys code
    f = open(fname, 'r')
    l = f.read()
    i = l.split(',')
    print 'i[1]'
    print [float(i[1])]
    print 'i[2]'
    print [float(i[2])]
    print 'i[3]'
    print [float(i[3])]
    return [float(i[1]),float(i[2]),float(i[3])]

  else:
    print 'fname',fname
    f = open(fname, 'r')
    # ignore line 1-8
    l = f.readlines()[8:]
    print 'l = ',str(l)
    number_of_fids=len(l)
    print ('amount of fids : '+str(number_of_fids))
    import string
    splitted=string.split(str(l),',')
    chunks=[splitted[x:x+6] for x in xrange(0, number_of_fids*6, 6)]
    fiducials=[]
    for i in range(0,1):
        # print ('fiducialPoint = '+str(chunks[i][1:4]))
        fiducials.append(chunks[i][1:4])
    return [float(fiducials[0][0]),float(fiducials[0][1]),float(fiducials[0][2])]


parser = argparse.ArgumentParser(description="Prepare configuration file for Slicer VisAIRe module")
parser.add_argument('case',help='case to be processed')
parser.add_argument('IntraDir',help='IntraDir to be processed')
parser.add_argument('RegDir',help='RegDir to be processed')
parser.add_argument('ResDir',help='ResDir to be processed')
parser.add_argument('TempDir',help='TempDir to be processed')

args = parser.parse_args()
case = args.case
IntraDir = args.IntraDir
RegDir = args.RegDir
ResDir = args.ResDir
TempDir = args.TempDir


try:
  os.mkdir(ResDir)
except:
  pass

initialPosition = ReadFiducial(IntraDir+'/CoverProstate-Centroid.fcsv')
initialTime = ReadInitialTime(case)
# print 'Initial time: ',initialTime

#   list all needle image ids first
needleImageIds = []
needleImages = glob.glob(IntraDir+'/[0-9]*nrrd')
for ni in needleImages:
  fname = string.split(ni,'/')[-1]
  #if string.find(fname,'TG') == -1:
  # keep only those images that look like 10.nrrd
  if re.match('\d+\.nrrd',fname):
    needleImageIds.append(int(string.split(fname,'.')[0]))
needleImageIds.sort()
print ('needle Image IDs')
print needleImageIds

summary=[]
cmd=('touch '+ResDir+'/summary_glandMotion.txt')
os.system(cmd)
f = open(ResDir+'/summary_glandMotion.txt', 'w')
f.write('case,nid,nidTime-initialTime,nidPosition[0]-initialPosition[0],nidPosition[1]-initialPosition[1],nidPosition[2]-initialPosition[2]')
for nid in needleImageIds:
  nidTime = ReadNeedleTime(case,nid)
  # print 'Needle time: ',nidTime

  # resampled = ResDir+'/'+str(nid)+'-BSplineRegistered-targets.fcsv'

  resampled = ResDir+'/'+str(nid)+'-BSplineRegistered-centroid.fcsv'
  print ('resampled = '+str(resampled))
  nidPosition = ReadFiducial(resampled)
  print case,',',nid,',',nidTime-initialTime,',',abs(nidPosition[0]-initialPosition[0]),', ',abs(nidPosition[1]-initialPosition[1]),', ',abs(nidPosition[2]-initialPosition[2])
  print 'nidPosition[0]'+str(nidPosition[0])
  print 'initialPosition[0]'+str(initialPosition[0])

  summary.append([case,nid,nidTime-initialTime,abs(nidPosition[0]-initialPosition[0]),abs(nidPosition[1]-initialPosition[1]),abs(nidPosition[2]-initialPosition[2])])
  f.write("\n"+str(case)+','+str(nid)+','+str(nidTime-initialTime)+','+str(abs(nidPosition[0]-initialPosition[0]))+', '+str(abs(nidPosition[1]-initialPosition[1]))+', '+str(abs(nidPosition[2]-initialPosition[2])))
  # BFResample(reference=fixedImage,moving=movingImage,tfm=bsplineTfm,output=resampled)

f.write("\n"+"_____________________________________")

print summary

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

print avgX
print avgY
print avgZ

f.write("\n"+str(case)+', '+str(avgX)+', '+str(avgY) + ', ' +str(avgZ))