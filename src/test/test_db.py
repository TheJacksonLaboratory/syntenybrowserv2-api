import unittest
from src.test import BaseDBTestCase

class DbConnectionTest(BaseDBTestCase):

    def test_db(self):
        with self.engine.connect() as conn:
            self.assertFalse(conn.closed)


from src.app.model.hello_world_model import Hello, HelloSchema

class SqlalchemyHelloModelTest(BaseDBTestCase):

    def setUp(self):
        self.common_names = ("Liam", "Noah", "William", "James", "Logan")
        hellos = [Hello(who=name) for name in self.common_names]
        self.session.bulk_save_objects(hellos)
        self.session.commit()

    def test_get_hellos(self):
        hellos = Hello.query.all()
        self.assertTrue(len(hellos) is 5)
        for hello in hellos:
            serialized = HelloSchema().dump(hello)
            self.assertTrue(serialized.data['who'] in self.common_names)

    def test_get_hello_by_name(self):
        hello = Hello.query.filter_by(who=self.common_names[0]).first()
        self.assertTrue(hello is not None)
        self.assertEqual(hello.who, self.common_names[0])

    def test_query_nonexistant_hello(self):
        hello = Hello.query.filter_by(who="John").first()
        self.assertEqual(hello, None)

    def test_update_hello(self):
        hello = Hello.query.filter_by(who=self.common_names[2]).first()
        hello.who = "Bill"
        self.session.commit()
        hello_bill = Hello.query.filter_by(who="Bill").first()
        self.assertEqual(hello_bill.who, "Bill")

    def test_delete_model(self):
        Hello.query.delete()
        self.session.commit()
        hellos = Hello.query.all()
        self.assertEqual(len(hellos), 0)

    def tearDown(self):
        Hello.query.delete()
        self.session.commit()
        self.session.remove()


if __name__ == '__main__':
    unittest.main()
