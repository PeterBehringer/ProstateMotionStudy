import os
import shutil

dataDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Cases003-298_data/Case0'

for case in range(44,51,1):

    sourceDir = '/Users/peterbehringer/MyStudies/Segmentations-Cases11-50/Case'+str(case)+'-ManualSegmentations/CoverProstate-label.nrrd'
    destDir = dataDir+str(case)+'/IntraopImages'

    shutil.copy(sourceDir, destDir)

    print 'copied '+str(sourceDir)+' to : '+str(destDir)+'  !'