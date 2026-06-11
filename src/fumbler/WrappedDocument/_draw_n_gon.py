from time import sleep
import FreeCAD, FreeCADGui, Part
import re
import math
from ..WrappedPart import WrappedPart

def draw_n_gon(
  self,
  n,
  R,
  name = "NGon"    
):
  """
    Draws a regular n-gon with radius R.
    
    Parameters:
    n (int): Number of sides
    R (float): Radius of the circumscribed circle
    
    Returns:
    WrappedPart<Part.Face>: The rounded n-gon face
  """
  points = []
  
  for i in range(n):
    
    points.append([
      R * math.cos(i * 2 * math.pi / n),
      R * math.sin(i * 2 * math.pi / n),
    ])

  return self.draw_polygon(points, name)
