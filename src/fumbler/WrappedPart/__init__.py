import FreeCAD, FreeCADGui, Part
import re
import math


class WrappedPart:


  def __init__(self, doc, part):
    self.doc = doc
    self.part = part

  from ._hide import hide
  from ._show import show
  from ._remove_and_clean import remove_and_clean
  from ._rename import rename
  from ._recolor import recolor
  from ._opacity import opacity
  from ._move import move
  from ._elevate import elevate
  from ._rotate import rotate
  from ._rotate_around import rotate_around
  from ._scale import scale
  from ._cut import cut
  from ._fuse import fuse
  from ._intersect import intersect
  from ._chamfer import chamfer
  from ._fillet import fillet
  from ._all_edges import all_edges
  from ._face_edges import face_edges


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

