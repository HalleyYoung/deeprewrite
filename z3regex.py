import z3

reg_types = "0|1|2|j|s|a|d|t|h|dt|dh".split("|")

reg_rhy1 = [Int("reg_rhy_1_" + str(i)) for i in range(5)]
reg_rhy2 = [Int("reg_rhy_2_" + str(i)) for i in range(5)]
reg_rhy3 = [Int("reg_rhy_3_" + str(i)) for i in range(5)]
reg_pats = [[Int("reg_pat_" + str(j) + "_" + str(i)) for i in range(4)] for j in range(2)]


s = Solver()
for i in range(len(reg_rhy1)):
	s.add(And(reg_rhy1[i] >= 0,reg_rhy1[i] < len(reg_types) + 1))
	s.add(And(reg_rhy2[i] >= 0, reg_rhy2[i] <= 2))
	s.add(And(reg_rhy3[i] >= 1, reg_rhy3[i] <= 3))
	s.add(Implies(Not(reg_rhy3[i] == len(reg_types)), reg_rhy3_i < 3))

for i in range(len(reg_pats)):
	s.add(And(reg_pats[i][0] >= 0, reg_pats[i][0] <= 2))
	s.add(And(reg_pats[i][1] >= 0, reg_pats[i][1] <= 2))
	s.add(And(reg_pats[i][2] >= -1, reg_pats[i][1] <= 2))
	s.add(And(reg_pats[i][3] >= -1, reg_pats[i][1] <= 2))
	s.add(Implies(reg_pats[2] == -1, reg_pats[3] == -1))
	s.add(Not(And([Or(reg_pats[i][j] == reg_pats[i][j + 1], reg_pats[i][j + 1] == -1) for j in range(1, len(reg_pats[i]))])))


len_reg = Int("len_reg")

len_pats = [Int("len_pats_" + str(i)) for i in range(2)]

s.add(If(reg_pats[0][2] == -1, len_pats[0] == 2, If(reg_pats[0][3] == -1, len_pats[0] == 3, len_pats[0] == 4)))
s.add(If(reg_pats[1][2] == -1, len_pats[1] == 2, If(reg_pats[1][3] == -1, len_pats[1] == 3, len_pats[1] == 4)))


len_each = [Int("len_" + str(i)) for i in range(5)]

for i in range(5):
	s.add(Implies(reg_rhy1[i] == reg_types.index("1"), len_each[i] == reg_rhy2[i]))
	s.add(Implies(reg_rhy1[i] == reg_types.index("2"), len_each[i] == reg_rhy2[i]))
	s.add(Implies(And(reg_rhy3[i] == 1, reg_rhy1[i] == reg_types.index("j")), len_each[i] == len_pats[0]))
	s.add(Implies(And(reg_rhy3[i] == 2, reg_rhy1[i] == reg_types.index("j")), len_each[i] == len_pats[1]))
	s.add(Implies(And(reg_rhy3[i] == 1, reg_rhy1[i] == reg_types.index("s")), len_each[i] == len_pats[0]))
	s.add(Implies(And(reg_rhy3[i] == 2, reg_rhy1[i] == reg_types.index("s")), len_each[i] == len_pats[1]))
	s.add(Implies(And(reg_rhy3[i] == 1, reg_rhy1[i] == reg_types.index("a")), len_each[i] == len_pats[0]))
	s.add(Implies(And(reg_rhy3[i] == 2, reg_rhy1[i] == reg_types.index("a")), len_each[i] == len_pats[1]))
	s.add(Implies(And(reg_rhy3[i] == 1, reg_rhy1[i] == reg_types.index("d")), len_each[i] == len_pats[0]))
	s.add(Implies(And(reg_rhy3[i] == 2, reg_rhy1[i] == reg_types.index("d")), len_each[i] == len_pats[1]))
	s.add(Implies(And(reg_rhy3[i] == 1, reg_rhy1[i] == reg_types.index("h")), len_each[i] == len_pats[0] + 1))
	s.add(Implies(And(reg_rhy3[i] == 2, reg_rhy1[i] == reg_types.index("h")), len_each[i] == len_pats[1] + 1))	
	s.add(Implies(And(reg_rhy3[i] == 1, reg_rhy1[i] == reg_types.index("t")), len_each[i] == len_pats[0] + 1))
	s.add(Implies(And(reg_rhy3[i] == 2, reg_rhy1[i] == reg_types.index("t")), len_each[i] == len_pats[1] + 1))
	s.add(Implies(And(reg_rhy3[i] == 1, reg_rhy1[i] == reg_types.index("dt"), len_each[i] == len_pats[0] - reg_rhy3[i])))
	s.add(Implies(And(reg_rhy3[i] == 2, reg_rhy1[i] == reg_types.index("dt"), len_each[i] == len_pats[1] - reg_rhy3[i])))
	s.add(Implies(And(reg_rhy3[i] == 1, reg_rhy1[i] == reg_types.index("dh"), len_each[i] == len_pats[0] - reg_rhy3[i])))
	s.add(Implies(And(reg_rhy3[i] == 2, reg_rhy1[i] == reg_types.index("dh"), len_each[i] == len_pats[1] - reg_rhy3[i])))

