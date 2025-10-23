(define (domain woodworking)
	(:requirements :strips :typing)

	(:types
		acolour awood woodobj machine surface treatmentstatus aboardsize apartsize - object
		highspeed-saw saw glazer grinder immersion-varnisher planer spray-varnisher - machine
		board part - woodobj
	)

	(:constants
		small medium large - apartsize
		varnished glazed untreated colourfragments - treatmentstatus

		natural - acolour
		verysmooth smooth rough - surface
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
		(empty ?agent - highspeed-saw)
		(in-highspeed-saw ?b - board ?agent - highspeed-saw)
		(grind-treatment-change ?agent - grinder ?old - treatmentstatus ?new - treatmentstatus)
	)

	(:action do-spray-varnish
		:parameters (?m - spray-varnisher ?x - part ?newcolour - acolour ?surface - surface)
		:precondition (and (available ?x) (has-colour ?m ?newcolour) (surface-condition ?x ?surface) (is-smooth ?surface) (treatment ?x untreated))
		:effect (and (treatment ?x varnished) (colour ?x ?newcolour) (not (treatment ?x untreated)) (not (colour ?x natural)))
	)

	(:action do-saw-small
		:parameters (?m - saw ?b - board ?p - part ?w - awood ?surface - surface ?size_before - aboardsize ?size_after - aboardsize)
		:precondition (and (unused ?p) (goalsize ?p small) (available ?b) (wood ?b ?w) (surface-condition ?b ?surface) (boardsize ?b ?size_before) (boardsize-successor ?size_after ?size_before))
		:effect (and (treatment ?p untreated) (available ?p) (boardsize ?b ?size_after) (surface-condition ?p ?surface) (colour ?p natural) (wood ?p ?w) (not (unused ?p)))
	)

	(:action do-saw-medium
		:parameters (?m - saw ?b - board ?p - part ?w - awood ?surface - surface ?size_before - aboardsize ?s1 - aboardsize ?size_after - aboardsize)
		:precondition (and (unused ?p) (goalsize ?p medium) (available ?b) (wood ?b ?w) (surface-condition ?b ?surface) (boardsize ?b ?size_before) (boardsize-successor ?size_after ?s1) (boardsize-successor ?s1 ?size_before))
		:effect (and (available ?p) (treatment ?p untreated) (wood ?p ?w) (surface-condition ?p ?surface) (colour ?p natural) (boardsize ?b ?size_after) (not (unused ?p)))
	)

	(:action do-saw-large
		:parameters (?m - saw ?b - board ?p - part ?w - awood ?surface - surface ?size_before - aboardsize ?s1 - aboardsize ?s2 - aboardsize ?size_after - aboardsize)
		:precondition (and (unused ?p) (goalsize ?p large) (available ?b) (wood ?b ?w) (surface-condition ?b ?surface) (boardsize ?b ?size_before) (boardsize-successor ?size_after ?s1) (boardsize-successor ?s1 ?s2) (boardsize-successor ?s2 ?size_before))
		:effect (and (available ?p) (wood ?p ?w) (surface-condition ?p ?surface) (colour ?p natural) (boardsize ?b ?size_after) (treatment ?p untreated) (not (unused ?p)))
	)

	(:action do-plane
		:parameters (?m - planer ?x - part ?oldsurface - surface ?oldcolour - acolour ?oldtreatment - treatmentstatus)
		:precondition (and (available ?x) (surface-condition ?x ?oldsurface) (treatment ?x ?oldtreatment) (colour ?x ?oldcolour))
		:effect (and (treatment ?x untreated) (colour ?x natural) (surface-condition ?x smooth) (not (treatment ?x ?oldtreatment)) (not (surface-condition ?x ?oldsurface)) (not (colour ?x ?oldcolour)))
	)

	(:action do-immersion-varnish
		:parameters (?m - immersion-varnisher ?x - part ?newcolour - acolour ?surface - surface)
		:precondition (and (available ?x) (has-colour ?m ?newcolour) (surface-condition ?x ?surface) (is-smooth ?surface) (treatment ?x untreated))
		:effect (and (colour ?x ?newcolour) (treatment ?x varnished) (not (colour ?x natural)) (not (treatment ?x untreated)))
	)

	(:action load-highspeed-saw
		:parameters (?m - highspeed-saw ?b - board)
		:precondition (and (empty ?m) (available ?b))
		:effect (and (in-highspeed-saw ?b ?m) (not (empty ?m)) (not (available ?b)))
	)

	(:action unload-highspeed-saw
		:parameters (?m - highspeed-saw ?b - board)
		:precondition (and (in-highspeed-saw ?b ?m))
		:effect (and (available ?b) (empty ?m) (not (in-highspeed-saw ?b ?m)))
	)

	(:action cut-board-small
		:parameters (?m - highspeed-saw ?b - board ?p - part ?w - awood ?surface - surface ?size_before - aboardsize ?size_after - aboardsize)
		:precondition (and (unused ?p) (goalsize ?p small) (in-highspeed-saw ?b ?m) (wood ?b ?w) (surface-condition ?b ?surface) (boardsize ?b ?size_before) (boardsize-successor ?size_after ?size_before))
		:effect (and (surface-condition ?p ?surface) (wood ?p ?w) (colour ?p natural) (available ?p) (boardsize ?b ?size_after) (treatment ?p untreated) (not (unused ?p)))
	)

	(:action cut-board-medium
		:parameters (?m - highspeed-saw ?b - board ?p - part ?w - awood ?surface - surface ?size_before - aboardsize ?s1 - aboardsize ?size_after - aboardsize)
		:precondition (and (unused ?p) (goalsize ?p medium) (in-highspeed-saw ?b ?m) (wood ?b ?w) (surface-condition ?b ?surface) (boardsize ?b ?size_before) (boardsize-successor ?size_after ?s1) (boardsize-successor ?s1 ?size_before))
		:effect (and (boardsize ?b ?size_after) (available ?p) (surface-condition ?p ?surface) (treatment ?p untreated) (wood ?p ?w) (colour ?p natural) (not (unused ?p)))
	)

	(:action cut-board-large
		:parameters (?m - highspeed-saw ?b - board ?p - part ?w - awood ?surface - surface ?size_before - aboardsize ?s1 - aboardsize ?s2 - aboardsize ?size_after - aboardsize)
		:precondition (and (unused ?p) (goalsize ?p large) (in-highspeed-saw ?b ?m) (wood ?b ?w) (surface-condition ?b ?surface) (boardsize ?b ?size_before) (boardsize-successor ?size_after ?s1) (boardsize-successor ?s1 ?s2) (boardsize-successor ?s2 ?size_before))
		:effect (and (surface-condition ?p ?surface) (colour ?p natural) (available ?p) (boardsize ?b ?size_after) (treatment ?p untreated) (wood ?p ?w) (not (unused ?p)))
	)

	(:action do-grind
		:parameters (?m - grinder ?x - part ?oldsurface - surface ?oldcolour - acolour ?oldtreatment - treatmentstatus ?newtreatment - treatmentstatus)
		:precondition (and (available ?x) (surface-condition ?x ?oldsurface) (is-smooth ?oldsurface) (colour ?x ?oldcolour) (treatment ?x ?oldtreatment) (grind-treatment-change ?m ?oldtreatment ?newtreatment))
		:effect (and (colour ?x natural) (surface-condition ?x verysmooth) (treatment ?x ?newtreatment) (not (surface-condition ?x ?oldsurface)) (not (treatment ?x ?oldtreatment)) (not (colour ?x ?oldcolour)))
	)

	(:action do-glaze
		:parameters (?m - glazer ?x - part ?newcolour - acolour)
		:precondition (and (available ?x) (has-colour ?m ?newcolour) (treatment ?x untreated))
		:effect (and (treatment ?x glazed) (colour ?x ?newcolour) (not (treatment ?x untreated)) (not (colour ?x natural)))
	)

)