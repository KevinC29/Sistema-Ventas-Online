from ..models import user

def validate_data_none_user(name, role, password_hash):
    validate_None = any(value is None for value in (name, role, password_hash))
    return validate_None
    
def validate_data_type_user(name, role, password_hash):
    is_name_valid = isinstance(name, str)
    is_role_valid = isinstance(role, str)
    is_password_valid = isinstance(password_hash, str)
    validate_Type = not all([is_name_valid, is_role_valid, is_password_valid])
    return validate_Type

def validate_data_role_user(role):
    validate_role = not role in ['editor', 'basic']
    return validate_role

def validate_exist_user(request, user_id):
    user_data = request.dbsession.query(user.User).filter_by(id=user_id).first()
    if not user_data:
        return True
    else:
        return user_data

def list_user(request):
    user_all = request.dbsession.query(user.User).all()
    if not user_all:
        return True
    else:
        users_json = [user.user_to_dict() for user in user_all]
        return users_json
            
def create_user(request, name, role, password_hash):
    new_user = user.User(
        name=name,
        role=role
    )
    new_user.set_password(password_hash)
    request.dbsession.add(new_user)
    request.dbsession.flush()
    return new_user.user_to_dict()

def update_user(request, user, name, role, password_hash):
    if user.name == name:
        user.role = role
        user.set_password(password_hash)
    else:
        user.name = name
        user.role = role
        user.set_password(password_hash)
    request.dbsession.flush()
    return user.user_to_dict()

def delete_user(request, user_id):
    user = validate_exist_user(request, user_id)
    if user == True:
        return True
    else:
        request.dbsession.delete(user)
        request.dbsession.flush()
        return False