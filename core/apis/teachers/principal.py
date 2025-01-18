from flask import Blueprint
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.teachers import Teacher

from .schema import TeacherSchema
principal_resources = Blueprint('principal_resources', __name__)

@principal_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers_for_principal(p):
    """Returns a list of all teachers"""
    teachers = Teacher.query.all()
    teachers_dump = TeacherSchema().dump(teachers, many=True)
    return APIResponse.respond(data=teachers_dump)
