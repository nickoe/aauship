EESchema Schematic File Version 2  date man 12 nov 2012 20:13:02 CET
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:special
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:ftdi
LIBS:msp430
LIBS:bowlThrusterControl-cache
EELAYER 25  0
EELAYER END
$Descr A4 11700 8267
encoding utf-8
Sheet 1 1
Title ""
Date "12 nov 2012"
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
Text Notes 5050 1300 0    60   ~ 0
VCC and VSS is swapped
Wire Wire Line
	3500 3400 3500 3050
Wire Wire Line
	4100 2850 4000 2700
Connection ~ 5850 3600
Wire Wire Line
	5850 3600 5850 3700
Connection ~ 4400 2500
Wire Wire Line
	4400 2500 4400 2150
Connection ~ 4600 1550
Wire Wire Line
	4600 1650 4600 1550
Connection ~ 6100 1750
Connection ~ 5550 1750
Wire Wire Line
	5550 1650 5550 1750
Connection ~ 7300 1500
Connection ~ 3400 1550
Wire Wire Line
	1950 2950 1950 1550
Wire Wire Line
	1950 1550 5800 1550
Wire Wire Line
	5300 1800 5300 1500
Wire Wire Line
	5300 1500 7950 1500
Connection ~ 6700 3600
Connection ~ 7300 3600
Wire Wire Line
	8550 2900 6100 2900
Wire Wire Line
	8550 2700 6100 2700
Wire Wire Line
	8550 2500 6100 2500
Wire Wire Line
	8550 2300 6100 2300
Wire Wire Line
	6700 1900 6700 3200
Wire Wire Line
	7300 1900 7300 3200
Wire Wire Line
	4700 2600 4400 2600
Wire Wire Line
	4400 2600 4400 3850
Wire Wire Line
	4400 3850 3300 3850
Connection ~ 3300 3050
Wire Wire Line
	3300 3850 3300 3050
Connection ~ 4300 3600
Connection ~ 3400 3600
Wire Wire Line
	4200 3450 4200 3600
Wire Wire Line
	4300 2500 4700 2500
Wire Wire Line
	3400 3600 3400 2600
Connection ~ 3600 2400
Connection ~ 3400 2500
Wire Wire Line
	3400 2400 4700 2400
Wire Wire Line
	3400 2500 3500 2500
Wire Wire Line
	3500 2500 3500 3000
Wire Wire Line
	3500 3000 4600 3000
Wire Wire Line
	4600 3000 4600 2800
Wire Wire Line
	4600 2800 4700 2800
Wire Wire Line
	4300 2900 4300 3600
Wire Wire Line
	6300 3600 6300 1750
Wire Wire Line
	6300 1750 5500 1750
Wire Wire Line
	5500 1750 5500 1800
Connection ~ 5700 3600
Wire Wire Line
	4200 3050 4500 3050
Wire Wire Line
	4500 3050 4500 2700
Wire Wire Line
	4500 2700 4700 2700
Wire Wire Line
	1950 3250 1950 3600
Connection ~ 4200 3600
Connection ~ 5500 3600
Wire Wire Line
	3500 3050 1950 3050
Wire Wire Line
	1950 3150 3200 3150
Wire Wire Line
	3200 3150 3200 3500
Wire Wire Line
	3200 3500 4700 3500
Wire Wire Line
	4700 3500 4700 2900
Connection ~ 6300 3600
Wire Wire Line
	7550 1900 7550 3200
Wire Wire Line
	7000 1900 7000 3200
Connection ~ 6700 2300
Connection ~ 7000 2500
Connection ~ 7300 2700
Connection ~ 7550 2900
Wire Wire Line
	8150 1500 8150 3600
Wire Wire Line
	8150 3600 1950 3600
Connection ~ 7550 3600
Connection ~ 7000 3600
Wire Wire Line
	5800 1550 5800 1800
Wire Wire Line
	3400 1550 3400 2300
Connection ~ 7550 1500
Connection ~ 7000 1500
Connection ~ 6700 1500
Connection ~ 6100 1500
Connection ~ 5300 1650
Wire Wire Line
	4400 1650 4400 1550
