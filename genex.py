
for (note_ind, (pitch, lyric)) in enumerate(notes):

	#print(dur - (actual_onset - prev_offset))
	onset_x = int((actual_onset - 0.01)* 705600000)
	song_string += '{"onset": ' + str(onset_x) + ', "duration": ' + str(int(705600000*dur)) + ', "lyric": ".' + lyric.replace("-", " ") + '", "comment": "", "pitch": ' + str(pitch - 1 - 9) 
	if lyric[0] == 's':
		song_string += ', "tSylOnset": 1.8e-1, "dF0Vbr": ' + ('0.7e-1' if dur < 0.5 else '1e-2') + '}, '
	else:
		song_string += ', "dF0Vbr": ' + ('0.7e-1' if dur < 0.5 else '1e-2') + '}, '
	#assert(note_ind == len(notes) - 1 or onset_x + int(705600000*dur) <= int(notes[note_ind + 1][3]*705600000)) #dur < 0.5
	#print("actual_onset = " + str(actual_onset) + " dur = " + str(notes[-1][1]))

	act_ons.append((actual_onset, dur2))

	accomp_parts = accomps[note_ind]
	for part_ind in range(len(accomp_parts)):
		notes_in_part = accomp_parts[part_ind]
		instr = instrs[part_ind]
		if instr not in ["Flute", "Oboe", "Bassoon", "C Trumpet", "Timpani"]:
			continue
		#instr = list(midi.keys())[part_ind]
		program = programs[instr]
		tot = sum([i[1] for i in notes_in_part])
		if tot > 0:
			ratio = dur2/tot
		else:
			ratio = 1
		if type(program) == int:
			ons = actual_onset
			for i in range(len(notes_in_part)):
				dur = notes_in_part[i][1]*ratio
				if i == len(notes_in_part) - 1  and word_break >= 0.25:
					dur += word_break
				MyMIDI.addNote(part_ind,0,notes_in_part[i][0] - 1 - 9,ons,dur,127)
				ons += notes_in_part[i][1]*ratio
		else:
			ons = actual_onset
			for i in range(len(notes_in_part)):
				MyMIDI.addNote(part_ind,9,program[1],ons,notes_in_part[i][1]*ratio,127)
				ons += notes_in_part[i][1]*ratio

	#if len(all_accomp_notes[note_ind]) == 0:
	#	print("baddd")
	#	part2.insert(actual_onset, Note(pitch, quarterLength=dur2))
	#else:
	#	part2.insert(actual_onset, Chord(all_accomp_notes[note_ind], quarterLength = dur2))
	prev_offset = actual_onset + dur
open("act_ons.txt", "w+").writelines([str(i[0]) + ", " + str(i[1]) + "\n" for i in act_ons])
song_string = song_string[:-2]
song_string += '], "gsEvents": null, "mixer": {"gainDecibel": 0, "pan": 0, "muted": false, "solo": false, "engineOn": true, "display": true}, "parameters": {"interval": 5512500, "pitchDelta": [0, 0], "vibratoEnv": [0, 0], "loudness": [0, 0], "tension": [0, 200, 127000, 200], "breathiness": [0, 0], "voicing": [0, 0], "gender": ['
song_string += ", ".join([str(i) + ", " + str(1.0e-1) for i in range(500000)])
song_string += ']}}'
song_string += '], "instrumental": {"filename": "", "offset": 0}, "mixer": {"gainInstrumentalDecibel": 0, "gainVocalMasterDecibel": 0, "instrumentalMuted": false, "vocalMasterMuted": false} }'

bass_notes = []