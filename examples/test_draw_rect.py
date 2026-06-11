############################################################
import math, re
import FreeCAD, FreeCADGui, Part, Draft
import os, sys

# Load fumbler dynamically
sys.path.append(os.path.join(
  os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
  "src"
))

print(os.path.join(
  os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
  "src"
))
print(sys.path)
import fumbler
fumbler.reload()
############################################################


A = fumbler.create_wrapped_document("TestDrawRect")

A.draw_rect(10, 10)
A.draw_rect(10, 10, fi=3).move((20, 0, 0))
A.draw_rect(10, 10, ch=3).move((40, 0, 0))
A.draw_rect(10, 10, fi=3, ftl=0, cbr=3).move((60, 0, 0))

A.flush()
