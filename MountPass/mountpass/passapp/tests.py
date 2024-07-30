import json

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from passapp.models import PerevalAdded, MyUser, Coord, Level, Images
from passapp.serializers import PerevalSerializer, CoordSerializer, LevelSerializer, ImagesSerializer, MyUserSerializer

'''python manage.py test . - Запускает все тесты
 python manage.py test passapp.tests.PerevalApiTestCase.test_get_list - для запуска одного конкретного теста
 coverage run --source='.' manage.py test . - создает слепок .coverage, при изменении теста команду повторить
 coverage report - по слепку создает отчет в консоли
coverage html - создает папку htmlcov\index.html и в ней отчет
 '''


class PerevalApiTestCase(APITestCase):
    def setUp(self):
        self.passage_1 = PerevalAdded.objects.create(
            beauty_title='Очередной перевал',
            title='Азишский',
            other_titles='Лагонаки',
            connect='хребет',
            user=MyUser.objects.create(
                email='test@example.com',
                fam='Петров',
                name='Петр',
                otc='Петрович',
                phone='89997776655'
            ),
            coords=Coord.objects.create(
                latitude=55.4,
                longitude=77.6,
                height=888
            ),
            level=Level.objects.create(
                winter='2А',
                spring='2А',
                summer='2А',
                autumn='2А'
            ),
        )
        self.image_1 = Images.objects.create(
            pereval=self.passage_1,
            title='some title',
            image='http://lagonaki-otdyh.ru/azishkij-pereval-03.jpg'
        )

        self.passage_2 = PerevalAdded.objects.create(
            beauty_title='Еще один перевал',
            title='Путешественников',
            other_titles='Пик Ленина',
            connect='верховья ручь',
            user=MyUser.objects.create(
                email='other@example.com',
                fam='Александров',
                name='Александр',
                otc='Александрович',
                phone='84443332211'
            ),
            coords=Coord.objects.create(
                latitude=33.2,
                longitude=22.1,
                height=999
            ),
            level=Level.objects.create(
                winter='3А',
                spring='3А',
                summer='3А',
                autumn='3А'
            ),
        )
        self.image_2 = Images.objects.create(
            pereval=self.passage_2,
            title='beauty',
            image='https://ic.pics.livejournal.com/frantsouzov/21599674/344349/344349_original.jpg'
        )

    def test_get_list(self):
        url = reverse("pereval-list")
        response = self.client.get(url)
        serializer_data = PerevalSerializer([self.passage_1, self.passage_2], many=True).data
        self.assertEquals(serializer_data, response.data)
        self.assertEquals(status.HTTP_200_OK, response.status_code)

    def test_get_detail(self):
        url = reverse("pereval-detail", args=(self.passage_1.id,))
        response = self.client.get(url)
        serializer_data = PerevalSerializer(self.passage_1).data
        self.assertEquals(serializer_data, response.data)
        self.assertEquals(status.HTTP_200_OK, response.status_code)

    def test_get_list_email_arg(self):
        response = self.client.get('/Pereval/?user__email=test@example.com')
        serializer_data = PerevalSerializer([self.passage_1], many=True).data
        self.assertEquals(response.data, serializer_data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 1)

    def test_pereval_create(self):
        url = reverse('pereval-list')
        data = {
            'user': {
                'fam': 'hhhh',
                'name': 'hhhh',
                'otc': 'sdfgh',
                'email': 'tqw@example.com',
                'phone': '88888888888'
            },
            "coords": {
                'latitude': 77,
                'longitude': 567,
                'height': 5879
            },
            "level": {
                "winter": "1A",
                "spring": "1A",
                "summer": "1A",
                "autumn": "1A"
            },
            "images": [
                {
                    "image": 'http://lagonaki-otdyh.ru/azishkij-pereval-03.jpg',
                    "title": "dfgh"
                }
            ],
            'beauty_title': 'dfgh',
            'title': 'fghm',
            'other_titles': 'ghjи',
            'connect': 'cvbn'
        }
        json_data = json.dumps(data)
        response = self.client.post(path=url, content_type='application/json', data=json_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

