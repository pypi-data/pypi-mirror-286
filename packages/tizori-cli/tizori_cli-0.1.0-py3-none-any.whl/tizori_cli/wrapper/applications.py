def list_applications(req_wrap):
    endpoint = "/applications"
    response, status = req_wrap.get(endpoint)
    if status == 200:
        applications = response
        return True, applications
    else:
        return False, response.get("detail", "Unknown Error")
    

def get_application_credentials(req_wrap, application_id):
    endpoint = f"/credentials/{application_id}"
    response, status = req_wrap.get(endpoint)
    if status == 200:
        credentials = response
        return True, credentials
    else:
        return False, response.get("detail", "Unknown Error")


def create_application(req_wrap, name):
    endpoint = "/applications"
    response, status = req_wrap.post(endpoint, data={"name": name})
    if status == 201:
        return True, ""
    else:
        return False, response.get("detail", "Unknown Error")
    

def update_application_credentials(req_wrap, application_id, data):
    endpoint = f"/credentials/{application_id}"
    response, status = req_wrap.patch(endpoint, data=data)
    if status == 200:
        return True, ""
    else:
        return False, response.get("detail", "Unknown Error")
    

def delete_application(req_wrap, application_id):
    endpoint = f"/applications/{application_id}"
    response, status = req_wrap.delete(endpoint)
    if status == 200:
        return True, ""
    else:
        return False, response.get("detail", "Unknown Error")
