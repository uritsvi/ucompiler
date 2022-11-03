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
LOCAL var_0:BYTE
LOCAL div_temp_res:DWORD
L0:
xor edx,edx
mov dl,97
mov var_0,dl
jmp L1
L1:
xor edx,edx
mov dl,var_0
xor ecx,ecx
mov cl,122
mov ebx,1
add ecx,ebx
mov ebx,ecx
cmp edx,ebx
jl L3
jmp L2
L3:
printf("%c\n",var_0)
xor ebx,ebx
mov bl,var_0
mov edx,1
add ebx,edx
mov edx,ebx
mov var_0,dl
jmp L1
L2:
ret
f_0 endp
end start
