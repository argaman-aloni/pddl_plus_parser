(define (problem depotprob7) (:domain Depot)
(:objects
	depot0 - depot
	distributor0 distributor1 distributor2 - distributor
	truck0 truck1 - truck
	pallet0 pallet1 pallet2 pallet3 pallet4 pallet5 pallet6 pallet7 pallet8 - pallet
	crate0 crate1 crate2 - crate
	hoist0 hoist1 hoist2 hoist3 - hoist)
(:init
	(at pallet0 depot0)
	(clear pallet0)
	(at pallet1 distributor0)
	(clear pallet1)
	(at pallet2 distributor1)
	(clear crate1)
	(at pallet3 distributor2)
	(clear pallet3)
	(at pallet4 depot0)
	(clear pallet4)
	(at pallet5 depot0)
	(clear crate0)
	(at pallet6 distributor1)
	(clear crate2)
	(at pallet7 distributor0)
	(clear pallet7)
	(at pallet8 distributor0)
	(clear pallet8)
	(at truck0 distributor1)
	(at truck1 distributor0)
	(at hoist0 depot0)
	(available hoist0)
	(at hoist1 distributor0)
	(available hoist1)
	(at hoist2 distributor1)
	(available hoist2)
	(at hoist3 distributor2)
	(available hoist3)
	(at crate0 depot0)
	(on crate0 pallet5)
	(at crate1 distributor1)
	(on crate1 pallet2)
	(at crate2 distributor1)
	(on crate2 pallet6)
)

(:goal (and
		(on crate0 pallet8)
		(on crate1 pallet4)
		(on crate2 pallet6)
	)
))
