(define (problem logistics-4-0) (:domain logistics)
(:objects
	obj21 - package
	obj22 - package
	obj23 - package
	apt2 - airport
	apt1 - airport
	obj11 - package
	obj13 - package
	obj12 - package
	pos1 - location

	(:private
		apn1 - airplane
	)
)
(:init
	(at apn1 apt2)
	(at obj11 pos1)
	(at obj12 pos1)
	(at obj13 pos1)
)
(:goal
	(and
		(at obj11 apt1)
		(at obj23 pos1)
		(at obj13 apt1)
		(at obj21 pos1)
	)
)
)