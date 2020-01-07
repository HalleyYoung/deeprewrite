#defining parts of a sonata
[sonata(t1, t2)] = x => [P(t1, t3), TR(t3, t4), S(t4,t5), MC(t5,t6), D(t6,t7), R(t7)]
#defining relationship between P, TR, and S of sonata
[P(t1,t2), TR(t2,t3), S(t3,t4)] = [distance((t1,t2), (t2,t3), [1,3]), distance((t2,t3), (t3,t4), [1,3]), restless((t1,t2), m), restless((t3,t4), [m + 1, m + 3])]


#defining distance with respect to division of lengths of time
[distance((t1,t2),(t3,t4),m)] = [distance(t1,t2), (t3,t5), [m - 1, m], distance(t1,t2), (t5,t6), [m - 1, m]]
#defining distance with respect to parts
[distance(t1,t2), (t3,t4), m) = partDistance((t1,t2), (t3,t4), is, [m - 2, m]), isMelody((t1,t2), is)


#defining distance metric with respect to diatonicTranspose
[distance(t1,t2), (t3,t4), 1), scale(t1,t4, c), t2 - t1 = t4 - t3] = [diatonicTranspose((t1,t2),(t3,t4, c)]

#defining when to fill in notes
[scale(t1,t2), contour(t1,t2), rhythm(t1,t2)] = fillInNotes(t1,t2)

[distance(t1,t2), (t3,t4),m), t2 - t1 > x, t4 - t3 > x,] = [scale(t1, t2, m), scale(t3,t4,m), distanceIntervals(t1,t2,[m,m + 2]), distanceRhythm((t1,t2), (t3,t4), [m,m + 2])]
hindustani(t1,t2) = unmetered(t1,t3), additiveMeter(t3,t2)
hindustani(t1,t2) = raga(t1,t2, c)
emphasizesNotes(t1,t2,*cs), tonic(t1,t2,*c2) = fillInRaga((c2,cs))
