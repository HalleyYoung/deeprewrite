:- use_module(library(clpfd)).


withinStep(X,Y) :-
	X - Y #> -24,
	X - Y #< 24.

twelveToneStep(X,Y) :-
	(X - Y) mod 6 == 0.

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


rhythmicDensity(Attacks,N) :- length(Attachs, G1), isTrue(Attacks, Attacks1), length(Attacks1, G2), N #> (G2 div G1) * 4, N #< (G2 div G1) * 4 - 1.

chord([], PCs).
chord([X], PCs) :- X ins PCs.
chord([X | Y], PCs) :- chord([X], PCs), chord(Y, PCs).