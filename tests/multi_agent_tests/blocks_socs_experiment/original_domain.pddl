(define (domain blocks)
	(:requirements :typing)
	(:types
		agent block - object
	)
	(:predicates
		(on ?x - block ?y - block)
		(ontable ?x - block)
		(clear ?x - block)

		(holding ?agent - agent ?x - block)
		(handempty ?agent - agent)
	)

	(:action stack
		:parameters (?a - agent ?x - block ?y - block)
		:precondition (and
			(holding ?a ?x)
			(clear ?y)
		)
		:effect (and
			(not (holding ?a ?x))
			(not (clear ?y))
			(clear ?x)
			(handempty ?a)
			(on ?x ?y)
		)
	)

	(:action pick-up
		:parameters (?a - agent ?x - block)
		:precondition (and
			(clear ?x)
			(ontable ?x)
			(handempty ?a)
		)
		:effect (and
			(not (ontable ?x))
			(not (clear ?x))
			(not (handempty ?a))
			(holding ?a ?x)
		)
	)

	(:action put-down
		:parameters (?a - agent ?x - block)
		:precondition (and (holding ?a ?x))
		:effect (and
			(not (holding ?a ?x))
			(clear ?x)
			(handempty ?a)
			(ontable ?x)
		)
	)

	(:action unstack
		:parameters (?a - agent ?x - block ?y - block)
		:precondition (and
			(on ?x ?y)
			(clear ?x)
			(handempty ?a)
		)
		:effect (and
			(holding ?a ?x)
			(clear ?y)
			(not (clear ?x))
			(not (handempty ?a))
			(not (on ?x ?y))
		)
	)

)