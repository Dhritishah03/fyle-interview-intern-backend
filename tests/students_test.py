from core.models.assignments import Assignment, AssignmentStateEnum
from core.models.students import Student
from core import db
from core.libs.exceptions import FyleError

def test_student_repr():
        """Test case for Student __repr__ method"""
        student = Student(id=1)
        assert repr(student) == '<Student 1>'

def test_assignment_repr():
        """Test case for Assignment __repr__ method"""
        assignment = Assignment(id=1)
        assert repr(assignment) == '<Assignment 1>'

def test_get_assignments_student_1(client, h_student_1):
    response = client.get(
        '/student/assignments',
        headers=h_student_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 1


def test_get_assignments_student_2(client, h_student_2):
    """Test case for getting assignments for student 2"""
    response = client.get(
        '/student/assignments',
        headers=h_student_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 2


def test_post_assignment_null_content(client, h_student_1):
    """
    failure case: content cannot be null
    """

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': None
        })

    assert response.status_code == 400


def test_post_assignment_student_1(client, h_student_1):
    content = 'ABCD TESTPOST'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == AssignmentStateEnum.DRAFT
    assert data['teacher_id'] is None


def test_post_assignment_student(client, h_student_1):
    """ Test case for posting an assignment by student """
    content = 'ABCD TESTPOST'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'id': 5,
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == AssignmentStateEnum.DRAFT
    assert data['teacher_id'] is None


def test_submit_assignment_student_1(client, h_student_1):
    """ Test case for submitting an assignment by student """
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['student_id'] == 1
    assert data['state'] == 'SUBMITTED'
    assert data['teacher_id'] == 2


def test_assignment_resubmit_error(client, h_student_1):
    """ failure case: for resubmitting an assignment by student """
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })
    error_response = response.json
    assert response.status_code == 400
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'only a draft assignment can be submitted'
    

def test_upsert_assignment_wrong_id(client, h_student_1):
    """
    failure case: assignment not found for particular assignment id
    """
    content = 'New Assignment Content'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'id': 12,
            'content': content
        })

    assert response.status_code == 404


def test_upsert_assignment_submitted_error(client, h_student_1):
    """
    failure case: Assignment can only be edited if it is in draft state
    """
    content = 'Assignment Content'
    
    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'id': 2,
            'content': content
        })

    assert response.status_code == 400

    error_response = response.json
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'only assignment in draft state can be edited'


def test_fyle_error(client, h_student_1):
    """Test case for dict FyleError"""
    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': None
        })
    
    status_code = response.status_code
    data = response.json
    message = data['error']
    error = FyleError(status_code, message)

    assert error.status_code == status_code
    assert error.message == message

    error_dict = error.to_dict()
    assert error_dict['message'] == message

    