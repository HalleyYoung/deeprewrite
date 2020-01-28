from z3 import *

#exec(open("z3isms.py").read())

def notNotTwo(Vars):
	xs = []
	for i in range(len(Vars)):
		for j in range(i + 1, len(Vars)):
			xs.append(Not(And(Not(Vars[i]), Not(Vars[j]))))
	return And(xs)

spec = [("theme1", (0,20)), ("bollywood", (0,40)), ("theme2", (20,30)), ("sci-fi", (30,40)), (["theme1", "theme2"], (30,40))]


tick = 5
###
#all variables

harmonic = ["ostinato_degs", "pedal_deg", "is_harmonic", "chord_progression", "chord_thickness", "cadence_type", "has_symmetric_scale", "extended_chords", "uses_quartal_quintal", "twelve_tone_mode", "is_twelve_tone", "dissonance"]
voice_leading = ["close_voice_leading"]
melodic = ["degree_seq", "contour", "note_seq", "melody_register"]
rhythmic = ["ostinato_rhythm", "rhythmic_density", "rhythmic_angularity", "rhythmic_syncopation", "meter", "is_polymeter", "is_polybeat", "is_additive_meter"]
melodic_transformations = ["retrograde", "retrograde_inversion", "inversion", "transposition", "elaboration", "simplification", "make_angular"]
rhythmic_transformations = ["retrograde_rhythm", "make_rhythm_angular", "replace_duples_triples", "diminutionStutter", "diminutionRepeat", "diminution", "augmentation", "elaborate", "simplify"]
scale_transformations = ["change_mode", "change_root", "transpose_scale"]
harmonic_transformations = []
textural = ["has_counter_melody", "has_accompaniment", "has_drone", "has_pedal", "has_ostinato", "has_sus_chords", "has_glissandi", "polyphony", "stereotyped_accompaniment_type"] 
textural_transformations = ["_".join(["add"] + i.split("_")[1:]) for i in textural] + ["_".join(["remove]"] + i.split("_")[1:]) for i in textural]
drums = ["has_unpitched", "unpitched_type", "has_tabla", "has_african", "has_western"]
orchestration = ["_has_glissandi", "_has_melody", "solo_tutti", "_has_accompaniment", "_has_sus_chords", "_has_drone", "_has_pedal", "_has_counter_melody", "_has_ostinato"]
orchestral_transformations = ["add_instrument", "add_instrument_type", "change_instrument_type", "remove_instrument_type", "remove_instrument"]
instr_types = ["woodwind", "synth", "brass", "strings", "percussion"]
finer_instr_types = ["unpitched_instrs", "woodwind_instrs", "brass_instrs", "synth_instrs"]
has_instr_types = ["has_" + str(instr_type) for instr_type in instr_types]
other = ["has_crescendo"]
varis = [(a, globals()[a]) for a in "other, finer_instr_types, has_instr_types, harmonic, voice_leading, melodic, rhythmic, rhythmic_transformations, melodic_transformations, scale_transformations, harmonic_transformations, textural, drums, orchestration, orchestral_transformations, textural_transformations".split(", ")] 

####

implies = [("chord_thickness", "is_harmonic"), ("uses_quartal_quintal", "is_harmonic"), ("close_voice_leading", "is_harmonic"), ("chord_progression", "is_harmonic"), ("chord_progression", "is_twelve_tone"), \
("is_polymeter", "polyphony"), ("is_polybeat", "polyphony"), ("cadence_type", ["is_harmonic", "is_twelve_tone"]), ("twelve_tone_mode", "is_twelve_tone"), ("extended_chords", ["is_harmonic", ("uses_quartal_quintal", False)]), \
("unpitched_type", "has_unpitched"), ("unpitched_instrs", "has_unpitched"), ("stereotyped_accompaniment_type", "has_accompaniment"), ("pedal_deg", "has_pedal"), ("ostinato_rhythm", "has_ostinato"), ("ostinato_degs", "has_ostinato"), \
("_has_counter_melody", "has_counter_melody")]


styles = ["horror", "sci-fi", "bollywood", "romance"]

all_vars = set()
for (var_type, vars_of_type) in varis:
	for var_of_type in vars_of_type:
		all_vars.add(var_of_type)
all_vars = list(all_vars)

open("muvars.txt", "w+").write("\n".join(list(all_vars)))
 
themes = ["theme1", "theme2"]

s = Solver()

