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
LOCAL var_3:DWORD
LOCAL var_5:DWORD
LOCAL div_temp_1:DWORD
LOCAL div_temp_2:DWORD
LOCAL div_temp_3:DWORD
LOCAL div_temp_res:DWORD
LOCAL var_4[10]:DWORD
program:
mov edx,0
mov var_0,edx
mov edx,0
mov var_1,edx
mov edx,10
mov var_2,edx
mov edx,0
mov var_3,edx
mov edx,0
mov var_5,edx
jmp L0
L0:
mov edx,var_0
mov ecx,var_2
cmp edx,ecx
jl L2
jmp L1
L2:
mov ecx,var_2
mov edx,var_0
sub ecx,edx
mov edx,var_0
imul edx,4
mov ebx,ecx
mov var_4[edx],ebx
mov edx,var_0
mov ecx,1
add edx,ecx
mov ecx,edx
mov var_0,ecx
jmp L0
L1:
jmp L3
L3:
mov edx,var_1
mov ecx,var_2
mov ebx,1
sub ecx,ebx
mov ebx,ecx
cmp edx,ebx
jl L5
jmp L4
L5:
mov ebx,var_1
mov var_3,ebx
mov ebx,var_1
mov edx,1
add ebx,edx
mov edx,ebx
mov var_0,edx
jmp L6
L6:
mov ebx,var_1
mov edx,var_2
cmp ebx,edx
jl L8
jmp L7
L8:
mov edx,var_0
imul edx,4
mov ebx,var_4[edx]
mov edx,var_3
imul edx,4
mov ecx,var_4[edx]
cmp ebx,ecx
jl L10
jmp L9
L10:
mov ecx,var_0
mov var_3,ecx
printf("%d\n",var_3)
jmp L9
L9:
mov ecx,var_1
mov ebx,1
add ecx,ebx
mov ebx,ecx
mov var_1,ebx
jmp L6
L7:
mov ecx,var_1
mov ebx,1
add ecx,ebx
mov ebx,ecx
mov var_1,ebx
jmp L3
L4:
invoke ExitProcess, 0
main endp
end start
