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
mov edx,5
mov var_1,edx
mov edx,var_1
mov ecx,1
cmp edx,ecx
jl L1
jmp L0
L1:
invoke ExitProcess,1
mov ecx,6
mov var_0,ecx
jmp L2
L0:
mov ecx,7
mov var_0,ecx
jmp L2
L2:
printf("%d\n",var_0)
invoke ExitProcess, 0
main endp
end start