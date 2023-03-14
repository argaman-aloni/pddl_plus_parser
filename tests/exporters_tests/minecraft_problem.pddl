; PolyCraft basic problem

(define (problem basic)

(:domain polycraft)

(:init
    ; Map
    (= (trees_in_map) 5)

    ; Items
    (= (count_log_in_inventory) 0)
    (= (count_planks_in_inventory) 0)
    (= (count_stick_in_inventory) 0)
    (= (count_sack_polyisoprene_pellets_in_inventory) 0)
    (= (count_tree_tap_in_inventory) 0)
    (= (count_wooden_pogo_stick_in_inventory) 0)
)

(:goal
    (and
        (= (count_wooden_pogo_stick_in_inventory) 1)
    )
)
)