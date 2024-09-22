import FreeCAD, FreeCADGui, Part
import re
import math


class WrappedPart:


  def __init__(self, doc, part):
    self.doc = doc
    self.part = part

  from ._maintenance import hide, remove_and_clean, rename, recolor
  from ._transform import move, elevate, rotate
  from ._boolean import cut, fuse, intersect
  from ._edges import chamfer, fillet


  def make_copy(self):
    return WrappedPart(self.doc, Part.show(self.part.Shape))


  def make_extruded(
    self,
    height,
    name = "Extruded",
  ):
    self.doc.recompute()

    shape = self.part.Shape.extrude(FreeCAD.Vector(0, 0, height))
    part = Part.show(shape, name)

    self.doc.remove_and_clean(self.part)
    self.doc.recompute()
    return WrappedPart(self.doc, part)


  def make_face(self, idx):
    part = self.doc.doc.addObject("Part::Feature", "Face")
    part.Shape = self.part.Shape.Faces[idx]
    self.doc.recompute()
    return WrappedPart(self.doc, part)

