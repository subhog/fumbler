from time import sleep
import FreeCAD, FreeCADGui, Part
import re
import math
from ..WrappedPart import WrappedPart

def draw_rounded_shape(
  self,
  centers,
  r,
  name = "RoundedShape"
):
    # dist_r = r * math.sin(math.pi / n)

  # for i in range(n):
  #   pr = here[(i - 1 + n) % n]
  #   he = here[i]
  #   ne = here[(i + 1) % n]
  #   prev.append(he.add(pr.sub(he).normalize().multiply(dist_r)))
  #   next.append(he.add(ne.sub(he).normalize().multiply(dist_r)))

  # # REGULAR FACE
  # for i in range(n):
  #   a = here[i]
  #   b = here[(i + 1) % n]
  #   segments.append(self.plot_line(a.x, a.y, b.x, b.y))

  # self.recompute()
  
  # wire = Part.Wire([segment.part.Shape for segment in segments])
  # face = Part.show(Part.Face(wire), name)

  # for segment in segments:
  #   self.remove_and_clean(segment.part)

  cent = [FreeCAD.Vector(c[0], c[1], 0) for c in centers]


  # ROUNDED FACE
  segments = []
  first = None
  previous = None
  n = len(centers)

  for i in range(n):
    
    b = cent[(i) % n]
    c = cent[(i + 1) % n]
    d = cent[(i + 2) % n]
    
    # // CALCULATE THESE ANGLES PROPERLY
    alpha = math.degrees(math.atan2(b.x - c.x, - b.y + c.y))
    beta = math.degrees(math.atan2(- d.x + c.x, d.y - c.y))

    alpha = (alpha + 360) % 360
    beta = (beta + 360) % 360
    # alpha = 0
    # beta = 40
    # (360 / n * i + 180 / n) % 360
    # beta = (360 / n * (i + 1) + 180 / n) % 360
    # print(i, "~->", alpha, beta)
    current = self.plot_arc(c.x, c.y, r, alpha, beta)
    if previous:
      segments.append(self.plot_line(
        previous.part.Shape.lastVertex().X,
        previous.part.Shape.lastVertex().Y,
        current.part.Shape.firstVertex().X,
        current.part.Shape.firstVertex().Y,
      ))
    else:
      first = current
    segments.append(current)
    previous = current
    # print("~->", alpha, beta)
    # segments.append(self.plot_line(b.x, b.y, d.x, d.y))

  segments.append(self.plot_line(
    previous.part.Shape.lastVertex().X,
    previous.part.Shape.lastVertex().Y,
    first.part.Shape.firstVertex().X,
    first.part.Shape.firstVertex().Y,
  ))


  # self.recompute()
  # sleep(1)
  
  wire = Part.Wire([segment.part.Shape for segment in segments])
  face = Part.show(Part.Face(wire), name)



  for segment in segments:
    self.remove_and_clean(segment.part)

  self.recompute()
  return WrappedPart(self, face)
