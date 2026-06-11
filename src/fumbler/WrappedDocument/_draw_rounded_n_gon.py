from time import sleep
import FreeCAD, FreeCADGui, Part
import re
import math
from ..WrappedPart import WrappedPart

def draw_rounded_n_gon(
  self,
  n,
  R,
  r,
  name = "NGon"    
):
  """
    Draws a regular n-gon with radius R and rounded corners with radius r.
    
    Parameters:
    n (int): Number of sides
    R (float): Radius of the circumscribed circle
    r (float): Radius of the corner circles
    name (string): Name of the drawing
    
    Returns:
    WrappedPart<Part.Face>: The rounded n-gon face
  """
  # Calculate angles
  # angle_step = 2 * math.pi / n
  # corner_angle = math.asin(r / (R - r))  # Angle from vertex to where corner circle touches edge
  
  # Calculate the distance from center to where corner circles touch the edges
  # edge_radius = R - r
  
  
  # here = []
  # prev = []
  # next = []
  cent = []

  corner_r = r / math.cos(math.pi / n)

  for i in range(n):
    # here.append(FreeCAD.Vector(
    #   R * math.cos(i * 2 * math.pi / n),
    #   R * math.sin(i * 2 * math.pi / n),
    #   0
    # ))
    cent.append(FreeCAD.Vector(
      (R - corner_r) * math.cos(i * 2 * math.pi / n),
      (R - corner_r) * math.sin(i * 2 * math.pi / n),
      0
    ))

  return self.draw_rounded_shape(cent, r, name)
