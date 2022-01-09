(define
    (domain ballphysics)
    (:requirements :time :typing)
    (:types
        ball - object
    )
    (:predicates
        (held ?b - ball)
    )
    (:functions
        (velocity ?b - ball)
        (distance-to-floor ?b - ball)
    )
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