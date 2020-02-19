import random

exps = ["surprise", "m", "rep", "rep-imp", "rep", "inertia", "mag", "gravity", "triad arp"]
transform = ["sequence", "retrograde", "invert", "stutter", "Tx"]

seq = {0:[(5, "m")], 1: []}

for i in range(10):
	if random.uniform(0,1) < 0.8:
		seq[0].append(random.choice(exps))
	else:
		if len(seq[1]) == 0: 
			seq[0].append(	)
			seq[1].append([])
		elif len([k for k in seq[0] if k == len(seq[1])]) < 2 or random.uniform(0,1) < 0.5 and len([k for k in seq[0] if k == len(seq[1])]) < 3:
			seq[0].append(len(seq[1]))
			seq[1].append([])
		else:
			seq[1].append([])
			seq[0].append(len(seq(1)))


for j in range(len(seq[1])):
	for k in range(3):
		seq[1][j].append(random.choice(exps))

