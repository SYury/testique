echo "<script type="text/javascript" src="problem-select.js"></script>" > "main.html"
cd pr
for d in */ ; do
    name=${d}
    name=${name::-1}
    name="<a href=\"show.html\" onclick=setProb('$name')>$name</a>"
    echo "$name" >> "../main.html"
    echo "<br>" >> "../main.html"
done
