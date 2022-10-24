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
LOCAL var_1:DWORD
LOCAL var_2:DWORD
LOCAL div_temp_1:DWORD
LOCAL div_temp_2:DWORD
LOCAL div_temp_3:DWORD
LOCAL div_temp_res:DWORD
LOCAL var_0[100]:DWORD
program:
mov edx,0
mov var_1,edx
mov edx,0
mov var_2,edx
jmp L0
L0:
mov edx,var_1
mov ecx,100
cmp edx,ecx
jl L2
jmp L1
L2:
mov ecx,var_1
imul ecx,4
mov edx,var_1
mov var_0[ecx],edx
mov ecx,var_1
mov edx,1
add ecx,edx
mov edx,ecx
mov var_1,edx
jmp L0
L1:
mov ecx,0
mov var_1,ecx
jmp L3
L3:
mov ecx,var_1
mov edx,100
cmp ecx,edx
jl L5
jmp L4
L5:
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
jmp L3
L4:
mov ecx,var_2
mov ebx,100
mov div_temp_1,eax
mov div_temp_2,ecx
mov div_temp_3,edx
mov eax,ecx
mov ecx,ebx
cdq
idiv ebx
mov div_temp_res,eax
mov eax,div_temp_1
mov edx,div_temp_3
mov ecx,div_temp_res
mov ebx,ecx
mov var_2,ebx
printf("%d\n",var_2)
invoke ExitProcess, 0
main endp
end start
