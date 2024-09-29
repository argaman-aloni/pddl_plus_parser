(define (problem ${instance_name})
	(:domain ${domain_name})
	(:objects
		${cells_list} - cell
		${students_list} - student
		${painting_list} - painting
		${math_tasks_list} - math-exercise
		homerooomteacher - teacher
	)
  (:init
        ${teacher_initial_position}
        ${students_initial_positions}
        ${tasks_initial_positions}
        ${initial_students_strengths}
        (= (works-collected) 0)
	)
	(:goal
		(and
			${goal_constraints}
		)
	)
)

