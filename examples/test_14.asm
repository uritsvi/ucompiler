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
LOCAL var_1:BYTE
LOCAL div_temp_res:DWORD
L0:
mov edx,10
mov var_0,edx
xor edx,edx
mov dl,114
mov var_1,dl
mov edx,var_0
xor ecx,ecx
mov cl,var_1
add edx,ecx
mov ecx,edx
mov edx,1000
cmp ecx,edx
jl L2
jmp L1
L2:
printf("good\n")
jmp L3
L1:
invoke ExitProcess,1
jmp L3
L3:
ret
f_0 endp
end start
