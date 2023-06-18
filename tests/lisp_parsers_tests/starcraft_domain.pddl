;Header and description

(define (domain domain_name)

    ;remove requirements that are not needed
    (:requirements :strips :fluents :typing :conditional-effects :negative-preconditions)

    (:types ;todo: enumerate types and their hierarchy here, e.g. car truck bus - vehicle
        agent - object
    )

    ; un-comment following line if constants are needed

    (:predicates ;todo: define predicates here
        (dead ?agent - agent)
    )

    (:functions ;todo: define numeric functions here
        (max_x) ;; bounds
        (max_y) ;; bounds
        (min_y) ;; bounds
        (min_x) ;; bounds
        (health ?agent - agent)
        (shield ?agent - agent)
        (coordinate_x ?agent - agent)
        (coordinate_y ?agent - agent)
    )

    ;define actions here
    (:action dead
        :parameters (?agent - agent)
        :precondition (and
            (= (health ?agent) 0)
        )
        :effect (and
            (dead ?agent)
        )
    )

    (:action stop
        :parameters (?agent - agent)
        :precondition (and
            (> (health ?agent) 0)
        )
        :effect (and)
    )

    (:action move_up
        :parameters (?agent - agent)
        :precondition (and
            (> (health ?agent) 0)
            (< (coordinate_y ?agent) (max_y))
        )
        :effect (and
            (increase (coordinate_x ?agent) 1)
        )
    )

    (:action move_down
        :parameters (?agent - agent)
        :precondition (and
            (> (health ?agent) 0)
            (> (coordinate_y ?agent) (min_y))
        )
        :effect (and
            (decrease (coordinate_y ?agent) 1)
        )
    )

    (:action move_right
        :parameters (?agent - agent)
        :precondition (and
            (> (health ?agent) 0)
            (< (coordinate_x ?agent) (max_x))
        )
        :effect (and
            (increase (coordinate_x ?agent) 1)
        )
    )

    (:action move_left
        :parameters (?agent - agent)
        :precondition (and
            (> (health ?agent) 0)
            (> (coordinate_x ?agent) (min_x))
        )
        :effect (and
            (decrease (coordinate_x ?agent) 1)
        )
    )

    (:action attack
        :parameters (?agent - agent ?enemy - agent)
        :precondition (and
            (> (health ?agent) 0)
            () ; should create a way to calculate the distance from the enemy.
        )
        :effect (and
            (when
                (and (> (shield ?enemy) 0))
                (decrease (shield ?enemy) 1))
            (when
                (and (<= (shield ?enemy) 0))
                (decrease (health ?enemy) 1))
        )
    )

)