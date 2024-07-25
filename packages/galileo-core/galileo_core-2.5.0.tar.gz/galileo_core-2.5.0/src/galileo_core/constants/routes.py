from enum import Enum


class Routes(str, Enum):
    healthcheck = "healthcheck"
    username_login = "login"
    api_key_login = "login/api_key"
    get_token = "get-token"
    current_user = "current_user"
    projects = "projects"
    project = "projects/{project_id}"
