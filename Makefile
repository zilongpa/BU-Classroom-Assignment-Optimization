

install:
	pip install -r requirements.txt
run:
	cd ./2.preprocess-mingyuan_sun/ && python get_classroom.py && python data_preprocessing.py
	cd ../3.annealing-mingyuan_sun/ && python annealing.py
	cd ../5.evaluation/ && python evalution.py
