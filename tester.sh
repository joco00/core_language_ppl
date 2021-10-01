#!/bin/bash

runner=$1

if test -f main.py
then
	runner="python3 main.py"
elif test -f Main.java
then
	echo "Attempting to compile..."
	javac *.java
	runner="java Main"
fi

for value in {1..9}
do
	echo ""
	echo "Running ${value}.code"
	${runner} Cases/Correct/${value}.code Cases/Correct/${value}.data > Cases/Correct/${value}.student
	echo "Running diff with ${value}.expected"
	diff -q Cases/Correct/${value}.expected Cases/Correct/${value}.student
done

echo "Running error cases:"
echo ""

echo "Running 00.error:"
timeout 5 ${runner} Cases/Error/00.code Cases/Error/00.data
read -n 1 -p "Error function body missing (no stmt-seq). Error message related to that? (y/n)" mainmenuinput
if [ $mainmenuinput = "y" ]; then
	echo -e "\nCorrect aknowledged"
else
	echo -e "\nIncorrect aknowledged"
fi
echo ""

echo "Running 01.error:"
timeout 5 ${runner} Cases/Error/01.code Cases/Error/01.data
read -n 1 -p "Error is bad function call. Error message related to that? (y/n)" mainmenuinput
if [ $mainmenuinput = "y" ]; then
	echo -e "\nCorrect aknowledged"
else
	echo -e "\nIncorrect aknowledged"
fi

echo "Running 02.error:"
timeout 5 ${runner} Cases/Error/02.code Cases/Error/02.data
read -n 1 -p "Error is bad function declaration (extra ')'). Error message related to that? (y/n)" mainmenuinput
if [ $mainmenuinput = "y" ]; then
	echo -e "\nCorrect aknowledged"
else
	echo -e "\nIncorrect aknowledged"
fi

echo "Running 03.error:"
timeout 5 ${runner} Cases/Error/03.code Cases/Error/03.data
read -n 1 -p "Error is bad function call (missing ';'). Error message related to that? (y/n)" mainmenuinput
if [ $mainmenuinput = "y" ]; then
	echo -e "\nCorrect aknowledged"
else
	echo -e "\nIncorrect aknowledged"
fi

echo "Running 04.error:"
timeout 5 ${runner} Cases/Error/04.code Cases/Error/04.data
read -n 1 -p "Error is bad function call (empty id list). Error message related to that? (y/n)" mainmenuinput
if [ $mainmenuinput = "y" ]; then
	echo -e "\nCorrect aknowledged"
else
	echo -e "\nIncorrect aknowledged"
fi

echo "Running 05.error:"
timeout 5 ${runner} Cases/Error/05.code Cases/Error/05.data
read -n 1 -p "Error is duplicate declaration for a function named x. Error message related to that? (y/n)" mainmenuinput
if [ $mainmenuinput = "y" ]; then
	echo -e "\nCorrect aknowledged"
else
	echo -e "\nIncorrect aknowledged"
fi

echo "Running 06.error:"
timeout 5 ${runner} Cases/Error/06.code Cases/Error/06.data
read -n 1 -p "Error is two different functions named x. Error message related to that? (y/n)" mainmenuinput
if [ $mainmenuinput = "y" ]; then
	echo -e "\nCorrect aknowledged"
else
	echo -e "\nIncorrect aknowledged"
fi

echo "Running 07.error:"
timeout 5 ${runner} Cases/Error/07.code Cases/Error/07.data
read -n 1 -p "Error is function call does not match function definition. Error message related to that? (y/n)" mainmenuinput
if [ $mainmenuinput = "y" ]; then
	echo -e "\nCorrect aknowledged"
else
	echo -e "\nIncorrect aknowledged"
fi

echo "Running 08.error:"
timeout 5 ${runner} Cases/Error/08.code Cases/Error/08.data
read -n 1 -p "Error is function call with constant as actual parameter. Error message related to that? (y/n)" mainmenuinput
if [ $mainmenuinput = "y" ]; then
	echo -e "\nCorrect aknowledged"
else
	echo -e "\nIncorrect aknowledged"
fi


echo "Done!"