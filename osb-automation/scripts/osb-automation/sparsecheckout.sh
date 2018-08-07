echo off
arg1=$1
arg2=$2
arg3=$3
arg4=$4
arg5=$5


rm -rf $arg4
mkdir $arg4
cd $arg4

git init
git remote add origin $arg1

git config core.sparsecheckout true

echo $arg5 > .git/info/sparse-checkout

git pull origin $arg3
cd ../..
