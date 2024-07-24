Usage Sample
''''''''''''

.. code:: python

    from sqlormx import Model, db
    from dataclasses import dataclass

    @dataclass
    class Person(Model):
        __table__ = 'person'
        id: int = None
        name: str = None
        age: int = None

    if __name__ == '__main__':
        db.init('test.db', driver='sqlite3', show_sql=True, debug=True)
        db.init_db("postgres://user:password@127.0.0.1:5432/testdb", driver='psycopg2', pool_size=5)
        db.init_db(host='127.0.0.1', port='3306', user='xxx', password='xxx', database='test', pool_size=5, show_sql=True)

        effected_rowcount = Person.insert(name='tianqi', age=77)

        persons = Person.query(name='tianqi')
        # select id, name, age from person where name = :name
        # result:
        # {'id': 7, 'name': 'tianqi', 'age': 77}

        persons = Person.query(name__eq='zhangsan')
        # select id, name, age from person where name = :name
        # result:
        # [{'id': 3, 'name': 'zhangsan', 'age': 15}]

Transaction
'''''''''''

.. code:: python

    from sqlormx import trans

    @trans
    def test_transaction():
        insert_func(....)
        update_func(....)


    def test_transaction2():
        with trans():
            insert_func(....)
            update_func(....)


If you want to operate MySQL database, may be you need MySqlx: https://pypi.org/project/mysqlx

If you want to operate PostgreSQL database, may be you need MySqlx: https://pypi.org/project/pgsqlx

If you just wanted a simple sql executor, may be you need sqlx-exec: https://pypi.org/project/sqlexecx
