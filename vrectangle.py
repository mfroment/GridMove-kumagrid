from fractions import Fraction


# a Vrectangle is a rectangle defined by its top, left, bottom, right coordinates as
# proportions of height & width of a parent canvas (itself a Vrectangle or None if top-level aka root canvas)
# top, left, bottom, right are handled as Fraction
class Vrectangle:
    def __init__(self, top=Fraction(0), left=Fraction(0),
                 bottom=Fraction(1), right=Fraction(1),
                 canvas=None):
        self.top = self._frac(top)
        self.left = self._frac(left)
        self.bottom = self._frac(bottom)
        self.right = self._frac(right)
        self.canvas = canvas
        if self.height() <= 0 or self.width() <= 0:
            raise ValueError("height and width must be strictly positive")

    def __str__(self):
        return ("" if self.canvas is None else f"{self.canvas} / ") + \
               f"[{self.top} {self.left}|{self.bottom} {self.right}]"

    def width(self):
        return self.right - self.left

    def height(self):
        return self.bottom - self.top

    def reframe(self, canvas=None):
        # return a Vrectangle reframed in the coordinate scheme of provided canvas
        reframed = self._reframe_root()
        # if input canvas is the root one, we are done
        if canvas is None:
            return reframed
        # otherwise, we need to reframe wrt to provided canvas
        # calculations are easier using reframed Vrectangle and canvas wrt root canvas
        reframed_canvas = canvas._reframe_root()
        top = (reframed.top - reframed_canvas.top) / reframed_canvas.height()
        bottom = (reframed.bottom - reframed_canvas.top) / reframed_canvas.height()
        left = (reframed.left - reframed_canvas.left) / reframed_canvas.width()
        right = (reframed.right - reframed_canvas.left) / reframed_canvas.width()
        return Vrectangle(top, left, bottom, right, canvas)

    def _reframe_once(self):
        # reframe wrt to parent canvas's canvas
        # if parent canvas is root canvas, we are done
        if self.canvas is None:
            return self
        # otherwise, compute top, bottom, left, right wrt to parent canvas's canvas
        top = self.canvas.top + self.top * self.canvas.height()
        bottom = self.canvas.top + self.bottom * self.canvas.height()
        left = self.canvas.left + self.left * self.canvas.width()
        right = self.canvas.left + self.right * self.canvas.width()
        canvas = self.canvas.canvas
        return Vrectangle(top, left, bottom, right, canvas)

    def _reframe_root(self):
        # reframe wrt to root canvas
        # if parent canvas is root canvas, we are done
        if self.canvas is None:
            return self
        # otherwise, call recursively on Vrectangle reframed wrt parent canvas's canvas
        return self._reframe_once()._reframe_root()

    def __eq__(self, other):
        if other is None:
            other = Vrectangle(0, 0, 1, 1, None)
        if not isinstance(other, Vrectangle):
            return NotImplemented
        reframed = self._reframe_root()
        reframed_other = other._reframe_root()
        return reframed.top == reframed_other.top and reframed.left == reframed_other.left and \
            reframed.bottom == reframed_other.bottom and reframed.right == reframed_other.right

    @staticmethod
    def _frac(value):
        return Fraction(value).limit_denominator()
