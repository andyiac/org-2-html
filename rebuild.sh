#!/bin/bash/

echo "======= rebuid http://org.andyiac.com ======="

echo "======= clean ./public/ dir ================="
rm  ~/code/org-2-html/public/*.*

echo "========cp org images to public image dir ====="
cp ~/org/image/*.* ~/code/org-2-html/public/image/

echo "=== cp static html files ==========="
cp ~/org/html/*.* ~/code/org-2-html/public/html/


echo "======= cp css files ================="
cp ~/code/org-2-html/src/*.css ~/code/org-2-html/public/

echo "======= cp js files ================="
cp ~/code/org-2-html/src/*.js ~/code/org-2-html/public/

echo "====== cp image ====================="
cp ~/code/org-2-html/src/*.png ~/code/org-2-html/public/


echo "======= rebuild html ======================="
python ~/code/org-2-html/org-to-html.py




