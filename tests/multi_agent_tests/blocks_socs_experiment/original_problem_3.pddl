(define (problem BLOCKS-4-0)
	(:domain blocks)
	(:objects
		a - block
		c - block
		b - block
		d - block

		a1 - agent
		a2 - agent
		a3 - agent
	)
	(:init
		(handempty a2)
		(handempty a1)
		(handempty a3)
		(clear c)
		(clear d)
		(clear a)
		(ontable b)
		(ontable c)
		(ontable d)
		(on a b)
	)
	(:goal
		(and
			(on b a)
			(on c b)
			(on d c)
		)
	)
)