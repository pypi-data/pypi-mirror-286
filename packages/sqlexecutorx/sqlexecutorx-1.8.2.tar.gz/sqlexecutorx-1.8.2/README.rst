Usage Sample
''''''''''''

.. code::

       import sqlexecutorx as db

       if __name__ == '__main__':
          db.init('test.db', driver='sqlite3', debug=True)

          # or
          db.init("postgres://user:password@127.0.0.1:5432/testdb", driver='psycopg2', pool_size=5, debug=True)

          # or
          db.init(host='127.0.0.1', port='5432', user='xxx', password='xxx', database='testdb', driver='psycopg2')

          # if driver is 'pymysql' or 'mysql.connector' of MySQL, the select_key is 'SELECT LAST_INSERT_ID()'
          select_key = "SELECT currval('person_id_seq')"

          id = db.save(select_key, 'INSERT INTO person(name, age) VALUES(%s,%s)', 'wangwu', 38)

          persons = db.select('select id, name, age from person')
          # result:
          # (3, 'zhangsan', 15)
          # (4, 'lisi', 26)
          # (5, 'wangwu', 38)
          # (6, 'zhaoliu', 45)

          persons = db.select_one('select id, name, age from person where name = %s', 'zhangsan')
          # result:
          # (3, 'zhangsan', 15)

          args = [
           ('李四', 55),
           ('王五', 35),
          ]
          db.batch_execute('INSERT INTO person(name,age) VALUES(%s,%s)', *args)

          db.close()

Transaction
''''''''''''

.. code::

       from sqlexecutorx import trans

       @trans
       def test_transaction():
          insert_func(....)
          update_func(....)


       def test_transaction2():
          with trans():
              insert_func(....)
              update_func(....)
