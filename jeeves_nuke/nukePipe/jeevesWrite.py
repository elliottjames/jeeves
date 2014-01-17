import nuke, os, errno, re, nukescripts, glob, time, sys, jeeves_core

def outputWrite():
    w = nuke.createNode('Write', inpanel=True)
    count = 1
    while nuke.exists('Jeeves_Write' + str(count)):
        count += 1
    w.knob('name').setValue('Jeeves_Write' + str(count))
    
    t = nuke.Tab_Knob("Output Write")
    w.addKnob(t)
    feedback = """
    [value dirName]
    """
    w.addKnob(nuke.EvalString_Knob('fileName', 'fileName', '[string trimright [string trimright [file tail [value root.name]] .nk] _thread0]'))
    w.addKnob(nuke.EvalString_Knob('dirName', 'dirName', os.path.join(jeeves_core.jobsRoot, os.getenv('JOB'), 'vfx', 'nuke', os.getenv('SHOT'), 'plates', 'output' ).replace('\\', '/')))
    w.addKnob(nuke.Enumeration_Knob('renderType', 'render_dir', ['slapcomp', 'cleanup', 'prerender', 'matte', 'final']))

    output_path = "[value dirName]/[value renderType]/[value fileName]/[value fileName].%04d.dpx"
    w.knob('file').fromScript(output_path)
    w.knob('colorspace').setValue('linear')
    w.knob('file_type').setValue('dpx')
    w.knob('datatype').setValue('10')
    
def photoshopWrite():
    w = nuke.createNode('Write', inpanel=True)
    count = 1
    while nuke.exists('photoshopWrite' + str(count)):
        count += 1
    w.knob('name').setValue('photoshopWrite' + str(count))
    
    t = nuke.Tab_Knob("Photoshop Write")
    w.addKnob(t)
    feedback = """
    [value dirName]
    """
    w.addKnob(nuke.EvalString_Knob('fileName', 'fileName', '[string trimright [string trimright [file tail [value root.name]] .nk] _thread0]'))
    w.addKnob(nuke.EvalString_Knob('dirName', 'dirName', os.path.join(jeevesStatic.jobsRoot, os.getenv('JOB'), 'vfx', 'adobe', 'photoshop', 'from_nuke', ).replace('\\', '/')))

    output_path = "[value dirName]/[value fileName]/[value fileName].%04d.tiff"
    w.knob('file').fromScript(output_path)
    
    w.knob('colorspace').setValue('srgb')
    w.knob('file_type').setValue('tiff')
    w.knob('datatype').setValue('16')
