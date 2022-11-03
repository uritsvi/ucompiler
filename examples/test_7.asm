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
mov edx,6
mov var_1,edx
mov edx,var_0
mov ecx,4
cmp edx,ecx
jg L3
jmp L1
L3:
mov ecx,var_0
mov edx,5
cmp ecx,edx
jl L2
jmp L4
L4:
mov edx,var_1
mov ecx,6
cmp edx,ecx
je L2
jmp L1
L2:
printf("hello\n")
jmp L5
L1:
invoke ExitProcess,1
jmp L5
L5:
ret
f_0 endp
end start
