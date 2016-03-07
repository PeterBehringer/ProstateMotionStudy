import os,string

# this script checks, if there are missing segmentations and if the case is useful regarding its length
def getTransformDir(case):

    if case < 10:
        transformDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Transforms/Case00'+str(case)+'/IntraopImages/'
    elif 9 < case < 100:
        transformDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Transforms/Case0'+str(case)+'/IntraopImages/'
    elif 99 < case:
        transformDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Transforms/Case'+str(case)+'/IntraopImages/'

    return transformDir

def getMovingImageID(IntraDir):
    movingImageID = []
    # returns list of Image ID's for case with dir intradir
    if os.path.isdir(IntraDir):
      listDir = os.listdir(IntraDir)
      #print 'HERE'
      #print listDir
      for i in range(len(listDir)):
          if 'CoverProstate' in listDir[i]:
              movingImageID.append(int(string.split(listDir[i],'-')[0]))
    else:
      print 'there is no path like: '+str(IntraDir)
    return movingImageID

def getLabelVolumeInL(label,image):

  import SimpleITK as sitk

  label = sitk.ReadImage(label)
  image = sitk.ReadImage(image)

  stats = sitk.LabelShapeStatisticsImageFilter()
  print "came here"
  stats.Execute(label)
  labelID=stats.GetLabels()[0]
  #print labelID

  pixelcount = stats.GetNumberOfPixels(labelID)

  volume = pixelcount * (image.GetSpacing()[0] * image.GetSpacing()[1] * image.GetSpacing()[2])
  print( """Computed volume is {vl} mm^3""".format( vl=volume ))

  # to liter: 1mm^3 = 0.000001 L
  volume = volume * 0.000001
  volume = volume * 1000

  return volume


def getCaseDir(case):

    if case < 10:
        caseDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Cases003-298_data/Case00'+str(case)+'/IntraopImages/'
    elif 9 < case < 100:
        caseDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Cases003-298_data/Case0'+str(case)+'/IntraopImages/'
    elif 99 < case:
        caseDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Cases003-298_data/Case'+str(case)+'/IntraopImages/'

    return caseDir

def getListOfCaseIDs(numberOfCases):

  listOfCaseIDs = []

  for case in range(numberOfCases):
    if case < 10:
        caseDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Cases003-298_data/Case00'+str(case)+'/IntraopImages/'
        #print caseDir
        if os.path.isdir(str(caseDir)):
             listOfCaseIDs.append(case)
    elif 9 < case < 100:
        caseDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Cases003-298_data/Case0'+str(case)+'/IntraopImages/'
        #print caseDir
        if os.path.isdir(str(caseDir)):
             listOfCaseIDs.append(case)
    elif 99 < case:
        caseDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/Cases003-298_data/Case'+str(case)+'/IntraopImages/'
        #print caseDir
        if os.path.isdir(str(caseDir)):
             listOfCaseIDs.append(case)

  return listOfCaseIDs

def getNeedleImageIDs(IntraDir):
    needleImageIds = []
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

count = 0
count2 = 0
count3 = 0
numberOfCases = 0

excel_column_CASE = []
excel_column_NEEDLEIMAGE = []

number_of_needleImagesList = []

prostate_volumes = []


numberOfCases = 300
listOfCaseIDs = []
ignoreCaseIDs = [4,5,7,8,52,60,69,72,101,142]

pelvisRegProbs = [18,23,28,29,32,33,40,42,43,46,47,66,67,76,80,81,83,91,97,99,107,108,112,114,115,
                  118,119,127,146,150,151,153,164,168,185,186,189,202,214,219,228,245,246,253,256,
                  262,268,272,273,290,295]

ignoreCaseIDsFromLackOfData = [10,49,80,81,117,121,123,134,135,137,138,141,146,150,177,212,213,218,227,241,254,255,266,289,290]


# get list of cases
listOfCaseIDs = getListOfCaseIDs(numberOfCases)

# ignore cases
listOfCaseIDs=list(set(listOfCaseIDs) - set(ignoreCaseIDs))

print listOfCaseIDs

listOfCaseIDs=list(set(listOfCaseIDs) - set(ignoreCaseIDsFromLackOfData))

print listOfCaseIDs

#listOfCaseIDs = [214]

numberOfCases = 0

for case in listOfCaseIDs:
    print case

count3=0

