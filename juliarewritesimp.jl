using PyCall

rewrites = quote(
	[ABA(t1, t2)] = [succeeds([t1,t3,t4,t2]), distance(notes(t1,t3), notes(t4,t2), [1,3])]
	[distance(notes(x1,x2), notes(x3,x4), m)] = [distance(rhythm(x1,x2), rhythm(x3,x4), [m - 1, m + 1]), distance(scale(x1,x2), scale(x2,x3), [0,1])]
	[distance(notes(x1,x2), notes(x3,x4), m)] = [distance(rhythm(x1,x2), rhythm(x3,x4), [m - 1, m + 1]), distance(contour(x1,x2), contour(x2,x3), [0,1])]
	[distance(rhythm(x1, x2), rhythm(x3,x4), 2)] = retrograde(rhythm(x1, x2), rhythm(x3,x4))
	[distance(rhythm(x1, x2), rhythm(x3,x4), 1)] = pdistance(rhythmSync(x1, x2), rhythmSync(x3,x4),0), distance(rhyDens(x1,x2), rhyDens(x3,x4), 0)]
end

