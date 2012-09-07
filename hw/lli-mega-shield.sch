EESchema Schematic File Version 2  date fre 07 sep 2012 20:49:57 CEST
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
LIBS:arduino_shieldsNCL
LIBS:argo
LIBS:lli-mega-shield-cache
EELAYER 25  0
EELAYER END
$Descr A4 11700 8267
encoding utf-8
Sheet 1 1
Title "Low Level Interface"
Date "7 sep 2012"
Rev "1"
Comp "Aalborg University"
Comment1 "Nick Østergaard"
Comment2 "AAUSHIP"
Comment3 ""
Comment4 ""
$EndDescr
Text Notes 3300 4800 0    60   Italic 12
Battery Sensor
Text Notes 900  2800 0    60   Italic 12
Temperature Sensors
$Comp
L LM35 U?
U 1 1 504A41AE
P 1500 4500
F 0 "U?" H 1500 4650 60  0000 C CNN
F 1 "LM35" H 1650 4250 60  0000 C CNN
	1    1500 4500
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 504A41AD
P 2150 4800
F 0 "R?" V 2230 4800 50  0000 C CNN
F 1 "75" V 2150 4800 50  0000 C CNN
	1    2150 4800
	1    0    0    -1  
$EndComp
$Comp
L C C?
U 1 1 504A41AC
P 2150 5300
F 0 "C?" H 2200 5400 50  0000 L CNN
F 1 "1uF" H 2200 5200 50  0000 L CNN
	1    2150 5300
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR?
U 1 1 504A41AB
P 1500 5100
F 0 "#PWR?" H 1500 5100 30  0001 C CNN
F 1 "GND" H 1500 5030 30  0001 C CNN
	1    1500 5100
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR?
U 1 1 504A41AA
P 900 4450
F 0 "#PWR?" H 900 4540 20  0001 C CNN
F 1 "+5V" H 900 4540 30  0000 C CNN
	1    900  4450
	1    0    0    -1  
$EndComp
$Comp
L LM35 U?
U 1 1 504A41A9
P 1500 4500
F 0 "U?" H 1500 4650 60  0000 C CNN
F 1 "LM35" H 1650 4250 60  0000 C CNN
	1    1500 4500
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR?
U 1 1 504A41A8
P 2150 5550
F 0 "#PWR?" H 2150 5550 30  0001 C CNN
F 1 "GND" H 2150 5480 30  0001 C CNN
	1    2150 5550
	1    0    0    -1  
$EndComp
Wire Wire Line
	900  4500 950  4500
Wire Wire Line
	900  4450 900  4500
Wire Wire Line
	2200 4500 2050 4500
Wire Wire Line
	2150 5100 2150 5050
Wire Wire Line
	2150 4500 2150 4550
Connection ~ 2150 4500
Wire Wire Line
	1500 5100 1500 5000
Wire Wire Line
	2150 5550 2150 5500
Wire Wire Line
	2150 4200 2150 4150
Wire Wire Line
	1500 3750 1500 3650
Connection ~ 2150 3150
Wire Wire Line
	2150 3150 2150 3200
Wire Wire Line
	2150 3750 2150 3700
Wire Wire Line
	1450 7200 1450 7150
Wire Wire Line
	1450 6450 1450 6750
Wire Wire Line
	1450 6450 1500 6450
Wire Wire Line
	1850 1000 1600 1000
Wire Wire Line
	1800 1300 1600 1300
Wire Wire Line
	1600 1600 1700 1600
Wire Wire Line
	1700 1600 1700 1650
Wire Wire Line
	1600 1500 1700 1500
Wire Wire Line
	1600 1200 1800 1200
Wire Notes Line
	1950 1750 1950 700 
Wire Notes Line
	1950 1750 650  1750
Wire Notes Line
	650  1750 650  700 
Wire Notes Line
	650  700  1950 700 
Wire Wire Line
	1150 6350 1500 6350
Connection ~ 1300 6350
Wire Wire Line
	1450 6750 1300 6750
Wire Wire Line
	1750 6950 1800 6950
Wire Wire Line
	2200 3150 2050 3150
Wire Wire Line
	900  3100 900  3150
Wire Wire Line
	900  3150 950  3150
$Comp
L GND #PWR?
U 1 1 504A414B
P 2150 4200
F 0 "#PWR?" H 2150 4200 30  0001 C CNN
F 1 "GND" H 2150 4130 30  0001 C CNN
	1    2150 4200
	1    0    0    -1  
