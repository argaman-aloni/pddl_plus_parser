
(define (domain UM-Translog-2)
	(:requirements :typing :adl :equality :negative-preconditions :existential-preconditions :universal-preconditions :fluents)
	(:types
		region package city location vehicle route equipment ptype vtype vptype rtype ltype - object
		crane plane-ramp - equipment
	)

	(:constants
		regularv flatbed tanker hopper auto air - vtype
		truck airplane train - vptype
		road-route rail-route air-route - rtype
		regularp bulky liquid granular cars mail - ptype
		airport train-station - ltype
	)

	(:predicates
		(at-packagel ?p - package ?l - location)
		(at-packagev ?p - package ?v - vehicle)
		(at-vehicle ?v - vehicle ?l - location)
		(availablev ?v - vehicle)
		(clear)
		(delivered ?p - package ?d - location)
		(door-open ?v - vehicle)
		(fees-collected ?p - package)
		(move ?p - package)
		(pv-compatible ?ptype - ptype ?vtype - vtype)
		(typep ?p - package ?type - ptype)
		(typev ?v - vehicle ?type - vtype)
		(unload ?v - vehicle)
	)
	(:functions
		(volume-cap-l ?l - location)
		(volume-cap-v ?v - vehicle)
		(volume-load-l ?l - location)
		(volume-load-v ?v - vehicle)
		(volume-p ?p - package)
		(weight-cap-v ?v - vehicle)
		(weight-p ?p - package)
		(weight-load-v ?v - vehicle)
	)

	(:action collect-fees
		:parameters (?p - package)
		:precondition (and (not (fees-collected ?p))
			(forall
				(?dd - location)
				(and (delivered ?p ?dd))))
		:effect (and (fees-collected ?p))
	)

	(:action deliver
		:parameters (?p - package ?d - location)
		:precondition (and (at-packagel ?p ?d)
			(forall
				(?dd - location)
				(and (delivered ?p ?dd))))
		:effect (and (delivered ?p ?d)
			(not (at-packagel ?p ?d))
			(decrease (volume-load-l ?d) (volume-p ?p)))
	)

	(:action open-door-regular
		:parameters (?v - vehicle)
		:precondition (and (not (door-open ?v))
			(typev ?v regularv))
		:effect (and (door-open ?v))
	)

	(:action close-door-regular
		:parameters (?v - vehicle)
		:precondition (and (door-open ?v)
			(typev ?v regularv))
		:effect (and (not (door-open ?v)))
	)

	(:action load-regular
		:parameters (?p - package ?v - vehicle ?l - location)
		:precondition (and (at-vehicle ?v ?l)
			(availablev ?v)
			(at-packagel ?p ?l)
			(typev ?v regularv)
			(forall
				(?ptype - ptype)
				(and (typep ?p ?ptype)
					(pv-compatible ?ptype regularv)))
			(door-open ?v)
			(>= (weight-cap-v ?v) (+ (weight-load-v ?v) (weight-p ?p)))
			(>= (volume-cap-v ?v) (+ (volume-load-v ?v) (volume-p ?p)))
			(fees-collected ?p))
		:effect (and (at-packagev ?p ?v)
			(not (at-packagel ?p ?l))
			(decrease (volume-load-l ?l) (volume-p ?p))
			(increase (weight-load-v ?v) (weight-p ?p))
			(increase (volume-load-v ?v) (volume-p ?p)))
	)

	(:action unload-regular
		:parameters (?p - package ?v - vehicle ?l - location)
		:precondition (and (at-vehicle ?v ?l)
			(at-packagev ?p ?v)
			(typev ?v regularv)
			(>= (volume-cap-l ?l) (+ (volume-load-l ?l) (volume-p ?p)))
			(door-open ?v))
		:effect (and (at-packagel ?p ?l)
			(not (at-packagev ?p ?v))
			(not (move ?p))
			(unload ?v)
			(not (clear))
			(increase (volume-load-l ?l) (volume-p ?p))
			(decrease (weight-load-v ?v) (weight-p ?p))
			(decrease (volume-load-v ?v) (volume-p ?p)))
	)

)