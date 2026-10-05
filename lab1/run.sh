#!/bin/sh
# Запуск без Maven: компиляция через javac и старт через java.
# Использование: sh run.sh
set -e
cd "$(dirname "$0")"
rm -rf out
mkdir -p out
find src/main/java -name "*.java" > out/sources.txt
javac -encoding UTF-8 -d out @out/sources.txt
java -Dfile.encoding=UTF-8 -cp out com.example.happiness.Main
