(define (domain zeno-travel)
(:requirements :typing :fluents :negative-preconditions :equality)
(:types 	aircraft person - movable
	movable city - object
)

(:predicates (at ?x - movable ?c - city)
	(in ?p - person ?a - aircraft)
)

(:functions (fuel ?a - aircraft)
	(distance ?c1 - city ?c2 - city)
	(slow-burn ?a - aircraft)
	(fast-burn ?a - aircraft)
	(capacity ?a - aircraft)
	(total-fuel-used )
	(onboard ?a - aircraft)
	(zoom-limit ?a - aircraft)
)

(:action board
	:parameters (?p - person ?a - aircraft ?c - city)
	:precondition (and (at ?a ?c)
	(at ?p ?c)
	(not (in ?p ?a))
	(<= (onboard ?a) 6)
	(>= (onboard ?a) 0))
	:effect (and (in ?p ?a)
		(not (at ?p ?c))
(increase (onboard ?a) 1)))

(:action debark
	:parameters (?p - person ?a - aircraft ?c - city)
	:precondition (and (at ?a ?c)
	(in ?p ?a)
	(not (at ?p ?c))
	(<= (onboard ?a) 7)
	(>= (onboard ?a) 1))
	:effect (and (at ?p ?c)
		(not (in ?p ?a))
(decrease (onboard ?a) 1)))

(:action fly
	:parameters (?a - aircraft ?c1 - city ?c2 - city)
	:precondition (and (at ?a ?c1)
	(not (at ?a ?c2))
	(<= (* (* (distance ?c1 ?c2) (slow-burn ?a)) -1) -466.24)
	(<= (* (* (distance ?c1 ?c2) (slow-burn ?a)) -1) -504.97)
	(<= (* (* (distance ?c1 ?c2) (slow-burn ?a)) -1) -505.17)
	(<= (* (total-fuel-used ) -1) 0)
	(<= (+ (* (fuel ?a) -0.01) (* (* (distance ?c1 ?c2) (slow-burn ?a)) -1)) -519.99)
	(<= (+ (* (fuel ?a) -0.01) (* (* (distance ?c1 ?c2) (slow-burn ?a)) -1)) -522.01)
	(<= (+ (* (fuel ?a) -0.01) (* (* (distance ?c1 ?c2) (slow-burn ?a)) -1)) -524.11)
	(<= (+ (* (fuel ?a) -0.04) (* (* (distance ?c1 ?c2) (slow-burn ?a)) -1)) -518.38)
	(<= (+ (* (fuel ?a) -0.05) (+ (* (total-fuel-used ) -0.05) (* (distance ?c1 ?c2) (slow-burn ?a)))) 4054.27)
	(<= (+ (* (fuel ?a) -0.06) (+ (* (total-fuel-used ) -0.01) (* (distance ?c1 ?c2) (slow-burn ?a)))) 4316.81)
	(<= (+ (* (fuel ?a) -0.06) (+ (* (total-fuel-used ) -0.05) (* (distance ?c1 ?c2) (slow-burn ?a)))) 3910.55)
	(<= (+ (* (fuel ?a) -0.07) (+ (* (total-fuel-used ) -0.07) (* (distance ?c1 ?c2) (slow-burn ?a)))) 3796.03)
	(<= (+ (* (fuel ?a) -0.09) (+ (* (total-fuel-used ) -0.03) (* (distance ?c1 ?c2) (slow-burn ?a)))) 3877.92)
	(<= (+ (* (fuel ?a) -0.26) (* (* (distance ?c1 ?c2) (slow-burn ?a)) -0.97)) -692.24)
	(<= (+ (* (fuel ?a) -0.35) (+ (* (total-fuel-used ) 0.03) (* (* (distance ?c1 ?c2) (slow-burn ?a)) 0.94))) 3485.47)
	(<= (+ (* (fuel ?a) -0.43) (+ (* (total-fuel-used ) -0.05) (* (* (distance ?c1 ?c2) (slow-burn ?a)) 0.90))) 1789.57)
	(<= (+ (* (fuel ?a) -0.51) (+ (* (total-fuel-used ) 0.01) (* (* (distance ?c1 ?c2) (slow-burn ?a)) 0.86))) 1579.85)
	(<= (+ (* (fuel ?a) -0.52) (+ (* (total-fuel-used ) 0.01) (* (* (distance ?c1 ?c2) (slow-burn ?a)) 0.85))) 1411.58)
	(<= (+ (* (fuel ?a) -0.52) (+ (* (total-fuel-used ) 0.01) (* (* (distance ?c1 ?c2) (slow-burn ?a)) 0.85))) 1424.13)
	(<= (+ (* (fuel ?a) -0.55) (+ (* (total-fuel-used ) 0.10) (* (* (distance ?c1 ?c2) (slow-burn ?a)) 0.83))) 4712.05)
	(<= (+ (* (fuel ?a) -0.58) (+ (* (total-fuel-used ) 0.01) (* (* (distance ?c1 ?c2) (slow-burn ?a)) 0.82))) 1022.93)
	(<= (+ (* (fuel ?a) -0.60) (+ (* (total-fuel-used ) 0.01) (* (* (distance ?c1 ?c2) (slow-burn ?a)) 0.80))) 962.22)
	(<= (+ (* (fuel ?a) -0.62) (* (* (distance ?c1 ?c2) (slow-burn ?a)) 0.79)) 684.97)
	(<= (+ (* (fuel ?a) -0.64) (* (* (distance ?c1 ?c2) (slow-burn ?a)) 0.77)) 433.44)
	(<= (+ (* (fuel ?a) -0.65) (+ (* (total-fuel-used ) 0.01) (* (* (distance ?c1 ?c2) (slow-burn ?a)) 0.76))) 599.71)
	(<= (+ (* (fuel ?a) -0.65) (+ (* (total-fuel-used ) 0.15) (* (* (distance ?c1 ?c2) (slow-burn ?a)) 0.74))) 6010.86)
	(<= (+ (* (fuel ?a) -0.66) (+ (* (total-fuel-used ) 0.01) (* (* (distance ?c1 ?c2) (slow-burn ?a)) 0.75))) 462.20)
	(<= (+ (* (fuel ?a) -0.66) (+ (* (total-fuel-used ) 0.02) (* (* (distance ?c1 ?c2) (slow-burn ?a)) 0.75))) 625.45)
	(<= (+ (* (fuel ?a) -0.67) (+ (* (total-fuel-used ) 0.02) (* (* (distance ?c1 ?c2) (slow-burn ?a)) 0.75))) 740.74)
	(<= (+ (* (fuel ?a) -0.69) (* (* (distance ?c1 ?c2) (slow-burn ?a)) 0.73)) 168.16)
	(<= (+ (* (fuel ?a) -0.70) (* (* (distance ?c1 ?c2) (slow-burn ?a)) 0.71)) 8.61)
	(<= (+ (* (fuel ?a) -0.70) (+ (* (total-fuel-used ) -0.01) (* (* (distance ?c1 ?c2) (slow-burn ?a)) 0.72))) 44.10)
	(<= (+ (* (fuel ?a) -0.71) (* (* (distance ?c1 ?c2) (slow-burn ?a)) 0.71)) -0.93)
	(<= (+ (* (fuel ?a) -0.71) (* (* (distance ?c1 ?c2) (slow-burn ?a)) 0.71)) 1.04)
	(<= (+ (* (fuel ?a) -0.71) (+ (* (total-fuel-used ) 0.01) (* (* (distance ?c1 ?c2) (slow-burn ?a)) 0.71))) 299.24)
	(<= (+ (* (fuel ?a) -0.71) (+ (* (total-fuel-used ) 0.01) (* (* (distance ?c1 ?c2) (slow-burn ?a)) 0.71))) 299.99)
	(<= (+ (* (fuel ?a) -0.72) (* (* (distance ?c1 ?c2) (slow-burn ?a)) 0.69)) -44.49)
	(<= (+ (* (fuel ?a) -0.72) (* (* (distance ?c1 ?c2) (slow-burn ?a)) 0.70)) -11.17)
	(<= (+ (* (fuel ?a) -0.83) (* (* (distance ?c1 ?c2) (slow-burn ?a)) 0.56)) -215.69)
	(<= (+ (* (fuel ?a) -0.83) (* (* (distance ?c1 ?c2) (slow-burn ?a)) 0.56)) -218.73)
	(<= (+ (* (fuel ?a) -0.83) (* (* (distance ?c1 ?c2) (slow-burn ?a)) 0.56)) -225.70)
	(<= (+ (* (fuel ?a) -0.89) (* (* (distance ?c1 ?c2) (slow-burn ?a)) 0.45)) -348.52)
	(<= (+ (* (fuel ?a) 0.01) (+ (* (total-fuel-used ) 0.01) (* (distance ?c1 ?c2) (slow-burn ?a)))) 5107.02)
	(<= (+ (* (fuel ?a) 0.01) (+ (* (total-fuel-used ) 0.01) (* (distance ?c1 ?c2) (slow-burn ?a)))) 5348.26)
	(<= (+ (* (fuel ?a) 0.02) (+ (* (total-fuel-used ) -0.10) (* (* (distance ?c1 ?c2) (slow-burn ?a)) 0.99))) 4781.10)
	(<= (+ (* (fuel ?a) 0.02) (+ (* (total-fuel-used ) 0.01) (* (distance ?c1 ?c2) (slow-burn ?a)))) 5324.10)
	(<= (+ (* (fuel ?a) 0.03) (* (* (distance ?c1 ?c2) (slow-burn ?a)) -1)) -346.16)
	(<= (+ (* (fuel ?a) 0.05) (* (* (distance ?c1 ?c2) (slow-burn ?a)) -1)) -391.86)
	(<= (+ (* (fuel ?a) 0.09) (+ (* (total-fuel-used ) -0.43) (* (* (distance ?c1 ?c2) (slow-burn ?a)) 0.90))) 5097.62)
	(<= (+ (* (fuel ?a) 0.12) (+ (* (total-fuel-used ) 0.38) (* (* (distance ?c1 ?c2) (slow-burn ?a)) -0.92))) 14891.35)
	(<= (+ (* (fuel ?a) 0.15) (+ (* (total-fuel-used ) 0.02) (* (* (distance ?c1 ?c2) (slow-burn ?a)) -0.99))) 455.22)
	(<= (+ (* (fuel ?a) 0.16) (* (* (distance ?c1 ?c2) (slow-burn ?a)) -0.99)) -54.32)
	(<= (+ (* (fuel ?a) 0.16) (* (* (distance ?c1 ?c2) (slow-burn ?a)) -0.99)) 42.14)
	(<= (+ (* (fuel ?a) 0.17) (* (* (distance ?c1 ?c2) (slow-burn ?a)) -0.99)) -39.17)
	(<= (+ (* (fuel ?a) 0.19) (+ (* (total-fuel-used ) 0.02) (* (* (distance ?c1 ?c2) (slow-burn ?a)) 0.98))) 7851.94)
	(<= (+ (* (fuel ?a) 0.20) (+ (* (total-fuel-used ) -0.14) (* (* (distance ?c1 ?c2) (slow-burn ?a)) -0.97))) 55.25)
	(<= (+ (* (fuel ?a) 0.20) (+ (* (total-fuel-used ) -0.15) (* (* (distance ?c1 ?c2) (slow-burn ?a)) -0.97))) 68.42)
	(<= (+ (* (fuel ?a) 0.20) (+ (* (total-fuel-used ) 0.09) (* (* (distance ?c1 ?c2) (slow-burn ?a)) -0.98))) 3421.25)
	(<= (+ (* (fuel ?a) 0.24) (+ (* (total-fuel-used ) -0.02) (* (* (distance ?c1 ?c2) (slow-burn ?a)) -0.97))) 603.52)
	(<= (+ (* (fuel ?a) 0.25) (+ (* (total-fuel-used ) 0.03) (* (* (distance ?c1 ?c2) (slow-burn ?a)) 0.97))) 8709.52)
	(<= (+ (* (fuel ?a) 0.25) (+ (* (total-fuel-used ) 0.25) (* (* (distance ?c1 ?c2) (slow-burn ?a)) 0.94))) 18030.96)
	(<= (+ (* (fuel ?a) 0.31) (+ (* (total-fuel-used ) 0.03) (* (* (distance ?c1 ?c2) (slow-burn ?a)) 0.95))) 9392.30)
	(<= (+ (* (fuel ?a) 0.32) (+ (* (total-fuel-used ) -0.16) (* (* (distance ?c1 ?c2) (slow-burn ?a)) 0.93))) 8582.61)
	(<= (+ (* (fuel ?a) 0.73) (+ (* (total-fuel-used ) 0.01) (* (* (distance ?c1 ?c2) (slow-burn ?a)) 0.68))) 14193.17)
	(<= (+ (* (fuel ?a) 0.75) (+ (* (total-fuel-used ) -0.05) (* (* (distance ?c1 ?c2) (slow-burn ?a)) -0.66))) 8306.13)
	(<= (+ (* (fuel ?a) 0.83) (+ (* (total-fuel-used ) -0.11) (* (* (distance ?c1 ?c2) (slow-burn ?a)) -0.54))) 9781.48)
	(<= (+ (* (fuel ?a) 0.97) (+ (* (total-fuel-used ) -0.04) (* (* (distance ?c1 ?c2) (slow-burn ?a)) -0.24))) 13159.52)
	(<= (+ (* (fuel ?a) 0.99) (* (* (distance ?c1 ?c2) (slow-burn ?a)) 0.14)) 15763.24)
	(<= (+ (fuel ?a) (+ (* (total-fuel-used ) -0.05) (* (* (distance ?c1 ?c2) (slow-burn ?a)) -0.01))) 14404.38)
	(<= (+ (fuel ?a) (+ (* (total-fuel-used ) -0.05) (* (* (distance ?c1 ?c2) (slow-burn ?a)) -0.02))) 14365.63)(not (= ?c1 ?c2)))
	:effect (and (at ?a ?c2)
		(not (at ?a ?c1))
(decrease (fuel ?a) (* (distance ?c1 ?c2) (slow-burn ?a)))
(increase (total-fuel-used ) (* (distance ?c1 ?c2) (slow-burn ?a)))))

(:action zoom
	:parameters (?a - aircraft ?c1 - city ?c2 - city)
	:precondition (and (at ?a ?c1)
	(not (at ?a ?c2))
	(<= (* (onboard ?a) -1) 0)
	(<= (* (onboard ?a) -1) 5.20)
	(<= (* (onboard ?a) -1) 6.56)
	(<= (* (total-fuel-used ) -1) 0)
	(<= (* (zoom-limit ?a) -1) -1)
	(<= (* (zoom-limit ?a) -1) -2)
	(<= (+ (* (fuel ?a) -0.01) (+ (* (onboard ?a) -0.08) (+ (* (zoom-limit ?a) -1) (* (* (distance ?c1 ?c2) (fast-burn ?a)) -0.01)))) -43.52)
	(<= (+ (* (fuel ?a) -0.01) (+ (* (onboard ?a) -0.22) (+ (* (zoom-limit ?a) -0.98) (* (* (distance ?c1 ?c2) (fast-burn ?a)) 0.01)))) -9.25)
	(<= (+ (* (fuel ?a) -0.01) (+ (* (onboard ?a) -0.60) (+ (* (zoom-limit ?a) 0.80) (* (* (distance ?c1 ?c2) (fast-burn ?a)) 0.01)))) 8.16)
	(<= (+ (* (fuel ?a) -0.01) (+ (* (onboard ?a) -0.95) (+ (* (zoom-limit ?a) 0.31) (* (* (distance ?c1 ?c2) (fast-burn ?a)) 0.01)))) -0.47)
	(<= (+ (* (fuel ?a) -0.01) (+ (* (onboard ?a) 0.50) (* (zoom-limit ?a) -0.87))) -31.09)
	(<= (+ (* (fuel ?a) -0.01) (+ (* (onboard ?a) 0.59) (* (zoom-limit ?a) -0.81))) -29.50)
	(<= (+ (* (fuel ?a) -0.01) (+ (* (onboard ?a) 0.99) (+ (* (zoom-limit ?a) 0.11) (* (* (distance ?c1 ?c2) (fast-burn ?a)) 0.01)))) -5.10)
	(<= (+ (* (fuel ?a) -0.05) (+ (* (onboard ?a) 0.90) (+ (* (zoom-limit ?a) 0.43) (* (* (distance ?c1 ?c2) (fast-burn ?a)) 0.05)))) 17.17)
	(<= (+ (* (fuel ?a) 0.01) (+ (* (onboard ?a) -0.43) (* (zoom-limit ?a) 0.90))) 61.39)
	(<= (+ (* (fuel ?a) 0.01) (+ (* (onboard ?a) 0.34) (* (zoom-limit ?a) 0.94))) 64.74)
	(<= (+ (* (onboard ?a) -0.01) (* (zoom-limit ?a) -1)) -2.64)
	(<= (+ (* (onboard ?a) -0.02) (* (zoom-limit ?a) -1)) -12.11)
	(<= (+ (* (onboard ?a) -0.02) (* (zoom-limit ?a) -1)) -12.12)
	(<= (+ (* (onboard ?a) -0.02) (* (zoom-limit ?a) -1)) -3.93)
	(<= (+ (* (onboard ?a) -0.02) (* (zoom-limit ?a) -1)) -6.15)
	(<= (+ (* (onboard ?a) -0.02) (* (zoom-limit ?a) -1)) -9.16)
	(<= (+ (* (onboard ?a) -0.03) (* (zoom-limit ?a) -1)) -11.63)
	(<= (+ (* (onboard ?a) -0.04) (* (zoom-limit ?a) -1)) -11.62)
	(<= (+ (* (onboard ?a) -0.05) (zoom-limit ?a)) 24.44)
	(<= (+ (* (onboard ?a) -0.05) (zoom-limit ?a)) 7.56)
	(<= (+ (* (onboard ?a) -0.06) (* (zoom-limit ?a) -1)) -11.61)
	(<= (+ (* (onboard ?a) -0.06) (* (zoom-limit ?a) -1)) -2.51)
	(<= (+ (* (onboard ?a) -0.06) (zoom-limit ?a)) 8.64)
	(<= (+ (* (onboard ?a) -0.07) (* (zoom-limit ?a) -1)) -0.11)
	(<= (+ (* (onboard ?a) -0.07) (zoom-limit ?a)) 5.82)
	(<= (+ (* (onboard ?a) -0.07) (zoom-limit ?a)) 6.43)
	(<= (+ (* (onboard ?a) -0.09) (* (zoom-limit ?a) -1)) -11.22)
	(<= (+ (* (onboard ?a) -0.09) (* (zoom-limit ?a) -1)) 0.68)
	(<= (+ (* (onboard ?a) -0.10) (* (zoom-limit ?a) 0.99)) 6.18)
	(<= (+ (* (onboard ?a) -0.12) (* (zoom-limit ?a) 0.99)) 8.65)
	(<= (+ (* (onboard ?a) -0.13) (* (zoom-limit ?a) 0.99)) 8.17)
	(<= (+ (* (onboard ?a) -0.14) (* (zoom-limit ?a) -0.99)) 1.26)
	(<= (+ (* (onboard ?a) -0.14) (* (zoom-limit ?a) 0.99)) 8.53)
	(<= (+ (* (onboard ?a) -0.15) (* (zoom-limit ?a) -0.99)) 1.21)
	(<= (+ (* (onboard ?a) -0.17) (* (zoom-limit ?a) 0.98)) 25.89)
	(<= (+ (* (onboard ?a) -0.17) (* (zoom-limit ?a) 0.99)) 8.41)
	(<= (+ (* (onboard ?a) -0.20) (* (zoom-limit ?a) -0.98)) 1.51)
	(<= (+ (* (onboard ?a) -0.22) (* (zoom-limit ?a) -0.97)) 0.53)
	(<= (+ (* (onboard ?a) -0.22) (* (zoom-limit ?a) -0.97)) 1.71)
	(<= (+ (* (onboard ?a) -0.22) (* (zoom-limit ?a) -0.98)) -2.45)
	(<= (+ (* (onboard ?a) -0.22) (* (zoom-limit ?a) -0.98)) 3.17)
	(<= (+ (* (onboard ?a) -0.23) (* (zoom-limit ?a) 0.97)) 5.96)
	(<= (+ (* (onboard ?a) -0.25) (* (zoom-limit ?a) -0.97)) -3.92)
	(<= (+ (* (onboard ?a) -0.26) (* (zoom-limit ?a) -0.97)) -3.42)
	(<= (+ (* (onboard ?a) -0.27) (* (zoom-limit ?a) 0.96)) 8.40)
	(<= (+ (* (onboard ?a) -0.28) (* (zoom-limit ?a) -0.96)) -0.86)
	(<= (+ (* (onboard ?a) -0.28) (* (zoom-limit ?a) -0.96)) -11.25)
	(<= (+ (* (onboard ?a) -0.28) (+ (* (zoom-limit ?a) 0.96) (* (* (distance ?c1 ?c2) (fast-burn ?a)) -0.01))) 14.72)
	(<= (+ (* (onboard ?a) -0.29) (* (zoom-limit ?a) -0.96)) -0.43)
	(<= (+ (* (onboard ?a) -0.29) (* (zoom-limit ?a) 0.96)) 8.34)
	(<= (+ (* (onboard ?a) -0.31) (* (zoom-limit ?a) 0.95)) 7.72)
	(<= (+ (* (onboard ?a) -0.33) (* (zoom-limit ?a) -0.94)) -0.88)
	(<= (+ (* (onboard ?a) -0.34) (* (zoom-limit ?a) 0.94)) 36.38)
	(<= (+ (* (onboard ?a) -0.36) (* (zoom-limit ?a) -0.93)) -0.79)
	(<= (+ (* (onboard ?a) -0.36) (* (zoom-limit ?a) -0.93)) -1.12)
	(<= (+ (* (onboard ?a) -0.38) (* (zoom-limit ?a) -0.92)) 3.12)
	(<= (+ (* (onboard ?a) -0.38) (* (zoom-limit ?a) -0.93)) -10.93)
	(<= (+ (* (onboard ?a) -0.38) (* (zoom-limit ?a) -0.93)) 3.10)
	(<= (+ (* (onboard ?a) -0.38) (* (zoom-limit ?a) 0.93)) 7.34)
	(<= (+ (* (onboard ?a) -0.39) (* (zoom-limit ?a) -0.92)) -6.60)
	(<= (+ (* (onboard ?a) -0.39) (* (zoom-limit ?a) -0.92)) -7.65)
	(<= (+ (* (onboard ?a) -0.39) (* (zoom-limit ?a) -0.92)) -8.66)
	(<= (+ (* (onboard ?a) -0.39) (* (zoom-limit ?a) -0.92)) 0.79)
	(<= (+ (* (onboard ?a) -0.39) (* (zoom-limit ?a) 0.92)) 6.66)
	(<= (+ (* (onboard ?a) -0.40) (* (zoom-limit ?a) -0.92)) -7.31)
	(<= (+ (* (onboard ?a) -0.40) (* (zoom-limit ?a) 0.92)) 24.92)
	(<= (+ (* (onboard ?a) -0.42) (* (zoom-limit ?a) -0.91)) -7.50)
	(<= (+ (* (onboard ?a) -0.43) (* (zoom-limit ?a) -0.90)) -10.78)
	(<= (+ (* (onboard ?a) -0.43) (* (zoom-limit ?a) -0.90)) -6.91)
	(<= (+ (* (onboard ?a) -0.43) (* (zoom-limit ?a) 0.90)) 7.18)
	(<= (+ (* (onboard ?a) -0.47) (* (zoom-limit ?a) -0.88)) -7.20)
	(<= (+ (* (onboard ?a) -0.49) (* (zoom-limit ?a) -0.87)) 1.74)
	(<= (+ (* (onboard ?a) -0.50) (* (zoom-limit ?a) -0.87)) -3.05)
	(<= (+ (* (onboard ?a) -0.50) (* (zoom-limit ?a) 0.86)) 5.70)
	(<= (+ (* (onboard ?a) -0.54) (* (zoom-limit ?a) -0.84)) -1.04)
	(<= (+ (* (onboard ?a) -0.54) (* (zoom-limit ?a) 0.84)) 6.14)
	(<= (+ (* (onboard ?a) -0.55) (* (zoom-limit ?a) -0.83)) -3.28)
	(<= (+ (* (onboard ?a) -0.55) (* (zoom-limit ?a) -0.83)) -6.64)
	(<= (+ (* (onboard ?a) -0.56) (* (zoom-limit ?a) -0.83)) -1.02)
	(<= (+ (* (onboard ?a) -0.56) (* (zoom-limit ?a) -0.83)) 1.49)
	(<= (+ (* (onboard ?a) -0.58) (* (zoom-limit ?a) 0.82)) 9.95)
	(<= (+ (* (onboard ?a) -0.59) (* (zoom-limit ?a) -0.80)) -0.63)
	(<= (+ (* (onboard ?a) -0.59) (* (zoom-limit ?a) -0.80)) -2.86)
	(<= (+ (* (onboard ?a) -0.59) (* (zoom-limit ?a) -0.81)) -1.05)
	(<= (+ (* (onboard ?a) -0.63) (* (zoom-limit ?a) 0.78)) 4.90)
	(<= (+ (* (onboard ?a) -0.65) (* (zoom-limit ?a) -0.76)) -6.18)
	(<= (+ (* (onboard ?a) -0.65) (* (zoom-limit ?a) 0.76)) 20.47)
	(<= (+ (* (onboard ?a) -0.66) (* (zoom-limit ?a) 0.75)) 5.19)
	(<= (+ (* (onboard ?a) -0.66) (* (zoom-limit ?a) 0.75)) 5.20)
	(<= (+ (* (onboard ?a) -0.66) (* (zoom-limit ?a) 0.75)) 5.23)
	(<= (+ (* (onboard ?a) -0.68) (* (zoom-limit ?a) -0.73)) -1.67)
	(<= (+ (* (onboard ?a) -0.70) (* (zoom-limit ?a) -0.71)) -1.23)
	(<= (+ (* (onboard ?a) -0.70) (* (zoom-limit ?a) -0.71)) -1.30)
	(<= (+ (* (onboard ?a) -0.71) (* (zoom-limit ?a) -0.71)) -1.31)
	(<= (+ (* (onboard ?a) -0.73) (* (zoom-limit ?a) -0.68)) -1.03)
	(<= (+ (* (onboard ?a) -0.73) (* (zoom-limit ?a) -0.69)) 0.44)
	(<= (+ (* (onboard ?a) -0.73) (* (zoom-limit ?a) 0.68)) 19.02)
	(<= (+ (* (onboard ?a) -0.75) (* (zoom-limit ?a) 0.66)) 12.43)
	(<= (+ (* (onboard ?a) -0.75) (+ (* (zoom-limit ?a) -0.66) (* (* (distance ?c1 ?c2) (fast-burn ?a)) -0.02))) -29.66)
	(<= (+ (* (onboard ?a) -0.78) (* (zoom-limit ?a) -0.63)) -2.38)
	(<= (+ (* (onboard ?a) -0.79) (* (zoom-limit ?a) -0.61)) 0.82)
	(<= (+ (* (onboard ?a) -0.80) (* (zoom-limit ?a) -0.60)) -6.41)
	(<= (+ (* (onboard ?a) -0.82) (* (zoom-limit ?a) -0.57)) -1.99)
	(<= (+ (* (onboard ?a) -0.82) (* (zoom-limit ?a) 0.57)) 6.42)
	(<= (+ (* (onboard ?a) -0.83) (* (zoom-limit ?a) -0.56)) -3.62)
	(<= (+ (* (onboard ?a) -0.86) (+ (* (zoom-limit ?a) 0.51) (* (* (distance ?c1 ?c2) (fast-burn ?a)) -0.03))) -24.54)
	(<= (+ (* (onboard ?a) -0.87) (* (zoom-limit ?a) -0.49)) -8.69)
	(<= (+ (* (onboard ?a) -0.88) (* (zoom-limit ?a) -0.47)) -3.20)
	(<= (+ (* (onboard ?a) -0.88) (* (zoom-limit ?a) -0.47)) -5.54)
	(<= (+ (* (onboard ?a) -0.88) (* (zoom-limit ?a) -0.48)) -2.23)
	(<= (+ (* (onboard ?a) -0.88) (* (zoom-limit ?a) 0.47)) 27.69)
	(<= (+ (* (onboard ?a) -0.89) (* (zoom-limit ?a) -0.46)) -4.55)
	(<= (+ (* (onboard ?a) -0.90) (* (zoom-limit ?a) -0.44)) 3.76)
	(<= (+ (* (onboard ?a) -0.90) (* (zoom-limit ?a) 0.43)) 2.85)
	(<= (+ (* (onboard ?a) -0.91) (* (zoom-limit ?a) -0.41)) -2.07)
	(<= (+ (* (onboard ?a) -0.92) (* (zoom-limit ?a) -0.38)) 0.47)
	(<= (+ (* (onboard ?a) -0.92) (* (zoom-limit ?a) 0.38)) 3.29)
	(<= (+ (* (onboard ?a) -0.92) (* (zoom-limit ?a) 0.39)) 2.83)
	(<= (+ (* (onboard ?a) -0.92) (* (zoom-limit ?a) 0.39)) 6.78)
	(<= (+ (* (onboard ?a) -0.93) (* (zoom-limit ?a) 0.38)) 5.33)
	(<= (+ (* (onboard ?a) -0.94) (* (zoom-limit ?a) -0.33)) -1.51)
	(<= (+ (* (onboard ?a) -0.94) (* (zoom-limit ?a) -0.33)) -3.96)
	(<= (+ (* (onboard ?a) -0.94) (* (zoom-limit ?a) -0.35)) -1.66)
	(<= (+ (* (onboard ?a) -0.95) (* (zoom-limit ?a) -0.31)) -0.81)
	(<= (+ (* (onboard ?a) -0.95) (* (zoom-limit ?a) -0.31)) -4.75)
	(<= (+ (* (onboard ?a) -0.95) (* (zoom-limit ?a) -0.32)) -3.80)
	(<= (+ (* (onboard ?a) -0.95) (* (zoom-limit ?a) -0.32)) -4.09)
	(<= (+ (* (onboard ?a) -0.95) (* (zoom-limit ?a) 0.31)) 2.14)
	(<= (+ (* (onboard ?a) -0.95) (* (zoom-limit ?a) 0.32)) 2.66)
	(<= (+ (* (onboard ?a) -0.96) (* (zoom-limit ?a) -0.27)) -3.91)
	(<= (+ (* (onboard ?a) -0.96) (* (zoom-limit ?a) -0.27)) 1.69)
	(<= (+ (* (onboard ?a) -0.96) (* (zoom-limit ?a) -0.29)) -4.38)
	(<= (+ (* (onboard ?a) -0.96) (* (zoom-limit ?a) -0.29)) 3.19)
	(<= (+ (* (onboard ?a) -0.96) (* (zoom-limit ?a) 0.29)) 0.32)
	(<= (+ (* (onboard ?a) -0.97) (* (zoom-limit ?a) -0.25)) 0.39)
	(<= (+ (* (onboard ?a) -0.97) (* (zoom-limit ?a) 0.23)) 3.50)
	(<= (+ (* (onboard ?a) -0.98) (* (zoom-limit ?a) -0.17)) 0.95)
	(<= (+ (* (onboard ?a) -0.98) (* (zoom-limit ?a) -0.18)) -1.13)
	(<= (+ (* (onboard ?a) -0.98) (* (zoom-limit ?a) -0.18)) -1.76)
	(<= (+ (* (onboard ?a) -0.98) (* (zoom-limit ?a) -0.19)) -0.36)
	(<= (+ (* (onboard ?a) -0.98) (* (zoom-limit ?a) -0.19)) -1.22)
	(<= (+ (* (onboard ?a) -0.98) (* (zoom-limit ?a) -0.19)) -1.27)
	(<= (+ (* (onboard ?a) -0.98) (* (zoom-limit ?a) -0.19)) 0.56)
	(<= (+ (* (onboard ?a) -0.98) (* (zoom-limit ?a) -0.20)) -2.81)
	(<= (+ (* (onboard ?a) -0.98) (* (zoom-limit ?a) -0.20)) -4.74)
	(<= (+ (* (onboard ?a) -0.98) (* (zoom-limit ?a) -0.22)) -0.42)
	(<= (+ (* (onboard ?a) -0.98) (* (zoom-limit ?a) -0.22)) -1.39)
	(<= (+ (* (onboard ?a) -0.98) (* (zoom-limit ?a) 0.21)) 3.22)
	(<= (+ (* (onboard ?a) -0.98) (* (zoom-limit ?a) 0.22)) 5.71)
	(<= (+ (* (onboard ?a) -0.99) (* (zoom-limit ?a) -0.10)) 0.71)
	(<= (+ (* (onboard ?a) -0.99) (* (zoom-limit ?a) -0.11)) -0.47)
	(<= (+ (* (onboard ?a) -0.99) (* (zoom-limit ?a) -0.14)) -0.52)
	(<= (+ (* (onboard ?a) -0.99) (* (zoom-limit ?a) -0.14)) -0.80)
	(<= (+ (* (onboard ?a) -0.99) (* (zoom-limit ?a) -0.14)) -1.70)
	(<= (+ (* (onboard ?a) -0.99) (* (zoom-limit ?a) -0.14)) -1.74)
	(<= (+ (* (onboard ?a) -0.99) (* (zoom-limit ?a) -0.14)) -1.79)
	(<= (+ (* (onboard ?a) -0.99) (* (zoom-limit ?a) -0.15)) -1.81)
	(<= (+ (* (onboard ?a) -0.99) (* (zoom-limit ?a) -0.15)) -1.83)
	(<= (+ (* (onboard ?a) -0.99) (* (zoom-limit ?a) -0.16)) 0.09)
	(<= (+ (* (onboard ?a) -0.99) (* (zoom-limit ?a) -0.17)) 0.85)
	(<= (+ (* (onboard ?a) -0.99) (* (zoom-limit ?a) 0.11)) 4.31)
	(<= (+ (* (onboard ?a) -0.99) (+ (* (zoom-limit ?a) 0.12) (* (* (distance ?c1 ?c2) (fast-burn ?a)) -0.01))) -16.01)
	(<= (+ (* (onboard ?a) -1) (* (zoom-limit ?a) -0.01)) 2.27)
	(<= (+ (* (onboard ?a) -1) (* (zoom-limit ?a) -0.02)) 1.08)
	(<= (+ (* (onboard ?a) -1) (* (zoom-limit ?a) -0.02)) 1.50)
	(<= (+ (* (onboard ?a) -1) (* (zoom-limit ?a) -0.03)) 0.34)
	(<= (+ (* (onboard ?a) -1) (* (zoom-limit ?a) -0.03)) 1.45)
	(<= (+ (* (onboard ?a) -1) (* (zoom-limit ?a) -0.04)) 1.26)
	(<= (+ (* (onboard ?a) -1) (* (zoom-limit ?a) -0.06)) 0.15)
	(<= (+ (* (onboard ?a) -1) (* (zoom-limit ?a) -0.07)) -0.59)
	(<= (+ (* (onboard ?a) -1) (* (zoom-limit ?a) -0.07)) -1.17)
	(<= (+ (* (onboard ?a) -1) (* (zoom-limit ?a) -0.07)) -1.19)
	(<= (+ (* (onboard ?a) -1) (* (zoom-limit ?a) -0.07)) -1.23)
	(<= (+ (* (onboard ?a) -1) (* (zoom-limit ?a) -0.07)) 0.54)
	(<= (+ (* (onboard ?a) -1) (* (zoom-limit ?a) -0.07)) 0.57)
	(<= (+ (* (onboard ?a) -1) (* (zoom-limit ?a) -0.07)) 0.95)
	(<= (+ (* (onboard ?a) -1) (* (zoom-limit ?a) -0.08)) 0.53)
	(<= (+ (* (onboard ?a) -1) (* (zoom-limit ?a) -0.08)) 1.84)
	(<= (+ (* (onboard ?a) -1) (* (zoom-limit ?a) -0.09)) -0.51)
	(<= (+ (* (onboard ?a) -1) (* (zoom-limit ?a) -0.10)) 0.64)
	(<= (+ (* (onboard ?a) -1) (* (zoom-limit ?a) 0.06)) 4.67)
	(<= (+ (* (onboard ?a) -1) (* (zoom-limit ?a) 0.08)) 2.45)
	(<= (+ (* (onboard ?a) -1) (+ (* (zoom-limit ?a) -0.01) (* (* (distance ?c1 ?c2) (fast-burn ?a)) -0.01))) 1.54)
	(<= (+ (* (onboard ?a) -1) (+ (* (zoom-limit ?a) -0.01) (* (* (distance ?c1 ?c2) (fast-burn ?a)) -0.01))) 1.61)
	(<= (+ (* (onboard ?a) -1) (+ (* (zoom-limit ?a) 0.04) (* (* (distance ?c1 ?c2) (fast-burn ?a)) -0.01))) 2.47)
	(<= (+ (* (onboard ?a) 0.01) (zoom-limit ?a)) 8.66)
	(<= (+ (* (onboard ?a) 0.02) (* (zoom-limit ?a) -1)) -1.97)
	(<= (+ (* (onboard ?a) 0.02) (* (zoom-limit ?a) -1)) 2.78)
	(<= (+ (* (onboard ?a) 0.02) (zoom-limit ?a)) 8.68)
	(<= (+ (* (onboard ?a) 0.03) (* (zoom-limit ?a) -1)) -1.92)
	(<= (+ (* (onboard ?a) 0.03) (* (zoom-limit ?a) -1)) -1.93)
	(<= (+ (* (onboard ?a) 0.04) (* (zoom-limit ?a) -1)) -2.92)
	(<= (+ (* (onboard ?a) 0.04) (zoom-limit ?a)) 8.53)
	(<= (+ (* (onboard ?a) 0.04) (zoom-limit ?a)) 8.73)
	(<= (+ (* (onboard ?a) 0.07) (* (zoom-limit ?a) -1)) -8.11)
	(<= (+ (* (onboard ?a) 0.08) (* (zoom-limit ?a) -1)) -0.57)
	(<= (+ (* (onboard ?a) 0.08) (* (zoom-limit ?a) -1)) 3.18)
	(<= (+ (* (onboard ?a) 0.09) (zoom-limit ?a)) 8.43)
	(<= (+ (* (onboard ?a) 0.09) (zoom-limit ?a)) 8.79)
	(<= (+ (* (onboard ?a) 0.10) (* (zoom-limit ?a) 0.99)) 8.73)
	(<= (+ (* (onboard ?a) 0.10) (zoom-limit ?a)) 8.38)
	(<= (+ (* (onboard ?a) 0.14) (* (zoom-limit ?a) 0.99)) 8.43)
	(<= (+ (* (onboard ?a) 0.15) (* (zoom-limit ?a) -0.99)) -11.83)
	(<= (+ (* (onboard ?a) 0.16) (* (zoom-limit ?a) 0.99)) 8.39)
	(<= (+ (* (onboard ?a) 0.16) (* (zoom-limit ?a) 0.99)) 8.42)
	(<= (+ (* (onboard ?a) 0.19) (* (zoom-limit ?a) -0.98)) 3.12)
	(<= (+ (* (onboard ?a) 0.24) (* (zoom-limit ?a) 0.97)) 8.22)
	(<= (+ (* (onboard ?a) 0.25) (* (zoom-limit ?a) -0.97)) 0.44)
	(<= (+ (* (onboard ?a) 0.27) (* (zoom-limit ?a) -0.96)) -0.50)
	(<= (+ (* (onboard ?a) 0.29) (* (zoom-limit ?a) 0.96)) 7.95)
	(<= (+ (* (onboard ?a) 0.31) (* (zoom-limit ?a) -0.95)) 3.13)
	(<= (+ (* (onboard ?a) 0.38) (+ (* (zoom-limit ?a) 0.92) (* (* (distance ?c1 ?c2) (fast-burn ?a)) -0.01))) 6.11)
	(<= (+ (* (onboard ?a) 0.41) (* (zoom-limit ?a) -0.91)) 3.11)
	(<= (+ (* (onboard ?a) 0.41) (* (zoom-limit ?a) 0.91)) 15.41)
	(<= (+ (* (onboard ?a) 0.43) (* (zoom-limit ?a) 0.90)) 20.89)
	(<= (+ (* (onboard ?a) 0.43) (* (zoom-limit ?a) 0.90)) 27.22)
	(<= (+ (* (onboard ?a) 0.46) (* (zoom-limit ?a) -0.89)) -0.43)
	(<= (+ (* (onboard ?a) 0.46) (* (zoom-limit ?a) -0.89)) 1.32)
	(<= (+ (* (onboard ?a) 0.46) (* (zoom-limit ?a) 0.89)) 7.45)
	(<= (+ (* (onboard ?a) 0.47) (* (zoom-limit ?a) 0.88)) 8.49)
	(<= (+ (* (onboard ?a) 0.48) (* (zoom-limit ?a) -0.88)) -11.44)
	(<= (+ (* (onboard ?a) 0.48) (* (zoom-limit ?a) 0.88)) 13.70)
	(<= (+ (* (onboard ?a) 0.50) (* (zoom-limit ?a) -0.87)) -17.05)
	(<= (+ (* (onboard ?a) 0.51) (* (zoom-limit ?a) -0.86)) -11.91)
	(<= (+ (* (onboard ?a) 0.51) (* (zoom-limit ?a) 0.86)) 8.69)
	(<= (+ (* (onboard ?a) 0.52) (* (zoom-limit ?a) 0.86)) 20.90)
	(<= (+ (* (onboard ?a) 0.53) (* (zoom-limit ?a) -0.85)) -0.26)
	(<= (+ (* (onboard ?a) 0.53) (* (zoom-limit ?a) -0.85)) -10.33)
	(<= (+ (* (onboard ?a) 0.53) (* (zoom-limit ?a) 0.85)) 3.54)
	(<= (+ (* (onboard ?a) 0.53) (* (zoom-limit ?a) 0.85)) 8.39)
	(<= (+ (* (onboard ?a) 0.55) (* (zoom-limit ?a) -0.83)) 1.78)
	(<= (+ (* (onboard ?a) 0.56) (* (zoom-limit ?a) -0.83)) -0.26)
	(<= (+ (* (onboard ?a) 0.56) (* (zoom-limit ?a) -0.83)) -9.96)
	(<= (+ (* (onboard ?a) 0.58) (* (zoom-limit ?a) -0.82)) -19.03)
	(<= (+ (* (onboard ?a) 0.58) (* (zoom-limit ?a) 0.81)) 17.95)
	(<= (+ (* (onboard ?a) 0.59) (* (zoom-limit ?a) -0.81)) -11.64)
	(<= (+ (* (onboard ?a) 0.59) (* (zoom-limit ?a) -0.81)) 2.01)
	(<= (+ (* (onboard ?a) 0.59) (* (zoom-limit ?a) 0.81)) 7.10)
	(<= (+ (* (onboard ?a) 0.60) (* (zoom-limit ?a) -0.80)) -0.04)
	(<= (+ (* (onboard ?a) 0.60) (* (zoom-limit ?a) -0.80)) -18.36)
	(<= (+ (* (onboard ?a) 0.62) (* (zoom-limit ?a) 0.79)) 8.18)
	(<= (+ (* (onboard ?a) 0.65) (* (zoom-limit ?a) 0.76)) 4.82)
	(<= (+ (* (onboard ?a) 0.65) (* (zoom-limit ?a) 0.76)) 5.73)
	(<= (+ (* (onboard ?a) 0.66) (* (zoom-limit ?a) -0.75)) -9.38)
	(<= (+ (* (onboard ?a) 0.68) (* (zoom-limit ?a) -0.74)) -0.94)
	(<= (+ (* (onboard ?a) 0.69) (* (zoom-limit ?a) 0.73)) 7.03)
	(<= (+ (* (onboard ?a) 0.70) (* (zoom-limit ?a) -0.72)) 0.44)
	(<= (+ (* (onboard ?a) 0.70) (* (zoom-limit ?a) -0.72)) 3.11)
	(<= (+ (* (onboard ?a) 0.71) (* (zoom-limit ?a) -0.70)) -10.62)
	(<= (+ (* (onboard ?a) 0.71) (* (zoom-limit ?a) -0.71)) 0)
	(<= (+ (* (onboard ?a) 0.71) (* (zoom-limit ?a) -0.71)) 2.79)
	(<= (+ (* (onboard ?a) 0.71) (* (zoom-limit ?a) 0.71)) 6.15)
	(<= (+ (* (onboard ?a) 0.74) (* (zoom-limit ?a) -0.68)) -17.29)
	(<= (+ (* (onboard ?a) 0.74) (* (zoom-limit ?a) 0.67)) 16.06)
	(<= (+ (* (onboard ?a) 0.75) (* (zoom-limit ?a) -0.66)) -6.87)
	(<= (+ (* (onboard ?a) 0.75) (* (zoom-limit ?a) -0.66)) 1.70)
	(<= (+ (* (onboard ?a) 0.75) (* (zoom-limit ?a) 0.66)) 7.28)
	(<= (+ (* (onboard ?a) 0.76) (* (zoom-limit ?a) -0.65)) 3.41)
	(<= (+ (* (onboard ?a) 0.77) (* (zoom-limit ?a) -0.64)) 2.24)
	(<= (+ (* (onboard ?a) 0.77) (* (zoom-limit ?a) 0.63)) 5.75)
	(<= (+ (* (onboard ?a) 0.77) (* (zoom-limit ?a) 0.64)) 3.93)
	(<= (+ (* (onboard ?a) 0.77) (* (zoom-limit ?a) 0.64)) 5.24)
	(<= (+ (* (onboard ?a) 0.79) (* (zoom-limit ?a) -0.62)) 2.61)
	(<= (+ (* (onboard ?a) 0.79) (+ (* (zoom-limit ?a) 0.62) (* (* (distance ?c1 ?c2) (fast-burn ?a)) -0.01))) 1.01)
	(<= (+ (* (onboard ?a) 0.80) (* (zoom-limit ?a) -0.60)) 1.52)
	(<= (+ (* (onboard ?a) 0.81) (* (zoom-limit ?a) -0.58)) 0.85)
	(<= (+ (* (onboard ?a) 0.81) (* (zoom-limit ?a) -0.58)) 1.03)
	(<= (+ (* (onboard ?a) 0.81) (* (zoom-limit ?a) 0.59)) 5.86)
	(<= (+ (* (onboard ?a) 0.82) (* (zoom-limit ?a) 0.57)) 5.70)
	(<= (+ (* (onboard ?a) 0.82) (* (zoom-limit ?a) 0.57)) 5.76)
	(<= (+ (* (onboard ?a) 0.82) (* (zoom-limit ?a) 0.58)) 3.89)
	(<= (+ (* (onboard ?a) 0.82) (* (zoom-limit ?a) 0.58)) 5.76)
	(<= (+ (* (onboard ?a) 0.83) (* (zoom-limit ?a) 0.55)) 12.04)
	(<= (+ (* (onboard ?a) 0.83) (* (zoom-limit ?a) 0.55)) 6.07)
	(<= (+ (* (onboard ?a) 0.83) (* (zoom-limit ?a) 0.56)) 5.57)
	(<= (+ (* (onboard ?a) 0.84) (* (zoom-limit ?a) -0.54)) -8.17)
	(<= (+ (* (onboard ?a) 0.84) (* (zoom-limit ?a) -0.55)) 2.72)
	(<= (+ (* (onboard ?a) 0.84) (+ (* (zoom-limit ?a) 0.54) (* (* (distance ?c1 ?c2) (fast-burn ?a)) -0.01))) 0.30)
	(<= (+ (* (onboard ?a) 0.85) (* (zoom-limit ?a) -0.53)) 3.14)
	(<= (+ (* (onboard ?a) 0.85) (* (zoom-limit ?a) 0.53)) 12.73)
	(<= (+ (* (onboard ?a) 0.85) (* (zoom-limit ?a) 0.53)) 4.13)
	(<= (+ (* (onboard ?a) 0.86) (* (zoom-limit ?a) -0.51)) -5.71)
	(<= (+ (* (onboard ?a) 0.86) (+ (* (zoom-limit ?a) 0.51) (* (* (distance ?c1 ?c2) (fast-burn ?a)) -0.01))) 7.39)
	(<= (+ (* (onboard ?a) 0.87) (* (zoom-limit ?a) 0.49)) 5.86)
	(<= (+ (* (onboard ?a) 0.88) (* (zoom-limit ?a) -0.47)) -7.27)
	(<= (+ (* (onboard ?a) 0.88) (* (zoom-limit ?a) -0.48)) -3.81)
	(<= (+ (* (onboard ?a) 0.89) (* (zoom-limit ?a) -0.45)) -11.17)
	(<= (+ (* (onboard ?a) 0.89) (* (zoom-limit ?a) 0.45)) 5.49)
	(<= (+ (* (onboard ?a) 0.89) (* (zoom-limit ?a) 0.46)) 10.19)
	(<= (+ (* (onboard ?a) 0.89) (+ (* (zoom-limit ?a) 0.45) (* (* (distance ?c1 ?c2) (fast-burn ?a)) 0.01))) 18.32)
	(<= (+ (* (onboard ?a) 0.90) (* (zoom-limit ?a) -0.43)) -7.07)
	(<= (+ (* (onboard ?a) 0.90) (* (zoom-limit ?a) -0.44)) -3.20)
	(<= (+ (* (onboard ?a) 0.90) (* (zoom-limit ?a) 0.43)) 2.87)
	(<= (+ (* (onboard ?a) 0.90) (* (zoom-limit ?a) 0.43)) 4.09)
	(<= (+ (* (onboard ?a) 0.90) (* (zoom-limit ?a) 0.44)) 4.30)
	(<= (+ (* (onboard ?a) 0.90) (* (zoom-limit ?a) 0.45)) 4.74)
	(<= (+ (* (onboard ?a) 0.90) (+ (* (zoom-limit ?a) 0.44) (* (* (distance ?c1 ?c2) (fast-burn ?a)) -0.01))) -6.78)
	(<= (+ (* (onboard ?a) 0.91) (* (zoom-limit ?a) -0.42)) -6.77)
	(<= (+ (* (onboard ?a) 0.91) (* (zoom-limit ?a) 0.41)) 11.69)
	(<= (+ (* (onboard ?a) 0.91) (+ (* (zoom-limit ?a) 0.41) (* (* (distance ?c1 ?c2) (fast-burn ?a)) -0.02))) -28.94)
	(<= (+ (* (onboard ?a) 0.92) (* (zoom-limit ?a) -0.39)) -8.73)
	(<= (+ (* (onboard ?a) 0.92) (* (zoom-limit ?a) 0.40)) 5.41)
	(<= (+ (* (onboard ?a) 0.93) (* (zoom-limit ?a) 0.36)) 11.85)
	(<= (+ (* (onboard ?a) 0.93) (* (zoom-limit ?a) 0.36)) 5.11)
	(<= (+ (* (onboard ?a) 0.94) (* (zoom-limit ?a) -0.34)) -6.66)
	(<= (+ (* (onboard ?a) 0.94) (* (zoom-limit ?a) 0.33)) 2.26)
	(<= (+ (* (onboard ?a) 0.94) (* (zoom-limit ?a) 0.34)) 1.98)
	(<= (+ (* (onboard ?a) 0.94) (* (zoom-limit ?a) 0.34)) 4.57)
	(<= (+ (* (onboard ?a) 0.94) (* (zoom-limit ?a) 0.35)) 1.58)
	(<= (+ (* (onboard ?a) 0.94) (* (zoom-limit ?a) 0.35)) 5.05)
	(<= (+ (* (onboard ?a) 0.95) (* (zoom-limit ?a) 0.32)) 0.46)
	(<= (+ (* (onboard ?a) 0.96) (* (zoom-limit ?a) -0.26)) -3.60)
	(<= (+ (* (onboard ?a) 0.96) (* (zoom-limit ?a) 0.27)) 5.68)
	(<= (+ (* (onboard ?a) 0.96) (* (zoom-limit ?a) 0.28)) 2.62)
	(<= (+ (* (onboard ?a) 0.96) (* (zoom-limit ?a) 0.28)) 7.79)
	(<= (+ (* (onboard ?a) 0.96) (* (zoom-limit ?a) 0.29)) 2.67)
	(<= (+ (* (onboard ?a) 0.96) (* (zoom-limit ?a) 0.29)) 9.93)
	(<= (+ (* (onboard ?a) 0.97) (* (zoom-limit ?a) -0.23)) -5.46)
	(<= (+ (* (onboard ?a) 0.97) (* (zoom-limit ?a) -0.24)) -5.10)
	(<= (+ (* (onboard ?a) 0.97) (* (zoom-limit ?a) -0.24)) -5.58)
	(<= (+ (* (onboard ?a) 0.97) (* (zoom-limit ?a) -0.25)) -13.48)
	(<= (+ (* (onboard ?a) 0.97) (* (zoom-limit ?a) -0.25)) -7.32)
	(<= (+ (* (onboard ?a) 0.97) (* (zoom-limit ?a) 0.23)) 3.09)
	(<= (+ (* (onboard ?a) 0.97) (* (zoom-limit ?a) 0.24)) 2.43)
	(<= (+ (* (onboard ?a) 0.97) (* (zoom-limit ?a) 0.24)) 2.88)
	(<= (+ (* (onboard ?a) 0.97) (* (zoom-limit ?a) 0.24)) 3.80)
	(<= (+ (* (onboard ?a) 0.97) (* (zoom-limit ?a) 0.24)) 6.54)
	(<= (+ (* (onboard ?a) 0.97) (* (zoom-limit ?a) 0.25)) 2.15)
	(<= (+ (* (onboard ?a) 0.97) (* (zoom-limit ?a) 0.25)) 4.03)
	(<= (+ (* (onboard ?a) 0.97) (* (zoom-limit ?a) 0.25)) 5.33)
	(<= (+ (* (onboard ?a) 0.97) (* (zoom-limit ?a) 0.25)) 5.39)
	(<= (+ (* (onboard ?a) 0.97) (* (zoom-limit ?a) 0.26)) 1.95)
	(<= (+ (* (onboard ?a) 0.97) (* (zoom-limit ?a) 0.26)) 1.99)
	(<= (+ (* (onboard ?a) 0.97) (* (zoom-limit ?a) 0.26)) 2)
	(<= (+ (* (onboard ?a) 0.97) (* (zoom-limit ?a) 0.26)) 2.74)
	(<= (+ (* (onboard ?a) 0.97) (+ (* (zoom-limit ?a) -0.24) (* (* (distance ?c1 ?c2) (fast-burn ?a)) -0.01))) -10.56)
	(<= (+ (* (onboard ?a) 0.98) (* (zoom-limit ?a) -0.20)) 0.10)
	(<= (+ (* (onboard ?a) 0.98) (* (zoom-limit ?a) -0.20)) 0.13)
	(<= (+ (* (onboard ?a) 0.98) (* (zoom-limit ?a) -0.21)) -4.31)
	(<= (+ (* (onboard ?a) 0.98) (* (zoom-limit ?a) -0.22)) -4.09)
	(<= (+ (* (onboard ?a) 0.98) (* (zoom-limit ?a) 0.18)) -0.16)
	(<= (+ (* (onboard ?a) 0.98) (* (zoom-limit ?a) 0.18)) -3.42)
	(<= (+ (* (onboard ?a) 0.98) (* (zoom-limit ?a) 0.19)) -1.28)
	(<= (+ (* (onboard ?a) 0.98) (* (zoom-limit ?a) 0.19)) 6.31)
	(<= (+ (* (onboard ?a) 0.98) (* (zoom-limit ?a) 0.19)) 8.05)
	(<= (+ (* (onboard ?a) 0.98) (* (zoom-limit ?a) 0.19)) 8.28)
	(<= (+ (* (onboard ?a) 0.98) (* (zoom-limit ?a) 0.19)) 8.34)
	(<= (+ (* (onboard ?a) 0.98) (+ (* (zoom-limit ?a) -0.21) (* (* (distance ?c1 ?c2) (fast-burn ?a)) -0.01))) -13.23)
	(<= (+ (* (onboard ?a) 0.99) (* (zoom-limit ?a) -0.13)) -0.42)
	(<= (+ (* (onboard ?a) 0.99) (* (zoom-limit ?a) -0.13)) -0.97)
	(<= (+ (* (onboard ?a) 0.99) (* (zoom-limit ?a) -0.13)) 3.77)
	(<= (+ (* (onboard ?a) 0.99) (* (zoom-limit ?a) -0.16)) -2.40)
	(<= (+ (* (onboard ?a) 0.99) (* (zoom-limit ?a) 0.12)) 14.53)
	(<= (+ (* (onboard ?a) 0.99) (* (zoom-limit ?a) 0.12)) 3.93)
	(<= (+ (* (onboard ?a) 0.99) (* (zoom-limit ?a) 0.15)) -1.33)
	(<= (+ (* (onboard ?a) 0.99) (* (zoom-limit ?a) 0.17)) -1.30)
	(<= (+ (* (onboard ?a) 0.99) (+ (* (zoom-limit ?a) -0.12) (* (* (distance ?c1 ?c2) (fast-burn ?a)) -0.01))) -4.39)
	(<= (+ (* (onboard ?a) 0.99) (+ (* (zoom-limit ?a) -0.14) (* (* (distance ?c1 ?c2) (fast-burn ?a)) -0.01))) -4.28)
	(<= (+ (onboard ?a) (* (zoom-limit ?a) -0.01)) 2.68)
	(<= (+ (onboard ?a) (* (zoom-limit ?a) -0.01)) 3)
	(<= (+ (onboard ?a) (* (zoom-limit ?a) -0.01)) 3.59)
	(<= (+ (onboard ?a) (* (zoom-limit ?a) -0.01)) 3.62)
	(<= (+ (onboard ?a) (* (zoom-limit ?a) -0.02)) 1.48)
	(<= (+ (onboard ?a) (* (zoom-limit ?a) -0.03)) -2.54)
	(<= (+ (onboard ?a) (* (zoom-limit ?a) -0.03)) -2.98)
	(<= (+ (onboard ?a) (* (zoom-limit ?a) -0.03)) 1.12)
	(<= (+ (onboard ?a) (* (zoom-limit ?a) -0.04)) 3.69)
	(<= (+ (onboard ?a) (* (zoom-limit ?a) -0.06)) -1.39)
	(<= (+ (onboard ?a) (* (zoom-limit ?a) -0.07)) -3.17)
	(<= (+ (onboard ?a) (* (zoom-limit ?a) -0.09)) 3.85)
	(<= (+ (onboard ?a) (* (zoom-limit ?a) -0.09)) 3.89)
	(<= (+ (onboard ?a) (* (zoom-limit ?a) 0.01)) 2.49)
	(<= (+ (onboard ?a) (* (zoom-limit ?a) 0.01)) 3.41)
	(<= (+ (onboard ?a) (* (zoom-limit ?a) 0.03)) 3.21)
	(<= (+ (onboard ?a) (* (zoom-limit ?a) 0.04)) 10.52)
	(<= (+ (onboard ?a) (* (zoom-limit ?a) 0.04)) 2.40)
	(<= (+ (onboard ?a) (* (zoom-limit ?a) 0.04)) 2.44)
	(<= (+ (onboard ?a) (* (zoom-limit ?a) 0.06)) 1.83)
	(<= (+ (onboard ?a) (* (zoom-limit ?a) 0.06)) 5.67)
	(<= (+ (onboard ?a) (* (zoom-limit ?a) 0.07)) 2)
	(<= (+ (onboard ?a) (* (zoom-limit ?a) 0.08)) 2.78)
	(<= (+ (onboard ?a) (* (zoom-limit ?a) 0.09)) 2.87)
	(<= (+ (onboard ?a) (+ (* (zoom-limit ?a) -0.04) (* (* (distance ?c1 ?c2) (fast-burn ?a)) -0.01))) -7.54)
	(<= (+ (onboard ?a) (+ (* (zoom-limit ?a) -0.05) (* (* (distance ?c1 ?c2) (fast-burn ?a)) -0.01))) -6.39)
	(<= (+ (onboard ?a) (+ (* (zoom-limit ?a) -0.10) (* (* (distance ?c1 ?c2) (fast-burn ?a)) -0.01))) -3.55)
	(<= (onboard ?a) 2)
	(<= (onboard ?a) 3.12)(not (= ?c1 ?c2)))
	:effect (and (at ?a ?c2)
		(not (at ?a ?c1))
(decrease (fuel ?a) (* (distance ?c1 ?c2) (fast-burn ?a)))
(increase (total-fuel-used ) (* (distance ?c1 ?c2) (fast-burn ?a)))))

(:action refuel
	:parameters (?a - aircraft ?c - city)
	:precondition (and (at ?a ?c)
	(<= (* (capacity ?a) -1) -2106)
	(<= (* (fuel ?a) -1) 0.26)
	(<= (* (fuel ?a) -1) 28.81)
	(<= (+ (* (fuel ?a) -0.11) (* (capacity ?a) -0.99)) -2136.95)
	(<= (+ (* (fuel ?a) -0.14) (* (capacity ?a) 0.99)) 15042.47)
	(<= (+ (* (fuel ?a) -0.89) (* (capacity ?a) 0.45)) 6404)
	(<= (+ (* (fuel ?a) -1) (* (capacity ?a) -0.08)) -234.36)
	(<= (+ (* (fuel ?a) -1) (* (capacity ?a) 0.05)) 583.60)
	(<= (+ (* (fuel ?a) 0.12) (* (capacity ?a) 0.99)) 15617.45)
	(<= (+ (* (fuel ?a) 0.70) (* (capacity ?a) -0.71)) -990.39)
	(<= (+ (* (fuel ?a) 0.91) (* (capacity ?a) -0.42)) -156.81)
	(<= (+ (* (fuel ?a) 0.99) (* (capacity ?a) 0.12)) 5467.53)
	(<= (+ (fuel ?a) (* (capacity ?a) -0.01)) 3721.92)
	(<= (capacity ?a) 15472))
	:effect (and
(assign (fuel ?a) (capacity ?a))))

)