import SimpleITK as sitk


coverProstate_image = "/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Cases003-298_data/Case018/IntraopImages/3-CoverProstate.nrrd"
coverProstate_label = "/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Cases003-298_data/Case018/IntraopImages/3-label.nrrd"

firstNeedle_image = "/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Cases003-298_data/Case018/IntraopImages/5-Needle.nrrd"


coverProstate_image = sitk.ReadImage(coverProstate_image)
coverProstate_label = sitk.ReadImage(coverProstate_label)

firstNeedle_image = sitk.ReadImage(firstNeedle_image)
"""
statsOld = sitk.LabelShapeStatisticsImageFilter()
statsOld.Execute(coverProstate_image)
#labelID=statsOld.GetLabels()[0]


statsNew = sitk.LabelShapeStatisticsImageFilter()
statsNew.Execute(coverProstate_image)
#labelID=statsNew.GetLabels()[0]
"""

print "SIZE old : "+str(coverProstate_image.GetSize())
print "SPACING old : "+str(coverProstate_image.GetSpacing())

new_size = firstNeedle_image.GetSize()
new_spacing = firstNeedle_image.GetSpacing()

old_size = coverProstate_image.GetSize()
old_spacing = coverProstate_image.GetSpacing()

print "SIZE new : "+str(firstNeedle_image.GetSize())
print "SPACING new : "+str(firstNeedle_image.GetSpacing())

old_xSize = old_size[0] * old_spacing[0]
old_ySize = old_size[1] * old_spacing[1]
old_zSize = old_size[2] * old_spacing[2]

new_xSize = new_size[0] * new_spacing[0]
new_ySize = new_size[1] * new_spacing[1]
new_zSize = new_size[2] * new_spacing[2]

print "REAL X size new : "+str(new_xSize)
print "REAL Y size new : "+str(new_ySize)
print "REAL Z size new : "+str(new_zSize)
print "origin new : "+str(coverProstate_image.GetOrigin())


print "REAL X size old : "+str(old_xSize)
print "REAL Y size old : "+str(old_ySize)
print "REAL Z size old : "+str(old_zSize)
print "origin new : "+str(firstNeedle_image.GetOrigin())

# create a label that fills out the whole room of the larger (new) image

newImage = sitk.Image(firstNeedle_image.GetSize(),sitk.sitkFloat32)
newImage.CopyInformation(firstNeedle_image)

print str(newImage.GetSpacing())
print 'size : ' +str(newImage.GetSize())
print 'newZsize : '+str(new_zSize)


for x in range(0,int(new_size[0])):
    for y in range(0,int(new_size[1])):
        for z in range(0,int(new_size[2])):
            newImage.SetPixel(x,y,z,1)




substractor = sitk.SubtractImageFilter()
#sitk.WriteImage(substractor.Execute(newImage,coverProstate_label),newMaskPath2)


# get label coordinates

stats = sitk.LabelShapeStatisticsImageFilter()
stats.Execute(coverProstate_label)
labels=stats.GetLabels()
label = labels[0]

print "label : "+str(label)
info = stats.GetBoundingBox(label)
print str(info)

for x in range(0,int(old_size[0])):
    for y in range(0,int(old_size[1])):
        for z in range(0,int(new_size[2])):
            print(str(coverProstate_label.GetPixel(x,y,z)))
            if int(coverProstate_label.GetPixel(x,y,z)) == 1:
                print "found label pixel, its : "+str(x)+" "+str(y)+" "+str(z)

                # substract from newimage

                newImage.SetPixel(x,y,z,0)




newMaskPath = "/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Cases003-298_data/Case018/IntraopImages/full_lable.nrrd"
newMaskPath2 = "/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Cases003-298_data/Case018/IntraopImages/full_lable2.nrrd"
sitk.WriteImage(newImage,newMaskPath)
