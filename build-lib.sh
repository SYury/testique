if [[ $1 = "-h" ]]; then
    echo "This script builds a library for testique"
    echo "Probems must be in separate folders inside $PWD/pr"
    echo "Each problem must contain files statement and time"
    echo "As well as checker check (executable file)"
    echo "It must also contain folder tests"
    echo "Each test in this folder must be present as testname.in and testname.out"
    exit 01
fi

echo "<script type="text/javascript" src="problem-select.js"></script>" > "main.html"
cd pr
for d in */ ; do
    name=${d}
    name=${name::-1}
    name="<a href=\"show.html\" onclick=setProb('$name')>$name</a>"
    echo "$name" >> "../main.html"
    echo "<br>" >> "../main.html"
done
