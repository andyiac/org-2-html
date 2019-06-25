#!/bin/bash/

echo "======= rebuid http://org.andyiac.com ======="

echo "======= clean ./public/ dir ================="
rm  ~/code/org-2-html/public/*.*


echo "======= cp css files ================="
cp ~/code/org-2-html/src/*.css ~/code/org-2-html/public/

echo "======= rebuild html ======================="
python ~/code/org-2-html/org-to-html.py




