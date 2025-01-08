(define (problem depotprob8765) (:domain depot)
(:objects
distributor1 - distributor
	distributor0 - distributor
	distributor2 - distributor
	depot0 - depot
	depot1 - depot
	depot2 - depot
	pallet5 - pallet
	pallet4 - pallet
	pallet1 - pallet
	pallet0 - pallet
	pallet3 - pallet
	pallet2 - pallet
	truck1 - truck
	truck0 - truck
	crate9 - crate
	crate8 - crate
	crate5 - crate
	crate4 - crate
	crate7 - crate
	crate6 - crate
	crate1 - crate
	crate0 - crate
	crate3 - crate
	crate2 - crate
	hoist2 - hoist
	hoist3 - hoist
	hoist0 - hoist
	hoist5 - hoist
	driver1 - driver
	driver0 - driver
	hoist1 - hoist
	hoist4 - hoist
)

(:init
	(at crate1 depot0)
	(at crate5 depot2)
	(at pallet1 depot1)
	(at hoist2 depot2)
	(at pallet4 distributor1)
	(at crate2 depot2)
	(at hoist4 distributor1)
	(at crate9 depot2)
	(at truck1 distributor0)
	(at crate3 depot1)
	(at pallet2 depot2)
	(at hoist5 distributor2)
	(at pallet0 depot0)
	(at crate7 distributor2)
	(at hoist3 distributor0)
	(at pallet3 distributor0)
	(at hoist1 depot1)
	(at pallet5 distributor2)
	(at crate6 distributor2)
	(at crate4 depot2)
	(at crate0 depot1)
	(at crate8 distributor2)
	(at hoist0 depot0)
	(at truck0 depot2)
	(clear pallet4)
	(clear crate1)
	(clear pallet3)
	(clear crate9)
	(clear crate3)
	(clear crate8)
	(available distributor0 hoist3)
	(available depot0 hoist0)
	(available depot2 hoist2)
	(available depot1 hoist1)
	(available distributor2 hoist5)
	(available distributor1 hoist4)
	(on crate2 pallet2)
	(on crate7 crate6)
	(on crate8 crate7)
	(on crate6 pallet5)
	(on crate4 crate2)
	(on crate0 pallet1)
	(on crate3 crate0)
	(on crate5 crate4)
	(on crate1 pallet0)
	(on crate9 crate5)
	(driving driver1 truck1)
	(driving driver0 truck0)

)

(:goal
	(and
	(on crate3 crate9)
	(on crate2 pallet5)
	(on crate0 crate7)
	(on crate7 crate1)
	(on crate5 pallet2)
	(on crate4 pallet0)
	(on crate6 crate5)
	(on crate9 crate2)
	(on crate8 pallet3)
	(on crate1 pallet4)
	(dummy-additional-predicate )
)
)

)