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
LOCAL var_1:DWORD
LOCAL var_2:DWORD
LOCAL div_temp_res:DWORD
LOCAL var_0[4]:DWORD
L0:
mov edx,0
imul edx,4
mov ecx,2
mov var_0[edx],ecx
mov edx,1
imul edx,4
mov ecx,4
mov var_0[edx],ecx
mov edx,2
imul edx,4
mov ecx,6
mov var_0[edx],ecx
mov edx,3
imul edx,4
mov ecx,8
mov var_0[edx],ecx
mov edx,0
mov var_1,edx
mov edx,0
mov var_2,edx
jmp L1
L1:
mov edx,var_2
mov ecx,4
cmp edx,ecx
jl L3
jmp L2
L3:
mov ecx,var_2
imul ecx,4
mov edx,var_1
mov ebx,var_0[ecx]
add edx,ebx
mov ebx,edx
mov var_1,ebx
mov edx,var_2
mov ebx,1
add edx,ebx
mov ebx,edx
mov var_2,ebx
jmp L1
L2:
mov edx,var_1
mov ebx,4
push edx
push ebx
mov eax,edx
mov ecx,ebx
cdq
idiv ecx
mov div_temp_res,eax
pop ebx
pop edx
mov edx,div_temp_res
mov ebx,edx
mov var_1,ebx
printf("%d\n",var_1)
ret
f_0 endp
end start
