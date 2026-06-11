import FreeCAD, FreeCADGui, Part
import re
import math
from ..WrappedPart import WrappedPart

from ..utils import TeethInset, TeethSide

def make_trapeze_thread(self, radius, step_height, total_height, thread_depth, thread_height):

  helix = self.doc.addObject("Part::Feature", "PATH")
  helix.Shape = Part.makeHelix(step_height, total_height, radius)

  (a, b, c, d) = (
    FreeCAD.Vector(0, 0, -thread_height / 2),
    FreeCAD.Vector(thread_depth, 0, -thread_height / 2 + thread_depth),
    FreeCAD.Vector(thread_depth, 0, thread_height / 2 - thread_depth),
    FreeCAD.Vector(0, 0, thread_height / 2),
  )

  tooth_a_wire = Part.Wire([
    Part.makeLine(a, b),
    Part.makeLine(b, c),
    Part.makeLine(c, d),
    Part.makeLine(d, a),
  ])
  tooth_a_wire.translate(FreeCAD.Vector(radius, 0, 0))
  tooth_a = Part.show(Part.Face(tooth_a_wire), "TOOTH")
  
  v = self.doc.addObject("Part::Sweep", "Screw")
  v.Sections = [tooth_a]
  v.Spine = helix
  v.Solid = True
  v.Frenet = True

  helix.Visibility = False
  tooth_a.Visibility = False

  self.recompute()
  return WrappedPart(self, v)
