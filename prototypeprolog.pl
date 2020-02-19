:- use_module(library(clpfd)).


withinStep(X,Y) :-
	X - Y #> -24,
	X - Y #< 24.

twelveToneStep(X,Y) :-
	(X - Y) mod 6 == 0.

twelveToneNote(Y) :- Y mod 12 is 0.

afterLeap(X,Y,Z) :- 
	X - Y #> 24,
	Y - Z #< 0,
	Y - Z #> -18.

afterLeap(X,Y,Z) :- 
	X - Y #< -24,
	Y - Z #> 0,
	Y - Z #< 18.


dissonantVertical(X,Y,Z) :- (X - Y) ins 1..24.
dissonantVertical(X,Y,Z) :- (Y - X) ins 1..24.
dissonantVertical(X,Y,Z) :- (X - Y) ins 60..71.
dissonantVertical(X,Y,Z) :- (Y - X) ins 60..71.


rhythmicDensity(Attacks,N) :- length(Attacks, G1), isTrue(Attacks, Attacks1), length(Attacks1, G2), N #> (G2 div G1) * 4, N #< (G2 div G1) * 4 - 1.

chord([], PCs).
chord([X], PCs) :- X ins PCs.
chord([X | Y], PCs) :- chord([X], PCs), chord(Y, PCs).


Regex -> pitVars(S1), rhyVars(S2), getMatching(Rs1, S1, S2), getMatching(Rs2, S1, S2), getMatching(Rs3, S1, S2).

pitVars(S) :- length(S) ins 2..4, allInRange(S, 0, 5).
rhyVars(S) :- length(S) ins 2..4, allInRange(S, 0, 3).

allInRange([X], N, M) :- X ins N..M.

 

getMatching([pitVal(P1), rhyVal(R1)], S1, S2) :- isPitRegex(P1), isRhyRegex(R1), isInterp(P1, S1, Ps), isInterp(R1, S2, Rs), length(Ps) #= length(Rs).


isPitRegex(rep(I, N)) :- I in 1..2, N in 1..2.
isPitRegex(seq_down(I, N)) :- I in 1..2, N in 1..2.
isPitRegex(seq_up(I, N)) :- I in 1..2, N in 1..2.
isPitRegex(invert(I)) :L- I in 1..2.
isPitRegex(inertia(N)) :- N in 1..3
inPitRegex(arpUp(N)) :- N in 3..4
inPitRegex(arpDown(N)) :- N in 3..4.

%isInterp(P1, S1, Ps)
isRhyRegex(jagged(N, M)) :- N in 1..2, M in 1..2.
isRhyRegex(smoothen(N,M)) :- N in 1..2, M in 1..2.
isRhyRegex(delHead(N,M)) :- N in 1..2, M in 1..2.
isRhyRegex(delTail(N,M)) :- N in 1..2, M in 1..2.
isRhyRegex(addHead(N,M)) :- N in 1..2, M in 1..3.
isRhyRegex(addTail(N,M)) :- N in 1..2, M in 1..3.

isVar(surface_melody_sub, is_sequence).
isVar(surface_melody_sub, is_scale).
isVar(orchestration, hasInstr(_)).
isVar(orchestration, delInstr(_)).
isVar()
instr()

%isIndividualPitReg()

%properties:


