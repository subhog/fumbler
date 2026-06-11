import FreeCAD, FreeCADGui, Part
import re
import math
from ..WrappedPart import WrappedPart

def make_sweep(
  self,
  shape,
  path,
):
  
  v = self.doc.addObject("Part::Sweep", "Screw")
  v.Sections = [shape.part]
  v.Spine = path.part
  v.Solid = True
  v.Frenet = True

  # helix.Visibility = False
  # tooth_a.Visibility = False
  # tooth_b.Visibility = False

  self.recompute()
  path.hide()
  shape.hide()
  return WrappedPart(self, v)
