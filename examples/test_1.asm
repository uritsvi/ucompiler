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
mov edx,7
mov var_1,edx
jmp L1
L1:
mov edx,var_1
mov ecx,5
cmp edx,ecx
jg L3
jmp L2
L3:
mov ecx,var_0
mov edx,1
add ecx,edx
mov edx,ecx
mov var_0,edx
mov ecx,var_1
mov edx,1
sub ecx,edx
mov edx,ecx
mov var_1,edx
jmp L1
L2:
mov ecx,var_0
mov edx,7
cmp ecx,edx
jne L5
jmp L6
L6:
mov edx,var_1
mov ecx,5
cmp edx,ecx
jne L5
jmp L4
L5:
invoke ExitProcess,1
jmp L4
L4:
printf("%d\n",var_0)
printf("%d\n",var_1)
ret
f_0 endp
end start
