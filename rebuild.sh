#!/bin/bash/

echo "======= rebuid http://org.andyiac.com ======="

echo "======= clean ./public/ dir ================="
rm  ./public/*.*


echo "======= cp css files ================="
cp ./src/*.css public/

echo "======= rebuild html ======================="
python ./org-to-html.py




