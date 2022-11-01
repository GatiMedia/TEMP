## TODO ##
## add warning messages
# message for not having a node selected OR multiple nodes are selected OR not Read node
nuke.message('<font color=orange><h3>Please, select a single Read node first!')
# message when no color passes
nuke.message('<font color=orange><h3>No color passes found!\nAvailable layers are:</h3>'+str(channelLayers))



curSel = nuke.toNode('Read2')
curSelChannels = curSel.channels()
layersList = []
for rawChannels in curSelChannels:
    splitRawChannels = rawChannels.split('.')
    layersList.append(splitRawChannels[0])
channelLayers = list(set(layersList))
colorGroup = []
for c in channelLayers:
    if c.startswith("C_"):
        colorGroup.append(c)
    else:
        continue
LayersNames = '' + '\n'.join(colorGroup)
print(channelLayers)

xDist = 1000
yDist = 200
gradeDist = 2500
selectVal = True


# create dotMain
dotMain = nuke.nodes.Dot()
dotMain['xpos'].setValue(int(curSel['xpos'].value())+(curSel.screenWidth()/2)-(dotMain.screenWidth()/2))
dotMain['ypos'].setValue(int(curSel['ypos'].value())+300)
dotMain.setSelected(selectVal)
dotMain.setInput(0, curSel)

# create dot
dot = connectDot = nuke.nodes.Dot()
dot['xpos'].setValue(int(dotMain['xpos'].value())-xDist)
dot['ypos'].setValue(int(dotMain['ypos'].value()))
dot.setSelected(selectVal)
dot.setInput(0, dotMain)

# create removeN
removeN = nuke.nodes.Remove()
removeN['operation'].setValue('remove')
removeN['channels'].setValue('all')
removeN['xpos'].setValue(int(connectDot['xpos'].value())-36)
removeN['ypos'].setValue(int(connectDot['ypos'].value())+200)
removeN.setSelected(selectVal)
removeN.setInput(0, connectDot)

mergeFromold = None
mergePlusOld = None

for index, n in enumerate(colorGroup):
    # creating dot
    newX = dot['xpos'].value()
    newY = dot['ypos'].value()
    oldDot = dot
    dot = nuke.nodes.Dot()
    dot['xpos'].setValue(int(newX)-xDist)
    dot['ypos'].setValue(newY)
    dot.setSelected(selectVal)
    newDot = dot
    newDot.setInput(0, oldDot)

    # creating shuffle
    shuffle = nuke.nodes.Shuffle2()
    shuffle['in1'].setValue(n)
    shuffle['label'].setValue("<b>"+n)
    shuffle['note_font_size'].setValue(25)
    shuffle['xpos'].setValue(int(dot['xpos'].value())-(shuffle.screenWidth()/2)+(dot.screenWidth()/2))
    shuffle['ypos'].setValue(int(dot['ypos'].value())+100)
    shuffle.setSelected(selectVal)
    shuffle.setInput(0, newDot)

    # creating dotshuf
    dotshuf = nuke.nodes.Dot()
    dotshuf['xpos'].setValue(int(shuffle['xpos'].value())-(dotshuf.screenWidth()/2)+(shuffle.screenWidth()/2))
    dotshuf['ypos'].setValue(int(dot['ypos'].value())+int(index*yDist)+250)
    dotshuf.setSelected(selectVal)
    dotshuf.setInput(0, shuffle)

    #creating mergeFrom
    mergeFrom = nuke.nodes.Merge2()
    mergeFrom['xpos'].setValue(int(curSel['xpos'].value()) - (len(colorGroup)+2)*xDist)
    mergeFrom['ypos'].setValue(int(dotshuf['ypos'].value())-(mergeFrom.screenHeight()/2))
    mergeFrom['operation'].setValue('from')
    mergeFrom.setSelected(selectVal)
    mergeFrom.setInput(1, dotshuf)
    if mergeFrom:
        mergeFrom.setInput(0, mergeFromold)
    if index == 0:
        mergefirst = mergeFrom 

    if index+1 == len(colorGroup):
        # creating dotUpCorner
        dotUpCorner = nuke.nodes.Dot()
        dotUpCorner['xpos'].setValue(int(mergeFrom['xpos'].value())+36)
        dotUpCorner['ypos'].setValue(int(newDot['ypos'].value()))
        dotUpCorner.setSelected(selectVal)
        dotUpCorner.setInput(0, newDot)

        mergefirst.setInput(0, dotUpCorner)

    mergeFromold = mergeFrom

    # creating dotgrade
    dotgrade = nuke.nodes.Dot()
    dotgrade['xpos'].setValue(int(dotshuf['xpos'].value()))
    dotgrade['ypos'].setValue(int(dot['ypos'].value())+int((len(colorGroup)+2)*yDist)+250)
    dotgrade.setSelected(selectVal)
    dotgrade.setInput(0, dotshuf)

    # creating unprem
    unprem = nuke.nodes.Unpremult()
    unprem['xpos'].setValue(int(shuffle['xpos'].value()))
    unprem['ypos'].setValue(int(dotgrade['ypos'].value())+100)
    unprem.setSelected(selectVal)
    unprem.setInput(0, dotgrade)

    # creating prem
    prem = nuke.nodes.Premult()
    prem['xpos'].setValue(int(shuffle['xpos'].value()))
    prem['ypos'].setValue(int(dotgrade['ypos'].value())+gradeDist-100)
    prem.setSelected(selectVal)
    prem.setInput(0, unprem)

    # creating dotgrade2
    dotgrade2 = nuke.nodes.Dot()
    dotgrade2['xpos'].setValue(int(dotgrade['xpos'].value()))
    dotgrade2['ypos'].setValue(int(dotgrade['ypos'].value())+gradeDist)
    dotgrade2.setSelected(selectVal)
    dotgrade2.setInput(0, prem)

    # creating expAlpha
    expAlpha = nuke.nodes.Expression()
    expAlpha['channel0'].setValue('alpha')
    expAlpha['expr0'].setValue('clamp(r+g+b)')
    expAlpha['xpos'].setValue(int(shuffle['xpos'].value()))
    expAlpha['ypos'].setValue(int(dotgrade2['ypos'].value())+200)
    expAlpha.setSelected(selectVal)
    expAlpha.setInput(0, dotgrade2)

    # creating dotExpr
    dotExpr = nuke.nodes.Dot()
    dotExpr['xpos'].setValue(int(dotgrade['xpos'].value()))
    dotExpr['ypos'].setValue(int(expAlpha['ypos'].value())+int(index*yDist)+250)
    dotExpr.setSelected(selectVal)
    dotExpr.setInput(0, expAlpha)


    #creating mergePlus
    mergePlus = nuke.nodes.Merge2()
    mergePlus['xpos'].setValue(int(removeN['xpos'].value()))
    mergePlus['ypos'].setValue(int(dotExpr['ypos'].value()))
    mergePlus['operation'].setValue('plus')
    mergePlus.setSelected(selectVal)
    mergePlus.setInput(1, dotExpr)
    if mergePlusOld:
        mergePlus.setInput(0, mergePlusOld)
    else:
        mergePlus.setInput(0, removeN)
    mergePlusOld = mergePlus

