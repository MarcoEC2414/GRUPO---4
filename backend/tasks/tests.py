from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Task

class TaskTests(APITestCase):
    def test_create_task_with_empty_title(self):
        """No se puede crear una tarea con título vacío"""
        url = reverse('task-list')
        data = {'title': ''}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_valid_task(self):
        """Se puede crear una tarea con título válido"""
        url = reverse('task-list')
        data = {'title': 'Tarea de prueba'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, 'Tarea de prueba')
    
    def test_mark_task_completed(self):
        """Se puede marcar/desmarcar una tarea como completada"""
        task = Task.objects.create(title='Tarea por completar')
        url = reverse('task-mark-completed', args=[task.id])
        
        # Marcar como completada
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertTrue(task.completed)
        
        # Desmarcar
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertFalse(task.completed)
    
    def test_delete_task(self):
        """Se puede eliminar una tarea"""
        task = Task.objects.create(title='Tarea a eliminar')
        url = reverse('task-detail', args=[task.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)