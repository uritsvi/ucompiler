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
mov edx,0
mov var_0,edx
jmp L1
L1:
mov edx,var_0
mov ecx,20
cmp edx,ecx
jl L3
jmp L2
L3:
mov ecx,var_0
mov edx,3
push ecx
push edx
mov eax,ecx
mov ecx,edx
cdq
idiv ecx
mov div_temp_res,edx
pop edx
pop ecx
mov ecx,div_temp_res
mov edx,ecx
mov ecx,0
cmp edx,ecx
je L6
jmp L4
L6:
mov ecx,var_0
mov edx,5
push ecx
push edx
mov eax,ecx
mov ecx,edx
cdq
idiv ecx
mov div_temp_res,edx
pop edx
pop ecx
mov ecx,div_temp_res
mov edx,ecx
mov ecx,0
cmp edx,ecx
je L5
jmp L4
L5:
printf("fizz buzz\n")
jmp L7
L4:
mov ecx,var_0
mov edx,3
push ecx
push edx
mov eax,ecx
mov ecx,edx
cdq
idiv ecx
mov div_temp_res,edx
pop edx
pop ecx
mov ecx,div_temp_res
mov edx,ecx
mov ecx,0
cmp edx,ecx
je L9
jmp L8
L9:
printf("fizz\n")
jmp L10
L8:
mov ecx,var_0
mov edx,5
push ecx
push edx
mov eax,ecx
mov ecx,edx
cdq
idiv ecx
mov div_temp_res,edx
pop edx
pop ecx
mov ecx,div_temp_res
mov edx,ecx
mov ecx,0
cmp edx,ecx
je L12
jmp L11
L12:
printf("buzz\n")
jmp L13
L11:
printf("%d\n",var_0)
jmp L13
L13:
jmp L10
L10:
jmp L7
L7:
mov ecx,var_0
mov edx,1
add ecx,edx
mov edx,ecx
mov var_0,edx
jmp L1
L2:
ret
f_0 endp
end start
