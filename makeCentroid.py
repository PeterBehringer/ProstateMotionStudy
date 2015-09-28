import argparse

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


parser = argparse.ArgumentParser(description="asd")
parser.add_argument('case',help='case to be processed')
parser.add_argument('coverProstate',help='IntraDir to be processed')
parser.add_argument('RegDir',help='RegDir to be processed')
parser.add_argument('ResDir',help='ResDir to be processed')


args = parser.parse_args()
case = args.case
image = args.coverProstate

RegDir = args.RegDir
ResDir = args.ResDir
TempDir = args.TempDir


mask = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Cases003-298_data/Case011/IntraopImages/4-label.nrrd'
result = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Cases003-298_data/Case011/IntraopImages/CoverProstate-Centroid.fcsv'
image = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Cases003-298_data/Case011/IntraopImages/3-CoverProstate'




GetCentroid(mask,result)




