## SmartVector to STMap ##

selSV = nuke.selectedNode()
selCheck = nuke.selectedNodes('Read')
if selCheck:
    sv_x = selSV['xpos'].value()
    sv_y = selSV['ypos'].value()
    sv_first = selSV['first'].value()
    sv_last = selSV['last'].value()
    sv_range = range(selSV['last'].value() - sv_first)
    selSV.setSelected(False)

    dot = nuke.nodes.Dot()
    dot.setInput(0, selSV)
    dot['xpos'].setValue(sv_x + 35)
    dotx = dot['xpos'].value()
    dot['ypos'].setValue(sv_y + 200)
    doty = dot['ypos'].value()
    dot.setSelected(True)

    vecDist1 = nuke.createNode('VectorDistort')
    vecDist1.setInput(0, dot)
    vecDist1['reference_frame'].setValue(sv_first)
    vecDist1['output_mode'].setValue('st-map')
    vecDist1['label'].setValue("""Ref fr.: [value reference_frame]\nOutput: [value output_mode]""")
    vecDist1['xpos'].setValue(sv_x)
    vecDist1['ypos'].setValue(doty + 200)
    vecDistY = vecDist1['ypos'].value()
    dot.setSelected(False)
    vecDist1.setSelected(True)

    # Create GBKWrite #
    from scarecrow.common import usage_logger;
    usage_logger.write_usage_log("nuke-menu", "Write GBK");
    from nuketools import writetab;
    writetab.createFidoWriteNode()

    nDispatch = nuke.selectedNode()

    nDispatch['removelicense'].setValue(True)
    nDispatch['label'].setValue("""Range: [value framestart] - [value frameend]\nBatch: [value batch]\nLic. Rem.: [if {[value removelicense]==true} {return "On"} {return "Off"}]\n[if { [value framestart] == [getenv FS] && [value frameend] == [getenv FE]} {return [knob tile_color 16711935]} else {return [knob tile_color 4278190335]}]""")

    writeNode = nDispatch.dependencies()[0]

    writeNode['precomp'].setValue(True)
    writeNode['channel'].setValue("rgb")
    writeNode['fecompname'].setValue("stmap_fr" + str(sv_first))

    dot.setSelected(True)

    for i in sv_range[0::10]:
        if i > 5:
            try:
                vecDist2 = nuke.createNode('VectorDistort')
                vecDist2.setInput(0, dot)
                vecDist2['reference_frame'].setValue(sv_first + i)
                vecDist2['output_mode'].setValue('st-map')
                vecDist1['label'].setValue("""Ref fr.: [value reference_frame]\nOutput: [value output_mode]""")
                vecDist2['ypos'].setValue(vecDistY)
                vecDist2_x = sv_x
                vecDist2['xpos'].setValue(vecDist2_x + (i * 33))
                vecDist2_x = vecDist2['xpos'].value()
                vecDist2.setSelected(True)

                # Create GBKWrite #
                from scarecrow.common import usage_logger;
                usage_logger.write_usage_log("nuke-menu", "Write GBK");
                from nuketools import writetab;
                writetab.createFidoWriteNode()

                nDispatch = nuke.selectedNode()
                nDispatch['removelicense'].setValue(True)
                nDispatch['label'].setValue("""Range: [value framestart] - [value frameend]\nBatch: [value batch]\nLic. Rem.: [if {[value removelicense]==true} {return "On"} {return "Off"}]\n[if { [value framestart] == [getenv FS] && [value frameend] == [getenv FE]} {return [knob tile_color 16711935]} else {return [knob tile_color 4278190335]}]""")

                writeNode = nDispatch.dependencies()[0]
                writeNode['precomp'].setValue(True)
                writeNode['channel'].setValue("rgb")
                writeNode['fecompname'].setValue("stmap_fr" + str(sv_first + i))


            except Exception:
                pass
else:
    nuke.message("""<center><b><font color=orange>Select a single node first\ncontaining a smartvector layer!""")
