import os,string
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

  #print label
  stats = sitk.LabelShapeStatisticsImageFilter()
  stats.Execute(sitk.ReadImage(label))
  labelID=stats.GetLabels()[0]
  print 'label ID : '+str(labelID)
  return labelID

def writeCentroid(name,coords,dir):

    cmd = 'touch '+str(dir)
    os.system(cmd)
    f = open(str(dir), 'w')
    f.write(str(name)+','+str(coords[0])+','+str(coords[1])+','+str(coords[2]))

def createLabelCentroid(mask,result):

  import SimpleITK as sitk

  # get centroid
  mask=sitk.ReadImage(mask)
  stats = sitk.LabelShapeStatisticsImageFilter()
  stats.Execute(mask)
  labels=stats.GetLabels()
  print labels
  coords = stats.GetCentroid(labels[0])
  print coords
  centroid = [0,0,0]
  centroid[0] = -coords[0]
  centroid[1] = -coords[1]
  centroid[2] = coords[2]
  #print coords
  # write fiducial

  writeCentroid('centroid_label',centroid,result)

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

  #print labelID
  #print mask

  stats = sitk.LabelShapeStatisticsImageFilter()
  stats.Execute(sitk.ReadImage(mask))
  bounding_box = stats.GetBoundingBox(labelID)

  return bounding_box

def convertPointFromIJKtoRAS(coords,originalImage):

    # convert (i,j,k) to RAS

    # spacing and origin is taken from original Image
    image=sitk.ReadImage(originalImage)
    origin=image.GetOrigin()
    spacing = image.GetSpacing()

    xOrigin=origin[0]
    yOrigin=origin[1]
    zOrigin=origin[2]

    xSpacing=spacing[0]
    ySpacing=spacing[1]
    zSpacing=spacing[2]

    xRAS=-1*(xOrigin+coords[0]*xSpacing)
    yRAS=-1*(yOrigin+coords[1]*ySpacing)
    zRAS=zOrigin+midSlice*zSpacing

    return [xRAS,yRAS,zRAS]

def getListOfCaseIDs(numberOfCases):

  listOfCaseIDs = []

  for case in range(numberOfCases):
    if case < 10:
        caseDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Cases003-298_data/Case00'+str(case)+'/IntraopImages/'
        if os.path.isdir(str(caseDir)):
             listOfCaseIDs.append(case)
    elif 9 < case < 100:
        caseDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Cases003-298_data/Case0'+str(case)+'/IntraopImages/'
        if os.path.isdir(str(caseDir)):
             listOfCaseIDs.append(case)
    elif 99 < case:
        caseDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Cases003-298_data/Case'+str(case)+'/IntraopImages/'
        if os.path.isdir(str(caseDir)):
             listOfCaseIDs.append(case)

  return listOfCaseIDs

def getMovingImageID(IntraDir):
    movingImageID = []
    # returns list of Image ID's for case with dir intradir
    if os.path.isdir(IntraDir):
      listDir = os.listdir(IntraDir)
      # print listDir
      for i in range(len(listDir)):
          if 'CoverProstate' in listDir[i]:
              'here'
              movingImageID.append(int(string.split(listDir[i],'-')[0]))
    else:
      print 'there is no path like: '+str(IntraDir)
    return movingImageID

def getCaseDir(case):

    if case < 10:
        caseDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Cases003-298_data/Case00'+str(case)+'/IntraopImages/'
    elif 9 < case < 100:
        caseDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Cases003-298_data/Case0'+str(case)+'/IntraopImages/'
    elif 99 < case:
        caseDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Cases003-298_data/Case'+str(case)+'/IntraopImages/'

    return caseDir


# # # # #

numberOfCases = 300
listOfCaseIDs = getListOfCaseIDs(numberOfCases)
ignoreCaseIDs = [4,5,7,8,52,60,69,72,101,142,150,275,278,280,281,282,285,286,287]
listOfCaseIDs=list(set(listOfCaseIDs) - set(ignoreCaseIDs))

