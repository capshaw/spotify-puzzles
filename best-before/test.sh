#!/bin/bash

passed=0
failed=0
count=1

for f in test-cases/*.testcase
do
	echo "[test $count]"
	echo "   testing using $f "

	# Run the program
	python best-before.py < $f > temp.txt

	a=`sed -n '2p' $f`;
	echo "   # $a";
	t=`sed -n '3p' $f`;

	echo $t > temp-ref.txt

	if diff temp.txt temp-ref.txt > /dev/null ; then
	    echo "   test passed"
	    passed=$[$passed+1]
	    echo ""
	else
	    echo "   test failed"
	    echo "---------------------output-------------------"
	    cat temp.txt
	    echo "---------------------exptec-------------------"
	    cat temp-ref.txt
	    echo "----------------------------------------------"
	    failed=$[$failed+1]
	fi

	count=$[$count+1]
done

rm temp.txt
rm temp-ref.txt

echo " "
echo " test results:"
echo "     passed: $passed"
echo "     failed: $failed"