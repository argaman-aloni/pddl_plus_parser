;; Enrico Scala (enricos83@gmail.com) and Miquel Ramirez (miquel.ramirez@gmail.com)
(define (problem ${instance_name})
	(:domain polycraft)

  (:init
		${trees_in_map_initial}
		${count_log_in_inventory_initial}
		${count_planks_in_inventory_initial}
		${count_stick_in_inventory_initial}
		${count_sack_polyisoprene_pellets_in_inventory_initial}
		${count_tree_tap_in_inventory_initial}
        (= (count_wooden_pogo_stick_in_inventory) 0)
	)
	(:goal
		(and
			(>= (count_wooden_pogo_stick_in_inventory) 1)
		)
	)
)

