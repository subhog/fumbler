import FreeCAD, FreeCADGui, Part
import re
import math



def remove_and_clean(self):
  self.doc.remove_and_clean(self.part)


def rename(self, name):
  self.part.Label = name
  return self

def recolor(self, color, transparency):
  self.part.ViewObject.ShapeColor = color
  self.part.ViewObject.Transparency = int(100 * (1 - transparency))
  return self

def hide(self):
  self.part.ViewObject.Visibility = False
  return self

