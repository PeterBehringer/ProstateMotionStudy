import os

# this function returns prostate motion tracker points of a given mask

def makeTrackerPoints(case,mask):


  targetDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Cases003-298_data/targets/Case13/output.nrrd'

  try:
    os.makedirs(targetDir)
  except:
    pass


  import SimpleITK as sitk

  mask=sitk.ReadImage(mask)

  print str(14)
  zslice = int(14)
  size = list( mask.GetSize() )
  print size
  zspacing = mask.GetSpacing()
  print zspacing
  #print size
  size[2] = 0
  origin = [0,0,0]
  origin = mask.GetOrigin()
  print 'origin = ' +str(origin)


  stats = sitk.LabelShapeStatisticsImageFilter()
  stats.Execute(mask)
  labelID=stats.GetLabels()[0]
  slicesWithLabel=[]

  for slice in range(0,mask.GetSize()[2]):

    print int(slice)
    zslice = slice

    index = [ 0, 0, zslice ]

    Extractor = sitk.ExtractImageFilter()
    Extractor.SetSize( size )
    Extractor.SetIndex( index )

    stats = sitk.LabelShapeStatisticsImageFilter()
    stats.Execute(Extractor.Execute(mask))

    if stats.HasLabel(labelID):
      print 'found z slice with label, its : '+str(zslice)
      slicesWithLabel.append(slice)

  firstSlice=min(slicesWithLabel)
  lastSlice=max(slicesWithLabel)

  print 'first slice : ' +str(firstSlice)
  print 'last slice : ' +str(lastSlice)

  #extract first slice:
  mask=sitk.ReadImage(maskDir)
  Extractor = sitk.ExtractImageFilter()
  size =  (320,320,0)
  print 'SIZE = ' +str(size)
  Extractor.SetSize( size)
  Extractor.SetIndex( [0,0,10])
  sitk.WriteImage( Extractor.Execute( mask), 'asdfirstSlice1.nrrd')

  """
  cmd = 'touch '+str(result)
  f = open(str(result), 'w')
  f.write(str(stats.GetCentroid(labels[0])))
  """

maskDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Cases003-298_data/Case013/IntraopImages/4-label.nrrd'
result = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/scripts/target.fcsv'

makeTrackerPoints(12,maskDir)

"""
  size = list(mask.GetSize())
  index = mask.GetDimension()


  print 'size : '+str(size[0])+'   '+str(size[1])+'   '+str(size[2])

  print 'index : '+str(size[0])+'   '+str(size[1])+'   '+str(size[2])

  Extractor = sitk.ExtractImageFilter()

  Extractor.SetIndex( index )
  Extractor.SetSize(size)

  sitk.WriteImage( Extractor.Execute( mask ), 'asd000.nrrd' )

"""
"""
  for index in range(0,30):
    print str(index)
    zslice = int(index)
    size = list( mask.GetSize() )
    #print size
    size[2] = 0
    origin = [0,0,0]
    origin = mask.GetOrigin()
    #print origin

    index = [ 0, 0, zslice  ]

    Extractor = sitk.ExtractImageFilter()
    Extractor.SetSize( size )
    Extractor.SetIndex( index )

    stats = sitk.LabelShapeStatisticsImageFilter()
    stats.Execute(mask)
    labels=stats.GetLabels()
    print stats.GetCentroid(labels[0])

    sitk.WriteImage( Extractor.Execute( mask), 'try_.nrrd')

    #image = sitk.ReadImage('/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/scripts/try_.nrrd')
    #origin2=[0,0,0]
    #origin2 = image.GetOrigin()
    #print origin2
    #break

  return True
"""