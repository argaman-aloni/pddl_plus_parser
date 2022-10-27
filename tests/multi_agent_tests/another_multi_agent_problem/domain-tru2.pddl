(define (domain logistics)
	(:requirements :factored-privacy :typing)
(:types
	 location vehicle package city - object 
 	 airport - location 
 	 truck airplane - vehicle 
 )
(:predicates
	(at ?obj - object ?loc - location)
	(in ?obj1 - package ?veh - vehicle)

	(:private
		(in-city ?agent - truck ?loc - location ?city - city)
	)
)

(:action load-truck
	:parameters (?truck - truck ?obj - package ?loc - location)
	:precondition (and
		(at ?truck ?loc)
		(at ?obj ?loc)
	)
	:effect (and
		(not (at ?obj ?loc))
		(in ?obj ?truck)
	)
)


(:action unload-truck
	:parameters (?truck - truck ?obj - package ?loc - location)
	:precondition (and
		(at ?truck ?loc)
		(in ?obj ?truck)
	)
	:effect (and
		(not (in ?obj ?truck))
		(at ?obj ?loc)
	)
)


(:action drive-truck
	:parameters (?truck - truck ?loc-from - location ?loc-to - location ?city - city)
	:precondition (and
		(at ?truck ?loc-from)
		(in-city ?truck ?loc-from ?city)
		(in-city ?truck ?loc-to ?city)
	)
	:effect (and
		(not (at ?truck ?loc-from))
		(at ?truck ?loc-to)
	)
)

)