(define (problem ${instance_name})
	(:domain ${domain_name})
	(:objects
		${counters_list} - counter
		${students_list} - student
		teacher - teacher
	)
  (:init
		${counters_initial_values}
        ${students_initial_positions}
        ${teacher_initial_position}
		(= (max-dimension) 100)
	)
	(:goal
		(and
			${goal_constraints}
		)
	)
)

