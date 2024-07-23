"""
This module provides access to math operations.

[NOTE]
Classes, methods and attributes that accept vectors also accept other numeric sequences,
such as tuples, lists.

The mathutils module provides the following classes:

* Color,
* Euler,
* Matrix,
* Quaternion,
* Vector,

mathutils.geometry.rst
mathutils.bvhtree.rst
mathutils.kdtree.rst
mathutils.interpolate.rst
mathutils.noise.rst

:maxdepth: 1
:caption: Submodules

```../examples/mathutils.py```

"""

import typing
import collections.abc
import typing_extensions
from . import bvhtree
from . import geometry
from . import interpolate
from . import kdtree
from . import noise

GenericType1 = typing.TypeVar("GenericType1")
GenericType2 = typing.TypeVar("GenericType2")

class Color:
    """This object gives access to Colors in Blender.Most colors returned by Blender APIs are in scene linear color space, as defined by    the OpenColorIO configuration. The notable exception is user interface theming colors,    which are in sRGB color space."""

    b: float
    """ Blue color channel.

    :type: float
    """

    g: float
    """ Green color channel.

    :type: float
    """

    h: float
    """ HSV Hue component in [0, 1].

    :type: float
    """

    hsv: Vector | collections.abc.Sequence[float]
    """ HSV Values in [0, 1].

    :type: Vector | collections.abc.Sequence[float]
    """

    is_frozen: bool
    """ True when this object has been frozen (read-only).

    :type: bool
    """

    is_valid: bool
    """ True when the owner of this data is valid.

    :type: bool
    """

    is_wrapped: bool
    """ True when this object wraps external data (read-only).

    :type: bool
    """

    owner: typing.Any
    """ The item this is wrapping or None  (read-only)."""

    r: float
    """ Red color channel.

    :type: float
    """

    s: float
    """ HSV Saturation component in [0, 1].

    :type: float
    """

    v: float
    """ HSV Value component in [0, 1].

    :type: float
    """

    def copy(self) -> typing.Self:
        """Returns a copy of this color.

        :return: A copy of the color.
        :rtype: typing.Self
        """
        ...

    def freeze(self) -> typing.Self:
        """Make this object immutable.After this the object can be hashed, used in dictionaries & sets.

        :return: An instance of this object.
        :rtype: typing.Self
        """
        ...

    def from_aces_to_scene_linear(self) -> typing.Self:
        """Convert from ACES2065-1 linear to scene linear color space.

        :return: A color in scene linear color space.
        :rtype: typing.Self
        """
        ...

    def from_rec709_linear_to_scene_linear(self) -> typing.Self:
        """Convert from Rec.709 linear color space to scene linear color space.

        :return: A color in scene linear color space.
        :rtype: typing.Self
        """
        ...

    def from_scene_linear_to_aces(self) -> typing.Self:
        """Convert from scene linear to ACES2065-1 linear color space.

        :return: A color in ACES2065-1 linear color space.
        :rtype: typing.Self
        """
        ...

    def from_scene_linear_to_rec709_linear(self) -> typing.Self:
        """Convert from scene linear to Rec.709 linear color space.

        :return: A color in Rec.709 linear color space.
        :rtype: typing.Self
        """
        ...

    def from_scene_linear_to_srgb(self) -> typing.Self:
        """Convert from scene linear to sRGB color space.

        :return: A color in sRGB color space.
        :rtype: typing.Self
        """
        ...

    def from_scene_linear_to_xyz_d65(self) -> typing.Self:
        """Convert from scene linear to CIE XYZ (Illuminant D65) color space.

        :return: A color in XYZ color space.
        :rtype: typing.Self
        """
        ...

    def from_srgb_to_scene_linear(self) -> typing.Self:
        """Convert from sRGB to scene linear color space.

        :return: A color in scene linear color space.
        :rtype: typing.Self
        """
        ...

    def from_xyz_d65_to_scene_linear(self) -> typing.Self:
        """Convert from CIE XYZ (Illuminant D65) to scene linear color space.

        :return: A color in scene linear color space.
        :rtype: typing.Self
        """
        ...

    def __init__(self, rgb=(0.0, 0.0, 0.0)):
        """

        :param rgb:
        """
        ...

    def __get__(self, instance, owner) -> typing.Self:
        """

        :param instance:
        :param owner:
        :return:
        :rtype: typing.Self
        """
        ...

    def __set__(self, instance, value: collections.abc.Sequence[float] | typing.Self):
        """

        :param instance:
        :param value:
        :type value: collections.abc.Sequence[float] | typing.Self
        """
        ...

    def __add__(
        self, other: collections.abc.Sequence[float] | typing.Self
    ) -> typing.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[float] | typing.Self
        :return:
        :rtype: typing.Self
        """
        ...

    def __sub__(
        self, other: collections.abc.Sequence[float] | typing.Self
    ) -> typing.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[float] | typing.Self
        :return:
        :rtype: typing.Self
        """
        ...

    def __mul__(self, other: float | int) -> typing.Self:
        """

        :param other:
        :type other: float | int
        :return:
        :rtype: typing.Self
        """
        ...

    def __truediv__(self, other: float | int) -> typing.Self:
        """

        :param other:
        :type other: float | int
        :return:
        :rtype: typing.Self
        """
        ...

    def __radd__(
        self, other: collections.abc.Sequence[float] | typing.Self
    ) -> typing.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[float] | typing.Self
        :return:
        :rtype: typing.Self
        """
        ...

    def __rsub__(
        self, other: collections.abc.Sequence[float] | typing.Self
    ) -> typing.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[float] | typing.Self
        :return:
        :rtype: typing.Self
        """
        ...

    def __rmul__(self, other: float | int) -> typing.Self:
        """

        :param other:
        :type other: float | int
        :return:
        :rtype: typing.Self
        """
        ...

    def __rtruediv__(self, other: float | int) -> typing.Self:
        """

        :param other:
        :type other: float | int
        :return:
        :rtype: typing.Self
        """
        ...

    def __iadd__(
        self, other: collections.abc.Sequence[float] | typing.Self
    ) -> typing.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[float] | typing.Self
        :return:
        :rtype: typing.Self
        """
        ...

    def __isub__(
        self, other: collections.abc.Sequence[float] | typing.Self
    ) -> typing.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[float] | typing.Self
        :return:
        :rtype: typing.Self
        """
        ...

    def __imul__(self, other: float | int) -> typing.Self:
        """

        :param other:
        :type other: float | int
        :return:
        :rtype: typing.Self
        """
        ...

    def __itruediv__(self, other: float | int) -> typing.Self:
        """

        :param other:
        :type other: float | int
        :return:
        :rtype: typing.Self
        """
        ...

    @typing.overload
    def __getitem__(self, key: int) -> float:
        """

        :param key:
        :type key: int
        :return:
        :rtype: float
        """
        ...

    @typing.overload
    def __getitem__(self, key: slice) -> tuple[float, ...]:
        """

        :param key:
        :type key: slice
        :return:
        :rtype: tuple[float, ...]
        """
        ...

    @typing.overload
    def __setitem__(self, key: int, value: float):
        """

        :param key:
        :type key: int
        :param value:
        :type value: float
        """
        ...

    @typing.overload
    def __setitem__(self, key: slice, value: collections.abc.Iterable[float]):
        """

        :param key:
        :type key: slice
        :param value:
        :type value: collections.abc.Iterable[float]
        """
        ...

class Euler:
    """This object gives access to Eulers in Blender.`Euler angles <https://en.wikipedia.org/wiki/Euler_angles>`__ on Wikipedia."""

    is_frozen: bool
    """ True when this object has been frozen (read-only).

    :type: bool
    """

    is_valid: bool
    """ True when the owner of this data is valid.

    :type: bool
    """

    is_wrapped: bool
    """ True when this object wraps external data (read-only).

    :type: bool
    """

    order: typing.Any
    """ Euler rotation order."""

    owner: typing.Any
    """ The item this is wrapping or None  (read-only)."""

    x: float
    """ Euler axis angle in radians.

    :type: float
    """

    y: float
    """ Euler axis angle in radians.

    :type: float
    """

    z: float
    """ Euler axis angle in radians.

    :type: float
    """

    def copy(self) -> typing.Self:
        """Returns a copy of this euler.

        :return: A copy of the euler.
        :rtype: typing.Self
        """
        ...

    def freeze(self) -> typing.Self:
        """Make this object immutable.After this the object can be hashed, used in dictionaries & sets.

        :return: An instance of this object.
        :rtype: typing.Self
        """
        ...

    def make_compatible(self, other):
        """Make this euler compatible with another,
        so interpolating between them works as intended.

                :param other:
        """
        ...

    def rotate(
        self,
        other: Matrix
        | Quaternion
        | collections.abc.Sequence[collections.abc.Sequence[float]]
        | collections.abc.Sequence[float]
        | typing.Self,
    ):
        """Rotates the euler by another mathutils value.

        :param other: rotation component of mathutils value
        :type other: Matrix | Quaternion | collections.abc.Sequence[collections.abc.Sequence[float]] | collections.abc.Sequence[float] | typing.Self
        """
        ...

    def rotate_axis(self, axis: str, angle: float):
        """Rotates the euler a certain amount and returning a unique euler rotation
        (no 720 degree pitches).

                :param axis: single character in ['X, 'Y', 'Z'].
                :type axis: str
                :param angle: angle in radians.
                :type angle: float
        """
        ...

    def to_matrix(self) -> Matrix:
        """Return a matrix representation of the euler.

        :return: A 3x3 rotation matrix representation of the euler.
        :rtype: Matrix
        """
        ...

    def to_quaternion(self) -> Quaternion:
        """Return a quaternion representation of the euler.

        :return: Quaternion representation of the euler.
        :rtype: Quaternion
        """
        ...

    def zero(self):
        """Set all values to zero."""
        ...

    def __init__(self, angles=(0.0, 0.0, 0.0), order="XYZ"):
        """

        :param angles:
        :param order:
        """
        ...

    def __get__(self, instance, owner) -> typing.Self:
        """

        :param instance:
        :param owner:
        :return:
        :rtype: typing.Self
        """
        ...

    def __set__(self, instance, value: collections.abc.Sequence[float] | typing.Self):
        """

        :param instance:
        :param value:
        :type value: collections.abc.Sequence[float] | typing.Self
        """
        ...

    @typing.overload
    def __getitem__(self, key: int) -> float:
        """

        :param key:
        :type key: int
        :return:
        :rtype: float
        """
        ...

    @typing.overload
    def __getitem__(self, key: slice) -> tuple[float, ...]:
        """

        :param key:
        :type key: slice
        :return:
        :rtype: tuple[float, ...]
        """
        ...

    @typing.overload
    def __setitem__(self, key: int, value: float):
        """

        :param key:
        :type key: int
        :param value:
        :type value: float
        """
        ...

    @typing.overload
    def __setitem__(self, key: slice, value: collections.abc.Iterable[float]):
        """

        :param key:
        :type key: slice
        :param value:
        :type value: collections.abc.Iterable[float]
        """
        ...

