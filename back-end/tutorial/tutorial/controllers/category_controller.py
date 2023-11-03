from ..models import models

def validate_data_none_category(name, desc):
    validate_None = any(value is None for value in (name, desc))
    return validate_None
    
def validate_data_type_category(name, desc):
    is_name_valid = isinstance(name, str)
    is_desc_valid = isinstance(desc, str)
    validate_Type = not all([is_name_valid, is_desc_valid])
    return validate_Type

def validate_exist_category(request, category_id):
    category = request.dbsession.query(models.Category).filter_by(id=category_id).first()
    if not category:
        return True
    else:
        return category

def list_category(request):
    category_all = request.dbsession.query(models.Category).all()
    if not category_all:
        return True
    else:
        categories_json = [category.category_to_dict() for category in category_all]
        return categories_json
            
def create_category(request, name, desc):
    new_category = models.Category(
        name=name,
        desc=desc
    )
    request.dbsession.add(new_category)
    request.dbsession.flush()
    return new_category.category_to_dict()

def update_category(request, category, name, desc):
    if category.name == name:
        category.desc = desc
    else:
        category.name = name
        category.desc = desc
    request.dbsession.flush()
    return category.category_to_dict()

def delete_category(request, category_id):
    category = validate_exist_category(request, category_id)
    if category == True:
        return True
    else:
        request.dbsession.delete(category)
        request.dbsession.flush()
        return False