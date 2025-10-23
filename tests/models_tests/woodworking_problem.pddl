(define (problem wood-prob)
  (:domain woodworking)
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
    spray-varnisher0 - spray-varnisher
    saw0 - saw
    planer0 - planer
    immersion-varnisher0 - immersion-varnisher
    highspeed-saw0 - highspeed-saw
    grinder0 - grinder
    glazer0 - glazer
  )

  (:init
    (goalsize p2 large)
    (has-colour glazer0 natural)
    (available b0)
    (available p2)
    (goalsize p1 medium)
    (available p0)
    (boardsize-successor s1 s2)
    (empty highspeed-saw0)
    (grind-treatment-change grinder0 varnished colourfragments)
    (has-colour spray-varnisher0 red)
    (wood b0 pine)
    (has-colour spray-varnisher0 natural)
    (surface-condition b0 rough)
    (has-colour glazer0 red)
    (is-smooth verysmooth)
    (boardsize-successor s2 s3)
    (treatment p0 varnished)
    (grind-treatment-change grinder0 glazed untreated)
    (unused p1)
    (colour p2 natural)
    (boardsize b0 s3)
    (wood p0 pine)
    (wood p2 teak)
    (boardsize-successor s0 s1)
    (surface-condition p2 verysmooth)
    (is-smooth smooth)
    (surface-condition p0 smooth)
    (grind-treatment-change grinder0 untreated untreated)
    (has-colour immersion-varnisher0 natural)
    (has-colour immersion-varnisher0 red)
    (goalsize p0 small)
    (grind-treatment-change grinder0 colourfragments untreated)
    (colour p0 red)
    (treatment p2 varnished)
  )

  (:goal
    (and
      (available p1)
      (available p2)
      (available p0)
      (wood p1 pine)
      (surface-condition p1 smooth)
      (colour p1 natural)
      (colour p2 red)
      (treatment p1 varnished)
      (colour p0 natural)
      (wood p0 pine)
      (wood p2 teak)
    )
  )

)