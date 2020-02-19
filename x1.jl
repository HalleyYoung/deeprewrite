using Reactive

spec = []

rando = Signal()

themes = Signal(map(makeThemes, spec, graph, rando_change_theme))

tick = Signal()

notes_as_array = Signal(map(getNotes, spec, themes, tick, rando_change_notes))

graph = Signal(map(getGraph, spec, rando_change_graph))

notes_as_list = Signal(map(getNotesAsList, notes_as_array))


while not notes_as_array[0]:
	push!(rando, rand)
	push!(rando_change_theme, rand)
	push!(tick, value(tick + 1))



