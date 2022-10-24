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
LOCAL var_2:DWORD
LOCAL var_3:DWORD
LOCAL div_temp_1:DWORD
LOCAL div_temp_2:DWORD
LOCAL div_temp_3:DWORD
LOCAL div_temp_res:DWORD
LOCAL var_0[20]:DWORD
LOCAL var_1[20]:DWORD
program:
mov edx,10
imul edx,4
mov ecx,19
mov var_1[edx],ecx
mov edx,10
imul edx,4
mov ecx,10
imul ecx,4
mov ebx,var_1[edx]
mov var_0[ecx],ebx
mov ecx,10
imul ecx,4
mov edx,var_0[ecx]
mov var_2,edx
mov ecx,2
mov var_3,ecx
mov ecx,var_3
mov edx,var_2
imul ecx,edx
mov edx,ecx
mov ecx,38
cmp edx,ecx
jne L1
jmp L0
L1:
invoke ExitProcess,1
jmp L0
L0:
mov ecx,var_3
mov edx,var_2
imul ecx,edx
printf("%d\n",ecx)
invoke ExitProcess, 0
main endp
end start
