import FreeCAD, FreeCADGui, Part
import re
import math


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
