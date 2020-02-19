motif1 = [(1.0, 9), (1.0, 4), (0.5, 5), (0.5, 7), (1.0, 9), (0.5, 5), (0.5, 4), (1.0, 5), (0.5, 2), (0.5, 5), (1.0, 4)]
motif2 = [(1.0, 7), (1.0, 10), (0.5, 12), (0.5, 10), (1.0, 7), (1.5, 5), (0.5, 9), (1.0, 9), (1.0, 14)]
motif3 = []



process = """
for jobs 1 and 2:
	play (all)
	invert (all)
	retrograde (1/2)
	seq-invert-retrograde
	sequence until hit 0
	elaborate-stutter 4 times (1/4)
	return elaborate-stutter/play


for jobs 3 and 4:
	play(all)
	retrograde
	two-play, one retrograde
	inversion of two-play, one retrograde
	sequence 5 times
"""
