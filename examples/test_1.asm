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
LOCAL var_1:BYTE
LOCAL div_temp_1:DWORD
LOCAL div_temp_2:DWORD
LOCAL div_temp_3:DWORD
LOCAL div_temp_res:DWORD
program:
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
jl L1
jmp L0
L1:
printf("yass goorl")
jmp L0
L0:
invoke ExitProcess, 0
main endp
end start
