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
mov edx,5
mov ecx,3
mov div_temp_1,eax
mov div_temp_2,ecx
mov div_temp_3,edx
mov eax,edx
mov ecx,ecx
cdq
idiv ecx
mov div_temp_res,edx
mov eax,div_temp_1
mov edx,div_temp_3
mov edx,div_temp_res
mov ecx,edx
mov var_0,ecx
mov edx,var_0
mov ecx,2
cmp edx,ecx
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
