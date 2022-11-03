.386
.model flat,stdcall
option casemap:none
includelib \masm32\lib\kernel32.lib
includelib C:\masm32\lib\masm32.lib
include C:\masm32\include\masm32rt.inc
.code
start:
call f_0
invoke ExitProcess,0
f_0 proc 
LOCAL var_0:DWORD
LOCAL var_1:DWORD
LOCAL div_temp_res:DWORD
L0:
mov edx,5
mov var_0,edx
mov edx,5
mov var_1,edx
mov edx,var_1
mov ecx,1
cmp edx,ecx
jl L2
jmp L1
L2:
invoke ExitProcess,1
mov ecx,6
mov var_0,ecx
jmp L3
L1:
mov ecx,7
mov var_0,ecx
jmp L3
L3:
printf("%d\n",var_0)
ret
f_0 endp
end start
