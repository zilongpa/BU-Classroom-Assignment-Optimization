install:
    pip install -r requirements.txt

get_classroom:
    python .\2.preprocess-mingyuan_sun\get_classroom.py

data_preprocessing:
    python .\2.preprocess-mingyuan_sun\data_preprocessing.py

run: get_classroom data_preprocessing
    a command to generate pickle file
    python .\3.annealing-junhui_huang\annealing.py --days_of_week monday --max_runtime 300

test_solution: data_preprocessing
    python python .\2.preprocess-mingyuan_sun\data_preprocessing.py