(define (domain woodworking)
(:requirements :factored-privacy :typing)
(:types 	acolour awood woodobj machine surface treatmentstatus aboardsize apartsize - object
	highspeed-saw saw glazer grinder immersion-varnisher planer spray-varnisher - machine
	board part - woodobj
)

(:predicates (available ?obj - woodobj)
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
	(grind-treatment-change ?agent - grinder ?old - treatmentstatus ?new - treatmentstatus)
	(empty ?agent - highspeed-saw)
	(in-highspeed-saw ?b - board ?agent - highspeed-saw)
)

(:constants 	small medium large - apartsize
	varnished glazed untreated colourfragments - treatmentstatus
	natural - acolour
	verysmooth smooth rough - surface
)

(:functions (total-cost )
	(spray-varnish-cost ?obj - part)
	(glaze-cost ?obj - part)
	(grind-cost ?obj - part)
	(plane-cost ?obj - part)
)

(:action do-glaze
	:parameters   (?m - glazer ?x - part ?newcolour - acolour)
	:precondition (and (available ?x) (has-colour ?m ?newcolour) (treatment ?x untreated))
	:effect       (and (colour ?x ?newcolour) (treatment ?x glazed) (not (colour ?x natural)) (not (treatment ?x untreated))
(increase (total-cost ) (glaze-cost ?x))
))

(:action do-grind
	:parameters   (?m - grinder ?x - part ?oldsurface - surface ?oldcolour - acolour ?oldtreatment - treatmentstatus ?newtreatment - treatmentstatus)
	:precondition (and (is-smooth ?oldsurface) (treatment ?x ?oldtreatment) (grind-treatment-change ?m ?oldtreatment ?newtreatment) (available ?x) (colour ?x ?oldcolour) (surface-condition ?x ?oldsurface))
	:effect       (and (surface-condition ?x verysmooth) (treatment ?x ?newtreatment) (colour ?x natural) (not (treatment ?x ?oldtreatment)) (not (surface-condition ?x ?oldsurface)) (not (colour ?x ?oldcolour))
(increase (total-cost ) (grind-cost ?x))
))

(:action load-highspeed-saw
	:parameters   (?m - highspeed-saw ?b - board)
	:precondition (and (available ?b) (empty ?m))
	:effect       (and (in-highspeed-saw ?b ?m) (not (available ?b)) (not (empty ?m))
(increase (total-cost ) 30.0)
))

(:action unload-highspeed-saw
	:parameters   (?m - highspeed-saw ?b - board)
	:precondition (and )
	:effect       (and (available ?b) (empty ?m) (not (in-highspeed-saw ?b ?m))
(increase (total-cost ) 10.0)
))

(:action cut-board-small
	:parameters   (?m - highspeed-saw ?b - board ?p - part ?w - awood ?surface - surface ?size_before - aboardsize ?size_after - aboardsize)
	:precondition (and (unused ?p) (goalsize ?p small) (boardsize-successor ?size_after ?size_before) (wood ?b ?w) (surface-condition ?b ?surface) (in-highspeed-saw ?b ?m) (boardsize ?b ?size_before))
	:effect       (and (available ?p) (wood ?p ?w) (boardsize ?b ?size_after) (surface-condition ?p ?surface) (treatment ?p untreated) (colour ?p natural) (not (unused ?p))
(increase (total-cost ) 10.0)
))

(:action cut-board-medium
	:parameters   (?m - highspeed-saw ?b - board ?p - part ?w - awood ?surface - surface ?size_before - aboardsize ?s1 - aboardsize ?size_after - aboardsize)
	:precondition (and (goalsize ?p medium) (boardsize-successor ?s1 ?size_before) (unused ?p) (boardsize-successor ?size_after ?s1) (wood ?b ?w) (surface-condition ?b ?surface) (in-highspeed-saw ?b ?m) (boardsize ?b ?size_before))
	:effect       (and (available ?p) (wood ?p ?w) (boardsize ?b ?size_after) (surface-condition ?p ?surface) (treatment ?p untreated) (colour ?p natural) (not (unused ?p))
(increase (total-cost ) 10.0)
))

(:action cut-board-large
	:parameters   (?m - highspeed-saw ?b - board ?p - part ?w - awood ?surface - surface ?size_before - aboardsize ?s1 - aboardsize ?s2 - aboardsize ?size_after - aboardsize)
	:precondition (and (boardsize-successor ?s2 ?size_before) (unused ?p) (boardsize-successor ?size_after ?s1) (wood ?b ?w) (goalsize ?p large) (boardsize-successor ?s1 ?s2) (surface-condition ?b ?surface) (in-highspeed-saw ?b ?m) (boardsize ?b ?size_before))
	:effect       (and (available ?p) (wood ?p ?w) (boardsize ?b ?size_after) (surface-condition ?p ?surface) (treatment ?p untreated) (colour ?p natural) (not (unused ?p))
(increase (total-cost ) 10.0)
))

(:action do-immersion-varnish
	:parameters   (?m - immersion-varnisher ?x - part ?newcolour - acolour ?surface - surface)
	:precondition (and (treatment ?x untreated) (available ?x) (surface-condition ?x ?surface) (is-smooth ?surface) (has-colour ?m ?newcolour))
	:effect       (and (colour ?x ?newcolour) (treatment ?x varnished) (not (colour ?x natural)) (not (treatment ?x untreated))
(increase (total-cost ) 10.0)
))

(:action do-plane
	:parameters   (?m - planer ?x - part ?oldsurface - surface ?oldcolour - acolour ?oldtreatment - treatmentstatus)
	:precondition (and (treatment ?x ?oldtreatment) (surface-condition ?x ?oldsurface) (available ?x) (colour ?x ?oldcolour))
	:effect       (and (surface-condition ?x smooth) (colour ?x natural) (treatment ?x untreated) (not (treatment ?x ?oldtreatment)) (not (surface-condition ?x ?oldsurface)) (not (colour ?x ?oldcolour))
(increase (total-cost ) (plane-cost ?x))
))

(:action do-saw-small
	:parameters   (?m - saw ?b - board ?p - part ?w - awood ?surface - surface ?size_before - aboardsize ?size_after - aboardsize)
	:precondition (and (available ?b) (unused ?p) (goalsize ?p small) (boardsize-successor ?size_after ?size_before) (wood ?b ?w) (surface-condition ?b ?surface) (boardsize ?b ?size_before))
	:effect       (and (available ?p) (wood ?p ?w) (boardsize ?b ?size_after) (surface-condition ?p ?surface) (treatment ?p untreated) (colour ?p natural) (not (unused ?p))
(increase (total-cost ) 30.0)
))

(:action do-saw-medium
	:parameters   (?m - saw ?b - board ?p - part ?w - awood ?surface - surface ?size_before - aboardsize ?s1 - aboardsize ?size_after - aboardsize)
	:precondition (and (goalsize ?p medium) (boardsize-successor ?s1 ?size_before) (available ?b) (unused ?p) (boardsize-successor ?size_after ?s1) (wood ?b ?w) (surface-condition ?b ?surface) (boardsize ?b ?size_before))
	:effect       (and (available ?p) (wood ?p ?w) (boardsize ?b ?size_after) (surface-condition ?p ?surface) (treatment ?p untreated) (colour ?p natural) (not (unused ?p))
(increase (total-cost ) 30.0)
))

(:action do-saw-large
	:parameters   (?m - saw ?b - board ?p - part ?w - awood ?surface - surface ?size_before - aboardsize ?s1 - aboardsize ?s2 - aboardsize ?size_after - aboardsize)
	:precondition (and (available ?b) (unused ?p) (boardsize-successor ?size_after ?s1) (boardsize-successor ?s2 ?size_before) (wood ?b ?w) (goalsize ?p large) (boardsize-successor ?s1 ?s2) (surface-condition ?b ?surface) (boardsize ?b ?size_before))
	:effect       (and (available ?p) (wood ?p ?w) (boardsize ?b ?size_after) (surface-condition ?p ?surface) (treatment ?p untreated) (colour ?p natural) (not (unused ?p))
(increase (total-cost ) 30.0)
))

(:action do-spray-varnish
	:parameters   (?m - spray-varnisher ?x - part ?newcolour - acolour ?surface - surface)
	:precondition (and (treatment ?x untreated) (available ?x) (has-colour ?m ?newcolour) (surface-condition ?x ?surface) (is-smooth ?surface))
	:effect       (and (colour ?x ?newcolour) (treatment ?x varnished) (not (colour ?x natural)) (not (treatment ?x untreated))
(increase (total-cost ) (spray-varnish-cost ?x))
))

)