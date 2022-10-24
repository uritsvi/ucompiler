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
LOCAL var_0:BYTE
LOCAL div_temp_1:DWORD
LOCAL div_temp_2:DWORD
LOCAL div_temp_3:DWORD
LOCAL div_temp_res:DWORD
program:
xor edx,edx
mov dl,97
mov var_0,dl
jmp L0
L0:
xor edx,edx
mov dl,var_0
xor ecx,ecx
mov cl,122
mov ebx,1
add ecx,ebx
xor ebx,ebx
mov bl,cl
cmp edx,ebx
jl L2
jmp L1
L2:
printf("%c\n",var_0)
xor ebx,ebx
mov bl,var_0
mov edx,1
add ebx,edx
xor edx,edx
mov dl,bl
mov var_0,dl
jmp L0
L1:
invoke ExitProcess, 0
main endp
end start
