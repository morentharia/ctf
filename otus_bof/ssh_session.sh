ssh mor@192.168.149.24
1

cd Z:\\bof\\Debug\\
Copy-Item '.\BoF_Simple.exe' -Destination C:\\ 
C:\BoF_Simple.exe
C:\\PSTools\\PsExec.exe -i 1 -s 'C:\\BoF_Simple.exe'

