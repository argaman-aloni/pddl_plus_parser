(define (problem DLOG-17-1-70)
	(:domain driverlog)
	(:objects
	driver1 - driver
	driver2 - driver
	driver3 - driver
	driver4 - driver
	driver5 - driver
	driver6 - driver
	driver7 - driver
	driver8 - driver
	driver9 - driver
	driver10 - driver
	driver11 - driver
	driver12 - driver
	driver13 - driver
	driver14 - driver
	driver15 - driver
	driver16 - driver
	driver17 - driver
	truck1 - truck
	package1 - obj
	package2 - obj
	package3 - obj
	package4 - obj
	package5 - obj
	package6 - obj
	package7 - obj
	package8 - obj
	package9 - obj
	package10 - obj
	package11 - obj
	package12 - obj
	package13 - obj
	package14 - obj
	package15 - obj
	package16 - obj
	package17 - obj
	package18 - obj
	package19 - obj
	package20 - obj
	package21 - obj
	package22 - obj
	package23 - obj
	package24 - obj
	package25 - obj
	package26 - obj
	package27 - obj
	package28 - obj
	package29 - obj
	package30 - obj
	package31 - obj
	package32 - obj
	package33 - obj
	package34 - obj
	package35 - obj
	package36 - obj
	package37 - obj
	package38 - obj
	package39 - obj
	package40 - obj
	package41 - obj
	package42 - obj
	package43 - obj
	package44 - obj
	package45 - obj
	package46 - obj
	package47 - obj
	package48 - obj
	package49 - obj
	package50 - obj
	package51 - obj
	package52 - obj
	package53 - obj
	package54 - obj
	package55 - obj
	package56 - obj
	package57 - obj
	package58 - obj
	package59 - obj
	package60 - obj
	package61 - obj
	package62 - obj
	package63 - obj
	package64 - obj
	package65 - obj
	package66 - obj
	package67 - obj
	package68 - obj
	package69 - obj
	package70 - obj
	s0 - location
	s1 - location
	s2 - location
	s3 - location
	s4 - location
	s5 - location
	s6 - location
	s7 - location
	s8 - location
	s9 - location
	s10 - location
	s11 - location
	s12 - location
	p0-8 - location
	p2-1 - location
	p3-0 - location
	p3-9 - location
	p3-11 - location
	p4-1 - location
	p4-2 - location
	p4-6 - location
	p5-11 - location
	p5-12 - location
	p7-3 - location
	p7-10 - location
	p8-1 - location
	p8-10 - location
	p8-11 - location
	p9-1 - location
	p9-3 - location
	p10-4 - location
	p10-5 - location
	p11-1 - location
	p12-1 - location
	p12-7 - location
	)
	(:init
	(at driver1 s0)
	(at driver2 s10)
	(at driver3 s5)
	(at driver4 s1)
	(at driver5 s4)
	(at driver6 s6)
	(at driver7 s1)
	(at driver8 s6)
	(at driver9 s10)
	(at driver10 s6)
	(at driver11 s2)
	(at driver12 s12)
	(at driver13 s10)
	(at driver14 s5)
	(at driver15 s4)
	(at driver16 s8)
	(at driver17 s4)
	(at truck1 s0)
	(empty truck1)
	(= (load truck1) 0)
	(= (fuel-per-minute truck1) 10)
	(at package1 s6)
	(at package2 s4)
	(at package3 s6)
	(at package4 s0)
	(at package5 s12)
	(at package6 s10)
	(at package7 s3)
	(at package8 s3)
	(at package9 s12)
	(at package10 s8)
	(at package11 s0)
	(at package12 s2)
	(at package13 s4)
	(at package14 s5)
	(at package15 s2)
	(at package16 s2)
	(at package17 s5)
	(at package18 s3)
	(at package19 s4)
	(at package20 s7)
	(at package21 s8)
	(at package22 s2)
	(at package23 s10)
	(at package24 s8)
	(at package25 s10)
	(at package26 s12)
	(at package27 s8)
	(at package28 s1)
	(at package29 s1)
	(at package30 s11)
	(at package31 s6)
	(at package32 s6)
	(at package33 s3)
	(at package34 s2)
	(at package35 s3)
	(at package36 s6)
	(at package37 s9)
	(at package38 s2)
	(at package39 s1)
	(at package40 s6)
	(at package41 s12)
	(at package42 s6)
	(at package43 s4)
	(at package44 s10)
	(at package45 s2)
	(at package46 s11)
	(at package47 s0)
	(at package48 s11)
	(at package49 s12)
	(at package50 s6)
	(at package51 s0)
	(at package52 s4)
	(at package53 s5)
	(at package54 s3)
	(at package55 s5)
	(at package56 s8)
	(at package57 s0)
	(at package58 s2)
	(at package59 s2)
	(at package60 s3)
	(at package61 s1)
	(at package62 s5)
	(at package63 s8)
	(at package64 s1)
	(at package65 s11)
	(at package66 s3)
	(at package67 s11)
	(at package68 s4)
	(at package69 s11)
	(at package70 s8)
	(path s0 p0-8)
	(path p0-8 s0)
	(path s8 p0-8)
	(path p0-8 s8)
	(= (time-to-walk s0 p0-8) 6)
	(= (time-to-walk p0-8 s0) 6)
	(= (time-to-walk s8 p0-8) 41)
	(= (time-to-walk p0-8 s8) 41)
	(path s2 p2-1)
	(path p2-1 s2)
	(path s1 p2-1)
	(path p2-1 s1)
	(= (time-to-walk s2 p2-1) 36)
	(= (time-to-walk p2-1 s2) 36)
	(= (time-to-walk s1 p2-1) 5)
	(= (time-to-walk p2-1 s1) 5)
	(path s3 p3-0)
	(path p3-0 s3)
	(path s0 p3-0)
	(path p3-0 s0)
	(= (time-to-walk s3 p3-0) 4)
	(= (time-to-walk p3-0 s3) 4)
	(= (time-to-walk s0 p3-0) 38)
	(= (time-to-walk p3-0 s0) 38)
	(path s3 p3-9)
	(path p3-9 s3)
	(path s9 p3-9)
	(path p3-9 s9)
	(= (time-to-walk s3 p3-9) 10)
	(= (time-to-walk p3-9 s3) 10)
	(= (time-to-walk s9 p3-9) 49)
	(= (time-to-walk p3-9 s9) 49)
	(path s3 p3-11)
	(path p3-11 s3)
	(path s11 p3-11)
	(path p3-11 s11)
	(= (time-to-walk s3 p3-11) 4)
	(= (time-to-walk p3-11 s3) 4)
	(= (time-to-walk s11 p3-11) 41)
	(= (time-to-walk p3-11 s11) 41)
	(path s4 p4-1)
	(path p4-1 s4)
	(path s1 p4-1)
	(path p4-1 s1)
	(= (time-to-walk s4 p4-1) 56)
	(= (time-to-walk p4-1 s4) 56)
	(= (time-to-walk s1 p4-1) 52)
	(= (time-to-walk p4-1 s1) 52)
	(path s4 p4-2)
	(path p4-2 s4)
	(path s2 p4-2)
	(path p4-2 s2)
	(= (time-to-walk s4 p4-2) 18)
	(= (time-to-walk p4-2 s4) 18)
	(= (time-to-walk s2 p4-2) 49)
	(= (time-to-walk p4-2 s2) 49)
	(path s4 p4-6)
	(path p4-6 s4)
	(path s6 p4-6)
	(path p4-6 s6)
	(= (time-to-walk s4 p4-6) 59)
	(= (time-to-walk p4-6 s4) 59)
	(= (time-to-walk s6 p4-6) 22)
	(= (time-to-walk p4-6 s6) 22)
	(path s5 p5-11)
	(path p5-11 s5)
	(path s11 p5-11)
	(path p5-11 s11)
	(= (time-to-walk s5 p5-11) 3)
	(= (time-to-walk p5-11 s5) 3)
	(= (time-to-walk s11 p5-11) 45)
	(= (time-to-walk p5-11 s11) 45)
	(path s5 p5-12)
	(path p5-12 s5)
	(path s12 p5-12)
	(path p5-12 s12)
	(= (time-to-walk s5 p5-12) 48)
	(= (time-to-walk p5-12 s5) 48)
	(= (time-to-walk s12 p5-12) 61)
	(= (time-to-walk p5-12 s12) 61)
	(path s7 p7-3)
	(path p7-3 s7)
	(path s3 p7-3)
	(path p7-3 s3)
	(= (time-to-walk s7 p7-3) 34)
	(= (time-to-walk p7-3 s7) 34)
	(= (time-to-walk s3 p7-3) 28)
	(= (time-to-walk p7-3 s3) 28)
	(path s7 p7-10)
	(path p7-10 s7)
	(path s10 p7-10)
	(path p7-10 s10)
	(= (time-to-walk s7 p7-10) 19)
	(= (time-to-walk p7-10 s7) 19)
	(= (time-to-walk s10 p7-10) 35)
	(= (time-to-walk p7-10 s10) 35)
	(path s8 p8-1)
	(path p8-1 s8)
	(path s1 p8-1)
	(path p8-1 s1)
	(= (time-to-walk s8 p8-1) 25)
	(= (time-to-walk p8-1 s8) 25)
	(= (time-to-walk s1 p8-1) 14)
	(= (time-to-walk p8-1 s1) 14)
	(path s8 p8-10)
	(path p8-10 s8)
	(path s10 p8-10)
	(path p8-10 s10)
	(= (time-to-walk s8 p8-10) 51)
	(= (time-to-walk p8-10 s8) 51)
	(= (time-to-walk s10 p8-10) 35)
	(= (time-to-walk p8-10 s10) 35)
	(path s8 p8-11)
	(path p8-11 s8)
	(path s11 p8-11)
	(path p8-11 s11)
	(= (time-to-walk s8 p8-11) 58)
	(= (time-to-walk p8-11 s8) 58)
	(= (time-to-walk s11 p8-11) 17)
	(= (time-to-walk p8-11 s11) 17)
	(path s9 p9-1)
	(path p9-1 s9)
	(path s1 p9-1)
	(path p9-1 s1)
	(= (time-to-walk s9 p9-1) 23)
	(= (time-to-walk p9-1 s9) 23)
	(= (time-to-walk s1 p9-1) 63)
	(= (time-to-walk p9-1 s1) 63)
	(path s10 p10-4)
	(path p10-4 s10)
	(path s4 p10-4)
	(path p10-4 s4)
	(= (time-to-walk s10 p10-4) 58)
	(= (time-to-walk p10-4 s10) 58)
	(= (time-to-walk s4 p10-4) 59)
	(= (time-to-walk p10-4 s4) 59)
	(path s10 p10-5)
	(path p10-5 s10)
	(path s5 p10-5)
	(path p10-5 s5)
	(= (time-to-walk s10 p10-5) 2)
	(= (time-to-walk p10-5 s10) 2)
	(= (time-to-walk s5 p10-5) 61)
	(= (time-to-walk p10-5 s5) 61)
	(path s11 p11-1)
	(path p11-1 s11)
	(path s1 p11-1)
	(path p11-1 s1)
	(= (time-to-walk s11 p11-1) 30)
	(= (time-to-walk p11-1 s11) 30)
	(= (time-to-walk s1 p11-1) 12)
	(= (time-to-walk p11-1 s1) 12)
	(path s12 p12-1)
	(path p12-1 s12)
	(path s1 p12-1)
	(path p12-1 s1)
	(= (time-to-walk s12 p12-1) 44)
	(= (time-to-walk p12-1 s12) 44)
	(= (time-to-walk s1 p12-1) 34)
	(= (time-to-walk p12-1 s1) 34)
	(path s12 p12-7)
	(path p12-7 s12)
	(path s7 p12-7)
	(path p12-7 s7)
	(= (time-to-walk s12 p12-7) 53)
	(= (time-to-walk p12-7 s12) 53)
	(= (time-to-walk s7 p12-7) 33)
	(= (time-to-walk p12-7 s7) 33)
	(link s0 s1)
	(link s1 s0)
	(= (time-to-drive s0 s1) 19)
	(= (time-to-drive s1 s0) 19)
	(link s0 s5)
	(link s5 s0)
	(= (time-to-drive s0 s5) 4)
	(= (time-to-drive s5 s0) 4)
	(link s0 s10)
	(link s10 s0)
	(= (time-to-drive s0 s10) 15)
	(= (time-to-drive s10 s0) 15)
	(link s1 s3)
	(link s3 s1)
	(= (time-to-drive s1 s3) 12)
	(= (time-to-drive s3 s1) 12)
	(link s1 s8)
	(link s8 s1)
	(= (time-to-drive s1 s8) 26)
	(= (time-to-drive s8 s1) 26)
	(link s2 s3)
	(link s3 s2)
	(= (time-to-drive s2 s3) 18)
	(= (time-to-drive s3 s2) 18)
	(link s2 s6)
	(link s6 s2)
	(= (time-to-drive s2 s6) 56)
	(= (time-to-drive s6 s2) 56)
	(link s2 s7)
	(link s7 s2)
	(= (time-to-drive s2 s7) 8)
	(= (time-to-drive s7 s2) 8)
	(link s2 s11)
	(link s11 s2)
	(= (time-to-drive s2 s11) 12)
	(= (time-to-drive s11 s2) 12)
	(link s3 s0)
	(link s0 s3)
	(= (time-to-drive s3 s0) 23)
	(= (time-to-drive s0 s3) 23)
	(link s3 s6)
	(link s6 s3)
	(= (time-to-drive s3 s6) 35)
	(= (time-to-drive s6 s3) 35)
	(link s4 s1)
	(link s1 s4)
	(= (time-to-drive s4 s1) 31)
	(= (time-to-drive s1 s4) 31)
	(link s4 s3)
	(link s3 s4)
	(= (time-to-drive s4 s3) 58)
	(= (time-to-drive s3 s4) 58)
	(link s4 s5)
	(link s5 s4)
	(= (time-to-drive s4 s5) 59)
	(= (time-to-drive s5 s4) 59)
	(link s4 s7)
	(link s7 s4)
	(= (time-to-drive s4 s7) 45)
	(= (time-to-drive s7 s4) 45)
	(link s4 s9)
	(link s9 s4)
	(= (time-to-drive s4 s9) 42)
	(= (time-to-drive s9 s4) 42)
	(link s6 s7)
	(link s7 s6)
	(= (time-to-drive s6 s7) 27)
	(= (time-to-drive s7 s6) 27)
	(link s7 s0)
	(link s0 s7)
	(= (time-to-drive s7 s0) 37)
	(= (time-to-drive s0 s7) 37)
	(link s7 s10)
	(link s10 s7)
	(= (time-to-drive s7 s10) 58)
	(= (time-to-drive s10 s7) 58)
	(link s8 s0)
	(link s0 s8)
	(= (time-to-drive s8 s0) 50)
	(= (time-to-drive s0 s8) 50)
	(link s8 s2)
	(link s2 s8)
	(= (time-to-drive s8 s2) 33)
	(= (time-to-drive s2 s8) 33)
	(link s8 s4)
	(link s4 s8)
	(= (time-to-drive s8 s4) 49)
	(= (time-to-drive s4 s8) 49)
	(link s8 s5)
	(link s5 s8)
	(= (time-to-drive s8 s5) 42)
	(= (time-to-drive s5 s8) 42)
	(link s9 s1)
	(link s1 s9)
	(= (time-to-drive s9 s1) 35)
	(= (time-to-drive s1 s9) 35)
	(link s9 s2)
	(link s2 s9)
	(= (time-to-drive s9 s2) 44)
	(= (time-to-drive s2 s9) 44)
	(link s9 s7)
	(link s7 s9)
	(= (time-to-drive s9 s7) 6)
	(= (time-to-drive s7 s9) 6)
	(link s9 s8)
	(link s8 s9)
	(= (time-to-drive s9 s8) 46)
	(= (time-to-drive s8 s9) 46)
	(link s9 s10)
	(link s10 s9)
	(= (time-to-drive s9 s10) 21)
	(= (time-to-drive s10 s9) 21)
	(link s10 s3)
	(link s3 s10)
	(= (time-to-drive s10 s3) 39)
	(= (time-to-drive s3 s10) 39)
	(link s10 s5)
	(link s5 s10)
	(= (time-to-drive s10 s5) 32)
	(= (time-to-drive s5 s10) 32)
	(link s10 s8)
	(link s8 s10)
	(= (time-to-drive s10 s8) 54)
	(= (time-to-drive s8 s10) 54)
	(link s11 s0)
	(link s0 s11)
	(= (time-to-drive s11 s0) 57)
	(= (time-to-drive s0 s11) 57)
	(link s11 s1)
	(link s1 s11)
	(= (time-to-drive s11 s1) 36)
	(= (time-to-drive s1 s11) 36)
	(link s11 s6)
	(link s6 s11)
	(= (time-to-drive s11 s6) 3)
	(= (time-to-drive s6 s11) 3)
	(link s11 s7)
	(link s7 s11)
	(= (time-to-drive s11 s7) 3)
	(= (time-to-drive s7 s11) 3)
	(link s11 s10)
	(link s10 s11)
	(= (time-to-drive s11 s10) 62)
	(= (time-to-drive s10 s11) 62)
	(link s11 s12)
	(link s12 s11)
	(= (time-to-drive s11 s12) 20)
	(= (time-to-drive s12 s11) 20)
	(link s12 s2)
	(link s2 s12)
	(= (time-to-drive s12 s2) 58)
	(= (time-to-drive s2 s12) 58)
	(link s12 s7)
	(link s7 s12)
	(= (time-to-drive s12 s7) 3)
	(= (time-to-drive s7 s12) 3)
	(link s12 s9)
	(link s9 s12)
	(= (time-to-drive s12 s9) 32)
	(= (time-to-drive s9 s12) 32)
	(= (fuel-used) 0)
)
	(:goal (and
	(at driver1 s4)
	(at driver2 s5)
	(at driver3 s12)
	(at driver4 s7)
	(at driver5 s6)
	(at driver6 s9)
	(at driver7 s0)
	(at driver8 s8)
	(at driver9 s10)
	(at driver11 s12)
	(at driver12 s9)
	(at driver13 s1)
	(at driver14 s3)
	(at driver15 s8)
	(at driver16 s1)
	(at driver17 s3)
	(at truck1 s9)
	(at package1 s7)
	(at package2 s0)
	(at package3 s3)
	(at package4 s3)
	(at package5 s0)
	(at package6 s6)
	(at package7 s10)
	(at package9 s10)
	(at package11 s4)
	(at package12 s9)
	(at package13 s2)
	(at package14 s2)
	(at package15 s1)
	(at package16 s12)
	(at package17 s3)
	(at package18 s6)
	(at package19 s5)
	(at package20 s1)
	(at package22 s3)
	(at package23 s7)
	(at package24 s0)
	(at package25 s2)
	(at package26 s5)
	(at package27 s10)
	(at package28 s1)
	(at package29 s5)
	(at package30 s0)
	(at package31 s9)
	(at package32 s11)
	(at package33 s8)
	(at package34 s4)
	(at package35 s1)
	(at package36 s1)
	(at package37 s9)
	(at package39 s12)
	(at package40 s11)
	(at package41 s5)
	(at package42 s12)
	(at package43 s2)
	(at package44 s4)
	(at package45 s8)
	(at package46 s2)
	(at package47 s11)
	(at package50 s8)
	(at package51 s7)
	(at package52 s0)
	(at package53 s5)
	(at package54 s2)
	(at package55 s5)
	(at package56 s4)
	(at package57 s4)
	(at package58 s3)
	(at package59 s2)
	(at package60 s8)
	(at package61 s9)
	(at package62 s0)
	(at package63 s6)
	(at package64 s9)
	(at package65 s1)
	(at package66 s10)
	(at package67 s10)
	(at package68 s0)
	(at package69 s3)
	(at package70 s6)
	))

(:metric minimize (+ (* 1 (total-time)) (* 3 (fuel-used))))

)
