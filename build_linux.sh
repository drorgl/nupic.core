#!/bin/bash
gyp nupic.gyp --no-duplicate-basename-check -DOS=linux -Dtarget_arch=x64 --depth=$(pwd) -f make -Dbuildtype=Debug --generator-output=./build.linux/

