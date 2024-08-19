import FreeCAD, FreeCADGui, Part
import re
import math



def fuse(self, gizmos):
  if type(gizmos) != list:
    gizmos = [gizmos]

  label = self.part.Label
  result = self.part

  for gizmo in gizmos:
    prev = result
    result = Part.show(prev.Shape.fuse(gizmo.part.Shape))
    self.doc.remove_and_clean(prev)
    self.doc.remove_and_clean(gizmo.part)
    self.doc.recompute()

  self.part = result
  self.part.Label = label
  return self


def cut(self, gizmos):
  if type(gizmos) != list:
    gizmos = [gizmos]

  label = self.part.Label
  result = self.part
  for gizmo in gizmos:
    prev = result
    result = Part.show(prev.Shape.cut(gizmo.part.Shape))
    self.doc.remove_and_clean(prev)
    self.doc.remove_and_clean(gizmo.part)
    self.doc.recompute()

  self.part = result
  self.part.Label = label
  return self


def intersect(self, gizmos):
  if type(gizmos) != list:
    gizmos = [gizmos]

  label = self.part.Label
  result = self.part
  for gizmo in gizmos:
    prev = result
    result = Part.show(prev.Shape.common(gizmo.part.Shape))
    self.doc.remove_and_clean(prev)
    self.doc.remove_and_clean(gizmo.part)
    self.doc.recompute()

  self.part = result
  self.part.Label = label
  return self
