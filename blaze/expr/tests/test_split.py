from blaze.expr import *
from blaze.expr.split import *
from blaze.api.dplyr import transform
import datashape

t = TableSymbol('t', '{name: string, amount: int, id: int}')


def test_path_split():
    expr = t.amount.sum() + 1
    assert path_split(t, expr).isidentical(t.amount.sum())

    expr = t.amount.distinct().sort()
    assert path_split(t, expr).isidentical(t.amount.distinct())

    t2 = transform(t, id=t.id * 2)
    expr = by(t2.id, amount=t2.amount.sum()).amount + 1
    assert path_split(t, expr).isidentical(by(t2.id, amount=t2.amount.sum()))

    expr = count(t.amount.distinct())
    assert path_split(t, expr).isidentical(t.amount.distinct())



def test_sum():
    (chunk, chunk_expr), (agg, agg_expr) = split(t, t.amount.sum())

    assert chunk.schema == t.schema
    assert chunk_expr.isidentical(chunk.amount.sum())

    assert agg.iscolumn
    assert agg_expr.isidentical(sum(agg))


def test_distinct():
    (chunk, chunk_expr), (agg, agg_expr) = split(t, count(t.amount.distinct()))

    assert chunk.schema == t.schema
    assert chunk_expr.isidentical(chunk.amount.distinct())

    assert agg.iscolumn
    assert agg_expr.isidentical(count(agg.distinct()))
