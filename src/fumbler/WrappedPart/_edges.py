import FreeCAD, FreeCADGui, Part
import re
import math


def fillet(
  self,
  edges,
  radius,
  second_radius = None,
):
  label = self.part.Label
  result = self.doc.doc.addObject("Part::Fillet", "Fillet")
  result.Base = self.part
  r2 = second_radius if second_radius is not None else radius
  result.Edges = [(idx, radius, r2) for idx in edges];

  self.part.Label = label + " Raw"
  self.part.Visibility = False
  self.doc.recompute()
  self.part = result
  self.part.Label = label
  return self

def fillet_all(
  self,
  edges_rounded,
):
  label = self.part.Label
  result = self.doc.doc.addObject("Part::Fillet", "Fillet")
  result.Base = self.part
  result.Edges = edges_rounded

  self.part.Label = label + " Raw"
  self.part.Visibility = False
  self.doc.recompute()
  self.part = result
  self.part.Label = label
  return self


def chamfer(
  self,
  edges,
  radius,
  second_radius = None,
):
  label = self.part.Label
  result = self.doc.doc.addObject("Part::Chamfer", "Chamfer")
  result.Base = self.part
  r2 = second_radius if second_radius is not None else radius
  result.Edges = [(idx, radius, r2) for idx in edges];

  self.part.Label = label + " Raw"
  self.part.Visibility = False
  self.doc.recompute()
  self.part = result
  self.part.Label = label
  return self


def fillet_exact(
  self,
  edges,
):
  label = self.part.Label
  result = self.doc.doc.addObject("Part::Fillet", "Fillet")
  result.Base = self.part
  result.Edges = edges;

  self.part.Label = label + " Raw"
  self.part.Visibility = False
  self.doc.recompute()
  self.part = result
  self.part.Label = label
  return self