$EndComp
$Comp
L LM35 U?
U 1 1 504A39E8
P 1500 3150
F 0 "U?" H 1500 3300 60  0000 C CNN
F 1 "LM35" H 1650 2900 60  0000 C CNN
	1    1500 3150
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR?
U 1 1 504A39DE
P 900 3100
F 0 "#PWR?" H 900 3190 20  0001 C CNN
F 1 "+5V" H 900 3190 30  0000 C CNN
	1    900  3100
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR?
U 1 1 504A39D5
P 1500 3750
F 0 "#PWR?" H 1500 3750 30  0001 C CNN
F 1 "GND" H 1500 3680 30  0001 C CNN
	1    1500 3750
	1    0    0    -1  
$EndComp
$Comp
L C C?
U 1 1 504A39C7
P 2150 3950
F 0 "C?" H 2200 4050 50  0000 L CNN
F 1 "1uF" H 2200 3850 50  0000 L CNN
	1    2150 3950
	1    0    0    -1  
$EndComp
$Comp
L R R?
U 1 1 504A39C1
P 2150 3450
F 0 "R?" V 2230 3450 50  0000 C CNN
F 1 "75" V 2150 3450 50  0000 C CNN
	1    2150 3450
	1    0    0    -1  
$EndComp
$Comp
L LM35 U?
U 1 1 504A39B9
P 1500 3150
F 0 "U?" H 1500 3300 60  0000 C CNN
F 1 "LM35" H 1650 2900 60  0000 C CNN
	1    1500 3150
	1    0    0    -1  
$EndComp
Text Notes 1000 7400 0    60   ~ 0
Disconnects supply to all actuators
Text Notes 1000 5850 0    60   Italic 12
Kill Switch
$Comp
L +5V #PWR?
U 1 1 504A299E
P 1150 6350
F 0 "#PWR?" H 1150 6440 20  0001 C CNN
F 1 "+5V" H 1150 6440 30  0000 C CNN
	1    1150 6350
	1    0    0    -1  
$EndComp
NoConn ~ 2300 6050
$Comp
L R R?
U 1 1 504A2942
P 2050 6950
F 0 "R?" V 2130 6950 50  0000 C CNN
F 1 "1K" V 2050 6950 50  0000 C CNN
	1    2050 6950
	0    -1   -1   0   
$EndComp
$Comp
L GND #PWR?
U 1 1 504A293C
P 1450 7200
F 0 "#PWR?" H 1450 7200 30  0001 C CNN
F 1 "GND" H 1450 7130 30  0001 C CNN
	1    1450 7200
	1    0    0    -1  
$EndComp
$Comp
L DIODE D?
U 1 1 504A2907
P 1300 6550
F 0 "D?" H 1300 6650 40  0000 C CNN
F 1 "DIODE" H 1300 6450 40  0000 C CNN
	1    1300 6550
	0    -1   -1   0   
$EndComp
$Comp
L NPN Q?
U 1 1 504A28F4
P 1550 6950
F 0 "Q?" H 1550 6800 50  0000 R CNN
F 1 "NPN" H 1550 7100 50  0000 R CNN
	1    1550 6950
	-1   0    0    1   
$EndComp
Text Notes 650  700  0    60   Italic 12
UHF Radio Module
Text Notes 950  800  0    60   ~ 0
RF_EN high to enable\n
Text Label 1800 1300 2    60   ~ 0
RXD
NoConn ~ 1600 1100
NoConn ~ 1600 1400
$Comp
L +5V #PWR?
U 1 1 504A27A3
P 1700 1500
F 0 "#PWR?" H 1700 1590 20  0001 C CNN
F 1 "+5V" H 1700 1590 30  0000 C CNN
	1    1700 1500
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR?
U 1 1 504A279C
P 1700 1650
F 0 "#PWR?" H 1700 1650 30  0001 C CNN
F 1 "GND" H 1700 1580 30  0001 C CNN
	1    1700 1650
	1    0    0    -1  
$EndComp
Text Label 1850 1000 2    60   ~ 0
RF_EN
Text Label 1800 1200 2    60   ~ 0
TXD
$Comp
L APC220 U?
U 1 1 504A274B
P 1100 1250
F 0 "U?" H 1100 1600 60  0000 C CNN
F 1 "APC220" V 1050 1200 60  0000 C CNN
	1    1100 1250
	1    0    0    -1  
$EndComp
$Comp
L RELAY_1RT K?
U 1 1 504A271B
P 1900 6300
F 0 "K?" H 1900 6600 70  0000 C CNN
F 1 "36.11.9.003.4000" H 1950 6000 70  0000 C CNN
	1    1900 6300
	1    0    0    -1  
$EndComp
$Comp
L ARDUINO_MEGA_SHIELD SHIELD?
U 1 1 504A215E
P 6000 3750
F 0 "SHIELD?" H 5600 6250 60  0000 C CNN
F 1 "ARDUINO_MEGA_SHIELD" H 5900 1050 60  0000 C CNN
	1    6000 3750
	1    0    0    -1  
$EndComp
$EndSCHEMATC
