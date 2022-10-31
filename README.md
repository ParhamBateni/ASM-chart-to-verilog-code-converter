# ASM-chart-to-verilog-code-converter
This is a python program which takes a ASM chart by graphical user interface using tkinter package and produces the equivalent code in verilog language.
## Phase1:
ASM chart is converted to its equivalent variables table.
For example we have:
![ASM_Chart_Test2](https://user-images.githubusercontent.com/79264909/199072487-6966031e-5184-4aad-953e-6f36d6f5272b.png)

Cycle: 1<br/>
ASM Block: 1<br/>
Variable	Value<br/>
S	1<br/>
*************************<br/>
Cycle: 2<br/>
ASM Block: 4<br/>
Variable	Value<br/>
S	1<br/>
sum	0<br/>
i	0<br/>
e	20<br/>
*************************<br/>
Cycle: 3<br/>
ASM Block: 4<br/>
Variable	Value<br/>
S	1<br/>
sum	0<br/>
i	1<br/>
e	20<br/>
*************************<br/>
Cycle: 4<br/>
ASM Block: 4<br/>
Variable	Value<br/>
S	1<br/>
sum	1<br/>
i	2<br/>
e	20<br/>
*************************<br/>
Cycle: 5<br/>
ASM Block: 4<br/>
Variable	Value<br/>
S	1<br/>
sum	3<br/>
i	3<br/>
e	20<br/>
*************************<br/>
Cycle: 6<br/>
ASM Block: 4<br/>
Variable	Value<br/>
S	1<br/>
sum	6<br/>
i	4<br/>
e	20<br/>
*************************<br/>
Cycle: 7<br/>
ASM Block: 4<br/>
Variable	Value<br/>
S	1<br/>
sum	10<br/>
i	5<br/>
e	20<br/>
*************************<br/>
Cycle: 8<br/>
ASM Block: 4<br/>
Variable	Value<br/>
S	1<br/>
sum	15<br/>
i	6<br/>
e	20<br/>
*************************<br/>
Cycle: 9<br/>
ASM Block: 4<br/>
Variable	Value<br/>
S	1<br/>
sum	21<br/>
i	7<br/>
e	20<br/>
*************************<br/>
Cycle: 10<br/>
ASM Block: 4<br/>
Variable	Value<br/>
S	1<br/>
sum	28<br/>
i	8<br/>
e	20<br/>
*************************<br/>
Cycle: 11<br/>
ASM Block: 4<br/>
Variable	Value<br/>
S	1<br/>
sum	36<br/>
i	9<br/>
e	20<br/>
*************************<br/>
Cycle: 12<br/>
ASM Block: 4<br/>
Variable	Value<br/>
S	1<br/>
sum	45<br/>
i	10<br/>
e	20<br/>
*************************<br/>
Cycle: 13<br/>
ASM Block: 4<br/>
Variable	Value<br/>
S	1<br/>
sum	55<br/>
i	11<br/>
e	20<br/>
*************************<br/>
Cycle: 14<br/>
ASM Block: 4<br/>
Variable	Value<br/>
S	1<br/>
sum	66<br/>
i	12<br/>
e	20<br/>
*************************<br/>
Cycle: 15<br/>
ASM Block: 4<br/>
Variable	Value<br/>
S	1<br/>
sum	78<br/>
i	13<br/>
e	20<br/>
*************************<br/>
Cycle: 16<br/>
ASM Block: 4<br/>
Variable	Value<br/>
S	1<br/>
sum	91<br/>
i	14<br/>
e	20<br/>
*************************<br/>
Cycle: 17<br/>
ASM Block: 4<br/>
Variable	Value<br/>
S	1<br/>
sum	105<br/>
i	15<br/>
e	20<br/>
*************************<br/>
Cycle: 18<br/>
ASM Block: 4<br/>
Variable	Value<br/>
S	1<br/>
sum	120<br/>
i	16<br/>
e	20<br/>
*************************<br/>
Cycle: 19<br/>
ASM Block: 4<br/>
Variable	Value<br/>
S	1<br/>
sum	136<br/>
i	17<br/>
e	20<br/>
*************************<br/>
Cycle: 20<br/>
ASM Block: 4<br/>
Variable	Value<br/>
S	1<br/>
sum	153<br/>
i	18<br/>
e	20<br/>
*************************<br/>
Cycle: 21<br/>
ASM Block: 4<br/>
Variable	Value<br/>
S	1<br/>
sum	171<br/>
i	19<br/>
e	20<br/>
*************************<br/>
Cycle: 22<br/>
ASM Block: 4<br/>
Variable	Value<br/>
S	1<br/>
sum	190<br/>
i	20<br/>
e	20<br/>
*************************<br/>
Cycle: 23<br/>
ASM Block: 4<br/>
Variable	Value<br/>
S	1<br/>
sum	210<br/>
i	21<br/>
e	20<br/>
*************************<br/>
Cycle: 24<br/>
ASM Block: 1<br/>
Variable	Value<br/>
S	1<br/>
sum	210<br/>
i	21<br/>
e	20<br/>
result	210<br/>
ready	1<br/>
*************************<br/>



## Phase2: ASM chart is converted into verilog modules.
Forexample for the previous ASM chart we will have following files created:
![image](https://user-images.githubusercontent.com/79264909/199075386-b6d4a6e2-7708-4eb6-9c93-82120dd42657.png)

and the final wave result would be:
![Wave2_Test2](https://user-images.githubusercontent.com/79264909/199076096-fca54185-a4c8-4815-9262-6bcc08d02ca0.png)
which computes 1+2+...+20=210 correctly
