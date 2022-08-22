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

(:action do-spray-varnish
	:parameters (?m - spray-varnisher ?x - part ?newcolour - acolour ?surface - surface)
	:precondition (and
		(available ?x)
		(has-colour ?m ?newcolour)
		(surface-condition ?x ?surface)
		(is-smooth ?surface)
		(treatment ?x untreated)
	)
	:effect (and
		(increase ( total-cost ) ( spray-varnish-cost ?x ))
		(not (treatment ?x untreated))
		(treatment ?x varnished)
		(not (colour ?x natural))
		(colour ?x ?newcolour)
	)
)

)