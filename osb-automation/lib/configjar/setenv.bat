@echo off


@rem    Product Home directories

set OSB_HOME=..\..
for %%i in ("%OSB_HOME%") do set OSB_HOME=%%~fsi

set MW_HOME=%OSB_HOME%\..
for %%i in ("%MW_HOME%") do set MW_HOME=%%~fsi

call %OSB_HOME%\common\bin\setHomeDirs.cmd


@rem    JAVA \ ANT settings

call %WL_HOME%\common\bin\commEnv.cmd

set PATH=%MW_HOME%\modules\org.apache.ant_1.7.1\bin;%PATH%


@rem    The ConfigJar Tool Home directory

set CONFIGJAR_HOME=%OSB_HOME%\tools\configjar


@rem    System properties required by OSB

set OSB_OPTS=
set OSB_OPTS= %OSB_OPTS% -Dweblogic.home="%WL_HOME%"
set OSB_OPTS= %OSB_OPTS% -Dosb.home="%OSB_HOME%"

set JAVA_OPTS=%JAVA_OPTS% %OSB_OPTS%
set ANT_OPTS=%ANT_OPTS% %OSB_OPTS%


@rem  classpath representing OSB

set CLASSPATH=%CLASSPATH%;%MW_HOME%\modules\features\weblogic.server.modules_10.3.6.0.jar
set CLASSPATH=%CLASSPATH%;%WL_HOME%\server\lib\weblogic.jar

set CLASSPATH=%CLASSPATH%;%MW_HOME%\oracle_common\modules\oracle.http_client_11.1.1.jar
set CLASSPATH=%CLASSPATH%;%MW_HOME%\oracle_common\modules\oracle.xdk_11.1.0\xmlparserv2.jar
set CLASSPATH=%CLASSPATH%;%MW_HOME%\oracle_common\modules\oracle.webservices_11.1.1\orawsdl.jar
set CLASSPATH=%CLASSPATH%;%MW_HOME%\oracle_common\modules\oracle.wsm.common_11.1.1\wsm-dependencies.jar

set CLASSPATH=%CLASSPATH%;%OSB_HOME%\modules\features\osb.server.modules_11.1.1.7.jar
set CLASSPATH=%CLASSPATH%;%OSB_HOME%\soa\modules\oracle.soa.common.adapters_11.1.1\oracle.soa.common.adapters.jar
set CLASSPATH=%CLASSPATH%;%OSB_HOME%\lib\external\log4j_1.2.8.jar
set CLASSPATH=%CLASSPATH%;%OSB_HOME%\lib\alsb.jar

@rem  classpath for ConfigJar tool

set CLASSPATH=%CLASSPATH%;%CONFIGJAR_HOME%\configjar.jar
set CLASSPATH=%CLASSPATH%;%CONFIGJAR_HOME%\L10N
