# hieretikz
Generate a tikz diagram of a hierarchy, for use in reverse mathematics


Terminology
===========

model
-----
A model is a triple `(name, low, high)`, where `name` is a string, and `low`
and `high` are frozen sets of formulae.

proof
-----
A proof is a tuple `(premise1, ..., premisen, conclusion)`.


separation
----------
A separation is a model, but is used only in the hierarchy context.

edge
----
An edge is a proof, but is used only in the hierarchy context.

pathtree
--------
A path tree from `V` to `w` gives the edges that connect `V` to `w`, defined
inductively by
```
	T(V, v) = ()
    T(V, w) = ((t1, ..., tn, w), T(V, t1), ..., T(V, tn))
```
(where `v` is in `V`).

downward closure
----------------
The downward closure for a vertex set `V` is a dictionary mapping each vertex
`w` reachable from `V` to the path tree from `V` to `w`.

complete separation
-------------------
From a separation `(name, low, high)`, a vertex set `V`, and an edge set `E`, a
complete separation `(name, closed, comphigh)` satisfies that
* If a member of `low` is in the downward closure of `v`, then `v` is in
  `complow`
* If `w` is in the downward closure of `high`, then `w` is in `comphigh`


separating triple
----------------
A separating triple for `V` and `w` is a triple `(sep_name, to_low, from_high)`
where `sep_name` is the name of a separation `(sep_name, low, high)`, `to_low`
is a pathtree from `V` to some element of `low`, and `from_high` is a pathtree
from `high` to `w`.
