module test.

import lists.

kind value_type		type.

type instrs	union (list int) (int).

type time_inst union (list int) (int).

kind valued_type	value_type -> A.

kind pair    type -> type -> type.
type pr      A -> B -> pair A B.

type time 	pair time_inst time_inst.

type times 	list time

kind var  union3 (time) (instrs) (valued_type).

time_defined  var -> o.

instrs_defined	var -> o.

value_defined	var -> o.

type prototype 	valued_type.

Inductive Union (B C:Ensemble) : Ensemble :=
    | Union_introl : forall x:U, In B x -> In (Union B C) x
    | Union_intror : forall x:U, In C x -> In (Union B C) x.