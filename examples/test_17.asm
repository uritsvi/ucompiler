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
LOCAL var_3[6]:DWORD
program:
mov edx,0
mov var_0,edx
mov edx,5
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
mov var_2,ebx
jmp L3
L3:
mov ebx,var_2
mov edx,var_2
imul ebx,edx
mov edx,ebx
mov ebx,var_1
mov ecx,1
add ebx,ecx
mov ecx,ebx
cmp edx,ecx
jl L5
jmp L4
L5:
mov ecx,var_2
imul ecx,4
mov edx,var_3[ecx]
mov ecx,1
cmp edx,ecx
je L7
jmp L6
L7:
mov ecx,var_2
mov edx,2
imul ecx,edx
mov edx,ecx
mov var_0,edx
jmp L8
L8:
mov ecx,var_0
mov edx,var_1
mov ebx,1
add edx,ebx
mov ebx,edx
cmp ecx,ebx
jl L10
jmp L9
L10:
mov ebx,var_0
imul ebx,4
mov ecx,0
mov var_3[ebx],ecx
mov ebx,var_0
mov ecx,var_2
add ebx,ecx
mov ecx,ebx
mov var_0,ecx
jmp L8
L9:
jmp L6
L6:
mov ebx,var_2
mov ecx,1
add ebx,ecx
mov ecx,ebx
mov var_2,ecx
jmp L3
L4:
mov ebx,2
mov var_0,ebx
jmp L11
L11:
mov ebx,var_0
mov ecx,var_1
mov edx,1
add ecx,edx
mov edx,ecx
cmp ebx,edx
jl L13
jmp L12
L13:
mov edx,var_0
imul edx,4
mov ebx,var_3[edx]
mov edx,1
cmp ebx,edx
je L15
jmp L14
L15:
printf("%d\n",var_0)
jmp L14
L14:
mov edx,var_0
mov ebx,1
add edx,ebx
mov ebx,edx
mov var_0,ebx
jmp L11
L12:
printf("done\n")
invoke ExitProcess, 0
main endp
end start
