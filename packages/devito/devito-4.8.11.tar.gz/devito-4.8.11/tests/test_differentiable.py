import sympy
from devito import Function, Grid, Differentiable
from devito.finite_differences.differentiable import Add, Mul, Pow, diffify


def test_differentiable():
    a = Function(name="a", grid=Grid((10, 10)))
    e = Function(name="e", grid=Grid((10, 10)))

    assert isinstance(1.2 * a.dx, Mul)
    assert isinstance(e + a, Add)
    assert isinstance(e * a, Mul)
    assert isinstance(a * a, Pow)
    assert isinstance(1 / (a * a), Pow)

    addition = a + 1.2 * a.dx
    assert isinstance(addition, Add)
    assert all(isinstance(a, Differentiable) for a in addition.args)

    addition2 = a + e * a.dx
    assert isinstance(addition2, Add)
    assert all(isinstance(a, Differentiable) for a in addition2.args)


def test_diffify():
    a = Function(name="a", grid=Grid((10, 10)))
    e = Function(name="e", grid=Grid((10, 10)))

    assert isinstance(diffify(sympy.Mul(*[1.2, a.dx])), Mul)
    assert isinstance(diffify(sympy.Add(*[a, e])), Add)
    assert isinstance(diffify(sympy.Mul(*[e, a])), Mul)
    assert isinstance(diffify(sympy.Mul(*[a, a])), Pow)
    assert isinstance(diffify(sympy.Pow(*[a*a, -1])), Pow)

    addition = diffify(sympy.Add(*[a, sympy.Mul(*[1.2, a.dx])]))
    assert isinstance(addition, Add)
    assert all(isinstance(a, Differentiable) for a in addition.args)

    addition2 = diffify(sympy.Add(*[a, sympy.Mul(*[e, a.dx])]))
    assert isinstance(addition2, Add)
    assert all(isinstance(a, Differentiable) for a in addition2.args)


def test_shift():
    a = Function(name="a", grid=Grid((10, 10)))
    x = a.dimensions[0]
    assert a.shift(x, x.spacing) == a._subs(x, x + x.spacing)
    assert a.shift(x, x.spacing).shift(x, -x.spacing) == a
    assert a.shift(x, x.spacing).shift(x, x.spacing) == a.shift(x, 2*x.spacing)
    assert a.dx.evaluate.shift(x, x.spacing) == a.shift(x, x.spacing).dx.evaluate
    assert a.shift(x, .5 * x.spacing)._grid_map == {x: x + .5 * x.spacing}
