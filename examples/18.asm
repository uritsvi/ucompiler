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
LOCAL var_1:DWORD
LOCAL var_2:DWORD
LOCAL div_temp_1:DWORD
LOCAL div_temp_2:DWORD
LOCAL div_temp_3:DWORD
LOCAL div_temp_res:DWORD
LOCAL var_3[10]:DWORD
program:
mov edx,0
mov var_0,edx
mov edx,9
mov var_1,edx
mov edx,0
mov var_2,edx
jmp L0
L0:
mov edx,var_0
mov ecx,var_1
mov ebx,1
add ecx,ebx
mov ebx,ecx
cmp edx,ebx
jl L2
jmp L1
L2:
mov ebx,var_0
imul ebx,4
mov edx,1
mov var_3[ebx],edx
mov ebx,var_0
mov edx,1
add ebx,edx
mov edx,ebx
mov var_0,edx
jmp L0
L1:
mov ebx,2
mov var_0,ebx
jmp L3
L3:
mov ebx,var_0
mov edx,var_1
mov ecx,1
add edx,ecx
mov ecx,edx
cmp ebx,ecx
jl L5
jmp L4
L5:
printf("%d\n",var_0)
mov ecx,var_0
mov ebx,1
add ecx,ebx
mov ebx,ecx
mov var_0,ebx
jmp L3
L4:
invoke ExitProcess, 0
main endp
end start
