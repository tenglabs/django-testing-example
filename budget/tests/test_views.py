from django.test import TestCase, Client
from django.urls import reverse
from budget.models import Project, Category, Expense
import json



class TestViews(TestCase):


    def setUp(self):
        self.client = Client()
        self.list_url = reverse('list')
        self.detail_url = reverse('detail', args=['project1'])
        self.project1 = Project.objects.create(
            name='project1',
            budget=10000
        )

    def test_project_list_GET(self):

        response = self.client.get(reverse('list'))


        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'budget/project-list.html')


    def test_detail_GET(self):
        response = self.client.get(self.detail_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'budget/project-detail.html')

    
    def test_detail_POST_adds_ne(self):
        Category.objects.create(
            project = self.project1,
            name = 'testcat'
        )

        response = self.client.post(self.detail_url,
        {
            'title': 'expense1',
            'amount': 1000,
            'category': 'testcat'
        }
        )

        self.assertEquals(response.status_code, 302)
        self.assertEquals(self.project1.expenses.first().title, 'expense1')

    
    def test_p_detail_POST_no_DATA(self):

        response = self.client.post(self.detail_url)

        self.assertEquals(response.status_code, 302)

        self.assertEquals(self.project1.expenses.count(), 0)

    def test_del_expense(self):

        category1 = Category.objects.create(
            project=self.project1,
            name='dev'
        )
        Expense.objects.create(
            project=self.project1,
            title='expense1',
            amount=1000,
            category=category1
        )

        response = self.client.delete(self.detail_url, json.dumps({
            'id':1

        }))


        self.assertEquals(response.status_code, 204)
        self.assertEquals(self.project1.expenses.count(), 0 )


    def test_del_no_id(self):

        category1 = Category.objects.create(
            project=self.project1,
            name='dev'
        )
        Expense.objects.create(
            project=self.project1,
            title='expense1',
            amount=1000,
            category=category1
        )

        response = self.client.delete(self.detail_url)


        self.assertEquals(response.status_code, 404)
        self.assertEquals(self.project1.expenses.count(), 1)

    
    def test_create_POST