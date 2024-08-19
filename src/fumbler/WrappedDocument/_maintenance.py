import FreeCAD, FreeCADGui, Part
import re
import math
from ..WrappedPart import WrappedPart


def recompute(self):
  self.doc.recompute()
  return self


def flush(self):
  FreeCADGui.updateGui()
  FreeCADGui.ActiveDocument.ActiveView.viewAxometric()
  FreeCADGui.ActiveDocument.ActiveView.fitAll()
  return self

def remove_and_clean(self, part):
  leftovers = []
  if hasattr(part, "Sections"):
    leftovers += part.Sections
  if hasattr(part, "Base"):
    leftovers += [part.Base]

  self.doc.removeObject(part.Name)
  
  for item in leftovers:
    self.remove_and_clean(item)

  return self

