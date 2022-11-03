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
LOCAL div_temp_res:DWORD
LOCAL var_3[6]:DWORD
L0:
mov edx,0
mov var_0,edx
mov edx,5
mov var_1,edx
mov edx,0
mov var_2,edx
jmp L1
L1:
mov edx,var_0
mov ecx,var_1
mov ebx,1
add ecx,ebx
mov ebx,ecx
cmp edx,ebx
jl L3
jmp L2
L3:
mov ebx,var_0
imul ebx,4
mov edx,1
mov var_3[ebx],edx
mov ebx,var_0
mov edx,1
add ebx,edx
mov edx,ebx
mov var_0,edx
jmp L1
L2:
mov ebx,2
mov var_2,ebx
jmp L4
L4:
mov ebx,var_2
mov edx,var_2
imul ebx,edx
mov edx,ebx
mov ebx,var_1
mov ecx,1
add ebx,ecx
mov ecx,ebx
cmp edx,ecx
jl L6
jmp L5
L6:
mov ecx,var_2
imul ecx,4
mov edx,var_3[ecx]
mov ecx,1
cmp edx,ecx
je L8
jmp L7
L8:
mov ecx,var_2
mov edx,2
imul ecx,edx
mov edx,ecx
mov var_0,edx
jmp L9
L9:
mov ecx,var_0
mov edx,var_1
mov ebx,1
add edx,ebx
mov ebx,edx
cmp ecx,ebx
jl L11
jmp L10
L11:
mov ebx,var_0
imul ebx,4
mov ecx,0
mov var_3[ebx],ecx
mov ebx,var_0
mov ecx,var_2
add ebx,ecx
mov ecx,ebx
mov var_0,ecx
jmp L9
L10:
jmp L7
L7:
mov ebx,var_2
mov ecx,1
add ebx,ecx
mov ecx,ebx
mov var_2,ecx
jmp L4
L5:
mov ebx,2
mov var_0,ebx
jmp L12
L12:
mov ebx,var_0
mov ecx,var_1
mov edx,1
add ecx,edx
mov edx,ecx
cmp ebx,edx
jl L14
jmp L13
L14:
mov edx,var_0
imul edx,4
mov ebx,var_3[edx]
mov edx,1
cmp ebx,edx
je L16
jmp L15
L16:
printf("%d\n",var_0)
jmp L15
L15:
mov edx,var_0
mov ebx,1
add edx,ebx
mov ebx,edx
mov var_0,ebx
jmp L12
L13:
printf("done\n")
ret
f_0 endp
end start
