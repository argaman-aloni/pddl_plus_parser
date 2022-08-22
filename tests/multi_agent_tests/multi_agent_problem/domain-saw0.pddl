(define (domain woodworking)
	(:requirements :factored-privacy :typing)
(:types
	 acolour awood woodobj machine surface treatmentstatus aboardsize apartsize - object 
 	 highspeed-saw saw glazer grinder immersion-varnisher planer spray-varnisher - machine 
 	 board part - woodobj 
 )
(:constants
	small medium large  - apartsize
	varnished glazed untreated colourfragments  - treatmentstatus
	natural  - acolour
	verysmooth smooth rough  - surface
)
(:predicates
	(available ?obj - woodobj)
	(surface-condition ?obj - woodobj ?surface - surface)
	(treatment ?obj - part ?treatment - treatmentstatus)
	(colour ?obj - part ?colour - acolour)
	(wood ?obj - woodobj ?wood - awood)
	(is-smooth ?surface - surface)
	(has-colour ?agent - machine ?colour - acolour)
	(goalsize ?part - part ?size - apartsize)
	(boardsize-successor ?size1 - aboardsize ?size2 - aboardsize)
	(unused ?obj - part)
	(boardsize ?board - board ?size - aboardsize)
)
(:functions
	(total-cost) 
	(spray-varnish-cost ?obj - part)
	(glaze-cost ?obj - part)
	(grind-cost ?obj - part)
	(plane-cost ?obj - part)
)

(:action do-saw-small
	:parameters (?m - saw ?b - board ?p - part ?w - awood ?surface - surface ?size_before - aboardsize ?size_after - aboardsize)
	:precondition (and
		(unused ?p)
		(goalsize ?p small)
		(available ?b)
		(wood ?b ?w)
		(surface-condition ?b ?surface)
		(boardsize ?b ?size_before)
		(boardsize-successor ?size_after ?size_before)
	)
	:effect (and
		(increase ( total-cost ) 30)
		(not (unused ?p))
		(available ?p)
		(wood ?p ?w)
		(surface-condition ?p ?surface)
		(colour ?p natural)
		(treatment ?p untreated)
		(boardsize ?b ?size_after)
	)
)


(:action do-saw-medium
	:parameters (?m - saw ?b - board ?p - part ?w - awood ?surface - surface ?size_before - aboardsize ?s1 - aboardsize ?size_after - aboardsize)
	:precondition (and
		(unused ?p)
		(goalsize ?p medium)
		(available ?b)
		(wood ?b ?w)
		(surface-condition ?b ?surface)
		(boardsize ?b ?size_before)
		(boardsize-successor ?size_after ?s1)
		(boardsize-successor ?s1 ?size_before)
	)
	:effect (and
		(increase ( total-cost ) 30)
		(not (unused ?p))
		(available ?p)
		(wood ?p ?w)
		(surface-condition ?p ?surface)
		(colour ?p natural)
		(treatment ?p untreated)
		(boardsize ?b ?size_after)
	)
)


(:action do-saw-large
	:parameters (?m - saw ?b - board ?p - part ?w - awood ?surface - surface ?size_before - aboardsize ?s1 - aboardsize ?s2 - aboardsize ?size_after - aboardsize)
	:precondition (and
		(unused ?p)
		(goalsize ?p large)
		(available ?b)
		(wood ?b ?w)
		(surface-condition ?b ?surface)
		(boardsize ?b ?size_before)
		(boardsize-successor ?size_after ?s1)
		(boardsize-successor ?s1 ?s2)
		(boardsize-successor ?s2 ?size_before)
	)
	:effect (and
		(increase ( total-cost ) 30)
		(not (unused ?p))
		(available ?p)
		(wood ?p ?w)
		(surface-condition ?p ?surface)
		(colour ?p natural)
		(treatment ?p untreated)
		(boardsize ?b ?size_after)
	)
)

)