from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop, TestServer
from motor.motor_asyncio import AsyncIOMotorCollection
from models import MongoModel, NotFoundItem, Users, Rooms, Messages
import asyncio
import unittest
import app


class ABCTestCase(AioHTTPTestCase):

    def get_app(self):
        return app.get_app()


class ABCModelTestCase(ABCTestCase):

    def get_app(self):
        _app = super().get_app()
        self.db = _app.client.test_db
        return _app

    def tearDown(self):
        async def drop_collection():
            await self.mongo_model.collection.drop()

        self.loop.run_until_complete(drop_collection())
        super().tearDown()


class MongoModelTestCase(ABCModelTestCase):

    def setUp(self):
        super().setUp()
        self.mongo_model = MongoModel(self.db, 'items')

    @unittest_run_loop
    async def test_model_get_error(self):
        with self.assertRaises(NotFoundItem):
            await self.mongo_model.get({'_id': "_"})

    @unittest_run_loop
    async def test_model_insert_get(self):
        test_doc = {'user': 'User'}
        item = await self.mongo_model.insert(test_doc)
        item_get = await self.mongo_model.get(item.inserted_id)
        self.assertEqual(item_get['user'], test_doc['user'])


class UsersModelTestCase(ABCModelTestCase):

    def setUp(self):
        super().setUp()
        self.mongo_model = Users(self.db, 'users')

    @unittest_run_loop
    async def test_get_by_session_raise_error(self):
        with self.assertRaises(NotFoundItem):
            await self.mongo_model.get_by_session_id("awdj392jr")

    @unittest_run_loop
    async def test_get_by_session_id(self):
        session_id = "md3i232od"
        await self.mongo_model.insert({'session_id': session_id})
        user = await self.mongo_model.get_by_session_id(session_id)
        self.assertEqual(user['session_id'], session_id)


class RoomModelTestCase(ABCModelTestCase):

    def setUp(self):
        super().setUp()
        self.mongo_model = Rooms(self.db, 'rooms')

    @unittest_run_loop
    async def test_private_authenticate_fail(self):
        room = await self.mongo_model.insert({'password': '1234'})
        room_get = await self.mongo_model.authenticate(room.inserted_id, '')
        self.assertFalse(room_get)

    @unittest_run_loop
    async def test_private_authenticate(self):
        room = await self.mongo_model.insert({'password': '123'})
        room_get = await self.mongo_model.authenticate(room.inserted_id, '123')
        self.assertEqual(room_get['_id'], room.inserted_id)

    @unittest_run_loop
    async def test_authenticate(self):
        room = await self.mongo_model.insert({})
        room_get = await self.mongo_model.authenticate(room.inserted_id)
        self.assertEqual(room_get['_id'], room.inserted_id)


class MessageModelTestCase(ABCModelTestCase):

    def setUp(self):
        super().setUp()
        self.mongo_model = Messages(self.db, 'messages')


    @unittest_run_loop
    async def test_insert_and_get_by_room_id(self):
        room_id = '123'
        count = 10
        for i in range(count):
            await self.mongo_model.insert({'room_id': room_id})
        msgs = await self.mongo_model.get_by_room_id(room_id)
        self.assertEqual(len(msgs), count)


class MemberModelTestCase(ABCModelTestCase):
    pass


        





    
# class MyAppTestCase(SelfAioHTTPTestCase):

#     def test_one(self):
#         assert 2 == 2

#     # the unittest_run_loop decorator can be used in tandem with
#     # the AioHTTPTestCase to simplify running
#     # tests that are asynchronous
#     @unittest_run_loop
#     async def test_example(self):
#         request = await self.client.request("GET", "/")
#         assert request.status == 200
#         text = await request.text()
#         assert "Hello, world" in text

#     # a vanilla example
#     def test_example2(self):
#         async def test_get_route():
#             url =  "/"
#             resp = await self.client.request("GET", url)
#             self.assertEqual(resp.status, 200)
#             text = await resp.text()
#             self.assertIn("Hello, world", text)

#         self.loop.run_until_complete(test_get_route())


if __name__ == '__main__':
    unittest.main(verbosity=2, exit=True)
