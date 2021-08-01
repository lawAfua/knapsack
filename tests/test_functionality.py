from src.flask_app import app


def test_send_knapsack():
	client = app.test_client()
	data = {"problem": {"capacity": 60, "weights": [10, 20, 33], "values": [10, 3, 30]}}
	response = client.post("/knapsack", json=data)
	assert response.status_code == 200


def test_get_knapsack():
	client = app.test_client()
	response = client.get("/knapsack/nbd43jhb")
	# Since ID is generated at run time it may or may not exist if executed before post request
	#  if id is not found then we pass 404 response else 200.
	assert response.status_code == 200 or response.status_code == 404