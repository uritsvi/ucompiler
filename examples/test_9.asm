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
LOCAL div_temp_res:DWORD
L0:
mov edx,5
mov ecx,3
push edx
push ecx
mov eax,edx
mov ecx,ecx
cdq
idiv ecx
mov div_temp_res,edx
pop ecx
pop edx
mov edx,div_temp_res
mov ecx,edx
mov var_0,ecx
mov edx,var_0
mov ecx,2
cmp edx,ecx
jne L2
jmp L1
L2:
invoke ExitProcess,1
jmp L1
L1:
printf("%d\n",var_0)
ret
f_0 endp
end start