#creating shuffleExtra
shuffle = nuke.nodes.Shuffle2()
shuffle['in1'].setValue('rgba')
shuffle['out1'].setValue('C_Extra_Light')
shuffle['label'].setValue("<b>[value in1] -> [value out1]")
shuffle['note_font_size'].setValue(25)
shuffle['xpos'].setValue(int(mergeFrom['xpos'].value()))
shuffle['ypos'].setValue(int(mergeFrom['ypos'].value())+100)
shuffle.setSelected(selectVal)
shuffle.setInput(0, mergeFrom)

# creating expAlphaSide
expAlphaSide = nuke.nodes.Expression()
expAlphaSide['channel0'].setValue('alpha')
expAlphaSide['expr0'].setValue('clamp(r+g+b)')
expAlphaSide['xpos'].setValue(int(shuffle['xpos'].value()))
expAlphaSide['ypos'].setValue(int(expAlpha['ypos'].value()))
expAlphaSide.setSelected(selectVal)
expAlphaSide.setInput(0, shuffle)

# creating dotExprSide
dotExprSide = nuke.nodes.Dot()
dotExprSide['xpos'].setValue(int(expAlphaSide['xpos'].value())+36)
dotExprSide['ypos'].setValue(int(dotExpr['ypos'].value())+int(yDist))
dotExprSide.setSelected(selectVal)
dotExprSide.setInput(0, expAlphaSide)

#creating mergePlusSide
mergePlusSide = nuke.nodes.Merge2()
mergePlusSide['xpos'].setValue(int(mergePlus['xpos'].value()))
mergePlusSide['ypos'].setValue(int(dotExprSide['ypos'].value()))
mergePlusSide['operation'].setValue('plus')
mergePlusSide.setSelected(selectVal)
mergePlusSide.setInput(1, dotExprSide)
mergePlusSide.setInput(0, mergePlusOld)

# creating dotMsg
## TODO - add NAN_INF_KILLER _ nuke.createNode('NST_NAN_INF_Killer') - causing connestion problems
dotMsg = nuke.nodes.Dot()
dotMsg['xpos'].setValue(int(connectDot['xpos'].value()))
dotMsg['ypos'].setValue(int(mergePlusSide['ypos'].value())+(yDist*4))
dotMsg['label'].setValue(' Add a <b>NAN_INF_Killer</b> node here!')
dotMsg['note_font_size'].setValue(32)
dotMsg.setSelected(selectVal)
dotMsg.setInput(0, mergePlusSide)

# creating dotCorner 
dotCorner = nuke.nodes.Dot()
dotCorner['xpos'].setValue(int(connectDot['xpos'].value()))
dotCorner['ypos'].setValue(int(dotMsg['ypos'].value())+yDist)
dotCorner.setSelected(selectVal)
dotCorner.setInput(0, dotMsg)

# creating copyNode
copyNode = nuke.nodes.Copy()
copyNode['xpos'].setValue(int(curSel['xpos'].value()))
copyNode['ypos'].setValue(int(dotCorner['ypos'].value()))
copyNode['channels'].setValue('rgb')
copyNode.setSelected(selectVal)
copyNode.setInput(1, dotCorner)
copyNode.setInput(0, dotMain)