mel_types = "rep_up, rep_continue_up, rep_down, rep_continue_down, invert, rep, arp, m, forces".split(", ")

reg_mel1 = [Int("reg_mel_1_" + str(i)) for i in range(5)]
reg_mel2 = [Int("reg_mel_2_" + str(i)) for i in range(5)]
reg_mel3 = [Int("reg_mel_3_" + str(i)) for i in range(5)]
reg_mel_pats = [[Int("reg_mel_pat_" + str(j) + "_" + str(i)) for i in range(4)] for j in range(2)]

len_each_mel = [Int("len_mel_each_" + str(i)) for i in range(5)]
len_mel_pats = [Int("len_mel_pat_" + str(i)) for i in range(2)]





for i in range(len(reg_mel_pats)):
	s.add(And(reg_mel_pats[i][0] >= 0, reg_mel_pats[i][0] <= 2))
	s.add(And(reg__mel_pats[i][1] >= 0, reg_mel_pats[i][1] <= 2))
	s.add(And(reg_mel_pats[i][2] >= -1, reg_mel_pats[i][1] <= 2))
	s.add(And(reg_mel_pats[i][3] >= -1, reg_mel_pats[i][1] <= 2))
	s.add(Implies(reg_mel_pats[2] == -1, reg_mel_pats[3] == -1))
	s.add(Not(And([Or(reg_mel_pats[i][j] == reg_mel_pats[i][j + 1], reg_mel_pats[i][j + 1] == -1) for j in range(1, len(reg_mel_pats[i]))])))


for i in range(5):
	s.add(And(reg_mel1[i] >= 0, reg_mel1[i] < len(mel_types)))
	s.add(And(reg_mel2[i] >= 1, reg_mel2[i] <= 3))
	s.add(And(reg_mel3[i] >= 1, reg_mel3[i] <= 3))


	s.add(Implies(And(reg_mel1[i] == mel_types.index("rep_up"), reg_rhy3[i] == 1), len_each_mel[i] == reg_rhy2[i]*len_mel_pats[0]))
	s.add(Implies(And(reg_mel1[i] == mel_types.index("rep_up"), reg_rhy3[i] == 2), len_each_mel[i] == reg_rhy2[i]*len_mel_pats[1]))
	s.add(Implies(And(reg_mel1[i] == mel_types.index("rep_down"), reg_rhy3[i] == 1), len_each_mel[i] == reg_rhy2[i]*len_mel_pats[0]))
	s.add(Implies(And(reg_mel1[i] == mel_types.index("rep_down"), reg_rhy3[i] == 2), len_each_mel[i] == reg_rhy2[i]*len_mel_pats[1]))
	s.add(Implies(And(reg_mel1[i] == mel_types.index("rep_continue_up"), reg_rhy3[i] == 1), len_each_mel[i] == reg_rhy2[i]*len_mel_pats[0]))
	s.add(Implies(And(reg_mel1[i] == mel_types.index("rep_continue_up"), reg_rhy3[i] == 2), len_each_mel[i] == reg_rhy2[i]*len_mel_pats[1]))
	s.add(Implies(And(reg_mel1[i] == mel_types.index("rep_continue_down"), reg_rhy3[i] == 1), len_each_mel[i] == reg_rhy2[i]*len_mel_pats[0]))
	s.add(Implies(And(reg_mel1[i] == mel_types.index("rep_continue_down"), reg_rhy3[i] == 2), len_each_mel[i] == reg_rhy2[i]*len_mel_pats[1]))
	s.add(Implies(reg_mel1[i] == mel_types.index("arp"), len_each_mel[i] == reg_rhy2[i]))
	s.add(Implies(reg_mel1[i] == mel_types.index("m"), len_each_mel[i] == 1))
	s.add(Implies(reg_mel1[i] == mel_types.index("forces"), len_each_mel[i] == reg_rhy2[i]))

tot_len_rhy = Int("tot_len_rhy")
tot_len_mel = Int("tot_len_mel")

s.add(tot_len_rhy == Sum(len_each))
s.add(tot_len_mel == Sum(len_each_mel))
s.add(tot_len_rhy == tot_len_mel)
s.add(Or(len_each[0] + len_each[1] == len_each_mel[0] + len_each_mel[1], len_each[-1] + len_each[-2] == len_each_mel[-1] + len_each_mel[-2]))


s.check()
model = s.model()

rhy_conts = []
for i in range(5):
	rhy_type = reg_types[reg_types.index(model[reg_rhy1[i]])]
	if rhy_type == "0":
		rhy_conts.extend([0 for j in range(model[reg_rhy2[i]])])
	elif rhy_type == "1":
		rhy_conts.extend([1 for j in range(model[reg_rhy2[i]])])
	elif rhy_type == "2":
		rhy_conts.extend([2 for j in range(model[reg_rhy2[i]])])
	elif rhy_type == "a":
		rhy_conts.extend([model[reg_pats[model[reg_rhy3[i]]]][j] + 1 for j in range(model[len_pats[model[reg_rhy3[i]]]])])


mel_conts = []


rhy_conts_map = {0:0.25, 1:0.5, 2:0.75, 3:1.0, 4:1.5, 5:2.0, 6:3.0}



