r"""
Vector math utils.

.. code-block:: python

   import nvtools as nv

   # create new vectors
   a = nv.Vector(1, -1, 1)
   b = nv.Vector(2, 1, -3)

   # useful methods
   a.length
   a.angle(b)
   a.scalar_product(b)
   a.cross_product(b)
"""

import numpy as np


class NVVector:
    """NV unit vectors."""

    @property
    def vectors(self):
        r"""
        NV unit vectors.

        .. math::
            \hat{n}_1 = \frac{1}{\sqrt{3}} \begin{pmatrix} 1 \\ 1 \\ 1 \end{pmatrix} \enspace
            \hat{n}_2 = \frac{1}{\sqrt{3}} \begin{pmatrix} -1 \\ -1 \\ 1 \end{pmatrix} \enspace
            \hat{n}_3 = \frac{1}{\sqrt{3}} \begin{pmatrix} -1 \\ 1 \\ -1 \end{pmatrix} \enspace
            \hat{n}_4 = \frac{1}{\sqrt{3}} \begin{pmatrix} 1 \\ -1 \\ -1 \end{pmatrix}
        """
        return (
            Vector(1, 1, 1).normalize(),
            Vector(-1, -1, 1).normalize(),
            Vector(-1, 1, -1).normalize(),
            Vector(1, -1, -1).normalize(),
        )


class Vector:
    """N-dim Vector."""

    def __init__(self, *args):
        """N-dim Vector."""
        if isinstance(args[0], str):
            if args[0].lower() == "x":
                self.vals = np.array([1, 0, 0])
            elif args[0].lower() == "y":
                self.vals = np.array([0, 1, 0])
            elif args[0].lower() == "z":
                self.vals = np.array([0, 0, 1])
            else:
                raise ValueError("unknown input")

        elif hasattr(args[0], "__iter__"):
            self.vals = np.array(args[0])
        else:
            self.vals = np.array([*args])

    def __len__(self) -> int:
        """Dimensionality."""
        return len(self.vals)

    def __abs__(self) -> float:
        """Length."""
        return self.length

    def __str__(self) -> str:
        """String representation."""
        return f"Vector({self.vals})"

    def __repr__(self) -> str:
        """String representation."""
        return self.__str__()

    def __iter__(self):
        """Iteration."""
        yield from self.vals

    def __neg__(self):
        """Negation."""
        return self * -1

    def __add__(self, other):
        """Vector addition."""
        return Vector(np.add(self.vals, other.vals))

    def __sub__(self, other):
        """Vector subtraction."""
        return Vector(np.subtract(self.vals, other.vals))

    def __mul__(self, other):
        """LHS Multiplication."""
        if isinstance(other, (int, float)):
            return Vector(self.vals * other)
        if isinstance(other, Vector):
            return self.scalar_product(other)

        return NotImplemented

    def __rmul__(self, other):
        """RHS Multiplication."""
        if isinstance(other, (int, float)):
            return Vector(self.vals * other)

        return NotImplemented

    def __matmul__(self, other):
        """Cross product."""
        if isinstance(other, Vector):
            return self.cross_product(other)

        return NotImplemented

    def __truediv__(self, scalar):
        """Scalar division."""
        return Vector(self.vals / scalar)

    @property
    def dim(self) -> float:
        """Dimensionality."""
        return len(self.vals)

    @property
    def x(self):
        """X component."""
        return self.vals[0]

    @property
    def y(self):
        """Y component."""
        return self.vals[1]

    @property
    def z(self):
        """Z component."""
        return self.vals[2]

    def __eq__(self, other):
        """Check if nearly equal vector components."""
        return np.allclose(self.vals, other.vals)

    @property
    def length(self) -> float:
        r"""
        Euclidian length.

        .. math::
            \text{length} = \sqrt{\sum_i v_i}
        """
        return np.sqrt(np.sum(np.power(self.vals, 2)))

    def normalize(self) -> "Vector":
        """Normalize to unit length."""
        return self / self.length

    def rotate(self, u: "Vector", theta: float) -> "Vector":
        """
        Rotate around arbitrary axis.

        :param Vector u: Rotation axis (Vector of arbitrary length)
        :param float theta: Rotation angle in radians
        """
        u = u.normalize()
        ux = u.vals[0]
        uy = u.vals[1]
        uz = u.vals[2]
        sx = self.vals[0]
        sy = self.vals[1]
        sz = self.vals[2]

        cos = np.cos(theta)
        sin = np.sin(theta)

        x = (
            (cos + np.power(ux, 2) * (1 - cos)) * sx
            + (ux * uy * (1 - cos) - uz * sin) * sy
            + (ux * uz * (1 - cos) + uy * sin) * sz
        )
        y = (
            (uy * ux * (1 - cos) + uz * sin) * sx
            + (cos + np.power(uy, 2) * (1 - cos)) * sy
            + (uy * uz * (1 - cos) - ux * sin) * sz
        )
        z = (
            (uz * ux * (1 - cos) - uy * sin) * sx
            + (uz * uy * (1 - cos) + ux * sin) * sy
            + (cos + np.power(uz, 2) * (1 - cos)) * sz
        )
        return Vector((x, y, z))

    def scalar_product(self, other) -> float:
        """Scalar Product between self and other."""
        return np.dot(self.vals, other.vals)

    def cross_product(self, other) -> "Vector":
        """Cross Product between self and other."""
        return Vector(np.cross(self.vals, other.vals))

    def angle(self, other) -> float:
        r"""
        Angle between self and other in radians.

        .. math::
            \text{angle} = \arccos\left(\frac{\vec{v}_1 \cdot \vec{v}_2}{|\vec{v}_1| |\vec{v}_2|}\right)
        """
        v1 = self.normalize()
        v2 = other.normalize()

        return np.arccos(np.clip(np.dot(v1.vals, v2.vals), -1.0, 1.0))

    def angle_normal(self, other) -> float:
        r"""
        Angle between self and normal vector of a plane.

        .. math::
            \text{angle normal} = \arcsin\left(\frac{\vec{v}_1 \cdot \vec{n}_2}{|\vec{v}_1| |\vec{n}_2|}\right)
        """
        v1 = self.normalize()
        v2 = other.normalize()

        return np.arcsin(np.clip(np.dot(v1.vals, v2.vals), -1.0, 1.0))
