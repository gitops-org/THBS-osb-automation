@echo off

set WLST_PROPERTIES=%JAVA_OPTS%

call "%WL_HOME%\common\bin\wlst" %*
