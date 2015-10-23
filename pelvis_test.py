import os


def transformFiducialsBRAINS(fidIn,tfmIn,fidOut):
  CMD='/Users/peterbehringer/MyProjects/BRAINSTools/BRAINSTools-build/bin/BRAINSConstellationLandmarksTransform -i '+fidIn+' -t '+tfmIn+' -o '+fidOut
  print 'about to run : '+CMD

  ret = os.system(CMD)
  if ret:
   exit()



fidIn = '/Applications/F.fcsv'
tfmIn = '/Applications/tfm.h5'
fidOut = '/Applications/F-transformed.fcsv'

transformFiducialsBRAINS(fidIn,tfmIn,fidOut)