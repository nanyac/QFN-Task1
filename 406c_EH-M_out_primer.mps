! пример формата выходного файла сечения MPS файла по заданной частоте
!
! Т.е. в исходном MPS файле идут блоки данных S-параметров по частоте для разных фиксированных VGS_pulsed
! В выходной файл надо выгрузить блок (или несколько блоков) тех же S-параметров для одной (или ряда) частоты,
! только в первую колонку надо выписывать (мб разумно округленное) значение разности [Vgs_quiestient-Vgs_pulsed] (должно быть положительным и не равным нулю, т.ч. тут первое значение 0,001),
! а в остальные колонки выгрузить S-параметры на заданной частоте.
! Соответственно, для каждой из ряда частот надо составить свой блок данных, с заголовком в формате "!!NAME" (NAME - имя блока данных, например значение частоты. Пример: !!F = 0.3GHz )
!
! Строку форматирования "# Hz S RI R 50" оставить без изменения, чтобы обмануть IV-CAD. Т.ч. он будет строить нам графики зависимостей от VGS, думая, что это частота в Гц.


!!F = 0.3 GHz 
!
! Frequency: F=+3.00000E8
!
! Quiescent point : Vgs=-4.00 Vds=+5.00
! Pulsed point : Vds=+5.35839E-03
! Period : +2.00000E-04
! Input Supply timing : delay=+1.80000E-05 width=+5.50000E-06
! Output Supply timing : delay=+1.93000E-05 width=+3.00000E-06
! RF timing : delay=+2.07000E-05 width=+1.40000E-06
! VNA timing : delay=+2.12000E-05 width=+8.00000E-07
# Hz S RI R 50
0.001 +9.95250E-01 -4.15191E-02 +9.80655E-04 +1.28457E-02 -2.16566E-03 +1.51418E-02 +9.91595E-01 -3.17236E-02
0.2 +9.93273E-01 -3.94093E-02 +1.94947E-03 +1.23710E-02 +1.93723E-04 +1.51354E-02 +9.94062E-01 -4.01567E-02
!..... далее строки для остальных значений, округленных до 0,01 В, разности [Vgs_quiestient-Vgs_pulsed] по списку значений Vgs_pulsed исходного MPS файла


!!F = 1.0 GHz 
!
! Frequency: F=+1.00000E9
!
! Quiescent point : Vgs=-4.00 Vds=+5.00
! Pulsed point : Vds=+5.35839E-03
! Period : +2.00000E-04
! Input Supply timing : delay=+1.80000E-05 width=+5.50000E-06
! Output Supply timing : delay=+1.93000E-05 width=+3.00000E-06
! RF timing : delay=+2.07000E-05 width=+1.40000E-06
! VNA timing : delay=+2.12000E-05 width=+8.00000E-07
# Hz S RI R 50
0.001 +9.95250E-01 -4.15191E-02 +9.80655E-04 +1.28457E-02 -2.16566E-03 +1.51418E-02 +9.91595E-01 -3.17236E-02
0.2 +9.93273E-01 -3.94093E-02 +1.94947E-03 +1.23710E-02 +1.93723E-04 +1.51354E-02 +9.94062E-01 -4.01567E-02
!..... далее строки для остальных значений, округленных до 0,01 В, разности [Vgs_quiestient-Vgs_pulsed] по списку значений Vgs_pulsed исходного MPS файла