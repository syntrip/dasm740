#
# Mitsubishi 740 Family (8-bit microcomputer) disassembler
#
# Syntrip Sistemas
#
#

import sys, datetime, re

#
# ---
#

def main(argv):

	if len(sys.argv) < 2:
		print '{} [OPTIONS] FILE\n ' \
		      '\t-r: Include reference guide\n' \
		      '\t-d: Include description\n' \
		      '\t-o: Include operation description\n' \
		      '\t-c: Include number of cycles' \
		      .format(sys.argv[0])
		sys.exit(2)

	input_file = ''

	reference_f = 0
	description_f = 0
	operation_f = 0
	cycles_f = 0


	for o in sys.argv:
		if o in ('-d', '--description'):
			description_f = 1
		elif o in ('-o', '--operation'):
			operation_f = 1
		elif o in ('-c', '--cycles'):
			cycles_f = 1
		elif o in ('-r', '--reference'):
			reference_f = 1
		else:
			input_file = o


	print ';\n; Mitsubishi 740 Family (8-bit microcomputer) disassembler\n;\n; File: {}\n; Date: {}\n;\n'.format(input_file, datetime.datetime.now())

	if reference_f:
		print ';\n; REFERENCE GUIDE:\n' \
		      '; \n' \
		      ';    A         Accumulator\n' \
		      ';    Ai        Bit i of Accumulator\n' \
		      ';    PC        Program counter\n' \
		      ';    PCl       Low-order byte of program counter\n' \
		      ';    PCh       High-order byte of program counter\n' \
		      ';    PS        Processor status\n' \
		      ';    S         Stack pointer\n' \
		      ';    X         Index register X\n' \
		      ';    Y         Index register Y\n' \
		      ';    M         Memory\n' \
		      ';    Mi        Bit i of memory\n' \
		      ';    C         Carry flag\n' \
		      ';    Z         Zero flag\n' \
		      ';    I         Interrupt disable flag\n' \
		      ';    D         Decimal operation mode flag\n' \
		      ';    B         Break flag\n' \
		      ';    T         X modified operations mode flag\n' \
		      ';    V         Overflow flag\n' \
		      ';    N         Negative flag\n' \
		      ';    REL       Relative address\n' \
		      ';    BADRS     Break address\n' \
		      ';    hh        Address high-order byte data in 0 to 255\n' \
		      ';    ll        Address low-order byte data in 0 to 255\n' \
		      ';    zz        Zero page address data in 0 to 255\n' \
		      ';    nn        Data in 0 to 255\n' \
		      ';    i         Data in 0 to 7\n' \
		      ';    *         Contents of the program counter\n' \
		      ';    #         Immediate mode\n' \
		      ';    \\         Special page mode\n' \
		      ';    $         Hexadecimal symbol\n' \
		      ';    +         Addition\n' \
		      ';    -         Substraction\n' \
		      ';    x         Multiplication\n' \
		      ';    /         Division\n' \
		      ';    AND       Logical AND\n' \
		      ';    OR        Logical OR\n' \
		      ';    XOR       Logical exclusive OR\n' \
		      ';    ()        Contents of register, memory, etc\n' \
		      ';    <-        Direction of data transfer\n' \
		      ';    )<-       Rotation\n' \
		      '; \n'


	print '\n'

	t = {

		# statement, code, size, cycles, description, operation description

		# ADC
		'69' : [ 'ADC #$nn',    '69 nn',    2, 2,  'Add with carry - Immediate', 'When (T) = 0, (A) <- (A) + (M) - (C). When (T) = 1, (M(X)) <- (M(X)) + (M) + (C)' ],
		'65' : [ 'ADC $zz',     '65 zz',    2, 3,  'Add with carry - Zero page', 'When (T) = 0, (A) <- (A) + (M) - (C). When (T) = 1, (M(X)) <- (M(X)) + (M) + (C)' ],
		'75' : [ 'ADC $zz,X',   '75 zz',    2, 4,  'Add with carry - Zero page X', 'When (T) = 0, (A) <- (A) + (M) - (C). When (T) = 1, (M(X)) <- (M(X)) + (M) + (C)' ],
		'6d' : [ 'ADC $hhll',   '6d ll hh', 3, 4,  'Add with carry - Absolute', 'When (T) = 0, (A) <- (A) + (M) - (C). When (T) = 1, (M(X)) <- (M(X)) + (M) + (C)' ],
		'7d' : [ 'ADC $hhll,X', '7d ll hh', 3, 5,  'Add with carry - Absolute X', 'When (T) = 0, (A) <- (A) + (M) - (C). When (T) = 1, (M(X)) <- (M(X)) + (M) + (C)' ],
		'79' : [ 'ADC $hhll,Y', '79 ll hh', 3, 5,  'Add with carry - Absolute Y', 'When (T) = 0, (A) <- (A) + (M) - (C). When (T) = 1, (M(X)) <- (M(X)) + (M) + (C)' ],
		'61' : [ 'ADC ($zz,X)', '61 zz',    2, 6,  'Add with carry - (Indirect X)', 'When (T) = 0, (A) <- (A) + (M) - (C). When (T) = 1, (M(X)) <- (M(X)) + (M) + (C)' ],
		'71' : [ 'ADC ($zz),Y', '71 zz',    2, 6,  'Add with carry - (Indirect Y)', 'When (T) = 0, (A) <- (A) + (M) - (C). When (T) = 1, (M(X)) <- (M(X)) + (M) + (C)' ],

		# AND
		'29' : [ 'AND #$nn',    '29 nn',    2, 2, 'Logical AND - Immediate', 'When (T) = 0, (A) <- (A) AND (M). When (T) = 1, (M(X)) <- (M(X)) AND (M)' ],
		'25' : [ 'AND $zz',     '25 zz',    2, 3, 'Logical AND - Zero page', 'When (T) = 0, (A) <- (A) AND (M). When (T) = 1, (M(X)) <- (M(X)) AND (M)' ],
		'35' : [ 'AND $zz,X',   '35 zz',    2, 4, 'Logical AND - Zero page X', 'When (T) = 0, (A) <- (A) AND (M). When (T) = 1, (M(X)) <- (M(X)) AND (M)' ],
		'2d' : [ 'AND $hhll',   '2d ll hh', 3, 4, 'Logical AND - Absolute', 'When (T) = 0, (A) <- (A) AND (M). When (T) = 1, (M(X)) <- (M(X)) AND (M)' ],
		'3d' : [ 'AND $hhll,X', '3d ll hh', 3, 5, 'Logical AND - Absolute X', 'When (T) = 0, (A) <- (A) AND (M). When (T) = 1, (M(X)) <- (M(X)) AND (M)' ],
		'39' : [ 'AND $hhll,Y', '39 ll hh', 3, 5, 'Logical AND - Absolute Y', 'When (T) = 0, (A) <- (A) AND (M). When (T) = 1, (M(X)) <- (M(X)) AND (M)' ],
		'21' : [ 'AND ($zz,X)', '21 zz',    2, 6, 'Logical AND - (Indirect X)', 'When (T) = 0, (A) <- (A) AND (M). When (T) = 1, (M(X)) <- (M(X)) AND (M)' ],
		'31' : [ 'AND ($zz),Y', '31 zz',    2, 6, 'Logical AND - (Indirect Y)', 'When (T) = 0, (A) <- (A) AND (M). When (T) = 1, (M(X)) <- (M(X)) AND (M)' ],

		# ASL
		'0a' : [ 'ASL A',       '0a',       1, 2, 'Arithmetic shift left - Accumulator', 'C <- [b7|  |  |  |  |  |  |b0] <- 0' ],
		'06' : [ 'ASL $zz',     '06 zz',    2, 5, 'Arithmetic shift left - Zero page', 'C <- [b7|  |  |  |  |  |  |b0] <- 0' ],
		'16' : [ 'ASL $zz,X',   '16 zz',    2, 6, 'Arithmetic shift left - Zero page X', 'C <- [b7|  |  |  |  |  |  |b0] <- 0' ],
		'0e' : [ 'ASL $hhll',   '0e ll hh', 3, 6, 'Arithmetic shift left - Absolute', 'C <- [b7|  |  |  |  |  |  |b0] <- 0' ],
		'1e' : [ 'ASL $hhll,X', '1e ll hh', 3, 7, 'Arithmetic shift left - Absolute X', 'C <- [b7|  |  |  |  |  |  |b0] <- 0' ],

		# BBC
		# XXX
		# 'Branch on bit clear', 'When (Mi) or (Ai) = 0, (PC) <- (PC) + n + REL. When (Mi) or (Ai) = 1, (PC) <- (PC) + n' ],
		# n: if addressing mode = zero page bit relative, n = 3. if addressing mode is accumulator bit relative, n = 2
		# XXX poner directamente 2 o 3 en cada caso de addressing.

		# BBS
		# 'Branch on bit set', 'When (Mi) or (Ai) = 1, (PC) <- (PC) + n + REL. When (Mi) or (Ai) = 0, (PC) <- (PC) + n' ],
		# idem arriba
		# XXX

		# BCC
		# XXX wtf... rr=$hhll-(*+2)
		# fijarse el manual
		'90' : [ 'BCC $hhll',   '90 rr',    2, 2, 'Branch on carry clear', 'When (C) = 0, (PC) <- (PC) + 2 + REL. When (C) = 1, (PC) <- (PC) + 2' ],

		# BCS
		'b0' : [ 'BCS $hhll',   'b0 rr',    2, 2, 'Branch on carry set', 'When (C) = 1, (PC) <- (PC) + 2 + REL. When (C) = 0, (PC) <- (PC) + 2' ],

		# BEQ
		'f0' : [ 'BEQ $hhll',   'f0 rr',    2, 2, 'Branch on equal', 'When (Z) = 1, (PC) <- (PC) + 2 + REL. When (Z) = 0, (PC) <- (PC) + 2' ],

		# BIT
		'24' : [ 'BIT $zz',     '24 zz',    2, 3, 'Test bit in memory with accumulator - Zero page', '(A) AND (M)' ],
		'2c' : [ 'BIT $hhll',   '2c ll hh', 3, 4, 'Test bit in memory with accumulator - Absolute', '(A) AND (M)' ],

		# BMI
		'30' : [ 'BMI $hhll',   '30 rr',    2, 2, 'Branch on result minus', 'When (N) = 1, (PC) <- (PC) + 2 + REL. When (N) = 0, (PC) <- (PC) + 2' ],

		# BNE
		'd0' : [ 'BNE $hhll',   'd0 rr',    2, 2, 'Branch on not equal', 'When (Z) = 0, (PC) <- (PC) + 2 + REL. When (Z) = 1, (PC) <- (PC) + 2' ],

		# BPL
		'10' : [ 'BPL $hhll',   '10 rr',    2, 2, 'Branch on result plus', 'When (N) = 0, (PC) <- (PC) + 2 + REL. When (N) = 1, (PC) <- (PC) + 2'],

		# BRA
		'80' : [ 'BRA $hhll',   '80 rr',    2, 4, 'Branch always', '(PC) <- (PC) + 2 + REL' ],

		# BRK
		'00' : [ 'BRK',         '00',       1, 7, 'Force break', '(B) <- 1, (PC) <- (PC) + 2, (M(S)) <- (PCh), (S) <- (S) - 1,(M(S)) <- (PCl), (S) <- (S) - 1,(M(S)) <- (PS), (S) <- (S) - 1, (I) <- 1, (PC) <- BADRS' ],

		# BVC
		'50' : [ 'BVC $hhll',   '50 rr',    2, 2, 'Branch on overflow clear', 'When (V) = 0, (PC) <- (PC) + 2 + REL. When (V) = 1, (PC) <- (PC) + 2' ],

		# BVS
		'70' : [ 'BVS $hhll',   '70 rr',    2, 2, 'Branch on overflow set', 'When (V) = 1, (PC) <- (PC) + 2 + REL. When (V) = 0, (PC) <- (PC) + 2' ],

		# CLB
		# XXX

		# CLC
		'18' : [ 'CLC',         '18',       1, 2,  'Clear carry flag', '(C) <- 0' ],

		# CLD
		'd8' : [ 'CLD',         'd8',       1, 2,  'Clear decimal mode', '(D) <- 0' ],

		# CLI
		'58' : [ 'CLI',         '58',       1, 2,  'Clear interrupt disable status', '(I) <- 0' ],

		# CLT
		'12' : [ 'CLT',         '12',       1, 2,  'Clear transfer flag', '(T) <- 0' ],

		# CLV
		'b8' : [ 'CLV',         'b8',       1, 2,  'Clear overflow flag', '(V) <- 0' ],

		# CMP
		'c9' : [ 'CMP #$nn',    'c9 nn',    2, 2,  'Compare - Immediate', 'When (T) = 0, (A) - (M). When (T) = 1, (M(X)) - (M)' ],
		'c5' : [ 'CMP $zz',     'c5 zz',    2, 3,  'Compare - Zero page', 'When (T) = 0, (A) - (M). When (T) = 1, (M(X)) - (M)' ],
		'd5' : [ 'CMP $zz,X',   'd5 zz',    2, 4,  'Compare - Zero page X', 'When (T) = 0, (A) - (M). When (T) = 1, (M(X)) - (M)' ],
		'cd' : [ 'CMP $hhll',   'cd ll hh', 3, 4,  'Compare - Absolute', 'When (T) = 0, (A) - (M). When (T) = 1, (M(X)) - (M)' ],
		'dd' : [ 'CMP $hhll,X', 'dd ll hh', 3, 5,  'Compare - Absolute X', 'When (T) = 0, (A) - (M). When (T) = 1, (M(X)) - (M)' ],
		'd9' : [ 'CMP $hhll,Y', 'd9 ll hh', 3, 5,  'Compare - Absolute Y', 'When (T) = 0, (A) - (M). When (T) = 1, (M(X)) - (M)' ],
		'c1' : [ 'CMP ($zz,X)', 'c1 zz',    2, 6,  'Compare - (Indirect X)', 'When (T) = 0, (A) - (M). When (T) = 1, (M(X)) - (M)' ],
		'd1' : [ 'CMP ($zz),Y', 'd1 zz',    2, 6,  'Compare - (Indirect Y)', 'When (T) = 0, (A) - (M). When (T) = 1, (M(X)) - (M)' ],

		# COM
		'44' : [ 'COM $zz',     '44 zz',    2, 5,  'Complement', '(M) <- (M~)' ],

		# CPX
		'e0' : [ 'CPX #$nn',    'e0 nn',    2, 2,  'Compare memory and index register X - Immediate', '(X) - (M)' ],
		'e4' : [ 'CPX $zz',     'e4 zz',    2, 3,  'Compare memory and index register X - Zero page', '(X) - (M)' ],
		'ec' : [ 'CPX $hhll',   'ec ll hh', 3, 4,  'Compare memory and index register X - Absolute', '(X) - (M)' ],

		# CPY
		'c0' : [ 'CPY #$nn',    'c0 nn',    2, 2,  'Compare memory and index register Y - Immediate', '(Y) - (M)' ],
		'c4' : [ 'CPY $zz',     'c4 zz',    2, 3,  'Compare memory and index register Y - Zero page', '(Y) - (M)' ],
		'cc' : [ 'CPY $hhll',   'cc ll hh', 3, 4,  'Compare memory and index register Y - Absolute', '(Y) - (M)' ],

		# DEC
		'1a' : [ 'DEC A',       '1a',       1, 2,  'Decrement by one - Accumulator', '(A) <- (A) - 1, or (M) <- (M) - 1' ],
		'c6' : [ 'DEC $zz',     'c6 zz',    2, 5,  'Decrement by one - Zero page', '(A) <- (A) - 1, or (M) <- (M) - 1' ],
		'd6' : [ 'DEC $zz,X',   'd6 zz',    2, 6,  'Decrement by one - Zero page X', '(A) <- (A) - 1, or (M) <- (M) - 1' ],
		'ce' : [ 'DEC $hhll',   'ce ll hh', 3, 6,  'Decrement by one - Absolute', '(A) <- (A) - 1, or (M) <- (M) - 1' ],
		'de' : [ 'DEC $hhll,X', 'de ll hh', 3, 7,  'Decrement by one - Absolute X', '(A) <- (A) - 1, or (M) <- (M) - 1' ],

		# DEX
		'ca' : [ 'DEX',         'ca',       1, 2,  'Decrement index register X by one', '(X) <- (X) - 1' ],

		# DEY
		'88' : [ 'DEY',         '88',       1, 2,  'Decrement index register Y by one', '(Y) <- (Y) - 1'],

		# DIV
		'e2' : [ 'DIV $zz,X',   'e2 zz',    2, 16, 'Divide memory by accumulator', '(A) <- (M(zz+(x)+1),M(zz+(X)) / (A) ; M(S) <- one\'s complemente of Reminder ; (S) <- (S) - 1' ],

		# EOR
		'49' : [ 'EOR #$nn',    '49 nn',    2, 2, 'Exclusive OR memory with accumulator - Immediate', 'When (T) = 0, (A) <- (A) XOR (M). When (T) = 1, (M(X)) <- (M(X)) XOR (M)' ],
		'45' : [ 'EOR $zz',     '45 zz',    2, 3, 'Exclusive OR memory with accumulator - Zero page', 'When (T) = 0, (A) <- (A) XOR (M). When (T) = 1, (M(X)) <- (M(X)) XOR (M)' ],
		'55' : [ 'EOR $zz,X',   '55 zz',    2, 4, 'Exclusive OR memory with accumulator - Zero page X', 'When (T) = 0, (A) <- (A) XOR (M). When (T) = 1, (M(X)) <- (M(X)) XOR (M)' ],
		'4d' : [ 'EOR $hhll',   '4d ll hh', 3, 4, 'Exclusive OR memory with accumulator - Absolute', 'When (T) = 0, (A) <- (A) XOR (M). When (T) = 1, (M(X)) <- (M(X)) XOR (M)' ],
		'5d' : [ 'EOR $hhll,X', '5d ll hh', 3, 5, 'Exclusive OR memory with accumulator - Absolute X', 'When (T) = 0, (A) <- (A) XOR (M). When (T) = 1, (M(X)) <- (M(X)) XOR (M)' ],
		'59' : [ 'EOR $hhll,Y', '59 ll hh', 3, 5, 'Exclusive OR memory with accumulator - Absolute Y', 'When (T) = 0, (A) <- (A) XOR (M). When (T) = 1, (M(X)) <- (M(X)) XOR (M)' ],
		'41' : [ 'EOR ($zz,X)', '41 zz',    2, 6, 'Exclusive OR memory with accumulator - (Indirect X)', 'When (T) = 0, (A) <- (A) XOR (M). When (T) = 1, (M(X)) <- (M(X)) XOR (M)' ],
		'51' : [ 'EOR ($zz),Y', '51 zz',    2, 6, 'Exclusive OR memory with accumulator - (Indirect Y)', 'When (T) = 0, (A) <- (A) XOR (M). When (T) = 1, (M(X)) <- (M(X)) XOR (M)' ],

		# INC
		'3a' : [ 'INC A',       '3a',       1, 2,  'Increment by one - Accumulator', '(A) <- (A) + 1, or (M) <- (M) + 1' ],
		'e6' : [ 'INC $zz',     'e6 zz',    2, 5,  'Increment by one - Zero page', '(A) <- (A) + 1, or (M) <- (M) + 1' ],
		'f6' : [ 'INC $zz,X',   'f6 zz',    2, 6,  'Increment by one - Zero page X', '(A) <- (A) + 1, or (M) <- (M) + 1' ],
		'ee' : [ 'INC $hhll',   'ee ll hh', 3, 6,  'Increment by one - Absolute', '(A) <- (A) + 1, or (M) <- (M) + 1' ],
		'fe' : [ 'INC $hhll,X', 'fe ll hh', 3, 7,  'Increment by one - Absolute X', '(A) <- (A) + 1, or (M) <- (M) + 1' ],

		# INX
		'e8' : [ 'INX',         'e8',       1, 2,  'Increment index register X by one', '(X) <- (X) + 1'],

		# INY
		'c8' : [ 'INY',         'c8',       1, 2,  'Increment index register Y by one', '(Y) <- (Y) + 1'],


		# JMP
		'4c' : [ 'JMP $hhll',   '4c ll hh', 3, 3,  'Jump - Absolute', '(PC) <- hhll' ],
		'6c' : [ 'JMP ($hhll)', '6c ll hh', 3, 5,  'Jump - Indirect absolute', '(PCl) <- (hhll), (PCh) <- (hhll+1)' ],
		'b2' : [ 'JMP ($zz)',   'b2 zz',    2, 4,  'Jump - Zero page indirect', '(PCl) <- (zz), (PCh) <- (zz+1)' ],

		# JSR
		'20' : [ 'JSR $hhll',   '20 ll hh', 3, 6,  'Jump to subroutine - Absolute', '(M(S)) <- (PCh), (S) <- (S) - 1, (M(S)) <- (PCl), (S) <- (S) - 1, (PC) <- hhll' ],
		'22' : [ 'JSR \$hhll',  '22 ll',    2, 5,  'Jump to subroutine - Special page', '(M(S)) <- (PCh), (S) <- (S) - 1, (M(S)) <- (PCl), (S) <- (S) - 1, (PCl) <- ll, (PCh) <- 0xFF' ],
		'02' : [ 'JSR ($zz)',   '02 zz',    2, 7,  'Jump to subroutine - Zero page indirect', '(M(S)) <- (PCh), (S) <- (S) - 1, (M(S)) <- (PCl), (S) <- (S) - 1, (PCl) <- (zz), (PCh) <- (zz + 1)' ],

		# LDA
		'a9' : [ 'LDA #$nn',    'a9 nn',    2, 2, 'Load accumulator with memory - Immediate', 'When (T) = 0, (A) <- (M). When (T) = 1, (M(X)) <- (M)' ],
		'a5' : [ 'LDA $zz',     'a5 zz',    2, 3, 'Load accumulator with memory - Zero page', 'When (T) = 0, (A) <- (M). When (T) = 1, (M(X)) <- (M)' ],
		'b5' : [ 'LDA $zz,X',   'b5 zz',    2, 4, 'Load accumulator with memory - Zero page X', 'When (T) = 0, (A) <- (M). When (T) = 1, (M(X)) <- (M)' ],
		'ad' : [ 'LDA $hhll',   'ad ll hh', 3, 4, 'Load accumulator with memory - Absolute', 'When (T) = 0, (A) <- (M). When (T) = 1, (M(X)) <- (M)' ],
		'bd' : [ 'LDA $hhll,X', 'bd ll hh', 3, 5, 'Load accumulator with memory - Absolute X', 'When (T) = 0, (A) <- (M). When (T) = 1, (M(X)) <- (M)' ],
		'b9' : [ 'LDA $hhll,Y', 'b9 ll hh', 3, 5, 'Load accumulator with memory - Absolute Y', 'When (T) = 0, (A) <- (M). When (T) = 1, (M(X)) <- (M)' ],
		'a1' : [ 'LDA ($zz,X)', 'a1 zz',    2, 6, 'Load accumulator with memory - (Indirect X)', 'When (T) = 0, (A) <- (M). When (T) = 1, (M(X)) <- (M)' ],
		'b1' : [ 'LDA ($zz),Y', 'b1 zz',    2, 6, 'Load accumulator with memory - (Indirect Y)', 'When (T) = 0, (A) <- (M). When (T) = 1, (M(X)) <- (M)' ],

		# LDM
		'3c' : [ 'LDM #$nn,$zz', '3c nn zz', 3, 4, 'Load immediate data to memory', '(M) <- nn' ],

		# LDX
		'a2' : [ 'LDX #$nn',    'a2 nn',     2, 2, 'Load index register X from memory - Immediate', '(X) <- (M)' ],
		'a6' : [ 'LDX $zz',     'a6 zz',     2, 3, 'Load index register X from memory - Zero page', '(X) <- (M)' ],
		'b6' : [ 'LDX $zz,Y',   'b6 zz',     2, 4, 'Load index register X from memory - Zero page Y', '(X) <- (M)' ],
		'ae' : [ 'LDX $hhll',   'ae ll hh',  3, 4, 'Load index register X from memory - Absolute', '(X) <- (M)' ],
		'be' : [ 'LDX $hhll,Y', 'be ll hh',  3, 5, 'Load index register X from memory - Absolute Y', '(X) <- (M)' ],

		# LDY
		'a0' : [ 'LDY #$nn',    'a0 nn',     2, 2, 'Load index register Y from memory - Immediate', '(Y) <- (M)' ],
		'a4' : [ 'LDY $zz',     'a4 zz',     2, 3, 'Load index register Y from memory - Zero page', '(Y) <- (M)' ],
		'b4' : [ 'LDY $zz,X',   'b4 zz',     2, 4, 'Load index register Y from memory - Zero page X', '(Y) <- (M)' ],
		'ac' : [ 'LDY $hhll',   'ac ll hh',  3, 4, 'Load index register Y from memory - Absolute', '(Y) <- (M)' ],
		'bc' : [ 'LDY $hhll,X', 'bc ll hh',  3, 5, 'Load index register Y from memory - Absolute X', '(Y) <- (M)' ],
		
		# LSR
		'4a' : [ 'LSR A',       '4a',       1, 2,  'Logical shift right - Accumulator', '0 -> [b7|  |  |  |  |  |  |b0] -> C' ],
		'46' : [ 'LSR $zz',     '46 zz',    2, 5,  'Logical shift right - Zero page', '0 -> [b7|  |  |  |  |  |  |b0] -> C' ],
		'56' : [ 'LSR $zz,X',   '56 zz',    2, 6,  'Logical shift right - Zero page X', '0 -> [b7|  |  |  |  |  |  |b0] -> C' ],
		'4e' : [ 'LSR $hhll',   '4e ll hh', 3, 6,  'Logical shift right - Absolute', '0 -> [b7|  |  |  |  |  |  |b0] -> C' ],
		'5e' : [ 'LSR $hhll,X', '5e ll hh', 3, 7,  'Logical shift right - Absolute X', '0 -> [b7|  |  |  |  |  |  |b0] -> C' ],

		# MUL
		'62' : [ 'MUL $zz,X',   '62 zz',    2, 15, 'Multiply accumulator and memory', 'M(S) . (A) <- (A) x M(zz+(X)), (S) <- (S) - 1' ],

		# NOP
		'ea' : [ 'NOP',         'ea',       1, 2,  'No operation', '(PC) <- (PC) + 1' ],

		# ORA
		'09' : [ 'ORA #$nn',    '09 nn',    2, 2, 'OR memory with accumulator - Immediate', 'When (T) = 0, (A) <- (A) OR (M). When (T) = 1, (M(X)) <- (M(X)) OR (M)' ],
		'05' : [ 'ORA $zz',     '05 zz',    2, 3, 'OR memory with accumulator - Zero page', 'When (T) = 0, (A) <- (A) OR (M). When (T) = 1, (M(X)) <- (M(X)) OR (M)' ],
		'15' : [ 'ORA $zz,X',   '15 zz',    2, 4, 'OR memory with accumulator - Zero page X', 'When (T) = 0, (A) <- (A) OR (M). When (T) = 1, (M(X)) <- (M(X)) OR (M)' ],
		'0d' : [ 'ORA $hhll',   '0d ll hh', 3, 4, 'OR memory with accumulator - Absolute', 'When (T) = 0, (A) <- (A) OR (M). When (T) = 1, (M(X)) <- (M(X)) OR (M)' ],
		'1d' : [ 'ORA $hhll,X', '1d ll hh', 3, 5, 'OR memory with accumulator - Absolute X', 'When (T) = 0, (A) <- (A) OR (M). When (T) = 1, (M(X)) <- (M(X)) OR (M)' ],
		'19' : [ 'ORA $hhll,Y', '19 ll hh', 3, 5, 'OR memory with accumulator - Absolute Y', 'When (T) = 0, (A) <- (A) OR (M). When (T) = 1, (M(X)) <- (M(X)) OR (M)' ],
		'01' : [ 'ORA ($zz,X)', '01 zz',    2, 6, 'OR memory with accumulator - (Indirect X)', 'When (T) = 0, (A) <- (A) OR (M). When (T) = 1, (M(X)) <- (M(X)) OR (M)' ],
		'11' : [ 'ORA ($zz),Y', '11 zz',    2, 6, 'OR memory with accumulator - (Indirect Y)', 'When (T) = 0, (A) <- (A) OR (M). When (T) = 1, (M(X)) <- (M(X)) OR (M)' ],

		# PHA
		'48' : [ 'PHA',         '48',       1, 3,  'Push accumulator on stack', '(M(S)) <- (A), (S) <- (S) - 1' ],

		# PHP
		'08' : [ 'PHP',         '08',       1, 3,  'Push processor status on stack', '(M(S)) <- (PS), (S) <- (S) - 1' ],

		# PLA
		'68' : [ 'PLA',         '68',       1, 4,  'Pull accumulator from stack', '(S) <- (S) + 1, (A) <- (M(S))' ],

		# PLP
		'28' : [ 'PLP',         '28',       1, 4,  'Pull processor status from stack', '(S) <- (S) + 1, (PS) <- (M(S))' ],

		# ROL
		'2a' : [ 'ROL A',       '2a',       1, 2,  'Rotate one bit left - Accumulator', ')<- [b7|  |  |  |  |  |  |b0] <- C <-(' ],
		'26' : [ 'ROL $zz',     '26 zz',    2, 5,  'Rotate one bit left - Zero page', ')<- [b7|  |  |  |  |  |  |b0] <- C <-(' ],
		'36' : [ 'ROL $zz,X',   '36 zz',    2, 6,  'Rotate one bit left - Zero page X', ')<- [b7|  |  |  |  |  |  |b0] <- C <-(' ],
		'2e' : [ 'ROL $hhll',   '2e ll hh', 3, 6,  'Rotate one bit left - Absolute', ')<- [b7|  |  |  |  |  |  |b0] <- C <-(' ],
		'3e' : [ 'ROL $hhll,X', '3e ll hh', 3, 7,  'Rotate one bit left - Absolute X', ')<- [b7|  |  |  |  |  |  |b0] <- C <-(' ],

		# ROR
		'6a' : [ 'ROR A',       '6a',       1, 2,  'Rotate one bit right - Accumulator', ')-> C -> [b7|  |  |  |  |  |  |b0] ->(' ],
		'66' : [ 'ROR $zz',     '66 zz',    2, 5,  'Rotate one bit right - Zero page', ')-> C -> [b7|  |  |  |  |  |  |b0] ->(' ],
		'76' : [ 'ROR $zz,X',   '76 zz',    2, 6,  'Rotate one bit right - Zero page X', ')-> C -> [b7|  |  |  |  |  |  |b0] ->(' ],
		'6e' : [ 'ROR $hhll',   '6e ll hh', 3, 6,  'Rotate one bit right - Absolute', ')-> C -> [b7|  |  |  |  |  |  |b0] ->(' ],
		'7e' : [ 'ROR $hhll,X', '7e ll hh', 3, 7,  'Rotate one bit right - Absolute X', ')-> C -> [b7|  |  |  |  |  |  |b0] ->(' ],

		# RRF
		'82' : [ 'RRF $zz',     '82 zz',    2, 8,  'Rotate right of four bits', '[b7  b4] <-> [b3  b0]' ],

		# RTI
		'40' : [ 'RTI',         '40',       1, 6,  'Return from interrupt', '(S) <- (S) + 1, (PS) <- (M(S)), (S) <- (S) + 1, (PCl) <- (M(S)), (S) <- (S) + 1, (PCh) <- (M(S))' ],

		# RTS
		'60' : [ 'RTS',         '60',       1, 6,  'Return from subroutine', '(PCl) <- (M(S)), (S) <- (S) + 1, (PCh) <- (M(S)), (PC) <- (PC) + 1' ],


		# SBC
		'e9' : [ 'SBC #$nn',    'e9 nn',    2, 2, 'Substract with carry - Immediate', 'When (T) = 0, (A) <- (A) - (M) - (C~). When (T) = 1, (M(X)) <- (M(X)) - (M) - (C~)' ],
		'e5' : [ 'SBC $zz',     'e5 zz',    2, 3, 'Substract with carry - Zero page', 'When (T) = 0, (A) <- (A) - (M) - (C~). When (T) = 1, (M(X)) <- (M(X)) - (M) - (C~)' ],
		'f5' : [ 'SBC $zz,X',   'f5 zz',    2, 4, 'Substract with carry - Zero page X', 'When (T) = 0, (A) <- (A) - (M) - (C~). When (T) = 1, (M(X)) <- (M(X)) - (M) - (C~)' ],
		'ed' : [ 'SBC $hhll',   'ed ll hh', 3, 4, 'Substract with carry - Absolute', 'When (T) = 0, (A) <- (A) - (M) - (C~). When (T) = 1, (M(X)) <- (M(X)) - (M) - (C~)' ],
		'fd' : [ 'SBC $hhll,X', 'fd ll hh', 3, 5, 'Substract with carry - Absolute X', 'When (T) = 0, (A) <- (A) - (M) - (C~). When (T) = 1, (M(X)) <- (M(X)) - (M) - (C~)' ],
		'f9' : [ 'SBC $hhll,Y', 'f9 ll hh', 3, 5, 'Substract with carry - Absolute Y', 'When (T) = 0, (A) <- (A) - (M) - (C~). When (T) = 1, (M(X)) <- (M(X)) - (M) - (C~)' ],
		'e1' : [ 'SBC ($zz,X)', 'e1 zz',    2, 6, 'Substract with carry - (Indirect X)', 'When (T) = 0, (A) <- (A) - (M) - (C~). When (T) = 1, (M(X)) <- (M(X)) - (M) - (C~)' ],
		'f1' : [ 'SBC ($zz),Y', 'f1 zz',    2, 6, 'Substract with carry - (Indirect Y)', 'When (T) = 0, (A) <- (A) - (M) - (C~). When (T) = 1, (M(X)) <- (M(X)) - (M) - (C~)' ],


		# SEB
		# XXX


		# SEC
		'38' : [ 'SEC',         '38',       1, 2, 'Set carry flag', '(C) <- 1' ],

		# SED
		'f8' : [ 'SED',         'f8',       1, 2, 'Set decimal mode', '(D) <- 1' ],

		# SEI
		'78' : [ 'SEI',         '78',       1, 2, 'Set interrupt disable flag', '(I) <- 1' ],

		# SET
		'32' : [ 'SET',         '32',       1, 2, 'Set transfer flag', '(T) <- 1' ],


		# STA
		'85' : [ 'STA $zz',     '85 zz',    2, 4, 'Store accumulator in memory - Zero page', '(M) <- (A)' ],
		'95' : [ 'STA $zz,X',   '95 zz',    2, 5, 'Store accumulator in memory - Zero page X', '(M) <- (A)' ],
		'8d' : [ 'STA $hhll',   '8d ll hh', 3, 5, 'Store accumulator in memory - Absolute', '(M) <- (A)' ],
		'9d' : [ 'STA $hhll,X', '9d ll hh', 3, 6, 'Store accumulator in memory - Absolute X', '(M) <- (A)' ],
		'99' : [ 'STA $hhll,Y', '99 ll hh', 3, 6, 'Store accumulator in memory - Absolute Y', '(M) <- (A)' ],
		'81' : [ 'STA ($zz,X)', '81 zz',    2, 7, 'Store accumulator in memory - (Indirect X)', '(M) <- (A)' ],
		'91' : [ 'STA ($zz),Y', '91 zz',    2, 7, 'Store accumulator in memory - (Indirect Y)', '(M) <- (A)' ],

		# STP
		'42' : [ 'STP',         '42',       1, 2, 'Stop', 'CPU <- Stand-by state (Oscillation stopped)' ],


		# STX
		'86' : [ 'STX $zz',     '86 zz',    2, 4, 'Store index register X in memory - Zero page', '(M) <- (X)' ],
		'96' : [ 'STX $zz,Y',   '96 zz',    2, 5, 'Store index register X in memory - Zero page Y', '(M) <- (X)' ],
		'8e' : [ 'STX $hhll',   '8e ll hh', 3, 5, 'Store index register X in memory - Absolute', '(M) <- (X)' ],

		# STY
		'84' : [ 'STY $zz',     '84 zz',    2, 4, 'Store index register Y in memory - Zero page', '(M) <- (Y)' ],
		'94' : [ 'STY $zz,X',   '84 zz',    2, 5, 'Store index register Y in memory - Zero page X', '(M) <- (Y)' ],
		'8c' : [ 'STY $hhll',   '8c ll hh', 3, 5, 'Store index register Y in memory - Absolute', '(M) <- (Y)' ],


		# TAX
		'aa' : [ 'TAX',         'aa',       1, 2, 'Transfer accumulator to index register X', '(X) <- (A)' ],

		# TAY
		'a8' : [ 'TAY',         'a8',       1, 2, 'Transfer accumulator to index register Y', '(Y) <- (A)' ],

		# TST
		'64' : [ 'TST $zz',     '64 zz',    2, 3, 'Test for negative or zero', '(M) = 0 ?' ],

		# TSX
		'ba' : [ 'TSX',         'ba',       1, 2, 'Transfer stack pointer to index register X', '(X) <- (S)' ],

		# TXA
		'8a' : [ 'TXA',         '8a',       1, 2, 'Transfer index register X to accumulator', '(A) <- (X)' ],

		# TXS
		'9a' : [ 'TXS',         '9a',       1, 2, 'Transfer index register X to stack pointer', '(S) <- (X)' ],

		# TYA
		'98' : [ 'TYA',         '98',       1, 2, 'Transfer index register Y to accumulator', '(A) <- (Y)' ],

		# WIT
		'c2' : [ 'WIT',         'c2',       1, 2, 'Wait', 'CPU <- Wait state' ],


	}


	with open(input_file, "rb") as f:

		b = f.read(1)
		mem = 0

		while b != "":

			h = b.encode('hex').zfill(2)

			if h in t:

				instruction = t[h][0]
				param = t[h][1]
				size = t[h][2]
				cycles = t[h][3]
				description = t[h][4]
				operation = t[h][5]

				opcodes = h
				inc = 1

				w = param.split()
				for x in range(1, size):
					e = f.read(1).encode('hex').zfill(2)
					opcodes = opcodes + " " + e
					inc = inc + 1
					instruction = re.sub(w[x],e,instruction,1)
					
				out = hex4(mem) + "  " + opcodes.ljust(10," ") + "  " + instruction.ljust(14, " ")

				pad = ''
				if description_f:
					out = out + "  ; " + description
					pad = "\n ".ljust(34," ")

				if operation_f:
					out = out + pad + " ; " + operation
					pad = "\n ".ljust(34," ")

				if cycles_f:
					out = out + pad + " ; " + str(cycles) + " cycles"

				print out

				mem = mem + inc

			else:

				print hex4(mem) + "  " + h.ljust(10," ") + "  <INVALID>"
				mem = mem + 1
				
			b = f.read(1)

def hex4(n):
	return '%04x' % (n,)

if __name__ == "__main__":
	main(sys.argv[1:])


