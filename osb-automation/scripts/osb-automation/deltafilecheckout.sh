echo off
arg1=$1
arg2=$2
arg3=$3
arg4=$4
arg5=$5

cd $arg3
#rm -rf *
rm -rf .git
git init
git remote add origin $arg1

git config core.sparsecheckout true

echo $arg2 > .git/info/sparse-checkout

git pull origin $arg5
cd ../..
