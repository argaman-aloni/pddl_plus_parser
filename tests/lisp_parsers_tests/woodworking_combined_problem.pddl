(define (problem wood-prob) (:domain woodworking)
(:objects
b0 - board
	p2 - part
	p0 - part
	p1 - part
	s3 - aboardsize
	s2 - aboardsize
	s1 - aboardsize
	s0 - aboardsize
	pine - awood
	teak - awood
	red - acolour
	glazer0 - glazer
	grinder0 - grinder
	highspeed-saw0 - highspeed-saw
	immersion-varnisher0 - immersion-varnisher
	planer0 - planer
	saw0 - saw
	spray-varnisher0 - spray-varnisher
)

(:init
	(is-smooth smooth)
	(is-smooth verysmooth)
	(boardsize-successor s2 s3)
	(boardsize-successor s0 s1)
	(boardsize-successor s1 s2)
	(has-colour immersion-varnisher0 natural)
	(has-colour immersion-varnisher0 red)
	(has-colour glazer0 red)
	(has-colour glazer0 natural)
	(has-colour spray-varnisher0 red)
	(has-colour spray-varnisher0 natural)
	(available b0)
	(available p2)
	(available p0)
	(colour p0 red)
	(colour p2 natural)
	(wood p2 teak)
	(wood p0 pine)
	(wood b0 pine)
	(surface-condition b0 rough)
	(surface-condition p0 smooth)
	(surface-condition p2 verysmooth)
	(treatment p2 varnished)
	(treatment p0 varnished)
	(goalsize p1 medium)
	(goalsize p0 small)
	(goalsize p2 large)
	(unused p1)
	(boardsize b0 s3)
	(grind-treatment-change grinder0 colourfragments untreated)
	(grind-treatment-change grinder0 varnished colourfragments)
	(grind-treatment-change grinder0 untreated untreated)
	(grind-treatment-change grinder0 glazed untreated)
	(empty highspeed-saw0)
	(= (total-cost ) 0.0)
	(= (spray-varnish-cost p0) 5.0)
	(= (glaze-cost p0) 10.0)
	(= (grind-cost p0) 15.0)
	(= (plane-cost p0) 10.0)
	(= (spray-varnish-cost p1) 10.0)
	(= (glaze-cost p1) 15.0)
	(= (grind-cost p1) 30.0)
	(= (plane-cost p1) 20.0)
	(= (spray-varnish-cost p2) 15.0)
	(= (glaze-cost p2) 20.0)
	(= (grind-cost p2) 45.0)
	(= (plane-cost p2) 30.0)

)

(:goal
	(and
	(wood p2 teak)
	(available p1)
	(colour p2 red)
	(colour p1 natural)
	(available p0)
	(surface-condition p1 smooth)
	(available p2)
	(colour p0 natural)
	(treatment p1 varnished)
	(wood p0 pine)
	(wood p1 pine)
)
)

)