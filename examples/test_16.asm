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
LOCAL var_0[100]:DWORD
L0:
mov edx,0
mov var_1,edx
mov edx,0
mov var_2,edx
jmp L1
L1:
mov edx,var_1
mov ecx,100
cmp edx,ecx
jl L3
jmp L2
L3:
mov ecx,var_1
imul ecx,4
mov edx,var_1
mov var_0[ecx],edx
mov ecx,var_1
mov edx,1
add ecx,edx
mov edx,ecx
mov var_1,edx
jmp L1
L2:
mov ecx,0
mov var_1,ecx
jmp L4
L4:
mov ecx,var_1
mov edx,100
cmp ecx,edx
jl L6
jmp L5
L6:
mov edx,var_1
imul edx,4
mov ecx,var_2
mov ebx,var_0[edx]
add ecx,ebx
mov ebx,ecx
mov var_2,ebx
mov ecx,var_1
mov ebx,1
add ecx,ebx
mov ebx,ecx
mov var_1,ebx
jmp L4
L5:
mov ecx,var_2
mov ebx,100
push ecx
push ebx
mov eax,ecx
mov ecx,ebx
cdq
idiv ecx
mov div_temp_res,eax
pop ebx
pop ecx
mov ecx,div_temp_res
mov ebx,ecx
mov var_2,ebx
printf("%d\n",var_2)
ret
f_0 endp
end start