for case in listOfCaseIDs:



    #print 'case = '+str(case)
    tag = 0
    caseDir = getCaseDir(case)
    nids =  getNeedleImageIDs(caseDir)


    """
    #### CHECK IF NEEDLE SERIES IS SHORT AND COVER-PROSTATE IMAGE IS MISSING

    #print getNeedleImageIDs(caseDir)

    if os.path.exists(caseDir):
        list = os.listdir(caseDir)

        county = 0
        for items in list:
            #print items
            if 'CoverProstate' in items:
                county = county + 1

            if county == 2:
                print 'found a double CoverProstate case, its : '+str(case)
    """

    #### CHECK IF NEEDLE SERIES IS SHORT AND COVER-PROSTATE IMAGE IS MISSING

    #print getNeedleImageIDs(caseDir)
    """
    if os.path.exists(caseDir):
        list = os.listdir(caseDir)

        if len(list) < 10:
            print 'case '+str(case)+' is short!'

        for f in range(len(list)):
            if not any("CoverProstate" in s for s in list):
              print 'COVER PROSTATE IS MISSING '+str(case)
              count += 1
              break
    """
    ####


    #### COUNT !
    count2 = 0


    for needleImgs in nids:
        count2 += 1
        count3 += 1
        #print case
        #print needleImgs
        print case

        excel_column_CASE.append(case)
        excel_column_NEEDLEIMAGE.append(needleImgs)

    number_of_needleImagesList.append(count2)

    #print count2

    ####

    ####
    # CHECK FOR USELESS TG

    firstNeedleImage = nids[0]


    #if os.path.exists(caseDir+str(firstNeedleImage)+'-TG.nrrd'):
        #print "case "+str(case)+' uses a TG'




    fileList = os.listdir(caseDir)
    for file in fileList:
        if 'Pelvis-Pelvis' in file:
            #print ('found pelvis pelvis file, its '+str(file))
            os.remove(caseDir+'/'+str(file))
    ####




    ####
    # CHECK FOR TG

    firstNeedleImage = nids[0]


    #if os.path.exists(caseDir+str(firstNeedleImage)+'-TG.nrrd'):
        #print "case "+str(case)+' uses a TG'


    fileList = os.listdir(caseDir)
    for file in fileList:
        if 'TG' in file:
            if 'Pelvis' not in file:
              count3 = count3 + 1
              # print 'found a tg, its '+str(file)

    ####

    """

    # GET PROSTATE SIZE in ml
    #for needleImgs in nids:

    movingImageID = getMovingImageID(caseDir)
    image = caseDir+str(movingImageID[0])+'-CoverProstate.nrrd'
    label = caseDir+str(movingImageID[0])+'-label.nrrd'
    size_in_mL = getLabelVolumeInL(label,image)

    #print size_in_mL
    prostate_volumes.append(size_in_mL)

    fileList = os.listdir(caseDir)
    for file in fileList:
        if 'TG' in file:
            if 'Pelvis' not in file:
              count3 = count3 + 1
              # print 'found a tg, its '+str(file)
    """
    ####




    ####
    """
    # CHECK IF TRANSFORMS ARE EXISTING FOR EACH NEEDLE CONFIRMATION IMAGE
    transDir = getTransformDir(case)
    for i in range(0,len(nids)):
        #print nids
        listDir = os.listdir(transDir)
        #print listDir
        if not any (str(nids[i])+'-' in s for s in listDir):
            print "TRANSFORM "+str(nids[i])+' IN CASE '+str(case)+' IS MISSING'
            tag = 1

    if tag == 1:

         print '____________________'
         print "\n"
         tag = 0

    ####

    # CHECK IF CONFIGS WERE CREATED

    configDir = '/Users/peterbehringer/MyStudies/2015-ProstateMotionStudy/configs'
    cfFileName = configDir+'/Case'+str(case)+'_VisAIRe.ini'

    if not os.path.exists(cfFileName):
        print 'config file is missing for case '+str(case)


    """
    numberOfCases = numberOfCases + 1


#print prostate_volumes

for i in range(0,len(prostate_volumes)):
    print prostate_volumes[i]

print prostate_volumes


print '____________________________________'
print ' no segmentation in '+str(count)+' cases'

print '____________________________________'
print 'there are '+str(numberOfCases)+' cases in total'

print '____________________________________'
print 'there are '+str(count3)+' needle images in total'

print '____________________________________'
print str(count3)+' manual segmentations were needed'


a=[159
,132
,179
,177
,177
,185
,200
,176
,185
,181
,193
,188
,155
,222
,172
,238
,194
,203
,201
,195
,162
,199.5
,178
,185
,187
,194
,182
,146
,184
,164
,177
,193
,199
,176
,183
,222
,159
,183
,176
,206
,180
,174
,216
,238
,185
,220
,174
,168
,229
,156
,202
,248
,162
,148
,208
,185
,200
,198
,156
,168
,196
,196
,194.9997929
,179.9998088
,199.9997876
,197.9997897
,179.9998088
,177.999811
,155.9998343
,234.9997504
,194.9997929
,199.9997876
,169.9998195
,184.9998035
,159.9998301
,182.9998056
,152
,172
,168
,182
,206
,224.999108
,206.9997802
,164.9998248
,271
,179
,219.9997664
,169.9998195
,204.9997823
,171.9998173
,164.9998248
,179.9998088
,277.9997048
,199.9997876
,194.9997929
,164.9998248
,179.9998088
,174.9998141
,179.9998088
,224.999761
,239.9997451
,191.9997961
,199.9997876
,179.9998088
,176
,204.9997823
,189.9997982
,193.999794
,156.9998333
,204.9997823
,159.9998301
,189.9997982
,219.9997664
,199.9997876
,230.0080046
,189.9941516
,181.991381
,156.9998333
,212.9993613
,200.0031264
,209.990055
,219.9990298
,178.0010188
,216.9997695
,217.9994395
,196.9997908
,169.9998195
,194.9997929
,189.9997982
,173
,160
,255
,174
,200
,226
,284
,220
,165
,218
,170
,150
,212
,144
,232
,147
,385
,168
,203
,180
,228
,183
,197
,196
,169
,142
,156
,190
,182
,165
,186
,180
,203
,242
,180
,240
,163
,243
,179
,201
,161
,177
,195
,188
,179
,171
,202
,193
,227
,179
,206
,228
,213
,163
,170
,189
,145
,218
,182
,262
,242
,167
,185
,187
,215
,183
,210
,167
,204
,166
,160
,218
,158
,199
,254
,175
,116
,167
,282
,175
,200
,174
,160
,195
,194
,225
,210
,170
,225
,185
,175
,175
,152
,192
,180
,170
,156
,166
,200
,238
,183
,177
,185
,160
,227
,228
,193
,190
,215
,159
,229
,168
,185
,182
,194
,257
,242
,230
,180
,203
,183
,220
,145
,180
,188
,212]

print a