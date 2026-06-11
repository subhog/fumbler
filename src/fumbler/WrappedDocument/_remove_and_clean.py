import FreeCAD, FreeCADGui, Part
import re
import math
from ..WrappedPart import WrappedPart

def remove_and_clean(self, part):
  leftovers = []
  if hasattr(part, "Sections"):
    leftovers += part.Sections
  if hasattr(part, "Spine"):
    leftovers += [part.Spine[0]]
  if hasattr(part, "Base"):
    leftovers += [part.Base]

  if hasattr(part, "Name"):
    self.doc.removeObject(part.Name)
  else:
    print("PART HAS NO NAME:", part)
  
  for item in leftovers:
    self.remove_and_clean(item)

  return self
