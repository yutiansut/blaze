"""SQL implementations of element-wise ufuncs."""

from __future__ import absolute_import, division, print_function

from blaze.compute.ops import ufuncs
from .kernel import sql_kernel

#------------------------------------------------------------------------
# Implement functions
#------------------------------------------------------------------------

def define_unop(signature, name, op):
    """Define a unary scidb operator"""
    def unop(x):
        return expr('%s %s' % (op, x))
    unop.__name__ = name
    _implement(unop, signature)
    return unop


def define_binop(signature, name, op):
    """Define a binary scidb operator"""
    def binop(a, b):
        return expr("%s %s %s" % (a, op, b))
    binop.__name__ = name
    _implement(binop, signature)
    return binop


def _implement(f, signature):
    name = f.__name__
    blaze_func = getattr(ufuncs, name)
    #print("implement", f, signature, blaze_func)
    sql_kernel(blaze_func, f, signature)

#------------------------------------------------------------------------
# Arithmetic
#------------------------------------------------------------------------

add = define_binop("a -> a -> a", "add", "+")
mul = define_binop("a -> a -> a", "mul", "*")
sub = define_binop("a : real -> a -> a", "sub", "-")
div = define_binop("a : real -> a -> a", "div", "/")
# floordiv = define_binop("a : real -> a -> a", "floordiv", "//")
# truediv = define_binop("a : real -> a -> a", "truediv", "/")
mod = define_binop("a : real -> a -> a", "mod", "%")

neg = define_unop("a -> a", "neg", "-")

#------------------------------------------------------------------------
# Compare
#------------------------------------------------------------------------

eq = define_binop("a..., T -> a..., T -> a..., bool", "add", "==")
ne = define_binop("a..., T -> a..., T -> a..., bool", "add", "!=")
lt = define_binop("a..., T -> a..., T -> a..., bool", "add", "<")
le = define_binop("a..., T -> a..., T -> a..., bool", "add", "<=")
gt = define_binop("a..., T -> a..., T -> a..., bool", "add", ">")
ge = define_binop("a..., T -> a..., T -> a..., bool", "add", ">=")

#------------------------------------------------------------------------
# Logical
#------------------------------------------------------------------------

logical_and = define_binop("a..., bool -> a..., bool -> a..., bool",
                           "logical_and", "AND")
logical_or  = define_binop("a..., bool -> a..., bool -> a..., bool",
                           "logical_or", "OR")
logical_xor = define_binop("a..., bool -> a..., bool -> a..., bool",
                           "logical_xor", "XOR")
logical_not = define_binop("a..., bool -> a..., bool -> a..., bool",
                           "logical_not", "NOT")

#------------------------------------------------------------------------
# SQL Functions
#------------------------------------------------------------------------

# TODO: AVG, MIN, MAX, SUM, ...

#------------------------------------------------------------------------
# Helper functions
#------------------------------------------------------------------------

def expr(e):
    return "(%s)" % (e,)