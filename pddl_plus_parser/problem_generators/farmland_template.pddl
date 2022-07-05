;; Enrico Scala (enricos83@gmail.com) and Miquel Ramirez (miquel.ramirez@gmail.com)
(define (problem ${instance_name})
	(:domain ${domain_name})
	(:objects
		${farm_name_list} - farm
	)
  (:init
        (= (cost) 0)
		${farm_init_allocation}
		${farm_connections}
	)
	(:goal
		(and
			${farm_final_requirement}
			${overall_reward_bound}
		)
	)
)

