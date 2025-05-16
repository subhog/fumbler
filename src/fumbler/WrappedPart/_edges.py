import FreeCAD, FreeCADGui, Part
import re
import math


def fillet(
  self,
  *args,
):
  label = self.part.Label
  result = self.doc.doc.addObject("Part::Fillet", "Fillet")
  result.Base = self.part

  if len(args) == 1:
    result.Edges = args[0]
  else:
    edges = args[0]
    radius = args[1]
    result.Edges = [(idx, radius, radius) for idx in edges];

  self.part.Label = label + " Raw"
  self.part.Visibility = False
  self.doc.recompute()
  self.part = result
  self.part.Label = label
  return self


def chamfer(
  self,
  *args,
):
  label = self.part.Label
  result = self.doc.doc.addObject("Part::Chamfer", "Chamfer")
  result.Base = self.part
  if len(args) == 1:
    result.Edges = args[0]
  else:
    edges = args[0]
    radius = args[1]
    result.Edges = [(idx, radius, radius) for idx in edges];

  self.part.Label = label + " Raw"
  self.part.Visibility = False
  self.doc.recompute()
  self.part = result
  self.part.Label = label
  return self


def all_edges(
  self,
):
  return [i for i, e in enumerate(self.part.Shape.Edges)]

def face_edges(
  self,
  face_idx,
):
  print(self.part.Shape.Faces[face_idx])
  # return [i for i, e in enumerate(self.part.Shape.Edges) if self.part.Shape.Faces[face_idx].contains(e)]
