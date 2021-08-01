from flask import Flask, request, Response
import time
import random
import string
import simplejson
import os
from apscheduler.schedulers.background import BackgroundScheduler
from ortools.algorithms import pywrapknapsack_solver

N = 8
TASK_ID = ""
START_DIR = "knapsack_start"
COMPLETED_DIR = "knapsack_complete"
DIR_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
START_PATH = os.path.join(DIR_PATH, START_DIR)
COMPLETE_PATH = os.path.join(DIR_PATH, COMPLETED_DIR)


def sensor():
    """ Function for test purposes. """
    start_path, complete_path, filename = file_properties()
    if os.path.isfile(os.path.join(start_path, filename)):
        with open(os.path.join(start_path, filename), 'r') as f:
            contents = simplejson.load(f)
        contents['status'] = "started"
        contents['timestamps']['started'] = time.time()

        with open(os.path.join(complete_path, filename), 'w') as f:
            simplejson.dump(contents, f)
        knapsack_solution(contents)


sched = BackgroundScheduler(daemon=True)
sched.add_job(sensor, 'interval', seconds=0.1)
sched.start()

app = Flask(__name__)


@app.route('/knapsack', methods=['POST'])
def knapsack_problem():
    data = request.get_json()
    global TASK_ID
    TASK_ID = ''.join(random.choices(string.ascii_lowercase+string.digits, k=N))
    result = {"task": TASK_ID, "status": "submitted", "timestamps": {"submitted": time.time(), "started": None, "completed": None}, "problem": data["problem"], "solution": {}}
    start_path, complete_path, filename = file_properties()
    if not os.path.isdir(start_path):
        os.mkdir(start_path)
    with open(os.path.join(start_path, filename), 'w') as f:
        simplejson.dump(result, f)
    output = simplejson.dumps(result)
    return output


@app.route('/knapsack/<id>', methods=['GET'])
def get_knapsack(id):
    try:
        start_path, complete_path, filename = file_properties()
        filename = id+".json"
        with open(os.path.join(complete_path, filename), 'r') as f:
            knapsack_sol = simplejson.load(f)
            return simplejson.dumps(knapsack_sol)
    except Exception as e:
        return Response("id not found", 404)



def file_properties():

    if not os.path.isdir(START_PATH):
        os.mkdir(START_PATH)

    if not os.path.isdir(COMPLETE_PATH):
        os.mkdir(COMPLETE_PATH)
    filename = TASK_ID + ".json"
    return START_PATH, COMPLETE_PATH, filename


def knapsack_solution(result):
    problem = result['problem']
    solver = pywrapknapsack_solver.KnapsackSolver(
        pywrapknapsack_solver.KnapsackSolver.
            KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER, 'KnapsackExample')

    weights = [problem['weights']]
    capacity = [problem['capacity']]
    solver.Init(problem['values'], weights, capacity)
    computed_value = solver.Solve()

    packed_items = []
    packed_weights = []
    total_weight = 0

    for i in range(len(problem['values'])):
        if solver.BestSolutionContains(i):
            packed_items.append(i)
            packed_weights.append(weights[0][i])
            total_weight += weights[0][i]

    result['status'] = "completed"
    result['timestamps']['completed'] = time.time()
    result['solution'] = {'packed_items': packed_items, 'total_value': computed_value}
    start_path, complete_path, filename = file_properties()
    with open(os.path.join(complete_path, filename), 'w') as f:
        simplejson.dump(result, f)
    os.remove(os.path.join(start_path, filename))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6543, debug=True)