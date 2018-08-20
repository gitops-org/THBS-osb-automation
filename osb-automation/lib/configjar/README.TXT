========================
PURPOSE
========================
This document describes how to create an OSB Config Jar from file system using
the following methods:
 - command line
 - ANT script
 - WLST script

This document contains the following sub-sections:
 - Contents
 - Setting the Environment
 - Command Line
 - ANT
 - WLST


========================
CONTENTS
========================

The tools/configjar directory ($CONFIGJAR_HOME) contains files that are used to
configure the configjar tool. The files/directorie listed below must not be
modified.
  - L10N/*
  - *.jar

This folder also contains the following:
  - setenv.*                [ Command line scripts to set the environment ]
  - configjar.*             [ Command line scripts to run the configjar tool ]
  - configjar-ant.xml       [ ANT build file defining the default ANT targets
                              that can be used to run the configjar tool ]
  - wlst.*                  [ Command line scripts to execute WLST scripts ]


========================
SETTING THE ENVIRONMENT
========================

Before running the tool via command line, ANT or WLST, you must set your
environment appropriately.

To set your environment, run the setenv.* script (note: you only need to run it
once per shell).
e.g.:
    cd $CONFIGJAR_HOME
    source setenv.sh


You can modify the setenv.* files to tune the JVM heap size, add additional JARs
to the CLASSPATH (e.g. if you have a JAR resource requiring custom jars on the
server classpath) or add additional system properties.


========================
COMMAND LINE
========================

Before running the tool, you must create a settings file. Then you can run the
configjar.* script.
e.g.:
    cd $CONFIGJAR_HOME
    source setenv.sh            [if the environment has not previously been set]
    ./configjar.sh -settingsfile MyConfigJarSettings.xml


When using the command line, you can use the following arguments:
    * To specify the settings file:
        -settingsfile <filename>


========================
ANT
========================

OSB provides an ANT file (configjar-ant.xml) with a target to run the Config Jar
tool.

You can create your own ANT build file and call that target.
e.g.:
    <project name="myproject" basedir=".">
        <target name="run">
            <ant antfile="configjar-ant.xml" target="run">
                <property name="settingsFile" value="/somepath/settings1.xml"/>
            </ant>
            <ant antfile="configjar-ant.xml" target="run">
                <property name="settingsFile" value="/somepath/settings2.xml"/>
            </ant>
        </target>
    </project>
You can run this build file as follow:
    cd $CONFIGJAR_HOME
    source setenv.sh            [if the environment has not previously been set]
    ant -f mybuild.xml run

In the build file, you can use properties to override the default behavior (see
the target init in configjar-ant.xml):
    * To control the behavior of the task:
        task.debug              [turn on debug logging]
        task.failonerror        [true by default, when set to false, the task
                                 does not fail but set the result in the
                                 property identified by task.errorproperty]
        task.errorproperty      [property name to receive the task result]
    * To define the settings file:
        settingsFile


========================
WLST
========================

To make sure WLST is properly configured, you can use the provided wlst.*
script.
e.g.:
    cd $CONFIGJAR_HOME
    source setenv.sh            [if the environment has not previously been set]
    wlst.sh <scriptname>

The following WLST script is an example how to run the tool.
e.g.:
    from com.bea.alsb.tools.configjar import ConfigJar
    args = []
    args.append('-settingsfile')
    args.append('somepath/mysettings.xml')
    ConfigJar.main(args)
