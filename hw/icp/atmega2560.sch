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
LIBS:argo
LIBS:icp-cache
EELAYER 27 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 2 2
Title ""
Date "4 jul 2013"
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L INDUCTOR L1
U 1 1 51B05B8C
P 4050 3000
F 0 "L1" V 4000 3000 40  0000 C CNN
F 1 "10µ" V 4150 3000 40  0000 C CNN
F 2 "~" H 4050 3000 60  0000 C CNN
F 3 "~" H 4050 3000 60  0000 C CNN
	1    4050 3000
	0    1    1    0   
$EndComp
$Comp
L C C9
U 1 1 51B05BD4
P 4400 2750
F 0 "C9" H 4400 2850 40  0000 L CNN
F 1 "100n" H 4406 2665 40  0000 L CNN
F 2 "~" H 4438 2600 30  0000 C CNN
F 3 "~" H 4400 2750 60  0000 C CNN
	1    4400 2750
	-1   0    0    1   
$EndComp
$Comp
L GND #PWR027
U 1 1 51B05BF9
P 4500 2550
F 0 "#PWR027" H 4500 2550 30  0001 C CNN
F 1 "GND" H 4500 2480 30  0001 C CNN
F 2 "" H 4500 2550 60  0000 C CNN
F 3 "" H 4500 2550 60  0000 C CNN
	1    4500 2550
	1    0    0    -1  
$EndComp
Wire Wire Line
	4400 2550 4400 2500
Wire Wire Line
	4400 2500 4500 2500
Wire Wire Line
	4350 3000 4600 3000
Wire Wire Line
	4400 2950 4400 3000
Connection ~ 4400 3000
$Comp
L C C10
U 1 1 51B05C72
P 4400 3550
F 0 "C10" H 4400 3650 40  0000 L CNN
F 1 "100n" H 4406 3465 40  0000 L CNN
F 2 "~" H 4438 3400 30  0000 C CNN
F 3 "~" H 4400 3550 60  0000 C CNN
	1    4400 3550
	-1   0    0    1   
$EndComp
Wire Wire Line
	3750 3300 4600 3300
Wire Wire Line
	4400 3300 4400 3350
$Comp
L GND #PWR028
U 1 1 51B05CD2
P 4400 3800
F 0 "#PWR028" H 4400 3800 30  0001 C CNN
F 1 "GND" H 4400 3730 30  0001 C CNN
F 2 "" H 4400 3800 60  0000 C CNN
F 3 "" H 4400 3800 60  0000 C CNN
	1    4400 3800
	1    0    0    -1  
$EndComp
Wire Wire Line
	4400 3800 4400 3750
Connection ~ 4400 3300
Wire Wire Line
	3750 3000 3750 3450
Connection ~ 3750 3300
Text Notes 4200 3650 2    60   ~ 0
Place capacitors\nnear pin on chip\non PCB layout
Text Notes 3450 2550 0    60   ~ 0
Analog supply\nfilter as\nof some Atmel\napplication note\nalso close to pin
Text HLabel 6500 3550 2    60   Input ~ 0
ADC0
Text HLabel 6500 3650 2    60   Input ~ 0
ADC1
Text HLabel 6500 3750 2    60   Input ~ 0
ADC2
Text HLabel 6500 3850 2    60   Input ~ 0
ADC3
Text HLabel 6500 3950 2    60   Input ~ 0
ADC4
Text HLabel 6500 4050 2    60   Input ~ 0
ADC5
Text HLabel 4600 4050 0    60   Input ~ 0
ADC6
Text HLabel 4600 4150 0    60   Input ~ 0
ADC7
Text HLabel 3750 3450 0    60   Input ~ 0
VCC
$Comp
L ATMEGA168-A IC1
U 1 1 51D47125
P 5500 3800
F 0 "IC1" H 4750 5050 40  0000 L BNN
F 1 "ATMEGA168P-20AU" H 5950 2400 40  0000 L BNN
F 2 "TQFP32" H 5500 3800 30  0000 C CIN
F 3 "~" H 5500 3800 60  0000 C CNN
	1    5500 3800
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR029
U 1 1 51D4849A
P 4500 5050
F 0 "#PWR029" H 4500 5050 30  0001 C CNN
F 1 "GND" H 4500 4980 30  0001 C CNN
F 2 "" H 4500 5050 60  0000 C CNN
F 3 "" H 4500 5050 60  0000 C CNN
	1    4500 5050
	1    0    0    -1  
$EndComp
Wire Wire Line
	4600 4800 4500 4800
Wire Wire Line
	4500 4800 4500 5050
Wire Wire Line
	4600 5000 4500 5000
Connection ~ 4500 5000
Wire Wire Line
	4600 4900 4500 4900
Connection ~ 4500 4900
Wire Wire Line
	4500 2500 4500 2550
