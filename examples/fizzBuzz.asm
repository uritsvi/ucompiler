.386
.model flat,stdcall
option casemap:none
includelib \masm32\lib\kernel32.lib
includelib C:\masm32\lib\masm32.lib
include C:\masm32\include\masm32rt.inc
.code
start:
call main
main proc
LOCAL var_0:DWORD
LOCAL div_temp_1:DWORD
LOCAL div_temp_2:DWORD
LOCAL div_temp_3:DWORD
LOCAL div_temp_res:DWORD
program:
mov edx,0
mov var_0,edx
jmp L0
L0:
mov edx,var_0
mov ecx,20
cmp edx,ecx
jl L2
jmp L1
L2:
mov ecx,var_0
mov edx,3
mov div_temp_1,eax
mov div_temp_2,ecx
mov div_temp_3,edx
mov eax,ecx
mov ecx,edx
cdq
idiv ecx
mov div_temp_res,edx
mov eax,div_temp_1
mov edx,div_temp_3
mov ecx,div_temp_res
mov edx,ecx
mov ecx,0
cmp edx,ecx
je L5
jmp L3
L5:
mov ecx,var_0
mov edx,5
mov div_temp_1,eax
mov div_temp_2,ecx
mov div_temp_3,edx
mov eax,ecx
mov ecx,edx
cdq
idiv ecx
mov div_temp_res,edx
mov eax,div_temp_1
mov edx,div_temp_3
mov ecx,div_temp_res
mov edx,ecx
mov ecx,0
cmp edx,ecx
je L4
jmp L3
L4:
printf("fizz buzz\n")
jmp L6
L3:
mov ecx,var_0
mov edx,3
mov div_temp_1,eax
mov div_temp_2,ecx
mov div_temp_3,edx
mov eax,ecx
mov ecx,edx
cdq
idiv ecx
mov div_temp_res,edx
mov eax,div_temp_1
mov edx,div_temp_3
mov ecx,div_temp_res
mov edx,ecx
mov ecx,0
cmp edx,ecx
je L8
jmp L7
L8:
printf("fizz\n")
jmp L9
L7:
mov ecx,var_0
mov edx,5
mov div_temp_1,eax
mov div_temp_2,ecx
mov div_temp_3,edx
mov eax,ecx
mov ecx,edx
cdq
idiv ecx
mov div_temp_res,edx
mov eax,div_temp_1
mov edx,div_temp_3
mov ecx,div_temp_res
mov edx,ecx
mov ecx,0
cmp edx,ecx
je L11
jmp L10
L11:
printf("buzz\n")
jmp L12
L10:
printf("%d\n",var_0)
jmp L12
L12:
jmp L9
L9:
jmp L6
L6:
mov ecx,var_0
mov edx,1
add ecx,edx
mov edx,ecx
mov var_0,edx
jmp L0
L1:
invoke ExitProcess, 0
main endp
end start
