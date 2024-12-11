install:
    pip install -r requirements.txt

get_classroom:
    python ./2.preprocess-mingyuan_sun/get_classroom.py

data_preprocessing:
    python ./2.preprocess-mingyuan_sun/data_preprocessing.py

annealing:
    python ./3.annealing-mingyuan_sun/annealing.py

annealing_test:
    python ./3.annealing-junhui_huang/annealing.py --days_of_week monday --max_runtime 300

evaluation:
    python ./5.evaluation/evalution.py
    
run:
    get_classroom
    data_preprocessing
    annealing
    evaluation
