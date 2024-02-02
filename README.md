# HTTP Log Analyser
Extract filtered data from Apache Logs

##How to use : 
Connect to the server with admin rights

Here is a batch you can use to get the logs with cmd
(notice that it is a very bad practice to keep the server in clear in your file, ask it at runtime)

sync_logs.bat

@echo off
```cmd
set LOG_PATH=your_log_file_path
set WINSCP_PATH="C:\Program Files (x86)\WinSCP\winscp.com"

set DEST_SERVER_IP=your_server_adress
set DEST_SERVER_USERNAME=your_admin_name
set DEST_SERVER_PASSWORD=your_admin_pasword
set DEST_SERVER_PORT=your_serveur_port

echo starting synchro...>s%LOG_PATH%

set DEST_SERVER_DIRECTORY=/var/log/httpd/
set LOCALPATH="C:\svnroot\oxyprj_1102\IA\memsoft_docs\Aides\logs"

echo get logs
%WINSCP_PATH% /command ^
    "option batch abort" ^
    "option confirm off" ^
    "open sftp://%DEST_SERVER_USERNAME%:%DEST_SERVER_PASSWORD%@%DEST_SERVER_IP%:%DEST_SERVER_PORT%" ^
    "synchronize local -preservetime -transfer=binary %LOCALPATH% %DEST_SERVER_DIRECTORY%" ^
    "exit">>%LOG_PATH%

```