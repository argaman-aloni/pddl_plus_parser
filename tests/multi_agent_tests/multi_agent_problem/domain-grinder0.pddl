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

	(:private
		(grind-treatment-change ?agent - grinder ?old - treatmentstatus ?new - treatmentstatus)
	)
)
(:functions
	(total-cost)
	(spray-varnish-cost ?obj - part)
	(glaze-cost ?obj - part)
	(grind-cost ?obj - part)
	(plane-cost ?obj - part)
)

(:action do-grind
	:parameters (?m - grinder ?x - part ?oldsurface - surface ?oldcolour - acolour ?oldtreatment - treatmentstatus ?newtreatment - treatmentstatus)
	:precondition (and
		(available ?x)
		(surface-condition ?x ?oldsurface)
		(is-smooth ?oldsurface)
		(colour ?x ?oldcolour)
		(treatment ?x ?oldtreatment)
		(grind-treatment-change ?m ?oldtreatment ?newtreatment)
	)
	:effect (and
		(increase ( total-cost ) ( grind-cost ?x ))
		(not (surface-condition ?x ?oldsurface))
		(surface-condition ?x verysmooth)
		(not (treatment ?x ?oldtreatment))
		(treatment ?x ?newtreatment)
		(not (colour ?x ?oldcolour))
		(colour ?x natural)
	)
)

)