;; Enrico Scala (enricos83@gmail.com) and Miquel Ramirez (miquel.ramirez@gmail.com)
(define (problem ${instance_name})
	(:domain ${domain_name})
	(:objects
		${taps_list} - tap
		${agents_list} - agent
		${plants_list} - plant

	)
  (:init
        (= (max_int) ${max_int_value})
        (= (maxx) 10)
        (= (minx) 1)
	    (= (maxy) 10)
	    (= (miny) 1)
	    (= (carrying) 0)
	    (= (total_poured) 0)
	    (= (total_loaded) 0)

		${poured_plants}
		${agents_locations}
		${plants_locations}
		${taps_locations}
	)
	(:goal
		(and
		    ${pour_goals}
			${total_poured_goal}
		)
	)
)

