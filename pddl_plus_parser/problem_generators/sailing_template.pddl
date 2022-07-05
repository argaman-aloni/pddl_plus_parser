;; Enrico Scala (enricos83@gmail.com) and Miquel Ramirez (miquel.ramirez@gmail.com)
(define (problem ${instance_name})

	(:domain ${domain_name})

	(:objects
		${boat_name_list} - boat
		${people_name_list} - person
	)

  (:init
		${boat_positions}

		${people_d_position}

	)

	(:goal
		(and
			${people_to_save}
		)
	)
)

