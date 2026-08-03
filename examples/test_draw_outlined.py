############################################################
import math, os, sys

# Load fumbler dynamically
sys.path.append(os.path.join(
  os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
  "src"
))
import fumbler
fumbler.reload()
############################################################


A = fumbler.create_wrapped_document("TestDrawOutlined")

wire = A.plot_cubic([
  ((0, 0, 0), (3, 0, 0), (7, 0, 0)),
  ((10, 0, 0), (10, 3, 0), (10, 7, 0)),
  ((10, 10, 0), (7, 10, 0), (3, 10, 0)),
  ((0, 10, 0), (0, 7, 0), (0, 3, 0)),
])
outlined = wire.draw_outlined(2)

assert wire.part.Shape.ShapeType == "Wire"
assert outlined.part.Shape.ShapeType == "Face"
assert len(outlined.part.Shape.Faces) == 1
assert outlined.part.Shape.Area > 70
assert math.isclose(outlined.part.Shape.BoundBox.XLength, 12, abs_tol=0.005)
assert math.isclose(outlined.part.Shape.BoundBox.YLength, 12, abs_tol=0.005)

line = A.plot_line(20, 0, 30, 0)
outlined_line = line.draw_outlined(2)

assert line.part.Shape.ShapeType == "Edge"
assert outlined_line.part.Shape.ShapeType == "Face"
assert len(outlined_line.part.Shape.Faces) == 1
assert math.isclose(outlined_line.part.Shape.Area, 20 + math.pi, abs_tol=0.001)
assert math.isclose(outlined_line.part.Shape.BoundBox.XLength, 12, abs_tol=0.001)
assert math.isclose(outlined_line.part.Shape.BoundBox.YLength, 2, abs_tol=0.001)

p = 1.5
open_cubic = A.plot_cubic([
  ((-p, 3*p, 0), (-p, 3.75*p, 0), (-0.75*p, 4*p, 0)),
  ((0, 4*p, 0), (0.75*p, 4*p, 0), (p, 3.75*p, 0)),
  ((p, 3*p, 0), (p, 2*p, 0), (-p, 2*p, 0)),
  ((-p, 0, 0), (0, 0.5*p, 0), (0.75*p, 0, 0)),
  ((p, 0, 0),),
])
one_side = open_cubic.part.Shape.makeOffset2D(0.4, 0, True, True, False)
outlined_cubic = open_cubic.draw_outlined(0.8)

assert not open_cubic.part.Shape.isClosed()
assert outlined_cubic.part.Shape.ShapeType == "Face", (
  outlined_cubic.part.Shape.ShapeType,
  len(outlined_cubic.part.Shape.Faces),
  [
    (face.Area, face.BoundBox.XMin, face.BoundBox.XMax)
    for face in outlined_cubic.part.Shape.Faces
  ],
)
assert len(outlined_cubic.part.Shape.Faces) == 1
assert outlined_cubic.part.Shape.Area > one_side.Area * 1.8
