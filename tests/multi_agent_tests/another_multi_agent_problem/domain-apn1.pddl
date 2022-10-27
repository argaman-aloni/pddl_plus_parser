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
)

(:action load-airplane
	:parameters (?airplane - airplane ?obj - package ?loc - airport)
	:precondition (and
		(at ?obj ?loc)
		(at ?airplane ?loc)
	)
	:effect (and
		(not (at ?obj ?loc))
		(in ?obj ?airplane)
	)
)


(:action unload-airplane
	:parameters (?airplane - airplane ?obj - package ?loc - airport)
	:precondition (and
		(in ?obj ?airplane)
		(at ?airplane ?loc)
	)
	:effect (and
		(not (in ?obj ?airplane))
		(at ?obj ?loc)
	)
)


(:action fly-airplane
	:parameters (?airplane - airplane ?loc-from - airport ?loc-to - airport)
	:precondition 
		(at ?airplane ?loc-from)
	:effect (and
		(not (at ?airplane ?loc-from))
		(at ?airplane ?loc-to)
	)
)

)