class Matrix:
    """This object gives access to Matrices in Blender, supporting square and rectangular
    matrices from 2x2 up to 4x4.
    """

    col: typing.Any
    """ Access the matrix by columns, 3x3 and 4x4 only, (read-only)."""

    is_frozen: bool
    """ True when this object has been frozen (read-only).

    :type: bool
    """

    is_identity: bool
    """ True if this is an identity matrix (read-only).

    :type: bool
    """

    is_negative: bool
    """ True if this matrix results in a negative scale, 3x3 and 4x4 only, (read-only).

    :type: bool
    """

    is_orthogonal: bool
    """ True if this matrix is orthogonal, 3x3 and 4x4 only, (read-only).

    :type: bool
    """

    is_orthogonal_axis_vectors: bool
    """ True if this matrix has got orthogonal axis vectors, 3x3 and 4x4 only, (read-only).

    :type: bool
    """

    is_valid: bool
    """ True when the owner of this data is valid.

    :type: bool
    """

    is_wrapped: bool
    """ True when this object wraps external data (read-only).

    :type: bool
    """

    median_scale: float
    """ The average scale applied to each axis (read-only).

    :type: float
    """

    owner: typing.Any
    """ The item this is wrapping or None  (read-only)."""

    row: typing.Any
    """ Access the matrix by rows (default), (read-only)."""

    translation: Vector
    """ The translation component of the matrix.

    :type: Vector
    """

    @classmethod
    def Diagonal(cls, vector: Vector | collections.abc.Sequence[float]) -> typing.Self:
        """Create a diagonal (scaling) matrix using the values from the vector.

        :param vector: The vector of values for the diagonal.
        :type vector: Vector | collections.abc.Sequence[float]
        :return: A diagonal matrix.
        :rtype: typing.Self
        """
        ...

    @classmethod
    def Identity(cls, size: int) -> typing.Self:
        """Create an identity matrix.

        :param size: The size of the identity matrix to construct [2, 4].
        :type size: int
        :return: A new identity matrix.
        :rtype: typing.Self
        """
        ...

    @classmethod
    def LocRotScale(
        cls,
        location: Vector | collections.abc.Sequence[float] | None,
        rotation: Euler | Quaternion | collections.abc.Sequence[float] | None,
        scale: Vector | collections.abc.Sequence[float] | None,
    ) -> typing.Self:
        """Create a matrix combining translation, rotation and scale,
        acting as the inverse of the decompose() method.Any of the inputs may be replaced with None if not needed.

                :param location: The translation component.
                :type location: Vector | collections.abc.Sequence[float] | None
                :param rotation: The rotation component.
                :type rotation: Euler | Quaternion | collections.abc.Sequence[float] | None
                :param scale: The scale component.
                :type scale: Vector | collections.abc.Sequence[float] | None
                :return: Combined transformation matrix.
                :rtype: typing.Self
        """
        ...

    @classmethod
    def OrthoProjection(
        cls, axis: Vector | collections.abc.Sequence[float] | str, size: int
    ) -> typing.Self:
        """Create a matrix to represent an orthographic projection.

                :param axis: Can be any of the following: ['X', 'Y', 'XY', 'XZ', 'YZ'],
        where a single axis is for a 2D matrix.
        Or a vector for an arbitrary axis
                :type axis: Vector | collections.abc.Sequence[float] | str
                :param size: The size of the projection matrix to construct [2, 4].
                :type size: int
                :return: A new projection matrix.
                :rtype: typing.Self
        """
        ...

    @classmethod
    def Rotation(
        cls,
        angle: float,
        size: int,
        axis: Vector | collections.abc.Sequence[float] | str | None = "",
    ) -> typing.Self:
        """Create a matrix representing a rotation.

                :param angle: The angle of rotation desired, in radians.
                :type angle: float
                :param size: The size of the rotation matrix to construct [2, 4].
                :type size: int
                :param axis: a string in ['X', 'Y', 'Z'] or a 3D Vector Object
        (optional when size is 2).
                :type axis: Vector | collections.abc.Sequence[float] | str | None
                :return: A new rotation matrix.
                :rtype: typing.Self
        """
        ...

    @classmethod
    def Scale(
        cls,
        factor: float,
        size: int,
        axis: Vector | collections.abc.Sequence[float] | None = [],
    ) -> typing.Self:
        """Create a matrix representing a scaling.

        :param factor: The factor of scaling to apply.
        :type factor: float
        :param size: The size of the scale matrix to construct [2, 4].
        :type size: int
        :param axis: Direction to influence scale. (optional).
        :type axis: Vector | collections.abc.Sequence[float] | None
        :return: A new scale matrix.
        :rtype: typing.Self
        """
        ...

    @classmethod
    def Shear(cls, plane: str, size: int, factor: float) -> typing.Self:
        """Create a matrix to represent an shear transformation.

                :param plane: Can be any of the following: ['X', 'Y', 'XY', 'XZ', 'YZ'],
        where a single axis is for a 2D matrix only.
                :type plane: str
                :param size: The size of the shear matrix to construct [2, 4].
                :type size: int
                :param factor: The factor of shear to apply. For a 3 or 4 size matrix
        pass a pair of floats corresponding with the plane axis.
                :type factor: float
                :return: A new shear matrix.
                :rtype: typing.Self
        """
        ...

    @classmethod
    def Translation(
        cls, vector: Vector | collections.abc.Sequence[float]
    ) -> typing.Self:
        """Create a matrix representing a translation.

        :param vector: The translation vector.
        :type vector: Vector | collections.abc.Sequence[float]
        :return: An identity matrix with a translation.
        :rtype: typing.Self
        """
        ...

    def adjugate(self):
        """Set the matrix to its adjugate.`Adjugate matrix <https://en.wikipedia.org/wiki/Adjugate_matrix>`__ on Wikipedia."""
        ...

    def adjugated(self) -> typing.Self:
        """Return an adjugated copy of the matrix.

        :return: the adjugated matrix.
        :rtype: typing.Self
        """
        ...

    def copy(self) -> typing.Self:
        """Returns a copy of this matrix.

        :return: an instance of itself
        :rtype: typing.Self
        """
        ...

    def decompose(self) -> tuple[Vector, Quaternion, Vector]:
        """Return the translation, rotation, and scale components of this matrix.

        :return: tuple of translation, rotation, and scale
        :rtype: tuple[Vector, Quaternion, Vector]
        """
        ...

    def determinant(self) -> float:
        """Return the determinant of a matrix.`Determinant <https://en.wikipedia.org/wiki/Determinant>`__ on Wikipedia.

        :return: Return the determinant of a matrix.
        :rtype: float
        """
        ...

    def freeze(self) -> typing.Self:
        """Make this object immutable.After this the object can be hashed, used in dictionaries & sets.

        :return: An instance of this object.
        :rtype: typing.Self
        """
        ...

    def identity(self):
        """Set the matrix to the identity matrix.`Identity matrix <https://en.wikipedia.org/wiki/Identity_matrix>`__ on Wikipedia."""
        ...

    def invert(
        self,
        fallback: collections.abc.Sequence[collections.abc.Sequence[float]]
        | typing.Self = None,
    ):
        """Set the matrix to its inverse.`Inverse matrix <https://en.wikipedia.org/wiki/Inverse_matrix>`__ on Wikipedia.

                :param fallback: Set the matrix to this value when the inverse cannot be calculated
        (instead of raising a `ValueError` exception).
                :type fallback: collections.abc.Sequence[collections.abc.Sequence[float]] | typing.Self
        """
        ...

    def invert_safe(self):
        """Set the matrix to its inverse, will never error.
        If degenerated (e.g. zero scale on an axis), add some epsilon to its diagonal, to get an invertible one.
        If tweaked matrix is still degenerated, set to the identity matrix instead.`Inverse Matrix <https://en.wikipedia.org/wiki/Inverse_matrix>`__ on Wikipedia.

        """
        ...

    def inverted(self, fallback: typing.Any = None) -> typing.Self:
        """Return an inverted copy of the matrix.

                :param fallback: return this when the inverse can't be calculated
        (instead of raising a `ValueError`).
                :type fallback: typing.Any
                :return: the inverted matrix or fallback when given.
                :rtype: typing.Self
        """
        ...

    def inverted_safe(self) -> typing.Self:
        """Return an inverted copy of the matrix, will never error.
        If degenerated (e.g. zero scale on an axis), add some epsilon to its diagonal, to get an invertible one.
        If tweaked matrix is still degenerated, return the identity matrix instead.

                :return: the inverted matrix.
                :rtype: typing.Self
        """
        ...

    def lerp(
        self,
        other: collections.abc.Sequence[collections.abc.Sequence[float]] | typing.Self,
        factor: float,
    ) -> typing.Self:
        """Returns the interpolation of two matrices. Uses polar decomposition, see   "Matrix Animation and Polar Decomposition", Shoemake and Duff, 1992.

        :param other: value to interpolate with.
        :type other: collections.abc.Sequence[collections.abc.Sequence[float]] | typing.Self
        :param factor: The interpolation value in [0.0, 1.0].
        :type factor: float
        :return: The interpolated matrix.
        :rtype: typing.Self
        """
        ...

    def normalize(self):
        """Normalize each of the matrix columns."""
        ...

    def normalized(self) -> typing.Self:
        """Return a column normalized matrix

        :return: a column normalized matrix
        :rtype: typing.Self
        """
        ...

    def resize_4x4(self):
        """Resize the matrix to 4x4."""
        ...

    def rotate(
        self,
        other: Euler
        | Quaternion
        | collections.abc.Sequence[collections.abc.Sequence[float]]
        | collections.abc.Sequence[float]
        | typing.Self,
    ):
        """Rotates the matrix by another mathutils value.

        :param other: rotation component of mathutils value
        :type other: Euler | Quaternion | collections.abc.Sequence[collections.abc.Sequence[float]] | collections.abc.Sequence[float] | typing.Self
        """
        ...

    def to_2x2(self) -> typing.Self:
        """Return a 2x2 copy of this matrix.

        :return: a new matrix.
        :rtype: typing.Self
        """
        ...

    def to_3x3(self) -> typing.Self:
        """Return a 3x3 copy of this matrix.

        :return: a new matrix.
        :rtype: typing.Self
        """
        ...

    def to_4x4(self) -> typing.Self:
        """Return a 4x4 copy of this matrix.

        :return: a new matrix.
        :rtype: typing.Self
        """
        ...

    def to_euler(
        self,
        order: str | None = "",
        euler_compat: Euler | collections.abc.Sequence[float] | None = [],
    ) -> Euler:
        """Return an Euler representation of the rotation matrix
        (3x3 or 4x4 matrix only).

                :param order: Optional rotation order argument in
        ['XYZ', 'XZY', 'YXZ', 'YZX', 'ZXY', 'ZYX'].
                :type order: str | None
                :param euler_compat: Optional euler argument the new euler will be made
        compatible with (no axis flipping between them).
        Useful for converting a series of matrices to animation curves.
                :type euler_compat: Euler | collections.abc.Sequence[float] | None
                :return: Euler representation of the matrix.
                :rtype: Euler
        """
        ...

    def to_quaternion(self) -> Quaternion:
        """Return a quaternion representation of the rotation matrix.

        :return: Quaternion representation of the rotation matrix.
        :rtype: Quaternion
        """
        ...

    def to_scale(self) -> Vector:
        """Return the scale part of a 3x3 or 4x4 matrix.

        :return: Return the scale of a matrix.
        :rtype: Vector
        """
        ...

    def to_translation(self) -> Vector:
        """Return the translation part of a 4 row matrix.

        :return: Return the translation of a matrix.
        :rtype: Vector
        """
        ...

    def transpose(self):
        """Set the matrix to its transpose.`Transpose <https://en.wikipedia.org/wiki/Transpose>`__ on Wikipedia."""
        ...

    def transposed(self) -> typing.Self:
        """Return a new, transposed matrix.

        :return: a transposed matrix
        :rtype: typing.Self
        """
        ...

    def zero(self):
        """Set all the matrix values to zero."""
        ...

    def __init__(
        self,
        rows=(
            (1.0, 0.0, 0.0, 0.0),
            (0.0, 1.0, 0.0, 0.0),
            (0.0, 0.0, 1.0, 0.0),
            (0.0, 0.0, 0.0, 1.0),
        ),
    ):
        """

        :param rows:
        """
        ...

    def __get__(self, instance, owner) -> typing.Self:
        """

        :param instance:
        :param owner:
        :return:
        :rtype: typing.Self
        """
        ...

    def __set__(
        self,
        instance,
        value: collections.abc.Sequence[collections.abc.Sequence[float]] | typing.Self,
    ):
        """

        :param instance:
        :param value:
        :type value: collections.abc.Sequence[collections.abc.Sequence[float]] | typing.Self
        """
        ...

    @typing.overload
    def __getitem__(self, key: int) -> Vector:
        """

        :param key:
        :type key: int
        :return:
        :rtype: Vector
        """
        ...

    @typing.overload
    def __getitem__(self, key: slice) -> tuple[Vector, ...]:
        """

        :param key:
        :type key: slice
        :return:
        :rtype: tuple[Vector, ...]
        """
        ...

    @typing.overload
    def __setitem__(self, key: int, value: Vector | collections.abc.Iterable[float]):
        """

        :param key:
        :type key: int
        :param value:
        :type value: Vector | collections.abc.Iterable[float]
        """
        ...

    @typing.overload
    def __setitem__(
        self,
        key: slice,
        value: collections.abc.Iterable[Vector | collections.abc.Iterable[float]],
    ):
        """

        :param key:
        :type key: slice
        :param value:
        :type value: collections.abc.Iterable[Vector | collections.abc.Iterable[float]]
        """
        ...

    def __len__(self) -> int:
        """

        :return:
        :rtype: int
        """
        ...

    def __add__(
        self,
        other: collections.abc.Sequence[collections.abc.Sequence[float]] | typing.Self,
    ) -> typing.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[collections.abc.Sequence[float]] | typing.Self
        :return:
        :rtype: typing.Self
        """
        ...

    def __sub__(
        self,
        other: collections.abc.Sequence[collections.abc.Sequence[float]] | typing.Self,
    ) -> typing.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[collections.abc.Sequence[float]] | typing.Self
        :return:
        :rtype: typing.Self
        """
        ...

    def __mul__(self, other: float | int) -> typing.Self:
        """

        :param other:
        :type other: float | int
        :return:
        :rtype: typing.Self
        """
        ...

    @typing.overload
    def __matmul__(
        self,
        other: collections.abc.Sequence[collections.abc.Sequence[float]] | typing.Self,
    ) -> typing.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[collections.abc.Sequence[float]] | typing.Self
        :return:
        :rtype: typing.Self
        """
        ...

    @typing.overload
    def __matmul__(self, other: Vector | collections.abc.Sequence[float]) -> Vector:
        """

        :param other:
        :type other: Vector | collections.abc.Sequence[float]
        :return:
        :rtype: Vector
        """
        ...

    def __radd__(
        self,
        other: collections.abc.Sequence[collections.abc.Sequence[float]] | typing.Self,
    ) -> typing.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[collections.abc.Sequence[float]] | typing.Self
        :return:
        :rtype: typing.Self
        """
        ...

    def __rsub__(
        self,
        other: collections.abc.Sequence[collections.abc.Sequence[float]] | typing.Self,
    ) -> typing.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[collections.abc.Sequence[float]] | typing.Self
        :return:
        :rtype: typing.Self
        """
        ...

    def __rmul__(self, other: float | int) -> typing.Self:
        """

        :param other:
        :type other: float | int
        :return:
        :rtype: typing.Self
        """
        ...

    def __imul__(self, other: float | int) -> typing.Self:
        """

        :param other:
        :type other: float | int
        :return:
        :rtype: typing.Self
        """
        ...

class Quaternion:
    """This object gives access to Quaternions in Blender.The constructor takes arguments in various forms:"""

    angle: float
    """ Angle of the quaternion.

    :type: float
    """

    axis: Vector
    """ Quaternion axis as a vector.

    :type: Vector
    """

    is_frozen: bool
    """ True when this object has been frozen (read-only).

    :type: bool
    """

    is_valid: bool
    """ True when the owner of this data is valid.

    :type: bool
    """

    is_wrapped: bool
    """ True when this object wraps external data (read-only).

    :type: bool
    """

    magnitude: float
    """ Size of the quaternion (read-only).

    :type: float
    """

    owner: typing.Any
    """ The item this is wrapping or None  (read-only)."""

    w: float
    """ Quaternion axis value.

    :type: float
    """

    x: float
    """ Quaternion axis value.

    :type: float
    """

    y: float
    """ Quaternion axis value.

    :type: float
    """

    z: float
    """ Quaternion axis value.

    :type: float
    """

    def conjugate(self):
        """Set the quaternion to its conjugate (negate x, y, z)."""
        ...

    def conjugated(self) -> typing.Self:
        """Return a new conjugated quaternion.

        :return: a new quaternion.
        :rtype: typing.Self
        """
        ...

    def copy(self) -> typing.Self:
        """Returns a copy of this quaternion.

        :return: A copy of the quaternion.
        :rtype: typing.Self
        """
        ...

    def cross(
        self, other: collections.abc.Sequence[float] | typing.Self
    ) -> typing.Self:
        """Return the cross product of this quaternion and another.

        :param other: The other quaternion to perform the cross product with.
        :type other: collections.abc.Sequence[float] | typing.Self
        :return: The cross product.
        :rtype: typing.Self
        """
        ...

    def dot(self, other: collections.abc.Sequence[float] | typing.Self) -> float:
        """Return the dot product of this quaternion and another.

        :param other: The other quaternion to perform the dot product with.
        :type other: collections.abc.Sequence[float] | typing.Self
        :return: The dot product.
        :rtype: float
        """
        ...

    def freeze(self) -> typing.Self:
        """Make this object immutable.After this the object can be hashed, used in dictionaries & sets.

        :return: An instance of this object.
        :rtype: typing.Self
        """
        ...

    def identity(self):
        """Set the quaternion to an identity quaternion."""
        ...

    def invert(self):
        """Set the quaternion to its inverse."""
        ...

    def inverted(self) -> typing.Self:
        """Return a new, inverted quaternion.

        :return: the inverted value.
        :rtype: typing.Self
        """
        ...

    def make_compatible(self, other):
        """Make this quaternion compatible with another,
        so interpolating between them works as intended.

                :param other:
        """
        ...

    def negate(self):
        """Set the quaternion to its negative."""
        ...

    def normalize(self):
        """Normalize the quaternion."""
        ...

    def normalized(self) -> typing.Self:
        """Return a new normalized quaternion.

        :return: a normalized copy.
        :rtype: typing.Self
        """
        ...

    def rotate(
        self,
        other: Euler
        | Matrix
        | collections.abc.Sequence[collections.abc.Sequence[float]]
        | collections.abc.Sequence[float]
        | typing.Self,
    ):
        """Rotates the quaternion by another mathutils value.

        :param other: rotation component of mathutils value
        :type other: Euler | Matrix | collections.abc.Sequence[collections.abc.Sequence[float]] | collections.abc.Sequence[float] | typing.Self
        """
        ...

    def rotation_difference(
        self, other: collections.abc.Sequence[float] | typing.Self
    ) -> typing.Self:
        """Returns a quaternion representing the rotational difference.

        :param other: second quaternion.
        :type other: collections.abc.Sequence[float] | typing.Self
        :return: the rotational difference between the two quat rotations.
        :rtype: typing.Self
        """
        ...

    def slerp(
        self, other: collections.abc.Sequence[float] | typing.Self, factor: float
    ) -> typing.Self:
        """Returns the interpolation of two quaternions.

        :param other: value to interpolate with.
        :type other: collections.abc.Sequence[float] | typing.Self
        :param factor: The interpolation value in [0.0, 1.0].
        :type factor: float
        :return: The interpolated rotation.
        :rtype: typing.Self
        """
        ...

    def to_axis_angle(self) -> tuple[Vector, float]:
        """Return the axis, angle representation of the quaternion.

        :return: axis, angle.
        :rtype: tuple[Vector, float]
        """
        ...

    def to_euler(
        self,
        order: str | None = "",
        euler_compat: Euler | collections.abc.Sequence[float] | None = [],
    ) -> Euler:
        """Return Euler representation of the quaternion.

                :param order: Optional rotation order argument in
        ['XYZ', 'XZY', 'YXZ', 'YZX', 'ZXY', 'ZYX'].
                :type order: str | None
                :param euler_compat: Optional euler argument the new euler will be made
        compatible with (no axis flipping between them).
        Useful for converting a series of matrices to animation curves.
                :type euler_compat: Euler | collections.abc.Sequence[float] | None
                :return: Euler representation of the quaternion.
                :rtype: Euler
        """
        ...

    def to_exponential_map(self):
        """Return the exponential map representation of the quaternion.This representation consist of the rotation axis multiplied by the rotation angle.
        Such a representation is useful for interpolation between multiple orientations.To convert back to a quaternion, pass it to the `Quaternion` constructor.

                :return: exponential map.
        """
        ...

    def to_matrix(self) -> Matrix:
        """Return a matrix representation of the quaternion.

        :return: A 3x3 rotation matrix representation of the quaternion.
        :rtype: Matrix
        """
        ...

    def to_swing_twist(self, axis) -> tuple[Quaternion, float]:
        """Split the rotation into a swing quaternion with the specified
        axis fixed at zero, and the remaining twist rotation angle.

                :param axis: twist axis as a string in ['X', 'Y', 'Z']
                :return: swing, twist angle.
                :rtype: tuple[Quaternion, float]
        """
        ...

    def __init__(self, seq=(1.0, 0.0, 0.0, 0.0)):
        """

        :param seq:
        """
        ...

    def __get__(self, instance, owner) -> typing.Self:
        """

        :param instance:
        :param owner:
        :return:
        :rtype: typing.Self
        """
        ...

    def __set__(self, instance, value: collections.abc.Sequence[float] | typing.Self):
        """

        :param instance:
        :param value:
        :type value: collections.abc.Sequence[float] | typing.Self
        """
        ...

    def __len__(self) -> int:
        """

        :return:
        :rtype: int
        """
        ...

    @typing.overload
    def __getitem__(self, key: int) -> float:
        """

        :param key:
        :type key: int
        :return:
        :rtype: float
        """
        ...

    @typing.overload
    def __getitem__(self, key: slice) -> tuple[float, ...]:
        """

        :param key:
        :type key: slice
        :return:
        :rtype: tuple[float, ...]
        """
        ...

    @typing.overload
    def __setitem__(self, key: int, value: float):
        """

        :param key:
        :type key: int
        :param value:
        :type value: float
        """
        ...

    @typing.overload
    def __setitem__(self, key: slice, value: collections.abc.Iterable[float]):
        """

        :param key:
        :type key: slice
        :param value:
        :type value: collections.abc.Iterable[float]
        """
        ...

    def __add__(
        self, other: collections.abc.Sequence[float] | typing.Self
    ) -> typing.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[float] | typing.Self
        :return:
        :rtype: typing.Self
        """
        ...

    def __sub__(
        self, other: collections.abc.Sequence[float] | typing.Self
    ) -> typing.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[float] | typing.Self
        :return:
        :rtype: typing.Self
        """
        ...

    def __mul__(
        self, other: collections.abc.Sequence[float] | float | int | typing.Self
    ) -> typing.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[float] | float | int | typing.Self
        :return:
        :rtype: typing.Self
        """
        ...

    @typing.overload
    def __matmul__(
        self, other: collections.abc.Sequence[float] | typing.Self
    ) -> typing.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[float] | typing.Self
        :return:
        :rtype: typing.Self
        """
        ...

    @typing.overload
    def __matmul__(self, other: Vector | collections.abc.Sequence[float]) -> Vector:
        """

        :param other:
        :type other: Vector | collections.abc.Sequence[float]
        :return:
        :rtype: Vector
        """
        ...

    def __radd__(
        self, other: collections.abc.Sequence[float] | typing.Self
    ) -> typing.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[float] | typing.Self
        :return:
        :rtype: typing.Self
        """
        ...

    def __rsub__(
        self, other: collections.abc.Sequence[float] | typing.Self
    ) -> typing.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[float] | typing.Self
        :return:
        :rtype: typing.Self
        """
        ...

    def __rmul__(
        self, other: collections.abc.Sequence[float] | float | int | typing.Self
    ) -> typing.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[float] | float | int | typing.Self
        :return:
        :rtype: typing.Self
        """
        ...

    def __imul__(
        self, other: collections.abc.Sequence[float] | float | int | typing.Self
    ) -> typing.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[float] | float | int | typing.Self
        :return:
        :rtype: typing.Self
        """
        ...

class Vector:
    """This object gives access to Vectors in Blender."""

    is_frozen: bool
    """ True when this object has been frozen (read-only).

    :type: bool
    """

    is_valid: bool
    """ True when the owner of this data is valid.

    :type: bool
    """

    is_wrapped: bool
    """ True when this object wraps external data (read-only).

    :type: bool
    """

    length: float
    """ Vector Length.

    :type: float
    """

    length_squared: float
    """ Vector length squared (v.dot(v)).

    :type: float
    """

    magnitude: float
    """ Vector Length.

    :type: float
    """

    owner: typing.Any
    """ The item this is wrapping or None  (read-only)."""

    w: float
    """ Vector W axis (4D Vectors only).

    :type: float
    """

    ww: typing.Self
    """ 

    :type: typing.Self
    """

    www: typing.Self
    """ 

    :type: typing.Self
    """

    wwww: typing.Self
    """ 

    :type: typing.Self
    """

    wwwx: typing.Self
    """ 

    :type: typing.Self
    """

    wwwy: typing.Self
    """ 

    :type: typing.Self
    """

    wwwz: typing.Self
    """ 

    :type: typing.Self
    """

    wwx: typing.Self
    """ 

    :type: typing.Self
    """

    wwxw: typing.Self
    """ 

    :type: typing.Self
    """

    wwxx: typing.Self
    """ 

    :type: typing.Self
    """

    wwxy: typing.Self
    """ 

    :type: typing.Self
    """

    wwxz: typing.Self
    """ 

    :type: typing.Self
    """

    wwy: typing.Self
    """ 

    :type: typing.Self
    """

    wwyw: typing.Self
    """ 

    :type: typing.Self
    """

    wwyx: typing.Self
    """ 

    :type: typing.Self
    """

    wwyy: typing.Self
    """ 

    :type: typing.Self
    """

    wwyz: typing.Self
    """ 

    :type: typing.Self
    """

    wwz: typing.Self
    """ 

    :type: typing.Self
    """

    wwzw: typing.Self
    """ 

    :type: typing.Self
    """

    wwzx: typing.Self
    """ 

    :type: typing.Self
    """

    wwzy: typing.Self
    """ 

    :type: typing.Self
    """

    wwzz: typing.Self
    """ 

    :type: typing.Self
    """

    wx: typing.Self
    """ 

    :type: typing.Self
    """

    wxw: typing.Self
    """ 

    :type: typing.Self
    """

    wxww: typing.Self
    """ 

    :type: typing.Self
    """

    wxwx: typing.Self
    """ 

    :type: typing.Self
    """

    wxwy: typing.Self
    """ 

    :type: typing.Self
    """

    wxwz: typing.Self
    """ 

    :type: typing.Self
    """

    wxx: typing.Self
    """ 

    :type: typing.Self
    """

    wxxw: typing.Self
    """ 

    :type: typing.Self
    """

    wxxx: typing.Self
    """ 

    :type: typing.Self
    """

    wxxy: typing.Self
    """ 

    :type: typing.Self
    """

    wxxz: typing.Self
    """ 

    :type: typing.Self
    """

    wxy: typing.Self
    """ 

    :type: typing.Self
    """

    wxyw: typing.Self
    """ 

    :type: typing.Self
    """

    wxyx: typing.Self
    """ 

    :type: typing.Self
    """

    wxyy: typing.Self
    """ 

    :type: typing.Self
    """

    wxyz: typing.Self
    """ 

    :type: typing.Self
    """

    wxz: typing.Self
    """ 

    :type: typing.Self
    """

    wxzw: typing.Self
    """ 

    :type: typing.Self
    """

    wxzx: typing.Self
    """ 

    :type: typing.Self
    """

    wxzy: typing.Self
    """ 

    :type: typing.Self
    """

    wxzz: typing.Self
    """ 

    :type: typing.Self
    """

    wy: typing.Self
    """ 

    :type: typing.Self
    """

    wyw: typing.Self
    """ 

    :type: typing.Self
    """

    wyww: typing.Self
    """ 

    :type: typing.Self
    """

    wywx: typing.Self
    """ 

    :type: typing.Self
    """

    wywy: typing.Self
    """ 

    :type: typing.Self
    """

    wywz: typing.Self
    """ 

    :type: typing.Self
    """

    wyx: typing.Self
    """ 

    :type: typing.Self
    """

    wyxw: typing.Self
    """ 

    :type: typing.Self
    """

    wyxx: typing.Self
    """ 

    :type: typing.Self
    """

    wyxy: typing.Self
    """ 

    :type: typing.Self
    """

    wyxz: typing.Self
    """ 

    :type: typing.Self
    """

    wyy: typing.Self
    """ 

    :type: typing.Self
    """

    wyyw: typing.Self
    """ 

    :type: typing.Self
    """

    wyyx: typing.Self
    """ 

    :type: typing.Self
    """

    wyyy: typing.Self
    """ 

    :type: typing.Self
    """

    wyyz: typing.Self
    """ 

    :type: typing.Self
    """

    wyz: typing.Self
    """ 

    :type: typing.Self
    """

    wyzw: typing.Self
    """ 

    :type: typing.Self
    """

    wyzx: typing.Self
    """ 

    :type: typing.Self
    """

    wyzy: typing.Self
    """ 

    :type: typing.Self
    """

    wyzz: typing.Self
    """ 

    :type: typing.Self
    """

    wz: typing.Self
    """ 

    :type: typing.Self
    """

    wzw: typing.Self
    """ 

    :type: typing.Self
    """

    wzww: typing.Self
    """ 

    :type: typing.Self
    """

    wzwx: typing.Self
    """ 

    :type: typing.Self
    """

    wzwy: typing.Self
    """ 

    :type: typing.Self
    """

    wzwz: typing.Self
    """ 

    :type: typing.Self
    """

    wzx: typing.Self
    """ 

    :type: typing.Self
    """

    wzxw: typing.Self
    """ 

    :type: typing.Self
    """

    wzxx: typing.Self
    """ 

    :type: typing.Self
    """

    wzxy: typing.Self
    """ 

    :type: typing.Self
    """

    wzxz: typing.Self
    """ 

    :type: typing.Self
    """

    wzy: typing.Self
    """ 

    :type: typing.Self
    """

    wzyw: typing.Self
    """ 

    :type: typing.Self
    """

    wzyx: typing.Self
    """ 

    :type: typing.Self
    """

    wzyy: typing.Self
    """ 

    :type: typing.Self
    """

    wzyz: typing.Self
    """ 

    :type: typing.Self
    """

    wzz: typing.Self
    """ 

    :type: typing.Self
    """

    wzzw: typing.Self
    """ 

    :type: typing.Self
    """

    wzzx: typing.Self
    """ 

    :type: typing.Self
    """

    wzzy: typing.Self
    """ 

    :type: typing.Self
    """

    wzzz: typing.Self
    """ 

    :type: typing.Self
    """

    x: float
    """ Vector X axis.

    :type: float
    """

    xw: typing.Self
    """ 

    :type: typing.Self
    """

    xww: typing.Self
    """ 

    :type: typing.Self
    """

    xwww: typing.Self
    """ 

    :type: typing.Self
    """

    xwwx: typing.Self
    """ 

    :type: typing.Self
    """

    xwwy: typing.Self
    """ 

    :type: typing.Self
    """

    xwwz: typing.Self
    """ 

    :type: typing.Self
    """

    xwx: typing.Self
    """ 

    :type: typing.Self
    """

    xwxw: typing.Self
    """ 

    :type: typing.Self
    """

    xwxx: typing.Self
    """ 

    :type: typing.Self
    """

    xwxy: typing.Self
    """ 

    :type: typing.Self
    """

    xwxz: typing.Self
    """ 

    :type: typing.Self
    """

    xwy: typing.Self
    """ 

    :type: typing.Self
    """

    xwyw: typing.Self
    """ 

    :type: typing.Self
    """

    xwyx: typing.Self
    """ 

    :type: typing.Self
    """

    xwyy: typing.Self
    """ 

    :type: typing.Self
    """

    xwyz: typing.Self
    """ 

    :type: typing.Self
    """

    xwz: typing.Self
    """ 

    :type: typing.Self
    """

    xwzw: typing.Self
    """ 

    :type: typing.Self
    """

    xwzx: typing.Self
    """ 

    :type: typing.Self
    """

    xwzy: typing.Self
    """ 

    :type: typing.Self
    """

    xwzz: typing.Self
    """ 

    :type: typing.Self
    """

    xx: typing.Self
    """ 

    :type: typing.Self
    """

    xxw: typing.Self
    """ 

    :type: typing.Self
    """

    xxww: typing.Self
    """ 

    :type: typing.Self
    """

    xxwx: typing.Self
    """ 

    :type: typing.Self
    """

    xxwy: typing.Self
    """ 

    :type: typing.Self
    """

    xxwz: typing.Self
    """ 

    :type: typing.Self
    """

    xxx: typing.Self
    """ 

    :type: typing.Self
    """

    xxxw: typing.Self
    """ 

    :type: typing.Self
    """

    xxxx: typing.Self
    """ 

    :type: typing.Self
    """

    xxxy: typing.Self
    """ 

    :type: typing.Self
    """

    xxxz: typing.Self
    """ 

    :type: typing.Self
    """

    xxy: typing.Self
    """ 

    :type: typing.Self
    """

    xxyw: typing.Self
    """ 

    :type: typing.Self
    """

    xxyx: typing.Self
    """ 

    :type: typing.Self
    """

    xxyy: typing.Self
    """ 

    :type: typing.Self
    """

    xxyz: typing.Self
    """ 

    :type: typing.Self
    """

    xxz: typing.Self
    """ 

    :type: typing.Self
    """

    xxzw: typing.Self
    """ 

    :type: typing.Self
    """

    xxzx: typing.Self
    """ 

    :type: typing.Self
    """

    xxzy: typing.Self
    """ 

    :type: typing.Self
    """

    xxzz: typing.Self
    """ 

    :type: typing.Self
    """

    xy: typing.Self
    """ 

    :type: typing.Self
    """

    xyw: typing.Self
    """ 

    :type: typing.Self
    """

    xyww: typing.Self
    """ 

    :type: typing.Self
    """

    xywx: typing.Self
    """ 

    :type: typing.Self
    """

    xywy: typing.Self
    """ 

    :type: typing.Self
    """

    xywz: typing.Self
    """ 

    :type: typing.Self
    """

    xyx: typing.Self
    """ 

    :type: typing.Self
    """

    xyxw: typing.Self
    """ 

    :type: typing.Self
    """

    xyxx: typing.Self
    """ 

    :type: typing.Self
    """

    xyxy: typing.Self
    """ 

    :type: typing.Self
    """

    xyxz: typing.Self
    """ 

    :type: typing.Self
    """

    xyy: typing.Self
    """ 

    :type: typing.Self
    """

    xyyw: typing.Self
    """ 

    :type: typing.Self
    """

    xyyx: typing.Self
    """ 

    :type: typing.Self
    """

    xyyy: typing.Self
    """ 

    :type: typing.Self
    """

    xyyz: typing.Self
    """ 

    :type: typing.Self
    """

    xyz: typing.Self
    """ 

    :type: typing.Self
    """

    xyzw: typing.Self
    """ 

    :type: typing.Self
    """

    xyzx: typing.Self
    """ 

    :type: typing.Self
    """

    xyzy: typing.Self
    """ 

    :type: typing.Self
    """

    xyzz: typing.Self
    """ 

    :type: typing.Self
    """

    xz: typing.Self
    """ 

    :type: typing.Self
    """

    xzw: typing.Self
    """ 

    :type: typing.Self
    """

    xzww: typing.Self
    """ 

    :type: typing.Self
    """

    xzwx: typing.Self
    """ 

    :type: typing.Self
    """

    xzwy: typing.Self
    """ 

    :type: typing.Self
    """

    xzwz: typing.Self
    """ 

    :type: typing.Self
    """

    xzx: typing.Self
    """ 

    :type: typing.Self
    """

    xzxw: typing.Self
    """ 

    :type: typing.Self
    """

    xzxx: typing.Self
    """ 

    :type: typing.Self
    """

    xzxy: typing.Self
    """ 

    :type: typing.Self
    """

    xzxz: typing.Self
    """ 

    :type: typing.Self
    """

    xzy: typing.Self
    """ 

    :type: typing.Self
    """

    xzyw: typing.Self
    """ 

    :type: typing.Self
    """

    xzyx: typing.Self
    """ 

    :type: typing.Self
    """

    xzyy: typing.Self
    """ 

    :type: typing.Self
    """

    xzyz: typing.Self
    """ 

    :type: typing.Self
    """

    xzz: typing.Self
    """ 

    :type: typing.Self
    """

    xzzw: typing.Self
    """ 

    :type: typing.Self
    """

    xzzx: typing.Self
    """ 

    :type: typing.Self
    """

    xzzy: typing.Self
    """ 

    :type: typing.Self
    """

    xzzz: typing.Self
    """ 

    :type: typing.Self
    """

    y: float
    """ Vector Y axis.

    :type: float
    """

    yw: typing.Self
    """ 

    :type: typing.Self
    """

    yww: typing.Self
    """ 

    :type: typing.Self
    """

    ywww: typing.Self
    """ 

    :type: typing.Self
    """

    ywwx: typing.Self
    """ 

    :type: typing.Self
    """

    ywwy: typing.Self
    """ 

    :type: typing.Self
    """

    ywwz: typing.Self
    """ 

    :type: typing.Self
    """

    ywx: typing.Self
    """ 

    :type: typing.Self
    """

    ywxw: typing.Self
    """ 

    :type: typing.Self
    """

    ywxx: typing.Self
    """ 

    :type: typing.Self
    """

    ywxy: typing.Self
    """ 

    :type: typing.Self
    """

    ywxz: typing.Self
    """ 

    :type: typing.Self
    """

    ywy: typing.Self
    """ 

    :type: typing.Self
    """

    ywyw: typing.Self
    """ 

    :type: typing.Self
    """

    ywyx: typing.Self
    """ 

    :type: typing.Self
    """

    ywyy: typing.Self
    """ 

    :type: typing.Self
    """

    ywyz: typing.Self
    """ 

    :type: typing.Self
    """

    ywz: typing.Self
    """ 

    :type: typing.Self
    """

    ywzw: typing.Self
    """ 

    :type: typing.Self
    """

    ywzx: typing.Self
    """ 

    :type: typing.Self
    """

    ywzy: typing.Self
    """ 

    :type: typing.Self
    """

    ywzz: typing.Self
    """ 

    :type: typing.Self
    """

    yx: typing.Self
    """ 

    :type: typing.Self
    """

    yxw: typing.Self
    """ 

    :type: typing.Self
    """

    yxww: typing.Self
    """ 

    :type: typing.Self
    """

    yxwx: typing.Self
    """ 

    :type: typing.Self
    """

    yxwy: typing.Self
    """ 

    :type: typing.Self
    """

    yxwz: typing.Self
    """ 

    :type: typing.Self
    """

    yxx: typing.Self
    """ 

    :type: typing.Self
    """

    yxxw: typing.Self
    """ 

    :type: typing.Self
    """

    yxxx: typing.Self
    """ 

    :type: typing.Self
    """

    yxxy: typing.Self
    """ 

    :type: typing.Self
    """

    yxxz: typing.Self
    """ 

    :type: typing.Self
    """

    yxy: typing.Self
    """ 

    :type: typing.Self
    """

    yxyw: typing.Self
    """ 

    :type: typing.Self
    """

    yxyx: typing.Self
    """ 

    :type: typing.Self
    """

    yxyy: typing.Self
    """ 

    :type: typing.Self
    """

    yxyz: typing.Self
    """ 

    :type: typing.Self
    """

    yxz: typing.Self
    """ 

    :type: typing.Self
    """

    yxzw: typing.Self
    """ 

    :type: typing.Self
    """

    yxzx: typing.Self
    """ 

    :type: typing.Self
    """

    yxzy: typing.Self
    """ 

    :type: typing.Self
    """

    yxzz: typing.Self
    """ 

    :type: typing.Self
    """

    yy: typing.Self
    """ 

    :type: typing.Self
    """

    yyw: typing.Self
    """ 

    :type: typing.Self
    """

    yyww: typing.Self
    """ 

    :type: typing.Self
    """

    yywx: typing.Self
    """ 

    :type: typing.Self
    """

    yywy: typing.Self
    """ 

    :type: typing.Self
    """

    yywz: typing.Self
    """ 

    :type: typing.Self
    """

    yyx: typing.Self
    """ 

    :type: typing.Self
    """

    yyxw: typing.Self
    """ 

    :type: typing.Self
    """

    yyxx: typing.Self
    """ 

    :type: typing.Self
    """

    yyxy: typing.Self
    """ 

    :type: typing.Self
    """

    yyxz: typing.Self
    """ 

    :type: typing.Self
    """

    yyy: typing.Self
    """ 

    :type: typing.Self
    """

    yyyw: typing.Self
    """ 

    :type: typing.Self
    """

    yyyx: typing.Self
    """ 

    :type: typing.Self
    """

    yyyy: typing.Self
    """ 

    :type: typing.Self
    """

    yyyz: typing.Self
    """ 

    :type: typing.Self
    """

    yyz: typing.Self
    """ 

    :type: typing.Self
    """

    yyzw: typing.Self
    """ 

    :type: typing.Self
    """

    yyzx: typing.Self
    """ 

    :type: typing.Self
    """

    yyzy: typing.Self
    """ 

    :type: typing.Self
    """

    yyzz: typing.Self
    """ 

    :type: typing.Self
    """

    yz: typing.Self
    """ 

    :type: typing.Self
    """

    yzw: typing.Self
    """ 

    :type: typing.Self
    """

    yzww: typing.Self
    """ 

    :type: typing.Self
    """

    yzwx: typing.Self
    """ 

    :type: typing.Self
    """

    yzwy: typing.Self
    """ 

    :type: typing.Self
    """

    yzwz: typing.Self
    """ 

    :type: typing.Self
    """

    yzx: typing.Self
    """ 

    :type: typing.Self
    """

    yzxw: typing.Self
    """ 

    :type: typing.Self
    """

    yzxx: typing.Self
    """ 

    :type: typing.Self
    """

    yzxy: typing.Self
    """ 

    :type: typing.Self
    """

    yzxz: typing.Self
    """ 

    :type: typing.Self
    """

    yzy: typing.Self
    """ 

    :type: typing.Self
    """

    yzyw: typing.Self
    """ 

    :type: typing.Self
    """

    yzyx: typing.Self
    """ 

    :type: typing.Self
    """

    yzyy: typing.Self
    """ 

    :type: typing.Self
    """

    yzyz: typing.Self
    """ 

    :type: typing.Self
    """

    yzz: typing.Self
    """ 

    :type: typing.Self
    """

    yzzw: typing.Self
    """ 

    :type: typing.Self
    """

    yzzx: typing.Self
    """ 

    :type: typing.Self
    """

    yzzy: typing.Self
    """ 

    :type: typing.Self
    """

    yzzz: typing.Self
    """ 

    :type: typing.Self
    """

    z: float
    """ Vector Z axis (3D Vectors only).

    :type: float
    """

    zw: typing.Self
    """ 

    :type: typing.Self
    """

    zww: typing.Self
    """ 

    :type: typing.Self
    """

    zwww: typing.Self
    """ 

    :type: typing.Self
    """

    zwwx: typing.Self
    """ 

    :type: typing.Self
    """

    zwwy: typing.Self
    """ 

    :type: typing.Self
    """

    zwwz: typing.Self
    """ 

    :type: typing.Self
    """

    zwx: typing.Self
    """ 

    :type: typing.Self
    """

    zwxw: typing.Self
    """ 

    :type: typing.Self
    """

    zwxx: typing.Self
    """ 

    :type: typing.Self
    """

    zwxy: typing.Self
    """ 

    :type: typing.Self
    """

    zwxz: typing.Self
    """ 

    :type: typing.Self
    """

    zwy: typing.Self
    """ 

    :type: typing.Self
    """

    zwyw: typing.Self
    """ 

    :type: typing.Self
    """

    zwyx: typing.Self
    """ 

    :type: typing.Self
    """

    zwyy: typing.Self
    """ 

    :type: typing.Self
    """

    zwyz: typing.Self
    """ 

    :type: typing.Self
    """

    zwz: typing.Self
    """ 

    :type: typing.Self
    """

    zwzw: typing.Self
    """ 

    :type: typing.Self
    """

    zwzx: typing.Self
    """ 

    :type: typing.Self
    """

    zwzy: typing.Self
    """ 

    :type: typing.Self
    """

    zwzz: typing.Self
    """ 

    :type: typing.Self
    """

    zx: typing.Self
    """ 

    :type: typing.Self
    """

    zxw: typing.Self
    """ 

    :type: typing.Self
    """

    zxww: typing.Self
    """ 

    :type: typing.Self
    """

    zxwx: typing.Self
    """ 

    :type: typing.Self
    """

    zxwy: typing.Self
    """ 

    :type: typing.Self
    """

    zxwz: typing.Self
    """ 

    :type: typing.Self
    """

    zxx: typing.Self
    """ 

    :type: typing.Self
    """

    zxxw: typing.Self
    """ 

    :type: typing.Self
    """

    zxxx: typing.Self
    """ 

    :type: typing.Self
    """

    zxxy: typing.Self
    """ 

    :type: typing.Self
    """

    zxxz: typing.Self
    """ 

    :type: typing.Self
    """

    zxy: typing.Self
    """ 

    :type: typing.Self
    """

    zxyw: typing.Self
    """ 

    :type: typing.Self
    """

    zxyx: typing.Self
    """ 

    :type: typing.Self
    """

    zxyy: typing.Self
    """ 

    :type: typing.Self
    """

    zxyz: typing.Self
    """ 

    :type: typing.Self
    """

    zxz: typing.Self
    """ 

    :type: typing.Self
    """

    zxzw: typing.Self
    """ 

    :type: typing.Self
    """

    zxzx: typing.Self
    """ 

    :type: typing.Self
    """

    zxzy: typing.Self
    """ 

    :type: typing.Self
    """

    zxzz: typing.Self
    """ 

    :type: typing.Self
    """

    zy: typing.Self
    """ 

    :type: typing.Self
    """

    zyw: typing.Self
    """ 

    :type: typing.Self
    """

    zyww: typing.Self
    """ 

    :type: typing.Self
    """

    zywx: typing.Self
    """ 

    :type: typing.Self
    """

    zywy: typing.Self
    """ 

    :type: typing.Self
    """

    zywz: typing.Self
    """ 

    :type: typing.Self
    """

    zyx: typing.Self
    """ 

    :type: typing.Self
    """

    zyxw: typing.Self
    """ 

    :type: typing.Self
    """

    zyxx: typing.Self
    """ 

    :type: typing.Self
    """

    zyxy: typing.Self
    """ 

    :type: typing.Self
    """

    zyxz: typing.Self
    """ 

    :type: typing.Self
    """

    zyy: typing.Self
    """ 

    :type: typing.Self
    """

    zyyw: typing.Self
    """ 

    :type: typing.Self
    """

    zyyx: typing.Self
    """ 

    :type: typing.Self
    """

    zyyy: typing.Self
    """ 

    :type: typing.Self
    """

    zyyz: typing.Self
    """ 

    :type: typing.Self
    """

    zyz: typing.Self
    """ 

    :type: typing.Self
    """

    zyzw: typing.Self
    """ 

    :type: typing.Self
    """

    zyzx: typing.Self
    """ 

    :type: typing.Self
    """

    zyzy: typing.Self
    """ 

    :type: typing.Self
    """

    zyzz: typing.Self
    """ 

    :type: typing.Self
    """

    zz: typing.Self
    """ 

    :type: typing.Self
    """

    zzw: typing.Self
    """ 

    :type: typing.Self
    """

    zzww: typing.Self
    """ 

    :type: typing.Self
    """

    zzwx: typing.Self
    """ 

    :type: typing.Self
    """

    zzwy: typing.Self
    """ 

    :type: typing.Self
    """

    zzwz: typing.Self
    """ 

    :type: typing.Self
    """

    zzx: typing.Self
    """ 

    :type: typing.Self
    """

    zzxw: typing.Self
    """ 

    :type: typing.Self
    """

    zzxx: typing.Self
    """ 

    :type: typing.Self
    """

    zzxy: typing.Self
    """ 

    :type: typing.Self
    """

    zzxz: typing.Self
    """ 

    :type: typing.Self
    """

    zzy: typing.Self
    """ 

    :type: typing.Self
    """

    zzyw: typing.Self
    """ 

    :type: typing.Self
    """

    zzyx: typing.Self
    """ 

    :type: typing.Self
    """

    zzyy: typing.Self
    """ 

    :type: typing.Self
    """

    zzyz: typing.Self
    """ 

    :type: typing.Self
    """

    zzz: typing.Self
    """ 

    :type: typing.Self
    """

    zzzw: typing.Self
    """ 

    :type: typing.Self
    """

    zzzx: typing.Self
    """ 

    :type: typing.Self
    """

    zzzy: typing.Self
    """ 

    :type: typing.Self
    """

    zzzz: typing.Self
    """ 

    :type: typing.Self
    """

    @classmethod
    def Fill(cls, size: int, fill: float = 0.0):
        """Create a vector of length size with all values set to fill.

        :param size: The length of the vector to be created.
        :type size: int
        :param fill: The value used to fill the vector.
        :type fill: float
        """
        ...

    @classmethod
    def Linspace(cls, start: int, stop: int, size: int):
        """Create a vector of the specified size which is filled with linearly spaced values between start and stop values.

        :param start: The start of the range used to fill the vector.
        :type start: int
        :param stop: The end of the range used to fill the vector.
        :type stop: int
        :param size: The size of the vector to be created.
        :type size: int
        """
        ...

    @classmethod
    def Range(cls, start: int, stop: int, step: int = 1):
        """Create a filled with a range of values.

        :param start: The start of the range used to fill the vector.
        :type start: int
        :param stop: The end of the range used to fill the vector.
        :type stop: int
        :param step: The step between successive values in the vector.
        :type step: int
        """
        ...

    @classmethod
    def Repeat(cls, vector: collections.abc.Sequence[float] | typing.Self, size: int):
        """Create a vector by repeating the values in vector until the required size is reached.

        :param vector: The vector to draw values from.
        :type vector: collections.abc.Sequence[float] | typing.Self
        :param size: The size of the vector to be created.
        :type size: int
        """
        ...

    def angle(
        self,
        other: collections.abc.Sequence[float] | typing.Self,
        fallback: typing.Any = None,
    ) -> float:
        """Return the angle between two vectors.

                :param other: another vector to compare the angle with
                :type other: collections.abc.Sequence[float] | typing.Self
                :param fallback: return this when the angle can't be calculated (zero length vector),
        (instead of raising a `ValueError`).
                :type fallback: typing.Any
                :return: angle in radians or fallback when given
                :rtype: float
        """
        ...

    def angle_signed(
        self, other: collections.abc.Sequence[float] | typing.Self, fallback: typing.Any
    ) -> float:
        """Return the signed angle between two 2D vectors (clockwise is positive).

                :param other: another vector to compare the angle with
                :type other: collections.abc.Sequence[float] | typing.Self
                :param fallback: return this when the angle can't be calculated (zero length vector),
        (instead of raising a `ValueError`).
                :type fallback: typing.Any
                :return: angle in radians or fallback when given
                :rtype: float
        """
        ...

    def copy(self) -> typing.Self:
        """Returns a copy of this vector.

        :return: A copy of the vector.
        :rtype: typing.Self
        """
        ...

    def cross(
        self, other: collections.abc.Sequence[float] | typing.Self
    ) -> typing.Self:
        """Return the cross product of this vector and another.

        :param other: The other vector to perform the cross product with.
        :type other: collections.abc.Sequence[float] | typing.Self
        :return: The cross product.
        :rtype: typing.Self
        """
        ...

    def dot(self, other: collections.abc.Sequence[float] | typing.Self) -> float:
        """Return the dot product of this vector and another.

        :param other: The other vector to perform the dot product with.
        :type other: collections.abc.Sequence[float] | typing.Self
        :return: The dot product.
        :rtype: float
        """
        ...

    def freeze(self) -> typing.Self:
        """Make this object immutable.After this the object can be hashed, used in dictionaries & sets.

        :return: An instance of this object.
        :rtype: typing.Self
        """
        ...

    def lerp(
        self, other: collections.abc.Sequence[float] | typing.Self, factor: float
    ) -> typing.Self:
        """Returns the interpolation of two vectors.

        :param other: value to interpolate with.
        :type other: collections.abc.Sequence[float] | typing.Self
        :param factor: The interpolation value in [0.0, 1.0].
        :type factor: float
        :return: The interpolated vector.
        :rtype: typing.Self
        """
        ...

    def negate(self):
        """Set all values to their negative."""
        ...

    def normalize(self):
        """Normalize the vector, making the length of the vector always 1.0."""
        ...

    def normalized(self) -> typing.Self:
        """Return a new, normalized vector.

        :return: a normalized copy of the vector
        :rtype: typing.Self
        """
        ...

    def orthogonal(self) -> typing.Self:
        """Return a perpendicular vector.

        :return: a new vector 90 degrees from this vector.
        :rtype: typing.Self
        """
        ...

    def project(
        self, other: collections.abc.Sequence[float] | typing.Self
    ) -> typing.Self:
        """Return the projection of this vector onto the other.

        :param other: second vector.
        :type other: collections.abc.Sequence[float] | typing.Self
        :return: the parallel projection vector
        :rtype: typing.Self
        """
        ...

    def reflect(
        self, mirror: collections.abc.Sequence[float] | typing.Self
    ) -> typing.Self:
        """Return the reflection vector from the mirror argument.

        :param mirror: This vector could be a normal from the reflecting surface.
        :type mirror: collections.abc.Sequence[float] | typing.Self
        :return: The reflected vector matching the size of this vector.
        :rtype: typing.Self
        """
        ...

    def resize(self, size=3):
        """Resize the vector to have size number of elements.

        :param size:
        """
        ...

    def resize_2d(self):
        """Resize the vector to 2D  (x, y)."""
        ...

    def resize_3d(self):
        """Resize the vector to 3D  (x, y, z)."""
        ...

    def resize_4d(self):
        """Resize the vector to 4D (x, y, z, w)."""
        ...

    def resized(self, size=3) -> typing.Self:
        """Return a resized copy of the vector with size number of elements.

        :param size:
        :return: a new vector
        :rtype: typing.Self
        """
        ...

    def rotate(
        self,
        other: Euler
        | Matrix
        | Quaternion
        | collections.abc.Sequence[collections.abc.Sequence[float]]
        | collections.abc.Sequence[float],
    ):
        """Rotate the vector by a rotation value.

        :param other: rotation component of mathutils value
        :type other: Euler | Matrix | Quaternion | collections.abc.Sequence[collections.abc.Sequence[float]] | collections.abc.Sequence[float]
        """
        ...

    def rotation_difference(
        self, other: collections.abc.Sequence[float] | typing.Self
    ) -> Quaternion:
        """Returns a quaternion representing the rotational difference between this
        vector and another.

                :param other: second vector.
                :type other: collections.abc.Sequence[float] | typing.Self
                :return: the rotational difference between the two vectors.
                :rtype: Quaternion
        """
        ...

    def slerp(
        self,
        other: collections.abc.Sequence[float] | typing.Self,
        factor: float,
        fallback: typing.Any = None,
    ) -> typing.Self:
        """Returns the interpolation of two non-zero vectors (spherical coordinates).

                :param other: value to interpolate with.
                :type other: collections.abc.Sequence[float] | typing.Self
                :param factor: The interpolation value typically in [0.0, 1.0].
                :type factor: float
                :param fallback: return this when the vector can't be calculated (zero length vector or direct opposites),
        (instead of raising a `ValueError`).
                :type fallback: typing.Any
                :return: The interpolated vector.
                :rtype: typing.Self
        """
        ...

    def to_2d(self) -> typing.Self:
        """Return a 2d copy of the vector.

        :return: a new vector
        :rtype: typing.Self
        """
        ...

    def to_3d(self) -> typing.Self:
        """Return a 3d copy of the vector.

        :return: a new vector
        :rtype: typing.Self
        """
        ...

    def to_4d(self) -> typing.Self:
        """Return a 4d copy of the vector.

        :return: a new vector
        :rtype: typing.Self
        """
        ...

    def to_track_quat(self, track: str, up: str) -> Quaternion:
        """Return a quaternion rotation from the vector and the track and up axis.

        :param track: Track axis in ['X', 'Y', 'Z', '-X', '-Y', '-Z'].
        :type track: str
        :param up: Up axis in ['X', 'Y', 'Z'].
        :type up: str
        :return: rotation from the vector and the track and up axis.
        :rtype: Quaternion
        """
        ...

    def to_tuple(self, precision: int = -1) -> tuple:
        """Return this vector as a tuple with.

        :param precision: The number to round the value to in [-1, 21].
        :type precision: int
        :return: the values of the vector rounded by precision
        :rtype: tuple
        """
        ...

    def zero(self):
        """Set all values to zero."""
        ...

    def __init__(self, seq=(0.0, 0.0, 0.0)):
        """

        :param seq:
        """
        ...

    def __get__(self, instance, owner) -> typing.Self:
        """

        :param instance:
        :param owner:
        :return:
        :rtype: typing.Self
        """
        ...

    def __set__(self, instance, value: collections.abc.Sequence[float] | typing.Self):
        """

        :param instance:
        :param value:
        :type value: collections.abc.Sequence[float] | typing.Self
        """
        ...

    def __len__(self) -> int:
        """

        :return:
        :rtype: int
        """
        ...

    @typing.overload
    def __getitem__(self, key: int) -> float:
        """

        :param key:
        :type key: int
        :return:
        :rtype: float
        """
        ...

    @typing.overload
    def __getitem__(self, key: slice) -> tuple[float, ...]:
        """

        :param key:
        :type key: slice
        :return:
        :rtype: tuple[float, ...]
        """
        ...

    @typing.overload
    def __setitem__(self, key: int, value: float):
        """

        :param key:
        :type key: int
        :param value:
        :type value: float
        """
        ...

    @typing.overload
    def __setitem__(self, key: slice, value: collections.abc.Iterable[float]):
        """

        :param key:
        :type key: slice
        :param value:
        :type value: collections.abc.Iterable[float]
        """
        ...

    def __neg__(self) -> typing.Self:
        """

        :return:
        :rtype: typing.Self
        """
        ...

    def __add__(
        self, other: collections.abc.Sequence[float] | typing.Self
    ) -> typing.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[float] | typing.Self
        :return:
        :rtype: typing.Self
        """
        ...

    def __sub__(
        self, other: collections.abc.Sequence[float] | typing.Self
    ) -> typing.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[float] | typing.Self
        :return:
        :rtype: typing.Self
        """
        ...

    def __mul__(self, other: float | int) -> typing.Self:
        """

        :param other:
        :type other: float | int
        :return:
        :rtype: typing.Self
        """
        ...

    def __truediv__(self, other: float | int) -> typing.Self:
        """

        :param other:
        :type other: float | int
        :return:
        :rtype: typing.Self
        """
        ...

    @typing.overload
    def __matmul__(self, other: collections.abc.Sequence[float] | typing.Self) -> float:
        """

        :param other:
        :type other: collections.abc.Sequence[float] | typing.Self
        :return:
        :rtype: float
        """
        ...

    @typing.overload
    def __matmul__(
        self, other: Matrix | collections.abc.Sequence[collections.abc.Sequence[float]]
    ) -> typing.Self:
        """

        :param other:
        :type other: Matrix | collections.abc.Sequence[collections.abc.Sequence[float]]
        :return:
        :rtype: typing.Self
        """
        ...

    def __radd__(
        self, other: collections.abc.Sequence[float] | typing.Self
    ) -> typing.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[float] | typing.Self
        :return:
        :rtype: typing.Self
        """
        ...

    def __rsub__(
        self, other: collections.abc.Sequence[float] | typing.Self
    ) -> typing.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[float] | typing.Self
        :return:
        :rtype: typing.Self
        """
        ...

    def __rmul__(self, other: float | int) -> typing.Self:
        """

        :param other:
        :type other: float | int
        :return:
        :rtype: typing.Self
        """
        ...

    def __rtruediv__(self, other: float | int) -> typing.Self:
        """

        :param other:
        :type other: float | int
        :return:
        :rtype: typing.Self
        """
        ...

    def __iadd__(
        self, other: collections.abc.Sequence[float] | typing.Self
    ) -> typing.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[float] | typing.Self
        :return:
        :rtype: typing.Self
        """
        ...

    def __isub__(
        self, other: collections.abc.Sequence[float] | typing.Self
    ) -> typing.Self:
        """

        :param other:
        :type other: collections.abc.Sequence[float] | typing.Self
        :return:
        :rtype: typing.Self
        """
        ...

    def __imul__(self, other: float | int) -> typing.Self:
        """

        :param other:
        :type other: float | int
        :return:
        :rtype: typing.Self
        """
        ...

    def __itruediv__(self, other: float | int) -> typing.Self:
        """

        :param other:
        :type other: float | int
        :return:
        :rtype: typing.Self
        """
        ...
