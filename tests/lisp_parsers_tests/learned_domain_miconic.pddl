(define (domain miconic)
	(:requirements :adl :typing :disjunctive-preconditions :negative-preconditions :equality :universal-preconditions)
	(:types
		passenger floor - object
	)

	(:predicates
		(origin ?person - passenger ?floor - floor)
		(destin ?person - passenger ?floor - floor)
		(above ?floor1 - floor ?floor2 - floor)
		(boarded ?person - passenger)
		(served ?person - passenger)
		(lift-at ?floor - floor)
	)

	(:action stop
		:parameters (?f - floor)
		:precondition (and
			(lift-at ?f)
			(forall
				(?p - passenger)
				(and (or (not (destin ?p ?f))
						(and (destin ?p ?f)
							(not (origin ?p ?f))
							(or (not (boarded ?p))
								(not (served ?p))))))))
		:effect (and
			(forall
				(?p - passenger)
				(when
					(and (destin ?p ?f)
						(boarded ?p))
					(and (served ?p))))
			(forall
				(?p - passenger)
				(when
					(and (not (served ?p))
						(origin ?p ?f))
					(and (boarded ?p))))
			(forall
				(?p - passenger)
				(when
					(and (destin ?p ?f)
						(boarded ?p)
						(not (served ?p))
						(not (origin ?p ?f)))
					(and (not (boarded ?p)))))
		)
	)

	(:action up
		:parameters (?f1 - floor ?f2 - floor)
		:precondition (and (not (above ?f2 ?f1))
			(above ?f1 ?f2)
			(not (lift-at ?f2))
			(lift-at ?f1)
			(not (= ?f1 ?f2)))
		:effect (and (not (lift-at ?f1))
			(lift-at ?f2)
		)
	)

	(:action down
		:parameters (?f1 - floor ?f2 - floor)
		:precondition (and (above ?f2 ?f1)
			(not (above ?f1 ?f2))
			(not (lift-at ?f2))
			(lift-at ?f1)
			(not (= ?f1 ?f2)))
		:effect (and (not (lift-at ?f1))
			(lift-at ?f2)
		)
	)

)