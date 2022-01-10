(define
    (domain ballphysics)
    (:requirements :time :typing)
    (:types
        acolour
        awood
        woodobj
        machine
        surface
        treatmentstatus
        aboardsize
        apartsize - object
        highspeed-saw
        saw
        glazer
        grinder
        immersion-varnisher
        planer
        spray-varnisher - machine
        board
        part - woodobj
    )
    (:constants
	small
	medium
	large - apartsize
	varnished
	glazed
	untreated
	colourfragments - treatmentstatus

	natural - acolour
	verysmooth
	smooth
	rough - surface
	)
    (:predicates
        (held ?b - ball)
    )
    (:functions
        (velocity ?b - ball)
        (distance-to-floor ?b - ball)
    )
    (:action empty
    :parameters (?jug1 - jug ?jug2 - jug)
    :precondition (and (fluent-test) (>= (- (capacity ?jug2) (amount ?jug2)) (amount ?jug1))))
    :effect (and (assign (amount ?jug1) 0) (assign (amount ?jug2) 10))
    )
    (:action do-spray-varnish
	:parameters   (?m - spray-varnisher ?x - part ?newcolour - acolour ?surface - surface)
	:precondition (and (available ?x) (has-colour ?m ?newcolour) (surface-condition ?x ?surface) (is-smooth ?surface) (treatment ?x untreated))
	:effect       (and (treatment ?x varnished) (colour ?x ?newcolour) (not (treatment ?x untreated)) (not (colour ?x natural))))
    (:process FALLING
        :parameters (?b - ball)
        :precondition (and
            (not (held ?b))
            (< (velocity ?b) 100)
        )
        :effect (and
            (increase (velocity ?b) (* #t 9.8))
            (decrease (distance-to-floor ?b) (* #t (velocity ?b)))
        )
    )
    (:event HIT-GROUND
        :parameters (?b - ball)
        :precondition (and
            (not (held ?b))
            (<= (distance-to-floor ?b) 0)
            (> (velocity ?b) 0)
        )
        :effect (
            (assign (velocity ?b) (* -0.8 (velocity ?b)))
        )
    )

    ; Actions omitted
)