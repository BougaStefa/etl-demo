def test_get_launches_unauthorized(client):
    """ Test unauthorized access to /launches endpoint """
    response = client.get("/launches")
    assert response.status_code == 401 # request rejected

def test_get_launches_authorized(client, auth_headers):
    """ Test authorized access to /launches endpoint """
    response = client.get("/launches", headers=auth_headers)
    assert response.status_code == 200 # valid jwt = success
    assert isinstance(response.json(), list) # returns a list of launches
