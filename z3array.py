"""
s = Solver()
has_melody_degs = Array("has_melody_degs", IntSort(), IntSort())
melody_degs = Array("melody_degs", IntSort(), IntSort())
melody_pits = Array("melody_pits", IntSort(), IntSort())
melody_durs = Array("melody_durs", IntSort(), IntSort())
melody_onsets = Array("melody_onsets", IntSort(), IntSort())
melody_n = Int("melody_n")
melody_i = Int("melody_i")
melody_z = Int("melody_z")
deg_seq_var = Array("deg_seq", IntSort(), IntSort())
for i in range(len(deg_seq)):
	s.add(deg_seq_var[i] == deg_seq[i])
s.add(melody_n < 40)
s.add(melody_n < 10)
s.add(melody_degs[0] == 0)
s.add(has_melody_degs[0] == 0)
s.add(ForAll(melody_i, Implies(And(melody_i < len(deg_seq), melody_i > 0), has_melody_degs[i] - has_melody_degs[i - 1] <= 3)))
s.add(ForAll(melody_i, Implies(And(melody_i < len(deg_seq), melody_i > 0), ForAll(melody_z, Implies(has_melody_degs[melody_i] == melody_z, melody_degs[melody_z] == deg_seq_var[melody_i])))))

s.check()
"""