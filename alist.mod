module alist.

import lists.

kind pair    type -> type -> type.
type pr      A -> B -> pair A B.

type assoc, assod   A -> B -> list (pair A B) -> o.

assoc X Y L :- memb   (pr X Y) L.
assod X Y L :- member (pr X Y) L.

type domain         list (pair A B) -> list A -> o.

domain nil nil.
domain ((pr X Y)::Alist) (X::L) :- domain Alist L.

type range          list (pair A B) -> list B -> o.

range nil nil.
range ((pr X Y)::Alist) (Y::L)  :- range Alist L.