Text HLabel 6500 4600 2    60   Input ~ 0
TACHO1
Text HLabel 6500 4500 2    60   Input ~ 0
TACHO0
Text HLabel 4500 4800 0    60   BiDi ~ 0
GND
Text HLabel 6500 2700 2    60   Input ~ 0
WLD1
Text HLabel 6500 2800 2    60   Input ~ 0
WLD2
Text HLabel 6500 4300 2    60   Input ~ 0
TXD
Text HLabel 6500 4400 2    60   Input ~ 0
RXD
Text HLabel 6500 4700 2    60   Input ~ 0
SDA
Text HLabel 6500 4800 2    60   Input ~ 0
SCL
Text Notes 7300 4950 0    60   ~ 0
I²C not using hardware, since they\nare taken by the ADC's so this\ndevice does not have to do a lot it\ncan slave easily in software.
Wire Notes Line
	6750 4850 6800 4800
Wire Notes Line
	6800 4800 6800 4700
Wire Notes Line
	6800 4700 6750 4650
$Comp
L CRYSTAL X1
U 1 1 51D4B87C
P 7700 3400
F 0 "X1" H 7700 3550 60  0000 C CNN
F 1 "16MHz" H 7700 3250 60  0000 C CNN
F 2 "~" H 7700 3400 60  0000 C CNN
F 3 "~" H 7700 3400 60  0000 C CNN
	1    7700 3400
	1    0    0    -1  
$EndComp
$Comp
L C C12
U 1 1 51D4B88B
P 8050 3650
F 0 "C12" H 8050 3750 40  0000 L CNN
F 1 "22p" H 8056 3565 40  0000 L CNN
F 2 "~" H 8088 3500 30  0000 C CNN
F 3 "~" H 8050 3650 60  0000 C CNN
	1    8050 3650
	1    0    0    -1  
$EndComp
$Comp
L C C11
U 1 1 51D4B898
P 7350 3650
F 0 "C11" H 7350 3750 40  0000 L CNN
F 1 "22p" H 7356 3565 40  0000 L CNN
F 2 "~" H 7388 3500 30  0000 C CNN
F 3 "~" H 7350 3650 60  0000 C CNN
	1    7350 3650
	1    0    0    -1  
$EndComp
Text HLabel 6500 4900 2    60   Input ~ 0
LED1
Text HLabel 6500 2900 2    60   Input ~ 0
LED0
Text HLabel 6500 3100 2    60   Input ~ 0
LED2
Text HLabel 6500 3200 2    60   Input ~ 0
LED3
Wire Wire Line
	6500 3400 7400 3400
Text HLabel 6500 5000 2    60   Input ~ 0
LED4
Text HLabel 6500 3000 2    60   Input ~ 0
BUZZ
Text Notes 7400 2650 0    60   ~ 0
The buzzer should be modulated with\n50% duty cycle sqyare wave with for\nexample a frequency of 2400 Hz.
Wire Notes Line
	6850 3000 6950 3000
Wire Notes Line
	6950 3000 7250 2700
Wire Notes Line
	7250 2700 7350 2700
Wire Notes Line
	7350 2700 7300 2650
Wire Notes Line
	7350 2700 7300 2750
Wire Notes Line
	6800 4750 6900 4750
Wire Notes Line
	6900 4750 7150 5050
Wire Notes Line
	7150 5050 7250 5050
Wire Notes Line
	7250 5050 7200 5000
Wire Notes Line
	7250 5050 7200 5100
$Comp
L GND #PWR030
U 1 1 51D5684A
P 8050 3900
F 0 "#PWR030" H 8050 3900 30  0001 C CNN
F 1 "GND" H 8050 3830 30  0001 C CNN
F 2 "" H 8050 3900 60  0000 C CNN
F 3 "" H 8050 3900 60  0000 C CNN
	1    8050 3900
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR031
U 1 1 51D56857
P 7350 3900
F 0 "#PWR031" H 7350 3900 30  0001 C CNN
F 1 "GND" H 7350 3830 30  0001 C CNN
F 2 "" H 7350 3900 60  0000 C CNN
F 3 "" H 7350 3900 60  0000 C CNN
	1    7350 3900
	1    0    0    -1  
$EndComp
Wire Wire Line
	7350 3450 7350 3400
Connection ~ 7350 3400
Wire Wire Line
	7350 3900 7350 3850
Wire Wire Line
	8050 3900 8050 3850
Wire Wire Line
	8050 3150 8050 3450
Wire Wire Line
	8050 3400 8000 3400
Connection ~ 8050 3400
Wire Wire Line
	6500 3300 6900 3300
Wire Wire Line
	6900 3300 7600 3150
Wire Wire Line
	7600 3150 8050 3150
Text Notes 8100 3300 0    60   ~ 0
As close to\nchip as possible
$EndSCHEMATC