Connection ~ 4400 1550
Wire Wire Line
	4600 2700 4600 2150
Connection ~ 4600 2700
Wire Wire Line
	3600 2850 3600 2400
Wire Wire Line
	4000 3400 3900 3250
$Comp
L GND #PWR01
U 1 1 50A0CF6D
P 5850 3700
F 0 "#PWR01" H 5850 3700 30  0001 C CNN
F 1 "GND" H 5850 3630 30  0001 C CNN
	1    5850 3700
	1    0    0    -1  
$EndComp
$Comp
L R R4
U 1 1 509CE5FB
P 4600 1900
F 0 "R4" V 4680 1900 50  0000 C CNN
F 1 "100k" V 4600 1900 50  0000 C CNN
	1    4600 1900
	1    0    0    -1  
$EndComp
$Comp
L R R3
U 1 1 509CE5F2
P 4400 1900
F 0 "R3" V 4480 1900 50  0000 C CNN
F 1 "100k" V 4400 1900 50  0000 C CNN
	1    4400 1900
	1    0    0    -1  
$EndComp
$Comp
L CAP-0505 C1
U 1 1 509C16F7
P 5300 1650
F 0 "C1" H 5300 1700 40  0000 L BNN
F 1 "CAP-0505" H 5300 1525 50  0000 L BNN
F 2 "scenix4-0505" H 5300 1800 50  0001 C CNN
	1    5300 1650
	1    0    0    -1  
$EndComp
$Comp
L CAP-0505 C2
U 1 1 509C16DD
P 6100 1750
F 0 "C2" H 6100 1800 50  0000 L BNN
F 1 "CAP-0505" H 6100 1625 50  0000 L BNN
F 2 "scenix4-0505" H 6100 1900 50  0001 C CNN
	1    6100 1750
	0    -1   -1   0   
$EndComp
$Comp
L CONN_2 P3
U 1 1 509C145B
P 8050 1150
F 0 "P3" V 8000 1150 40  0000 C CNN
F 1 "Battery" V 8100 1150 40  0000 C CNN
	1    8050 1150
	0    -1   -1   0   
$EndComp
$Comp
L CONN_2 P5
U 1 1 509C139F
P 8900 2800
F 0 "P5" V 8850 2800 40  0000 C CNN
F 1 "OUTPUT_2" V 8950 2800 40  0000 C CNN
	1    8900 2800
	1    0    0    -1  
$EndComp
$Comp
L CONN_2 P4
U 1 1 509C1393
P 8900 2400
F 0 "P4" V 8850 2400 40  0000 C CNN
F 1 "OUTPUT_1" V 8950 2400 40  0000 C CNN
	1    8900 2400
	1    0    0    -1  
$EndComp
$Comp
L DIODE D1
U 1 1 509C1105
P 6700 1700
F 0 "D1" H 6700 1800 40  0000 C CNN
F 1 "DIODE" H 6700 1600 40  0000 C CNN
	1    6700 1700
	0    -1   -1   0   
$EndComp
$Comp
L DIODE D8
U 1 1 509C10FE
P 7550 3400
F 0 "D8" H 7550 3500 40  0000 C CNN
F 1 "DIODE" H 7550 3300 40  0000 C CNN
	1    7550 3400
	0    -1   -1   0   
$EndComp
$Comp
L DIODE D6
U 1 1 509C10F9
P 7300 3400
F 0 "D6" H 7300 3500 40  0000 C CNN
F 1 "DIODE" H 7300 3300 40  0000 C CNN
	1    7300 3400
	0    -1   -1   0   
$EndComp
$Comp
L DIODE D5
U 1 1 509C10F5
P 7300 1700
F 0 "D5" H 7300 1800 40  0000 C CNN
F 1 "DIODE" H 7300 1600 40  0000 C CNN
	1    7300 1700
	0    -1   -1   0   
