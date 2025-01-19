from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment, AssignmentStateEnum
from .schema import AssignmentSchema, AssignmentGradeSchema

principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)


@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments_for_principal(p):
    """Returns list of all assignments that are either submitted or graded"""
    assignments = Assignment.filter(Assignment.state.in_([AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]))
    assignments_dump = AssignmentSchema().dump(assignments, many=True)
    return APIResponse.respond(data=assignments_dump)

@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def principal_regrade_assignment(p, incoming_payload):
    """Re-grade an assignment already graded by a teacher"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    graded_assignment = Assignment.query.get(grade_assignment_payload.id)

    graded_assignment = Assignment.mark_grade_principal(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )

    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)
