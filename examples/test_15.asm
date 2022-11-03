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
LOCAL var_1:BYTE
LOCAL div_temp_1:DWORD
LOCAL div_temp_2:DWORD
LOCAL div_temp_3:DWORD
LOCAL div_temp_res:DWORD
LOCAL var_0[10]:BYTE
L0:
mov edx,0
mov var_1,dl
jmp L1
L1:
xor edx,edx
mov dl,var_1
mov ecx,10
cmp edx,ecx
jl L3
jmp L2
L3:
xor ecx,ecx
mov cl,var_1
imul ecx,1
xor edx,edx
mov dl,97
mov var_0[ecx],dl
xor ecx,ecx
mov cl,var_1
mov edx,1
add ecx,edx
xor edx,edx
mov dl,cl
mov var_1,dl
jmp L1
L2:
invoke StdIn, addr var_0,9
printf("%s\n",addr var_0)
invoke StdIn, addr var_0,9
printf("%s\n",addr var_0)
ret
f_0 endp
end start
