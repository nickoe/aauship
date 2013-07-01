EESchema Schematic File Version 2
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
LIBS:jst-xh-illustration
LIBS:icp-cache
EELAYER 27 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 2 2
Title ""
Date "1 jul 2013"
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L ATMEGA2560-A IC?
U 1 1 51B05B73
P 3850 4700
F 0 "IC?" H 2700 7500 40  0000 L BNN
F 1 "ATMEGA2560-A" H 4550 1850 40  0000 L BNN
F 2 "TQFP100" H 3850 4700 30  0000 C CIN
F 3 "~" H 3850 4700 60  0000 C CNN
	1    3850 4700
	1    0    0    -1  
$EndComp
$Comp
L INDUCTOR L?
U 1 1 51B05B8C
P 4000 1400
F 0 "L?" V 3950 1400 40  0000 C CNN
F 1 "10µ" V 4100 1400 40  0000 C CNN
F 2 "~" H 4000 1400 60  0000 C CNN
F 3 "~" H 4000 1400 60  0000 C CNN
	1    4000 1400
	-1   0    0    1   
$EndComp
$Comp
L C C?
U 1 1 51B05BD4
P 4250 1750
F 0 "C?" H 4250 1850 40  0000 L CNN
F 1 "100n" H 4256 1665 40  0000 L CNN
F 2 "~" H 4288 1600 30  0000 C CNN
F 3 "~" H 4250 1750 60  0000 C CNN
	1    4250 1750
	0    -1   -1   0   
$EndComp
$Comp
L GND #PWR?
U 1 1 51B05BF9
P 4500 1800
F 0 "#PWR?" H 4500 1800 30  0001 C CNN
F 1 "GND" H 4500 1730 30  0001 C CNN
F 2 "" H 4500 1800 60  0000 C CNN
F 3 "" H 4500 1800 60  0000 C CNN
	1    4500 1800
	1    0    0    -1  
$EndComp
Wire Wire Line
	4450 1750 4500 1750
Wire Wire Line
	4500 1750 4500 1800
Wire Wire Line
	4000 1800 4000 1700
Wire Wire Line
	4050 1750 4000 1750
Connection ~ 4000 1750
$Comp
L C C?
U 1 1 51B05C54
P 3250 1700
F 0 "C?" H 3250 1800 40  0000 L CNN
F 1 "100n" H 3256 1615 40  0000 L CNN
F 2 "~" H 3288 1550 30  0000 C CNN
F 3 "~" H 3250 1700 60  0000 C CNN
	1    3250 1700
	0    -1   -1   0   
$EndComp
$Comp
L C C?
U 1 1 51B05C63
P 3350 1500
F 0 "C?" H 3350 1600 40  0000 L CNN
F 1 "100n" H 3356 1415 40  0000 L CNN
F 2 "~" H 3388 1350 30  0000 C CNN
F 3 "~" H 3350 1500 60  0000 C CNN
	1    3350 1500
	0    -1   -1   0   
$EndComp
$Comp
L C C?
U 1 1 51B05C72
P 3450 1300
F 0 "C?" H 3450 1400 40  0000 L CNN
F 1 "100n" H 3456 1215 40  0000 L CNN
F 2 "~" H 3488 1150 30  0000 C CNN
F 3 "~" H 3450 1300 60  0000 C CNN
	1    3450 1300
	0    -1   -1   0   
$EndComp
Wire Wire Line
	3500 1800 3500 1700
Wire Wire Line
	3450 1700 3700 1700
Wire Wire Line
	3600 1800 3600 1500
Wire Wire Line
	3600 1500 3550 1500
Wire Wire Line
	3700 1100 3700 1800
Wire Wire Line
	3700 1300 3650 1300
Connection ~ 3600 1700
Connection ~ 3500 1700
Connection ~ 3700 1700
$Comp
L GND #PWR?
U 1 1 51B05CB3
P 3100 1550
F 0 "#PWR?" H 3100 1550 30  0001 C CNN
F 1 "GND" H 3100 1480 30  0001 C CNN
F 2 "" H 3100 1550 60  0000 C CNN
F 3 "" H 3100 1550 60  0000 C CNN
	1    3100 1550
	1    0    0    -1  
$EndComp
Wire Wire Line
	3100 1550 3100 1500
Wire Wire Line
	3100 1500 3150 1500
$Comp
L GND #PWR?
U 1 1 51B05CD2
P 3200 1350
F 0 "#PWR?" H 3200 1350 30  0001 C CNN
F 1 "GND" H 3200 1280 30  0001 C CNN
F 2 "" H 3200 1350 60  0000 C CNN
F 3 "" H 3200 1350 60  0000 C CNN
	1    3200 1350
	1    0    0    -1  
$EndComp
Wire Wire Line
	3200 1350 3200 1300
Wire Wire Line
	3200 1300 3250 1300
$Comp
L GND #PWR?
U 1 1 51B05CF3
P 3000 1750
F 0 "#PWR?" H 3000 1750 30  0001 C CNN
F 1 "GND" H 3000 1680 30  0001 C CNN
F 2 "" H 3000 1750 60  0000 C CNN
F 3 "" H 3000 1750 60  0000 C CNN
	1    3000 1750
	1    0    0    -1  
$EndComp
Wire Wire Line
	3000 1750 3000 1700
Wire Wire Line
	3000 1700 3050 1700
Connection ~ 3700 1300
Wire Wire Line
	3550 1100 4000 1100
Connection ~ 3700 1100
Text Notes 2650 1050 0    60   ~ 0
Place capacitors\nnear pin on chip\non PCB layout
Text Notes 4100 1150 0    60   ~ 0
Analog supply\nfilter as\nof some Atmel\napplication note\nalso close to pin
$Comp
L GND #PWR?
U 1 1 51B0611C
P 3850 7700
F 0 "#PWR?" H 3850 7700 30  0001 C CNN
F 1 "GND" H 3850 7630 30  0001 C CNN
F 2 "" H 3850 7700 60  0000 C CNN
F 3 "" H 3850 7700 60  0000 C CNN
	1    3850 7700
	1    0    0    -1  
$EndComp
Wire Wire Line
	3700 7600 3700 7650
Wire Wire Line
	3700 7650 4000 7650
Wire Wire Line
	4000 7650 4000 7600
Wire Wire Line
	3900 7600 3900 7650
Connection ~ 3900 7650
Wire Wire Line
	3800 7600 3800 7650
Connection ~ 3800 7650
Wire Wire Line
	3850 7650 3850 7700
Connection ~ 3850 7650
Text HLabel 5150 6600 2    60   Input ~ 0
ADC0
Text HLabel 5150 6700 2    60   Input ~ 0
ADC1
Text HLabel 5150 6800 2    60   Input ~ 0
ADC2
Text HLabel 5150 6900 2    60   Input ~ 0
ADC3
Text HLabel 5150 7000 2    60   Input ~ 0
ADC4
Text HLabel 5150 7100 2    60   Input ~ 0
ADC5
Text HLabel 5150 7200 2    60   Input ~ 0
ADC6
Text HLabel 5150 7300 2    60   Input ~ 0
ADC7
Text HLabel 2550 3900 0    60   Input ~ 0
ADC8
Text HLabel 2550 4000 0    60   Input ~ 0
ADC9
Text HLabel 3550 1100 1    60   Input ~ 0
VCC
$EndSCHEMATC
