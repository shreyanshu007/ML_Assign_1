# ML_Assign_1

First you need to run pre_process.py

python3 pre_process.py

It reads few files to create dataset:

These files should be of same name and should be present at same position

	./text/labeledBow.feat
	./train/labledBow.feat
	./imdb.vocab
	./imdbEr.txt

( './text/labeledBow.feat' , './train/labledBow.feat' ) are not present in my zip folder. But it should be present at correct position.

It generats few files:

	./test/neg.txt
	./test/pos.txt
	./train/neg.txt
	./train/pos.txt
	./words.txt

TO train the model and see the results you have to run

python3 main.py

It will give you 5 options

 Enter 1 for exp1 
 Enter 2 for exp2 
 Enter 3 for exp3 
 Enter 4 for exp4 
 Enter 5 for exp5 
 
 If you will enter any other option then it will not work