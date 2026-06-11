import FreeCAD, FreeCADGui, Part
import re
import math

def scale(
  self,
  sx,
  sy,
  sz,
):
  placement = self.part.Placement
  scale_matrix = FreeCAD.Matrix()
  scale_matrix.scale(sx, sy, sz)

  scaled = self.part.Shape.transformGeometry(scale_matrix)
  self.part.Shape = scaled
  self.part.Placement = placement
  
  self.doc.recompute()
  return self
