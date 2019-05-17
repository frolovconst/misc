#!/bin/bash
cd /usr
mkdir java
cd java
cp /work/java.zip .
tar zxvf java.zip
export PATH=/usr/java/jre1.8.0_191/bin:$PATH
cd /work
unzip stanford-corenlp-full-2018-10-05.zip
cd stanford-corenlp-full-2018-10-05
for file in `find . -name "*.jar"`; do export CLASSPATH="$CLASSPATH:`realpath $file`"; done
cd /work
python3.6 extract_dialogues.py OliverTwist.txt

