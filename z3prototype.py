from z3 import *
#exec(open("z3prototype.py").read())

spec = [("theme1", (0,20)), ("bollywood", (0,40)), ("theme2", (20,30)), ("sci-fi", (30,40)), (["theme1", "theme2"], (30,40))]

#theme1_cats = [("rhythm", [1.0, 0.25, 0.75, 1.0]), ("deg_seq", [0,2,4,3,5,5,3,0]), ("rhythm_retrograde"), ("rhythmic_density", "mild")]
#theme2_cats = [("angularity", "high"), ("deg_seq", (0,8,5,4,4,1,0,0)), ("inversion"), ("_has_melody", "sitar")]

deg_seq = [0,2,4,3,5,5,3,0]
s = Solver()

glissando = {}
in_tuplets = False


num_tacti = 40*2*4*3*5

instrs = ["Violin", "Synth Pad",  "Sitar", "Flute", "Ethereal Choir"]
unpitched_instrs = ["Tabla"]

#a = simplify(s.model()[deg_seq_var][0])
#instrs_sound = [[Bool("sound_" + num_tact + "_instr_" + instr) for num_tact in num_tacti] for instr in instrs]
#instrs_attack = [[Bool("attack_" + num_tact + "_instr_" + instr) for num_tact in num_tacti] for instr in instrs]
#instrs_pitch = [[Int("pitch_" + num_tact + "_instr_" + instr) for num_tact in num_tacti] for instr in instrs]
#instrs_dynamic = [[Int("dynamic_" + num_tact + "_instr_" + instr) for num_tact in num_tacti] for instr in instrs]

instrs_sound_his = [[] for instr in instrs]
instrs_attack_his = [[] for instr in instrs]
instrs_pitch_his = [[] for instr in instrs]
instrs_dynamic_his = [[] for instr in instrs]
pitch_is_deg_his = []
deg_ind = 0

meter_hits = []
prev_beat = 0
for i in range(0,num_tacti):
	if i % 3*4*5 == 0:
		meter_hits.append({0:2,1:1,2:1,3:2,4:1}[prev_beat])
	elif i % 3*2*5 == 0:
		meter_hits.append(0)
	else:
		meter_hits.append(-1)

for num_tact in range(num_tacti):
	s = Solver()
	instrs_sound = [Bool("sound_" + str(num_tact) + "_instr_" + instr) for instr in instrs]
	instrs_attack = [Bool("attack_" + str(num_tact) + "_instr_" + instr) for instr in instrs]
	instrs_pitch = [Int("pitch_" + str(num_tact) + "_instr_" + instr) for instr in instrs]
	instrs_dynamic = [Int("dynamic_" +  "_instr_" + instr) for instr in instrs]
	for i in range(len(instrs)):
		s.add(instrs_pitch[i] < 72*4)
		s.add(instrs_pitch[i] >= 0)
		
		if not in_glissando[i]:
			s.add(instrs_pitch[i] % 6 == 0)
		elif len(instrs_pitch_his[i] > 0):
			s.add(instrs_pitch[i] - instrs_pitch_his[-1]) == 1


		if len(instrs_pitch_his[i]) > 0 and instrs_sound_his[-1]:
			s.add(instrs_pitch[i] - instrs_pitch_his[i][-1] < 78)
			s.add(instrs_pitch[i] - instrs_pitch_his[i][-1] > -78)
		if len(instrs_pitch_his[i]) > 1 and instrs_sound_his[i][-1]:
			s.add(If(And(instrs_pitch[i] - instrs_pitch_his[i][-2] > 4*6, instrs_attack_his[i]), And(instrs_pitch[i] - instrs_pitch_his[i][-1] < 0, instrs_pitch[i] - instrs_pitch_his[i][-1] > -3*6)))
			s.add(If(And(instrs_pitch[i] - instrs_pitch_his[i][-2] < -4*6, instrs_attack_his[i]), And(instrs_pitch[i] - instrs_pitch_his[i][-1] > 0, instrs_pitch[i] - instrs_pitch_his[i][-1] < -3*6)))

	for i in range(len(instrs)):
		for j in range(i + 1, len(instrs)):
			s.add(Implies(And(instrs_attack[i], instrs_attack[j]), And([(instrs_pitch[i] - instrs_pitch[j]) % 12 != k for k in list(range(1,24)) + list(range(72 - 24, 72))])))
			s.add(Implies(And(instrs_attack[i], instrs_attack[j]), And([(instrs_pitch[j] - instrs_pitch[i]) % 12 != k for k in list(range(1,24)) + list(range(72 - 24, 72))])))
			s.add(Implies(And(instrs_sound[i], instrs_sound[j]), And([(instrs_pitch[j] - instrs_pitch[i]) % 12  != k for k in list(range(1,24))])))
			s.add(Implies(And(instrs_sound[i], instrs_sound[j]), And([(instrs_pitch[i] - instrs_pitch[j]) % 12 != k for k in list(range(1,24))])))


	if meter_hits[num_tact] == 2:
		s.add(Or(instrs_attack))
	elif meter_hits[num_tact] == -1:
		for i in range(len(instrs)):
			for j in range(i + 1, len(instrs)):
				s.add(Not(And(instrs_attack[i], instrs_attack[j])))
	elif meter_hits[num_tact] == 1 and len(instrs_attack_his) > 3*4*5 and not any(instrs_attack_his[-3*4*5]):
		s.add(Or(instrs_attack))

	if not in_tuplets and num_tact % (3*5) != 0 and not not any([i in glissando for i in range(num_tact + 15)]):
		s.add(Not(Or(instrs_attack)))

	melody_instr = 3
	if not any([pitch_is_deg_his[melody_instr][k] for k in range(max(-3*4*5*3, len(pitch_is_deg_his)*-1),0)]):
		s.add(instrs_sound[melody_instr])
		s.add(instrs_pitch[melody_instr] % 12 == scales[cur_deg])


	s.check()
	model = s.model()
	for i in range(len(instrs)):
		instrs_pitch_his[i].append(model[instrs_pitch[i]])
		instrs_sound_his[i].append(model[instrs_sound[i]])
		instrs_attack_his[i].append(model[instrs_attack[i]])
		instrs_dynamic_his[i].append(model[instrs_dynamic[i]])
	print(instrs_pitch_his) 

