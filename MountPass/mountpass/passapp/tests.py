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
                winter='2A',
                spring='2A',
                summer='2A',
                autumn='2A'
            ),
            beauty_title='Очередной перевал',
            title='Азишский',
            other_titles='Лагонаки',
            connect='хребет'
        )
        self.image_1 = Images.objects.create(
            pereval=self.passage_1,
            title='some title',
            image='http://lagonaki-otdyh.ru/azishkij-pereval-03.jpg'
        )

        self.passage_2 = PerevalAdded.objects.create(
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
                winter='3A',
                spring='3A',
                summer='3A',
                autumn='3A'
            ),
            beauty_title='Еще один перевал',
            title='Путешественников',
            other_titles='Пик Ленина',
            connect='верховья ручь'
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

    def test_pereval_update(self):
        url = reverse('pereval-detail', args=(self.passage_1.id,))
        data = {
            'user': {
                'fam': 'Петров',
                'name': 'Петр',
                'otc': 'Петрович',
                'email': 'test@example.com',
                'phone': '89997776655'
            },
            "coords": {
                'latitude': 55.4,
                'longitude': 77.6,
                'height': 1000
            },
            "level": {
                "winter": "1A",
                "spring": "2A",
                "summer": "2A",
                "autumn": "2A"
            },
            "images": [
                {
                    "data": 'http://lagonaki-otdyh.ru/azishkij-pereval-03.jpg',
                    "title": "some title"
                }
            ],
            'beauty_title': 'Перевал изменен',
            'title': 'Азишский',
            'other_titles': 'Лагонаки',
            'connect': 'хребет'
        }
        json_data = json.dumps(data)
        response = self.client.patch(path=url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.passage_1.refresh_from_db()
        self.assertEqual('Перевал изменен', self.passage_1.beauty_title)
        self.assertEqual('1a', self.passage_1.level.winter)
        self.assertEqual(1000, self.passage_1.coordinates.height)

    # def test_user_update(self):
    #     url = reverse("pereval-detail", args=(self.pereval_1.id,))
    #     data = {
    #         "id": 6,
    #         "beauty_title": "perev.2",
    #         "title": "123gora2",
    #         "other_titles": "pereval2",
    #         "connect": "connect2",
    #         "user": {
    #             "email": "try@try.ru",
    #             "fam": "Изменено",
    #             "name": "Изменено",
    #             "otc": "Изменено",
    #             "phone": "Изменено"
    #         },
    #         "coords": {
    #             "latitude": "45.38420000",
    #             "longitude": "7.15250000",
    #             "height": 1200
    #         },
    #         "images": [
    #             {
    #                 "image": "https://www.yandex.ru/search.jpg",
    #                 "title": "Седловина"
    #             },
    #             {
    #                 "image": "https://www.yandex.ru/search.jpg",
    #                 "title": "Подъём"
    #             }
    #         ],
    #     }
    #     json_data = json.dumps(data)
    #     response = self.client.patch(path=url, content_type='application/json', data=json_data)
    #     self.assertEquals(status.HTTP_200_OK, response.status_code)
    #     self.pereval_1.refresh_from_db()
    #     self.assertEquals("try@try.ru", self.pereval_1.user.email)
    #     self.assertEquals("Петров", self.pereval_1.user.fam)
    #     self.assertEquals("Петр", self.pereval_1.user.name)
    #     self.assertEquals("Петрович", self.pereval_1.user.otc)

    # def test_pereval_update(self):
    #     url = reverse("pereval-detail", args=(self.pereval_1.id,))
    #     data = {
    #         "id": 6,
    #         "beauty_title": "Изменено",
    #         "title": "Изменено",
    #         "other_titles": "Изменено",
    #         "connect": "Изменено",
    #         "user": {
    #             "email": "try@try.ru",
    #             "fam": "Петров",
    #             "name": "Петр",
    #             "otc": "Петрович",
    #             "phone": "88005553535"
    #         },
    #         "coords": {
    #             "latitude": "45.38420000",
    #             "longitude": "7.15250000",
    #             "height": 1200
    #         },
    #         "images": [
    #             {
    #                 "image": "https://www.yandex.ru/search.jpg",
    #                 "title": "Седловина"
    #             },
    #             {
    #                 "image": "https://www.yandex.ru/search.jpg",
    #                 "title": "Подъём"
    #             }
    #         ],
    #     }
    #     json_data = json.dumps(data)
    #     response = self.client.patch(path=url, content_type='application/json', data=json_data)
    #     self.assertEquals(status.HTTP_200_OK, response.status_code)
    #     self.pereval_1.refresh_from_db()
    #     self.assertEquals("Изменено", self.pereval_1.beauty_title)


# class PerevalSerializerTestCase(TestCase):
#     def setUp(self):
#         self.user_1 = MyUser.objects.create(email="try@try.ru", fam="Петрров", name="Петр", otc="Петрович",
#                                            phone="88005553535")
#         self.coords_1 = Coord.objects.create(latitude=45.3842, longitude=7.1525, height=1200)
#         self.level_1 = Level.objects.create(winter="1A", summer="1A", autumn="1A", spring="1A", )
#         self.pereval_1 = PerevalAdded.objects.create(beauty_title="perev.", title="123gora", other_titles="pereval",
#                                                 connect="connect", user=self.user_1, coords=self.coords_1,
#                                                 level=self.level_1, )
#         self.images_1 = Images.objects.create(pereval=self.pereval_1, image="https://www.yandex.ru/search.jpg",
#                                               title="Седловина")
#         self.images_1_2 = Images.objects.create(pereval=self.pereval_1, image="https://www.yandex.ru/search.jpg",
#                                                 title="Подъём")
#
#     def test_check(self):
#         serializer_data = PerevalSerializer(self.pereval_1).data
#         expected_data = {
#             "id": 5,
#             "beauty_title": "perev.",
#             "title": "123gora",
#             "other_titles": "pereval",
#             "connect": "connect",
#             "user": {
#                 "email": "try@try.ru",
#                 "fam": "Петрров",
#                 "name": "Петр",
#                 "otc": "Петрович",
#                 "phone": "88005553535"
#             },
#             "coords": {
#                 "latitude": "45.38420000",
#                 "longitude": "7.15250000",
#                 "height": 1200
#             },
#             "level": {
#                 "winter": "1A",
#                 "summer": "1A",
#                 "autumn": "1A",
#                 "spring": "1A"
#             },
#             "images": [
#                 {
#                     "data": "https://www.yandex.ru/search.jpg",
#                     "title": "Седловина"
#                 },
#                 {
#                     "data": "https://www.yandex.ru/search.jpg",
#                     "title": "Подъём"
#                 }
#             ],
#             "status": "new"
#         }
#         self.assertEquals(serializer_data, expected_data)
