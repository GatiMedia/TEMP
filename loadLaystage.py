import os
import nuke

def loadLaystage():
    nodes = nuke.selectedNodes('Read')
    if len(nodes) == 0:
        nuke.alert('<font color=orange><h3>Please, select a Read node(s)\n of a plate first!')
    else:
        for n in nodes:
            shotdir = os.path.basename(n['file'].value())
            epName = shotdir.split("_")[1]
            seqName = shotdir.split("_")[2]
            shotName = shotdir.split("_")[3]
            laystagePath = ("/jobs/NTLS/EPISODES/%s/SEQUENCES/%s/SHOTS/%s/PUBLISH/renders/LAYSTAGE01/" % (epName, seqName, shotName))
            folders = []
            for folder in os.listdir(laystagePath):
                d = os.path.join(laystagePath, folder)
                if os.path.isdir(d):
                    folders.append(folder)
            folders.sort()
            latest_folder = folders[-1]
            full_laystagePath = laystagePath + latest_folder
            print(full_laystagePath)
            seq = (nuke.getFileNameList(full_laystagePath)[0]).split(" ")[1]
            print(seq)
            ## Create Read
            r=nuke.createNode('Read')
            r['file'].fromUserText(full_laystagePath + "/LAYSTAGE01.####.exr " + seq)
            r['xpos'].setValue(n['xpos'].value())
            r['ypos'].setValue(n['ypos'].value()+200)
            r['label'].setValue("Shot: [lindex [split [value file] /] 4 ]_[lindex [split [value file] /] 6 ]_[lindex [split [value file] /] 8 ]\nVersion: [lindex [split [value file] /] 12 ]\nFormat: [lindex [value format] 0]*[lindex [value format] 1]\nFr.Range: [value first] - [value last]")