for case in listOfCaseIDs:

    caseDir = getCaseDir(case)
    movingImageID=getMovingImageID(caseDir)
    maskDir = caseDir+str(movingImageID[len(movingImageID)-1])+'-label.nrrd'
    imageDir = caseDir+str(movingImageID[len(movingImageID)-1])+'-CoverProstate.nrrd'

    result1 = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/targets/Case'+str(case)+'/first_slice.nrrd'
    result2 = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/targets/Case'+str(case)+'/last_slice.nrrd'
    midSliceDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/targets/Case'+str(case)+'/mid_slice.nrrd'

    centroid0Dir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/targets/Case'+str(case)+'/centroid_label.fcsv'
    centroid1Dir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/targets/Case'+str(case)+'/centroid_apex.fcsv'
    centroid2Dir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/targets/Case'+str(case)+'/centroid_base.fcsv'
    centroid3Dir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/targets/Case'+str(case)+'/midgland_inferior.fcsv'
    centroid4Dir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/targets/Case'+str(case)+'/midgland_superior.fcsv'
    centroid5Dir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/targets/Case'+str(case)+'/midgland_right.fcsv'
    centroid6Dir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/targets/Case'+str(case)+'/midgland_left.fcsv'

    try:
        os.makedirs('/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/targets/Case'+str(case))
    except:
        pass

    # 1. create centroid for label
    createLabelCentroid(maskDir,centroid0Dir)

    #print '1 through'
    # 2. create centroid apex and base
    first,last=findFirstAndLastLabelSlices(maskDir,getLabelID(maskDir))

    extractSlice(maskDir,first,result1)
    extractSlice(maskDir,last,result2)

    centroid1 = getCentroid(result1,getLabelID(maskDir),first)
    centroid2 = getCentroid(result2,getLabelID(maskDir),last)

    writeCentroid('centroid_apex',centroid1,centroid1Dir)
    writeCentroid('centroid_base',centroid2,centroid2Dir)

    #print '2 through'
    # 3. create fiducials for midslice

    #print 'last = ' +str(last)
    #print 'first = ' +str(first)
    midSlice = int(((last-first)/2)+first)
    #print 'midSlice = '+str(midSlice)
    #print 'maskDir = '+str(maskDir)
    extractSlice(maskDir,midSlice,midSliceDir)

    boundingBox = getBoundingBox(maskDir,getLabelID(maskDir))

    upper_left = (boundingBox[0],boundingBox[1])
    down_right = (boundingBox[0]+boundingBox[3],boundingBox[1]+boundingBox[4])

    half_x_position = (down_right[0]-upper_left[0])/2+upper_left[0]
    half_y_position = (down_right[1]-upper_left[1])/2+upper_left[1]

    image=sitk.ReadImage(maskDir)

    points_vertical = down_right[1] - upper_left[1]
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
            # print (x,y,z)


    #print points_on_label_vertical
    #print points_on_label_horizontal

    midgland_superior = points_on_label_vertical[0]
    midgland_inferior = points_on_label_vertical[len(points_on_label_vertical)-1]
    midgland_left = points_on_label_horizontal[0]
    midgland_right = points_on_label_horizontal[len(points_on_label_horizontal)-1]

    pp1=convertPointFromIJKtoRAS(midgland_inferior,imageDir)
    pp2=convertPointFromIJKtoRAS(midgland_superior,imageDir)
    pp3=convertPointFromIJKtoRAS(midgland_right,imageDir)
    pp4=convertPointFromIJKtoRAS(midgland_left,imageDir)

    writeCentroid('midgland_inferior',pp1,centroid3Dir)
    writeCentroid('midgland_superior',pp2,centroid4Dir)
    writeCentroid('midgland_right',pp3,centroid5Dir)
    writeCentroid('midgland_left',pp4,centroid6Dir)


    # delete temp slices:
    os.remove(result1)
    os.remove(result2)
    os.remove(midSliceDir)

    print 'created fiducial motion trackers for case '+str(case)+' !'