time_is_defined_vars = [[Bool("is_defined_" + var + "_" + attr) for var in all_vars] for attr in ["t(" + str(i) + ", " + str(i + 10) + ")" for i in range(0,40,tick)]]
theme_is_defined_vars = [[Bool("is_defined_" + var + "_" + attr) for var in all_vars] for attr in ["theme1", "theme2"]]


time_enum_vals = {}
theme_enum_vals = {}



enum_values = {}
enum_values["chord_thickness"] = ["mild", "medium", "extended"]
enum_values["progression"] = ["andalusian", "deceptive", "four-chords", "mario", "pan-triadic"]
enum_values["remove_instrument_type"] = instr_types 
enum_values["add_instrument_type"] = instr_types
for val in orchestration:
	enum_values[val] = instr_types
enum_values["rhythmic_angularity"] = ["mild", "medium", "extended"]
enum_values["rhythmic_density"] = ["mild", "medium", "extended"]
enum_values["melody_register"] = [3,4,tick]
enum_values["12_tone_mode"] = ["major", "minor", "harmonic_minor", "lydian", "dorian", "mixolydian", "phrygian", "whole_tone", "octatonic"]

enum_vals = []
for (k, vs) in enum_values.items():
	time_enum_vals[k] = ([[Bool(str(attr) + "_" + k + "_is_" + str(v)) for v in vs] for attr in [str(i) for i in range(0,40,tick)]])
	theme_enum_vals[k] = ([[Bool(str(attr) + "_" + k + "_is_" + str(v)) for v in vs] for attr in  ["theme1", "theme2"]])

for val in all_vars:
	if val not in enum_values:
		time_enum_vals[val] = [Bool(str(attr) + "_" + val) for attr in range(0,40,tick)]
		theme_enum_vals[val] = [Bool(attr + "_" + val) for attr in  ["theme1", "theme2"]]


###3
#which variables increases tension by x amount
tension = [Int("tension_ind_" + i) for i in map(str, range(0,40,tick))]

