import FreeCAD, FreeCADGui, Part
import re
import math
from ...WrappedPart import WrappedPart

from ...utils import TeethInset, TeethSide

def make_square_spiral(self, radius, step_height, total_height, thread_depth, thread_width):

  helix = self.doc.addObject("Part::Feature", "PATH")
  helix.Shape = Part.makeHelix(step_height, total_height, radius)

  tooth_a_wire = Part.Wire([
    Part.makeLine(FreeCAD.Vector(0, -thread_width, 0), FreeCAD.Vector(thread_depth, -thread_width, 0)),
    Part.makeLine(FreeCAD.Vector(thread_depth, -thread_width, 0), FreeCAD.Vector(thread_depth, thread_width, 0)),
    Part.makeLine(FreeCAD.Vector(thread_depth, thread_width, 0), FreeCAD.Vector(0, thread_width, 0)),
    Part.makeLine(FreeCAD.Vector(0, thread_width, 0), FreeCAD.Vector(0, -thread_width, 0)),
  ])
  tooth_b_wire = Part.Wire([
    Part.makeLine(FreeCAD.Vector(0, -thread_width, 0), FreeCAD.Vector(thread_depth, -thread_width, 0)),
    Part.makeLine(FreeCAD.Vector(thread_depth, -thread_width, 0), FreeCAD.Vector(thread_depth, thread_width, 0)),
    Part.makeLine(FreeCAD.Vector(thread_depth, thread_width, 0), FreeCAD.Vector(0, thread_width, 0)),
    Part.makeLine(FreeCAD.Vector(0, thread_width, 0), FreeCAD.Vector(0, -thread_width, 0)),
  ])
  tooth_a_wire.translate(FreeCAD.Vector(radius, 0, 0))
  tooth_b_wire.translate(FreeCAD.Vector(radius, 0, total_height))
  tooth_b_wire.Placement.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1), 360 * ((total_height / step_height) % 1), True)

  tooth_a = Part.show(Part.Face(tooth_a_wire), "TOOTH")
  tooth_b = Part.show(Part.Face(tooth_b_wire), "TOOTH")

  v = self.doc.addObject("Part::Sweep", "Screw")
  v.Sections = [tooth_a, tooth_b]
  v.Spine = helix
  v.Solid = True
  v.Frenet = True

  helix.Visibility = False
  tooth_a.Visibility = False
  tooth_b.Visibility = False

  self.recompute()

  return WrappedPart(self, v)
