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
mov edx,6
mov ecx,7
add edx,ecx
mov ecx,5
mov ebx,edx
imul ecx,ebx
mov ebx,ecx
mov var_0,ebx
mov ecx,var_0
mov ebx,65
cmp ecx,ebx
jne L1
jmp L0
L1:
invoke ExitProcess,1
jmp L0
L0:
printf("%d\n",var_0)
invoke ExitProcess, 0
main endp
end start
