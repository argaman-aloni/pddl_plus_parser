; PolyCraft domain

(define (domain polycraft)

(:requirements :strips :typing :negative-preconditions :fluents)

(:functions
    ; Map
    (trees_in_map) ; 5x1 map contain 5 trees

    ; Items
    (count_log_in_inventory)
    (count_planks_in_inventory)
    (count_stick_in_inventory)
    (count_sack_polyisoprene_pellets_in_inventory)
    (count_tree_tap_in_inventory)
    (count_wooden_pogo_stick_in_inventory)
)

; Actions
(:action get_log ; to break, tp to tree/blank
    :parameters ()
    :precondition (and
        (> (trees_in_map) 0)
    )
    :effect (and
        (decrease (trees_in_map) 1)
        (increase (count_log_in_inventory) 1)
    )
)

(:action craft_plank
    :parameters ()
    :precondition (and
        (> (count_log_in_inventory) 0)
    )
    :effect (and
        (decrease (count_log_in_inventory) 1)
        (increase (count_planks_in_inventory) 4)
    )
)

(:action craft_stick
    :parameters ()
    :precondition (and
        (> (count_planks_in_inventory) 1)
    )
    :effect (and
        (decrease (count_planks_in_inventory) 2)
        (increase (count_stick_in_inventory) 4)
    )
)

(:action craft_tree_tap
    :parameters ()
    :precondition (and
        (> (count_planks_in_inventory) 4)
        (> (count_stick_in_inventory) 0)
    )
    :effect (and
        (decrease (count_planks_in_inventory) 5)
        (decrease (count_stick_in_inventory) 1)
        (increase (count_tree_tap_in_inventory) 1)
    )
)

(:action craft_wooden_pogo
    :parameters ()
    :precondition (and
        (> (count_planks_in_inventory) 1)
        (> (count_stick_in_inventory) 3)
        (> (count_sack_polyisoprene_pellets_in_inventory) 0)
    )
    :effect (and
        (decrease (count_planks_in_inventory) 2)
        (decrease (count_stick_in_inventory) 4)
        (decrease (count_sack_polyisoprene_pellets_in_inventory) 1)
        (increase (count_wooden_pogo_stick_in_inventory) 1)
    )
)

(:action place_tree_tap  ; make without tp
    :parameters ()
    :precondition (and
        (> (trees_in_map) 0)
        (> (count_tree_tap_in_inventory) 0)
    )
    :effect (and
        (decrease (count_tree_tap_in_inventory) 1)
        (increase (count_sack_polyisoprene_pellets_in_inventory) 1)
    )
)

)