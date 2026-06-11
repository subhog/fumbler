import FreeCAD, FreeCADGui, Part
import re
import math
from ..WrappedPart import WrappedPart

def flush(self):
  FreeCADGui.updateGui()
  FreeCADGui.ActiveDocument.ActiveView.viewAxometric()
  FreeCADGui.ActiveDocument.ActiveView.fitAll()
  return self
