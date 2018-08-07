echo off
arg1=$1
arg2=$2
arg3=$3
arg4=$4
arg5=$5

cd $arg3
rm -rf .git
git init
git remote add origin $arg1
git pull origin $arg5
cd ../..
