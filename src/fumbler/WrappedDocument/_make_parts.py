import FreeCAD, FreeCADGui, Part
import re
import math
from ..WrappedPart import WrappedPart

from ..utils import TeethInset, TeethSide

def make_teeth(
    self,
    length,
    tooth,
    height,
    depth,
    inset,
    side,
    tolerance = 0.1
  ):

  count = math.floor(length / tooth)
  step = (length - tolerance) / count
  width = step - tolerance

  parts = []

  if (inset == TeethInset.Outset) and (side == TeethSide.Bottom):
    for idx in range(count):
      if idx % 2 == 0:
        parts.append(
          self.make_loft([
            self.draw_rect(width, depth * 2).move((0, - tolerance / 2, 0)),
            self.draw_rect(width, depth * 2).move((0, - depth - tolerance / 2, height)),
          ])
          .move((width / 2, 0, 0))
          .move((idx * step + tolerance, 0, 0))
        )
  
  if (inset == TeethInset.Outset) and side == (TeethSide.Top):
    for idx in range(count):
      if idx % 2 == 1:
        parts.append(
          self.make_loft([
            self.draw_rect(width, depth * 2).move((0, + tolerance / 2, 0)),
            self.draw_rect(width, depth * 2).move((0, + depth + tolerance / 2, height)),
          ])
          .move((width / 2, 0, 0))
          .move((idx * step + tolerance, 0, 0))
        )

  if (inset == TeethInset.Inset) and (side == TeethSide.Bottom):
    for idx in range(count):
      if idx % 2 == 1:
        parts.append(
          self.make_loft([
            self.draw_rect(width + 2 * tolerance, depth * 2).move((0, - tolerance / 2, 0)),
            self.draw_rect(width + 2 * tolerance, depth * 2).move((0, depth - tolerance / 2, height)),
          ])
          .move((width / 2, 0, 0))
          .move((idx * step + tolerance, 0, 0))
        )

  if (inset == TeethInset.Inset) and (side == TeethSide.Top):
    for idx in range(count):
      if idx % 2 == 0:
        parts.append(
          self.make_loft([
            self.draw_rect(width + 2 * tolerance, depth * 2).move((0, + tolerance / 2, 0)),
            self.draw_rect(width + 2 * tolerance, depth * 2).move((0, - depth + tolerance / 2, height)),
          ])
          .move((width / 2, 0, 0))
          .move((idx * step + tolerance, 0, 0))
        )
      

  return self.make_fuse(parts)



def make_screw_thread(self, radius, step_height, total_height, thread_depth):

  helix = self.doc.addObject("Part::Feature", "PATH")
  helix.Shape = Part.makeHelix(step_height, total_height, radius)

  tooth_a_wire = Part.Wire([
    Part.makeLine(FreeCAD.Vector(0, 0, -thread_depth), FreeCAD.Vector(thread_depth, 0, 0)),
    Part.makeLine(FreeCAD.Vector(thread_depth, 0, 0,), FreeCAD.Vector(0, 0, thread_depth)),
    Part.makeLine(FreeCAD.Vector(0, 0, thread_depth,), FreeCAD.Vector(0, 0, -thread_depth)),
  ])
  tooth_b_wire = Part.Wire([
    Part.makeLine(FreeCAD.Vector(0, 0, -thread_depth), FreeCAD.Vector(thread_depth, 0, 0)),
    Part.makeLine(FreeCAD.Vector(thread_depth, 0, 0,), FreeCAD.Vector(0, 0, thread_depth)),
    Part.makeLine(FreeCAD.Vector(0, 0, thread_depth,), FreeCAD.Vector(0, 0, -thread_depth)),
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

