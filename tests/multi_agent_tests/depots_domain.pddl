(define (domain depot)
(:requirements :factored-privacy :typing)
(:types 	place locatable driver - object
	depot distributor - place
	truck hoist surface - locatable
	pallet crate - surface
)

(:predicates (at ?x - locatable ?y - place)
	(on ?x - crate ?y - surface)
	(in ?x - crate ?y - truck)
	(clear ?x - surface)
	(lifting ?agent - place ?x - hoist ?y - crate)
	(available ?agent - place ?x - hoist)
	(driving ?agent - driver ?t - truck)
	(dummy-additional-predicate )
)

(:action lift
	:parameters   (?p - place ?x - hoist ?y - crate ?z - surface)
	:precondition (and (available ?p ?x) (on ?y ?z) (at ?y ?p) (at ?x ?p) (clear ?y))
	:effect       (and (clear ?z) (lifting ?p ?x ?y) (not (at ?y ?p)) (not (on ?y ?z)) (not (available ?p ?x)) (not (clear ?y))
))

(:action drop
	:parameters   (?p - place ?x - hoist ?y - crate ?z - surface)
	:precondition (and (clear ?z) (at ?x ?p) (lifting ?p ?x ?y) (at ?z ?p))
	:effect       (and (at ?y ?p) (on ?y ?z) (available ?p ?x) (clear ?y) (not (clear ?z)) (not (lifting ?p ?x ?y))
))

(:action load
	:parameters   (?p - place ?x - hoist ?y - crate ?z - truck)
	:precondition (and (at ?z ?p) (at ?x ?p) (lifting ?p ?x ?y))
	:effect       (and (in ?y ?z) (available ?p ?x) (not (lifting ?p ?x ?y))
))

(:action unload
	:parameters   (?p - place ?x - hoist ?y - crate ?z - truck)
	:precondition (and (at ?z ?p) (at ?x ?p) (in ?y ?z) (available ?p ?x))
	:effect       (and (lifting ?p ?x ?y) (not (in ?y ?z)) (not (available ?p ?x))
))

(:action drive
	:parameters   (?a - driver ?x - truck ?y - place ?z - place)
	:precondition (and (at ?x ?y) (driving ?a ?x))
	:effect       (and (at ?x ?z) (not (at ?x ?y))
))

(:action dummy-add-predicate-action
	:parameters   (?agent - object)
	:precondition (and )
	:effect       (and (dummy-additional-predicate )
))

(:action dummy-del-predicate-action
	:parameters   (?agent - object)
	:precondition (and )
	:effect       (and (not (dummy-additional-predicate ))
))

)