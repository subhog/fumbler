import FreeCAD, FreeCADGui, Part
import re
import math
from ...WrappedPart import WrappedPart

from ...utils import TeethInset, TeethSide

def make_screw_thread(self, radius, step_height, total_height, thread_depth):

  helix = self.doc.addObject("Part::Feature", "PATH")
  helix.Shape = Part.makeHelix(step_height, total_height, radius)

  tooth_a_wire = Part.Wire([
    Part.makeLine(FreeCAD.Vector(0, 0, -thread_depth), FreeCAD.Vector(thread_depth, 0, 0)),
    Part.makeLine(FreeCAD.Vector(0, 0, thread_depth,), FreeCAD.Vector(0, 0, -thread_depth)),
    Part.makeLine(FreeCAD.Vector(thread_depth, 0, 0,), FreeCAD.Vector(0, 0, thread_depth)),
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
