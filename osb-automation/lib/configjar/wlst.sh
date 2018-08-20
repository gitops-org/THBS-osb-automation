#!/bin/sh

WLST_PROPERTIES="$JAVA_OPTS"
export WLST_PROPERTIES

"$WL_HOME/common/bin/wlst.sh" $*