#defines tension metric
for i in range(0,40,tick):
	s.add(tension[i] >= 0)
	s.add(tension[i] <= 3)
	s.add(Implies(tension[i] == 0, Or([Sum([1 if k else 0 for k in [time_enum_vals["has_crescendo"][i//tick], time_enum_vals["has_glissandi"[i//tick], time_enum_vals["rhythmic_density"][i//tick][2], time_enum_vals["rhythmic_angularity"][i//tick][2], time_enum_vals["dissonance"][i//tick][2], time_enum_vals["has_ostinato"][i//tick]]]]) == z for z in [0,1]])))
	s.add(Implies(tension[i] == 1, Or([Sum([1 if k else 0 for k in []]) == z for z in [1,3]])))
	s.add(Implies(tension[i] == 2, Or([Sum([1 if k else 0 for k in []]) == z for z in [2,4]])))
	s.add(Implies(tension[i] == 3, Or([Sum([1 if k else 0 for k in []]) == z for z in [3,7]])))



###
#which variables suggest bollywood
is_style_vars = {}
for style in styles:
	is_style_vars[style] = {}
	for i in range(0,40,tick):
		is_style_vars[style][i] = (Bool("is_style_" + style + "_ind_" + str(i)))

is_theme = []
for i in range(1,3):
	is_theme.append({})
	for j in range(0,40,tick):
		is_theme[-1][j] = Bool("is_theme_" + str(i) + "_at_" + str(j))

for i in range(1,3):
	for var in enum_vals:
		s.add(Sum([1 if x else 0 for x in theme_enum_vals[var][i]]) == 1)
for i in range(0,40,tick):
	for var in enum_vals:
		s.add(Sum([1 if x else 0 for x in time_enum_vals[var][i//tick]]) == 1)

#defines a difference between themes
themes_defined_differently_vars = [[Int("theme_" + str(i) + "defined_differently_" + str(var)) for i in range(1,3)] for var in all_vars]
for (var_ind, var) in enumerate(all_vars):
	if var in enum_values:
		themes_defined_differently_vars[var_ind] = And(Or(theme_is_defined_vars[0][var_ind], theme_is_defined[1][var_ind]), True)
	else:
		themes_defined_differently_vars[var_ind] = And(Or(theme_is_defined_vars[0][var_ind], theme_is_defined[1][var_ind]), theme_enum_vals[var][0] != theme_enum_vals[var][1])		

#extent of definition of melody
for k in range(1,3):
	s.add(Sum([1 if i else 0 for i in theme_is_defined_vars[k]]) > 4)


#if melody is defined, must have a value
for k in range(1,3):
	for var_ind, var in enumerate(enum_values):
		s.add(Implies(theme_is_defined[k][var_ind], Or(theme_enum_vals[var][k])))

#distance between defined themes
theme_distance = Int("theme_distance")
s.add(theme_distance == Sum([1 if i else 0 for i in themes_defined_differently]))
s.add(theme_distance > 4)


for i in range(1,3):
	for j in range(0,40,tick):
		for var in all_vars:
			if var in enum_values:
				s.add(Implies(is_theme[-1][j], Not(And([time_is_defined_vars[j//tick][all_vars.index(var)], theme_is_defined_vars[i][all_vars.index(var)]] + [XOR(time_enum_vals[var][j//tick][k], theme_enum_vals[var][i][k]) for k in range(len(theme_enum_vals[var][i]))])))
			else:
				s.add(Implies(is_theme[-1][j], Not(And([time_is_defined_vars[j//tick][all_vars.index(var)], theme_is_defined_vars[i][all_vars.index(var)]] + [XOR(time_enum_vals[var][j//tick], theme_enum_vals[var][i])]))))

####
#which variables suggest which styles
for i in range(0,40,tick):
	s.add(Implies(is_style_vars["bollywood"][i], notNotTwo([Not(time_enum_vals["is_harmonic"][i//tick]), Not(time_enum_vals["is_twelve_tone"][i//tick]), time_enum_vals["has_tabla"][i//tick], time_enum_vals["has_drone"][i//tick], time_enum_vals["is_additive_meter"][i//tick]])))
	s.add(Implies(is_style_vars["sci-fi"][i], notNotTwo([time_enum_vals["has_ostinato"][i//tick], time_enum_vals["has_synth"][i//tick], time_enum_vals["has_symmetric_scale"][i//tick], time_enum_vals["has_glissandi"][i//tick]])))


#adding specs
for i in range(0,40,tick):
	s.add(is_style_vars["bollywood"][i])

for i in range(30, 40, tick):
	s.add(is_style_vars["sci-fi"][i])


for i in range(0,20,tick):
	s.add(is_theme[0][i])

for i in range(20,30,tick):
	s.add(is_theme[1][i])

for i in range(30,40,tick):
	s.add(And(is_theme[0][i], is_theme[1][i]))


#for a role to exist, something has to play it
for (instr_ind, instr_type) in enumerate(instr_types):
	for i in range(0,40,tick):
		s.add(Implies(time_enum_vals["has_" + str(instr_type)][i//tick], Or([time_enum_vals["_has_" + instr_role][i//tick][instr_ind] for instr_role in ["sus_chords", "melody", "accompaniment", "ostinato", "counter_melody", "drone", "pedal"]])))
	for i in range(tick,40,tick):
		s.add(Implies(time_enum_vals["add_" + str(instr_type)[i//tick]], And(Not(time_enum_vals["has_" + str(instr_type)][(i//tick) - 1]), time_enum_vals["has_" + str(instr_type)][i//tick])))	
	for theme in range(2):
		s.add(Implies(theme_enum_vals["has_" + str(instr_role)][theme], Or([theme_enum_vals["_has_" + instr_role][theme][instr_ind] for instr_role in ["sus_chords", "melody", "accompaniment", "ostinato", "counter_melody", "drone", "pedal"]])))


#for any instrument to havef a role, that role must be defined
for i in range(0,40,tick):
	for texture_type in ["sus_chords", "accompaniment", "ostinato", "counter_melody", "drone", "pedal"]:
		s.add(Implies(Or(time_enum_vals["_has_" + str(texture_type)][i//tick]), time_enum_vals["has_" + str(texture_type)][i//tick]))

for i in range(2):
	s.add(Implies(Or(theme_enum_vals["_has_" + str(texture_type)][i]), theme_enum_vals["has_" + str(texture_type)][i]))


#if a property depends on another property to exist, that relation must hold
for tup in implies:
	if len(tup) == 2 and type(tup[0]) == str and type(tup[1]) == str:
		for i in range(0, 40, tick):
			s.add(Implies(time_is_defined_vars[i//tick][all_vars.index(tup[0])], time_is_defined_vars[i//tick][all_vars.index(tup[1])]))
		for i in range(2):
			s.add(Implies(theme_is_defined_vars[i][all_vars.index(tup[0])], theme_is_defined_vars[i][all_vars.index(tup[1])]))

#someone always has the melody
for i in range(0, 40, tick):
	s.add(Or(time_enum_vals["_has_melody"][i//tick]))


s.check()
print(s.model())
####
#recognizability of values

####
#distance between two themes


#(("texture_of_melody", "tutti"), ("n_instruments", "large")