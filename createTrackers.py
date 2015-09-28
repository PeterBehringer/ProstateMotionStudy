import os
import SimpleITK as sitk

# this function returns prostate motion tracker points of a given mask

def extractSlice(image,zslice,result):

  inputImage = sitk.ReadImage( image)
  size = list( inputImage.GetSize() )
  size[2] = 0
  index = [ 0, 0, zslice  ]
  Extractor = sitk.ExtractImageFilter()
  Extractor.SetSize( size )
  Extractor.SetIndex( index )
  sitk.WriteImage( Extractor.Execute( inputImage ), result )

def findFirstAndLastLabelSlices(mask,labelID):

  inputImage = sitk.ReadImage( mask)
  slicesWithLabel=[]
  for slice in range(0,inputImage.GetSize()[2]):

      size = list( inputImage.GetSize() )
      size[2] = 0
      zslice = slice
      index = [ 0, 0, zslice ]
      zSpacing =  inputImage.GetSpacing()[2]

      #print inputImage.GetDepth()
      #print inputImage.GetOrigin()
      #print inputImage.GetOrigin()[2]
      #print inputImage.GetOrigin()[2]+zslice*zSpacing
      #print '____________'

      Extractor = sitk.ExtractImageFilter()
      Extractor.SetSize( size )
      Extractor.SetIndex( index )

      stats = sitk.LabelShapeStatisticsImageFilter()
      stats.Execute(Extractor.Execute(inputImage))

      if stats.HasLabel(labelID):
        #print 'found z slice with label, its : '+str(zslice)
        slicesWithLabel.append(slice)

  first=min(slicesWithLabel)
  last=max(slicesWithLabel)
  return first,last

def getLabelID(label):

  stats = sitk.LabelShapeStatisticsImageFilter()
  stats.Execute(sitk.ReadImage(label))
  labelID=stats.GetLabels()[0]
  return labelID


def writeCentroid(name,coords,dir):

    cmd = 'touch '+str(dir)
    os.system(cmd)
    f = open(str(dir), 'w')
    f.write(str(name)+','+str(coords[0])+','+str(coords[1])+','+str(coords[2]))


def getCentroid(mask,labelID,zslice):

  import SimpleITK as sitk

  # get centroid
  mask=sitk.ReadImage(mask)
  stats = sitk.LabelShapeStatisticsImageFilter()
  stats.Execute(mask)
  labels=stats.GetLabels()
  centroid = [0,0,0]
  centroid[0] = -stats.GetCentroid(labels[0])[0]
  centroid[1] = -stats.GetCentroid(labels[0])[1]
  zorigin = sitk.ReadImage(maskDir).GetOrigin()[2]
  zspacing=sitk.ReadImage(maskDir).GetSpacing()[2]
  centroid[2] = zorigin+zslice*zspacing

  return centroid

def getBoundingBox(mask,labelID):

  stats = sitk.LabelShapeStatisticsImageFilter()
  stats.Execute(sitk.ReadImage(mask))
  bounding_box = stats.GetBoundingBox(labelID)

  return bounding_box


maskDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Cases003-298_data/Case013/IntraopImages/4-label.nrrd'
imageDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Cases003-298_data/Case013/IntraopImages/4-CoverProstate.nrrd'
result1 = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/scripts/first_slice.nrrd'
result2 = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/scripts/last_slice.nrrd'
midSliceDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/scripts/mid_slice.nrrd'

centroid1Dir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/scripts/centroid_1.fcsv'
centroid2Dir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/scripts/centroid_2.fcsv'

first,last=findFirstAndLastLabelSlices(maskDir,getLabelID(maskDir))

print first
print last

extractSlice(maskDir,first,result1)
extractSlice(maskDir,last,result2)

centroid1 = getCentroid(result1,getLabelID(maskDir),first)
centroid2 = getCentroid(result2,getLabelID(maskDir),last)

print centroid1
print centroid2

writeCentroid('centroid_apex',centroid1,centroid1Dir)
writeCentroid('centroid_base',centroid2,centroid2Dir)

midSlice = int(last-first/2)

extractSlice(maskDir,midSlice,midSliceDir)

boundingBox = getBoundingBox(maskDir,getLabelID(midSliceDir))
print boundingBox
upper_left = (boundingBox[0],boundingBox[1])
down_right = (boundingBox[0]+boundingBox[3],boundingBox[1]+boundingBox[4])
print "upper_left"
print upper_left
print "down_right"
print down_right

half_x_position = (down_right[0]-upper_left[0])/2+upper_left[0]
print half_x_position

half_y_position = (down_right[1]-upper_left[1])/2+upper_left[1]
print half_y_position

print '_______________'

image=sitk.ReadImage(maskDir)

points_vertical = down_right[1] - upper_left[1]
print points_vertical

points_horizontal = down_right[0] - upper_left[0]

# find vertical fiducials

points_on_label_vertical = []
points_on_label_horizontal = []

for ypixel in range(upper_left[1],down_right[1]):

    # search for points up to down

    x = half_x_position
    y = ypixel
    z = midSlice

    if image.GetPixel(x,y,z) != 0:
        points_on_label_vertical.append((x,y,z))

for xpixel in range(upper_left[0],down_right[0]):

    # search for points left to right

    x = xpixel
    y = half_y_position
    z = midSlice

    if image.GetPixel(x,y,z) != 0:
        points_on_label_horizontal.append((x,y,z))
        print (x,y,z)

midgland_superior = points_on_label_vertical[0]
midgland_inferior = points_on_label_vertical[len(points_on_label_vertical)-1]
midgland_left = points_on_label_horizontal[0]
midgland_right = points_on_label_horizontal[len(points_on_label_horizontal)-1]

print midgland_superior
print midgland_inferior
print midgland_left
print midgland_right


def convertPointFromIJKtoRAS(coords,originalImage):

    # convert (i,j,k) to RAS

    # spacing and origin is taken from original Image
    image=sitk.ReadImage(originalImage)
    origin=image.GetOrigin()
    spacing = image.GetSpacing()
    print origin
    print spacing

    xOrigin=origin[0]
    yOrigin=origin[1]
    zOrigin=origin[2]

    xSpacing=spacing[0]
    ySpacing=spacing[1]
    zSpacing=spacing[2]

    print 'coords : '
    print coords[0]
    print coords[1]
    print coords[2]
    print '_________'

    xRAS=-1*(xOrigin+coords[0]*xSpacing)
    yRAS=-1*(yOrigin+coords[1]*ySpacing)
    zRAS=zOrigin+midSlice*zSpacing

    print 'xRAS : '+str(xRAS)
    print 'yRAS : '+str(yRAS)
    print 'zRAS : '+str(zRAS)

    return [xRAS,yRAS,zRAS]


pp1=convertPointFromIJKtoRAS(midgland_inferior,imageDir)
pp2=convertPointFromIJKtoRAS(midgland_superior,imageDir)
pp3=convertPointFromIJKtoRAS(midgland_right,imageDir)
pp4=convertPointFromIJKtoRAS(midgland_left,imageDir)

centroid3Dir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/scripts/midgland_inferior.fcsv'
centroid4Dir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/scripts/midgland_superior.fcsv'
centroid5Dir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/scripts/midgland_right.fcsv'
centroid6Dir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/scripts/midgland_left.fcsv'

writeCentroid('midgland_inferior',pp1,centroid3Dir)
writeCentroid('midgland_superior',pp2,centroid4Dir)
writeCentroid('midgland_right',pp3,centroid5Dir)
writeCentroid('midgland_left',pp4,centroid6Dir)
