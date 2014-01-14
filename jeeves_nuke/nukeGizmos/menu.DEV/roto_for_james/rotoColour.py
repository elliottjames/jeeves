import nuke.rotopaint 
curves = nuke.toNode('RotoPaint1')['curves'] 
shape = curves.toElement('Shape2') 
attrs = shape.getAttributes() 
print help(attrs) 
r = 0.7
g = 0.4 
b = 0.8 
a = 1 
attrs.set(attrs.kRedOverlayAttribute, r) 
attrs.set(attrs.kGreenOverlayAttribute, g) 
attrs.set(attrs.kBlueOverlayAttribute, b) 
attrs.set(attrs.kAlphaOverlayAttribute, a)