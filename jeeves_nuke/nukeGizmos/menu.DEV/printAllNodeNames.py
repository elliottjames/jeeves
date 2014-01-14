def printAllNodeNames

    import nuke

    for i in nuke.allNodes():
        nuke.tprint (i.name())
