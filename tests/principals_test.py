from core.models.assignments import AssignmentStateEnum, GradeEnum, Assignment
from core import db
from core.models.principals import Principal

def test_principal_repr():
        """Test case for Principal __repr__ method"""
        principal = Principal(id=1)
        assert repr(principal) == '<Principal 1>'

def test_get_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]


def test_grade_assignment_draft_assignment(client, h_principal):
    """
    Failure case: If an assignment is in Draft state, it cannot be graded by principal
    """

    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 5,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    assert response.status_code == 400
    assert response.json.get('message') == 'Assignment must be in Submitted or Graded state'


def test_grade_assignment(client, h_principal):
    """Test case for grading an assignment"""
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.C


def test_regrade_assignment(client, h_principal):
    """Test case for regrading an assignment"""
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B


def test_principal_view_all_teachers(client, h_principal):
    """ Test case for viewing all teachers """
    response = client.get(
        '/principal/teachers',
        headers=h_principal
    )
    assert response.status_code == 200
    data = response.json['data']
    assert len(data) == 2
    



def test_grade_assignment_invalid_id(client, h_principal):
    """
    Failure case: Grading an assignment with an invalid ID
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 999,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    assert response.status_code == 404


def test_grade_assignment_invalid_grade(client, h_principal):
    """
    Failure case: Grading an assignment with an invalid grade
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': 'InvalidGrade'
        },
        headers=h_principal
    )

    assert response.status_code == 400
    assert response.json['message']['grade'] == ['Invalid enum member InvalidGrade']  


def test_invalid_api_path(client, h_principal):
    """Test case when there is no matching API path"""

    response = client.post('/invalid/api/path', headers={'X-Principal': h_principal})
    assert response.status_code == 404