import FreeCAD, FreeCADGui, Part, Draft
import re
import math
from ...WrappedPart import WrappedPart


def draft_linear_dimension(
  self,
  x1,
  y1,
  x2,
  y2,
  dim_x,
  dim_y,
  z = 0,
  part = None,
  i1 = 1,
  i2 = 2,
):
  """
  Adds a Draft linear dimension between two points or two vertices of a part.

  When part is omitted, measures the distance between (x1, y1) and (x2, y2).
  When part is given, measures between vertex i1 and vertex i2 of that part;
  dim_x and dim_y still define where the dimension line passes.

  Parameters:
  x1 (float): Start X coordinate (ignored when part is given)
  y1 (float): Start Y coordinate (ignored when part is given)
  x2 (float): End X coordinate (ignored when part is given)
  y2 (float): End Y coordinate (ignored when part is given)
  dim_x (float): X coordinate of a point the dimension line passes through
  dim_y (float): Y coordinate of a point the dimension line passes through

  Keyword arguments:
  z (float): Z coordinate. Default is 0.
  part (WrappedPart): Optional part to link the dimension to
  i1 (int): First vertex index (1-based). Default is 1.
  i2 (int): Second vertex index (1-based). Default is 2.

  Returns:
  App::FeaturePython: The created Draft dimension object
  """
  FreeCAD.setActiveDocument(self.doc.Name)
  dim_line = FreeCAD.Vector(dim_x, dim_y, z)
  if part is None:
    obj = Draft.make_linear_dimension(
      FreeCAD.Vector(x1, y1, z),
      FreeCAD.Vector(x2, y2, z),
      dim_line,
    )
  else:
    obj = Draft.make_linear_dimension_obj(part.part, i1=i1, i2=i2, dim_line=dim_line)
  self.recompute()
  return obj
