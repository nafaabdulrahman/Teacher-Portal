from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Student

class PortalTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='teacher', password='testpass')
        self.client.login(username='teacher', password='testpass')
        Student.objects.create(name='John', subject='Math', marks=50)

    def test_student_listed(self):
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John')

    def test_add_student_adds_marks(self):
    # POST data to add marks
        response = self.client.post('/add-student/', {
            'name': 'John',
            'subject': 'Math',
            'marks': 10
        })
        self.assertEqual(response.status_code, 302)  # assuming redirect on success

        # Reload student from DB
        student = Student.objects.get(name='John', subject='Math')
        student.refresh_from_db()

        # Expect marks to be updated from 50 to 60 (50 + 10)
        self.assertEqual(student.marks, 60)

