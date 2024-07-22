def list_roles(req_wrap):
    endpoint = "/roles"
    response, status = req_wrap.get(endpoint)
    if status == 200:
        roles = response
        return True, roles
    else:
        return False, response.get("detail", "Unknown Error")

def get_role(req_wrap, role_id):
    endpoint = f"/roles/{role_id}"
    response, status = req_wrap.get(endpoint)
    if status == 200:
        role = response
        return True, role
    else:
        return False, response.get("detail", "Unknown Error")
    
def create_role(req_wrap, name):
    endpoint = "/roles"
    response, status = req_wrap.post(endpoint, data={"name": name})
    if status == 201:
        return True, ""
    else:
        return False, response.get("detail", "Unknown Error")
    
def update_role(req_wrap, role_id, data):
    endpoint = f"/roles/{role_id}"
    response, status = req_wrap.patch(endpoint, data=data)
    if status == 200:
        return True, ""
    else:
        return False, response.get("detail", "Unknown Error")

def delete_role(req_wrap, role_id):
    endpoint = f"/roles/{role_id}"
    response, status = req_wrap.delete(endpoint)
    if status == 200:
        return True, ""
    else:
        return False, response.get("detail", "Unknown Error")
