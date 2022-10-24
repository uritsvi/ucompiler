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
LOCAL var_1:DWORD
LOCAL div_temp_1:DWORD
LOCAL div_temp_2:DWORD
LOCAL div_temp_3:DWORD
LOCAL div_temp_res:DWORD
program:
mov edx,5
mov var_0,edx
mov edx,6
mov var_1,edx
mov edx,var_0
mov ecx,4
cmp edx,ecx
jg L2
jmp L0
L2:
mov ecx,var_0
mov edx,5
cmp ecx,edx
jl L1
jmp L3
L3:
mov edx,var_1
mov ecx,6
cmp edx,ecx
je L1
jmp L0
L1:
printf("hello\n")
jmp L4
L0:
invoke ExitProcess,1
jmp L4
L4:
invoke ExitProcess, 0
main endp
end start
