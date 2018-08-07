@ECHO ON

@REM Change the environment variables below to suit your target environment
@REM The WLST_OUTPUT_PATH and WLST_OUTPUT_FILE environment variables in this script 
@REM determine the output directory and file of the script
@REM The WLST_OUTPUT_PATH directory value must have a trailing slash. If there is no trailing slash 
@REM script will error and not continue.


SETLOCAL

set WL_HOME=C:\Oracle\Middleware\wlserver_10.3
set DOMAIN_HOME=C:\Oracle\Middleware\user_projects\domains\base_domain
set WLST_OUTPUT_PATH=C:\temp\wlst\
set WLST_OUTPUT_FILE=WLST_MBean_Config_Summary.html

call "%WL_HOME%\common\bin\wlst.cmd" C:\Users\user\Desktop\AutomationScripts\scripts\resource\WLSDomainInfoOffline.py

pause

ENDLOCAL