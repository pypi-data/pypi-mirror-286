def list_users(req_wrap):
    endpoint = "/users"
    response, status = req_wrap.get(endpoint)
    if status == 200:
        users = response
        return True, users
    else:
        return False, response.get("detail", "Unknown Error")

def get_user(req_wrap, username):
    endpoint = f"/users/{username}"
    response, status = req_wrap.get(endpoint)
    if status == 200:
        user = response
        return True, user
    else:
        return False, response.get("detail", "Unknown Error")
    
def create_user(req_wrap, username, email, name):
    endpoint = "/users"
    response, status = req_wrap.post(endpoint, data={"username": username, "email": email, "name": name})
    if status == 201:
        return True, response.get("password")
    else:
        return False, response.get("detail", "Unknown Error")
    
def update_user(req_wrap, username, data):
    endpoint = f"/users/{username}"
    response, status = req_wrap.patch(endpoint, data=data)
    if status == 200:
        return True, ""
    else:
        return False, response.get("detail", "Unknown Error")

def delete_user(req_wrap, username):
    endpoint = f"/users/{username}"
    response, status = req_wrap.delete(endpoint)
    if status == 200:
        return True, ""
    else:
        return False, response.get("detail", "Unknown Error")