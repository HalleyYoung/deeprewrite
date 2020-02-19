from music21 import *
import exrex
#exec(open("pythonregex.py").read())

reg_rhy = "(((((1|2|j|s|a|d|t|h|dt|dh)(0|1|2)(1|2))|(0|1|2|3)(1|2|3)))\-){4,6}\$(([0-3]{2,4}\$)){2}"
reg_mel = "(((rep|seq)(1|2|3){2})|(rep_down|seq_up|seq_continue_up|seq_continue_down|invert)(1|2))\-{4,6}\$((M\-((arp_down | arp_up | rep | seq | turnUp | turnDown | inertia)(2|3|4) | M) \-){1,2}\$){2}"


xs = [exrex.getone(reg_rhy) for i in range(400)]
xs = [i for i in xs if len([j for j in i.split("-") if j[0].isalpha() or len(j) == 3 and j.isdigit()]) in range(3,5)]

ys = [exrex.getone(reg_rhy) for i in range(400)]
ys = [i for i in ys if len([j for j in i.split("-") if j[0].isalpha()]) in range(3,5)]


def interpRegex(rrhy):
	parts = rrhy.split("$")
	vars_interp = [[int(j) for j in list(i)] for i in parts[1:3]]
	seq = []
	orig = parts[0].split("-")
	for val in orig:
		if val.startswith("rep"):
			seq.extend(vars_interp[int(val)])
		elif val.startswith("seq") and val[3].isdigit():
	return vars_interp