$EndComp
$Comp
L DIODE D7
U 1 1 509C10F1
P 7550 1700
F 0 "D7" H 7550 1800 40  0000 C CNN
F 1 "DIODE" H 7550 1600 40  0000 C CNN
	1    7550 1700
	0    -1   -1   0   
$EndComp
$Comp
L DIODE D4
U 1 1 509C10ED
P 7000 3400
F 0 "D4" H 7000 3500 40  0000 C CNN
F 1 "DIODE" H 7000 3300 40  0000 C CNN
	1    7000 3400
	0    -1   -1   0   
$EndComp
$Comp
L DIODE D2
U 1 1 509C10E7
P 6700 3400
F 0 "D2" H 6700 3500 40  0000 C CNN
F 1 "DIODE" H 6700 3300 40  0000 C CNN
	1    6700 3400
	0    -1   -1   0   
$EndComp
$Comp
L DIODE D3
U 1 1 509C10DA
P 7000 1700
F 0 "D3" H 7000 1800 40  0000 C CNN
F 1 "DIODE" H 7000 1600 40  0000 C CNN
	1    7000 1700
	0    -1   -1   0   
$EndComp
$Comp
L BC547 T?
U 1 1 509C04D7
P 4100 3250
AR Path="/509BFFE5" Ref="T?"  Part="1" 
AR Path="/509C04D7" Ref="T2"  Part="1" 
F 0 "T2" H 3700 3550 50  0000 L BNN
F 1 "BC547" H 3700 3450 50  0000 L BNN
F 2 "transistor-TO92" H 4100 3400 50  0001 C CNN
	1    4100 3250
	1    0    0    -1  
$EndComp
$Comp
L R R2
U 1 1 509C04D6
P 3750 3400
F 0 "R2" V 3830 3400 50  0000 C CNN
F 1 "1k" V 3750 3400 50  0000 C CNN
	1    3750 3400
	0    -1   -1   0   
$EndComp
$Comp
L CONN_4 P2
U 1 1 509C043C
P 1600 3100
F 0 "P2" V 1550 3100 50  0000 C CNN
F 1 "INPUT_2" V 1650 3100 50  0000 C CNN
	1    1600 3100
	-1   0    0    -1  
$EndComp
Text GLabel 1450 3150 0    60   Input ~ 0
PWM2_in
Text GLabel 1450 3050 0    60   Input ~ 0
DIRECTION2_sel
Text GLabel 1450 3250 0    60   Input ~ 0
GND
Text GLabel 1450 2950 0    60   Input ~ 0
+5v
Text GLabel 2900 2300 0    60   Input ~ 0
+5v
Text GLabel 2900 2600 0    60   Input ~ 0
GND
Text GLabel 2900 2400 0    60   Input ~ 0
DIRECTION1_sel
Text GLabel 2900 2500 0    60   Input ~ 0
PWM1_in
$Comp
L R R1
U 1 1 509C0107
P 3850 2850
F 0 "R1" V 3930 2850 50  0000 C CNN
F 1 "1k" V 3850 2850 50  0000 C CNN
	1    3850 2850
	0    -1   -1   0   
$EndComp
$Comp
L BC547 T1
U 1 1 509BFFE5
P 4200 2700
F 0 "T1" H 3800 3000 50  0000 L BNN
F 1 "BC547" H 3800 2900 50  0000 L BNN
F 2 "transistor-TO92" H 4200 2850 50  0001 C CNN
	1    4200 2700
	1    0    0    -1  
$EndComp
$Comp
L CONN_4 P1
U 1 1 509BFE14
P 3050 2450
F 0 "P1" V 3000 2450 50  0000 C CNN
F 1 "INPUT_1" V 3100 2450 50  0000 C CNN
	1    3050 2450
	-1   0    0    -1  
$EndComp
$Comp
L L298 IC1
U 1 1 509BFCB0
P 5400 2700
F 0 "IC1" H 4918 3435 50  0000 L BNN
F 1 "L298" H 4941 2052 50  0000 L BNN
F 2 "sgs-thom-MW-15" H 5400 2850 50  0001 C CNN
	1    5400 2700
	1    0    0    -1  
$EndComp
$EndSCHEMATC
