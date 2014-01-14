import nuke

knob = nuke.toNode('RotoPaint1')['curves'] 
shape = knob.toElement('Bezier1') 
attrs = shape.getAttributes() 

randR = nuke.expression('random()') 
randG = nuke.expression('random()') 
randB = nuke.expression('random()') 

attrs.set(attrs.kRedOverlayAttribute, randR) 
attrs.set(attrs.kGreenOverlayAttribute, randG) 
attrs.set(attrs.kBlueOverlayAttribute, randB) 
attrs.set(attrs.kAlphaOverlayAttribute, 1)