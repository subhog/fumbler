############################################################
import math, re
import FreeCAD, FreeCADGui, Part, Draft
import os, sys

# Load fumbler dynamically
sys.path.append(os.path.join(
  os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
  "src"
))
import fumbler
fumbler.reload()
############################################################


A = fumbler.create_wrapped_document("TestDrawRect")

A.draw_rect(15, 10).move((5, 5, 0))
A.draw_rect(15, 10, fi=3).move((25, 5, 0))
A.draw_rect(15, 10, ch=3).move((45, 5, 0))
A.draw_rect(15, 10, fi=3, ftl=0, cbr=3).move((65, 5, 0))

A.flush()
