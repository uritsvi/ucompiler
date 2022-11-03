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
LOCAL var_1:DWORD
LOCAL var_2:DWORD
LOCAL var_3:DWORD
LOCAL var_5:DWORD
LOCAL div_temp_res:DWORD
LOCAL var_4[10]:DWORD
L0:
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
jmp L1
L1:
mov edx,var_0
mov ecx,var_2
cmp edx,ecx
jl L3
jmp L2
L3:
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
jmp L1
L2:
jmp L4
L4:
mov edx,var_1
mov ecx,var_2
mov ebx,1
sub ecx,ebx
mov ebx,ecx
cmp edx,ebx
jl L6
jmp L5
L6:
mov ebx,var_1
mov var_3,ebx
mov ebx,var_1
mov edx,1
add ebx,edx
mov edx,ebx
mov var_0,edx
jmp L7
L7:
mov ebx,var_1
mov edx,var_2
cmp ebx,edx
jl L9
jmp L8
L9:
mov edx,var_0
imul edx,4
mov ebx,var_4[edx]
mov edx,var_3
imul edx,4
mov ecx,var_4[edx]
cmp ebx,ecx
jl L11
jmp L10
L11:
mov ecx,var_0
mov var_3,ecx
printf("%d\n",var_3)
jmp L10
L10:
mov ecx,var_1
mov ebx,1
add ecx,ebx
mov ebx,ecx
mov var_1,ebx
jmp L7
L8:
mov ecx,var_1
mov ebx,1
add ecx,ebx
mov ebx,ecx
mov var_1,ebx
jmp L4
L5:
ret
f_0 endp
end start
