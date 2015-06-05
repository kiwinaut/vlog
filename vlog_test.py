import unittest
from vlog_model import VlogModel as model
from datetime import date

class TestModelMethods(unittest.TestCase):

    def test_get_show_list_towatch(self):
        db = model(':memory:')
        data = [
                (None, 'dinosour', 'abc', None, date(2015,5,28),1),
                (None, 'sqlite', 'abc', None, date(2015,5,27),1),
                (None, 'option', 'abc', None, date(2015,5,26),1),
                (None, 'justtitle', None, None, date(2015,5,26),1),
        ]
        season = [
                (None, 1, date(2015,5,11),1),
        ]  
        episodes = [
        ]  
        db.create_empty_db()
        for t in data:
            db.insert_show(t)
        for t in season:
            db.insert_season(t)
        for t in episodes:
            db.insert_episode(t)

        result = db.get_show_list_towatch()
        expected =[
                (2, u'sqlite', None, None, date(2015,5,27),1),
                (3, u'option', None, None, date(2015,5,26),1),
                (4, u'justtitle', None, None, date(2015,5,26),1),
        ]
        self.assertEqual(result, expected)



    def test_get_show_list_completed(self):
        db = model(':memory:')
        data = [
                (None, 'dinosour', 'abc', None, date(2015,5,28),1),
                (None, 'sqlite', 'abc', None, date(2015,5,27),1),
                (None, 'option', 'abc', None, date(2015,5,26),1),
                (None, 'justtitle', None, None, date(2015,5,26),1),
                (None, 'justanother', None, None, date(2015,5,25),1),
        ]
        season = [
                (None, 1, date(2015,5,11),1),
                (None, 2, date(2015,5,12),1),
                (None, 3, date(2015,5,13),1),
                (None, 1, date(2015,5,14),2),
                (None, 2, date(2015,5,15),2),
                (None, 1, date(2015,5,16),3),
                (None, 4, date(2015,5,18),5),
                (None, 1, date(2015,5,19),5),
                (None, 3, date(2015,5,19),5),  
                (None, 2, date(2015,5,19),5),
        ]  
        episodes = [
                (11, date(2015,5,11),3),
                (13, date(2015,7,19),3),
                (1, date(2015,7,19),5),
        ]  
        db.create_empty_db()
        for t in data:
            db.insert_show(t)
        for t in season:
            db.insert_season(t)
        for t in episodes:
            db.insert_episode(t)

        result = db.get_show_list_completed()
        expected =[
                (3, u'option', 1, None, date(2015,5,16),1),
                (5, u'justanother',3, None, date(2015,5,19),1),
        ]
        self.assertEqual(result, expected)

    def test_get_show_list_active(self):
        db = model(':memory:')
        data = [
                (None, 'dinosour', 'abc', None, date(2015,5,28),1),
                (None, 'sqlite', 'abc', None, date(2015,5,27),1),
                (None, 'option', 'abc', None, date(2015,5,26),1),
                (None, 'justtitle', None, None, date(2015,5,26),1),
                (None, 'justanother', None, None, date(2015,5,25),1),
        ]
        season = [
                (None, 2, date(2015,5,12),1),
                (None, 3, date(2015,5,13),1),
                (None, 4, date(2015,5,13),1),
                (None, 1, date(2015,5,13),1),
                (None, 1, date(2015,5,14),2),
                (None, 2, date(2015,5,15),2),
                (None, 1, date(2015,5,16),3),
                (None, 4, date(2015,5,18),5),
                (None, 3, date(2015,5,19),5),  
                (None, 2, date(2015,5,19),5),
        ]  
        episodes = [
                (14, date(2015,7,17),3),
                (10, date(2015,7,18),3),
                (13, date(2015,7,18),3),
                (11, date(2015,7,18),3),
                (1, date(2015,7,19),6),
        ]  
        db.create_empty_db()
        for t in data:
            db.insert_show(t)
        for t in season:
            db.insert_season(t)
        for t in episodes:
            db.insert_episode(t)

        result = db.get_show_list_active()
        expected =[
                (1, u'dinosour', 4, 13, date(2015,7,18),1),
                (2, u'sqlite',2, 1, date(2015,7,19),1),
        ]
        self.assertEqual(result, expected)



    def test_get_show_list(self):
        db = model(':memory:')
        data = [
                (None, 'dinosour', 'abc', None, date(2015,5,28),1),
                (None, 'sqlite', 'abc', None, date(2015,5,27),1),
                (None, 'option', 'abc', None, date(2015,5,26),1),
                (None, 'justtitle', None, None, date(2015,5,26),1),
                (None, 'justanother', None, None, date(2015,5,25),1),
        ]
        season = [
                (None, 2, date(2015,5,12),1),
                (None, 3, date(2015,5,13),1),
                (None, 4, date(2015,5,13),1),
                (None, 1, date(2015,5,13),1),
                (None, 1, date(2015,5,14),2),
                (None, 2, date(2015,5,15),2),
                (None, 1, date(2015,5,16),3),
                (None, 4, date(2015,5,18),5),
                (None, 3, date(2015,5,19),5),  
                (None, 2, date(2015,5,19),5),
        ]  
        episodes = [
                (14, date(2015,7,17),3),
                (10, date(2015,7,18),3),
                (13, date(2015,7,18),3),
                (11, date(2015,7,18),3),
                (1, date(2015,7,19),6),
        ]  
        db.create_empty_db()
        for t in data:
            db.insert_show(t)
        for t in season:
            db.insert_season(t)
        for t in episodes:
            db.insert_episode(t)

        result = db.get_show_list()
        expected =[
                (3, u'option', 1, None, date(2015,5,16),1),
                (5, u'justanother', 3, None, date(2015,5,19),1),
                (1, u'dinosour', 4, 13, date(2015,7,18),1),
                (2, u'sqlite',2, 1, date(2015,7,19),1),
                (4, u'justtitle',None, None, date(2015,5,26),1),
        ]
        self.assertEqual(result, expected)





    def test_search(self):
        db = model(':memory:')
        data = [
                (None, 'jdinosour', 'abc', None, date(2015,5,28),1),
                (None, 'sqlite', 'abc', None, date(2015,5,27),1),
                (None, 'option', 'abc', None, date(2015,5,26),1),
                (None, 'justtitle', None, None, date(2015,5,26),1),
                (None, 'justanother', None, None, date(2015,5,25),1),
        ]
        season = [
                (None, 2, date(2015,5,12),1),
                (None, 3, date(2015,5,13),1),
                (None, 4, date(2015,5,13),1),
                (None, 1, date(2015,5,13),1),
                (None, 1, date(2015,5,14),2),
                (None, 2, date(2015,5,15),2),
                (None, 1, date(2015,5,16),3),
                (None, 4, date(2015,5,18),5),
                (None, 3, date(2015,5,19),5),  
                (None, 2, date(2015,5,19),5),
        ]  
        episodes = [
                (14, date(2015,7,17),3),
                (10, date(2015,7,18),3),
                (13, date(2015,7,18),3),
                (11, date(2015,7,18),3),
                (1, date(2015,7,19),6),
        ]  
        db.create_empty_db()
        for t in data:
            db.insert_show(t)
        for t in season:
            db.insert_season(t)
        for t in episodes:
            db.insert_episode(t)

        result = db.search('j')
        expected =[
                (1, u'jdinosour', 4, 13, date(2015,7,18),1),
                (4, u'justtitle',None, None, date(2015,5,26),1),
                (5, u'justanother', 3, None, date(2015,5,19),1),
        ]
        self.assertEqual(result, expected)
        
        
        
        
    def test_get_show(self):
        db = model(':memory:')
        data = [
                (None, 'jdinosour', 'abc', None, date(2015,5,28),1),
                (None, 'sqlite', 'abc', None, date(2015,5,27),1),
                (None, 'option', 'abc', None, date(2015,5,26),1),
                (None, 'justtitle', None, None, date(2015,5,26),1),
                (None, 'justanother', None, None, date(2015,5,25),1),
        ]
        season = [
                (None, 2, date(2015,5,12),1),
                (None, 3, date(2015,5,13),1),
                (None, 4, date(2015,5,13),1),
                (None, 1, date(2015,5,13),1),
                (None, 1, date(2015,5,14),2),
                (None, 2, date(2015,5,15),2),
                (None, 1, date(2015,5,16),3),
                (None, 4, date(2015,5,18),5),
                (None, 3, date(2015,5,19),5),  
                (None, 2, date(2015,5,19),5),
        ]  
        episodes = [
                (14, date(2015,7,17),3),
                (10, date(2015,7,18),3),
                (13, date(2015,7,18),3),
                (11, date(2015,7,18),3),
                (1, date(2015,7,19),6),
        ]  
        db.create_empty_db()
        for t in data:
            db.insert_show(t)
        for t in season:
            db.insert_season(t)
        for t in episodes:
            db.insert_episode(t)

        result = db.get_show(1)
        expected =[
                (1, u'jdinosour', 4, 13, date(2015,7,18),1),
        ]
        self.assertEqual(result, expected)
        result = db.get_show(4)
        expected =[
                (4, u'justtitle',None, None, date(2015,5,26),1),
        ]
        self.assertEqual(result, expected)
        result = db.get_show(5)
        expected =[
                (5, u'justanother', 3, None, date(2015,5,19),1),
        ]
        self.assertEqual(result, expected)





    def test_get_show_deep(self):
        db = model(':memory:')
        data = [
                (None, 'jdinosour', 'abc', None, date(2015,5,28),1),
                (None, 'sqlite', 'abc', None, date(2015,5,27),1),
                (None, 'option', 'abc', None, date(2015,5,26),1),
                (None, 'justtitle', None, None, date(2015,5,26),1),
                (None, 'justanother', None, None, date(2015,5,25),1),
        ]
        season = [
                (None, 2, date(2015,5,12),1),
                (None, 3, date(2015,5,13),1),
                (None, 4, date(2015,5,13),1),
                (None, 1, date(2015,5,13),1),
                (None, 1, date(2015,5,14),2),
                (None, 2, date(2015,5,15),2),
                (None, 1, date(2015,5,16),3),
                (None, 4, date(2015,5,18),5),
                (None, 3, date(2015,5,19),5),  
                (None, 2, date(2015,5,19),5),
        ]  
        episodes = [
                (14, date(2015,7,17),3),
                (10, date(2015,7,18),3),
                (13, date(2015,7,18),3),
                (11, date(2015,7,18),3),
                (1, date(2015,7,19),6),
        ]  
        db.create_empty_db()
        for t in data:
            db.insert_show(t)
        for t in season:
            db.insert_season(t)
        for t in episodes:
            db.insert_episode(t)

        result = db.get_show_deep(1)
        #print result
        expected =[
                u'jdinosour', u'abc', None, date(2015,5,28),1,
                    [(2, date(2015,5,12),[]),
                        (3, date(2015,5,13),[]),
                        (4, date(2015,5,13),[
                            (14, date(2015,7,17)),
                            (10, date(2015,7,18)),
                            (13, date(2015,7,18)),
                            (11, date(2015,7,18))]),
                        (1, date(2015,5,13),[])
                    ]]
        self.assertEqual(result, expected)




    def test_set_season_done(self):
        db = model(':memory:')
        data = [
                (None, 'jdinosour', 'abc', None, date(2015,5,28),1),
                (None, 'sqlite', 'abc', None, date(2015,5,27),1),
                (None, 'option', 'abc', None, date(2015,5,26),1),
                (None, 'justtitle', None, None, date(2015,5,26),1),
                (None, 'justanother', None, None, date(2015,5,25),1),
        ]
        season = [
                (None, 2, date(2015,5,12),1),
                (None, 3, date(2015,5,13),1),
                (None, 4, date(2015,5,13),1),
                (None, 1, date(2015,5,13),1),
                (None, 1, date(2015,5,14),2),
                (None, 2, date(2015,5,15),2),
                (None, 1, date(2015,5,16),3),
                (None, 4, date(2015,5,18),5),
                (None, 3, date(2015,5,19),5),  
                (None, 2, date(2015,5,19),5),
        ]  
        episodes = [
                (14, date(2015,7,17),3),
                (10, date(2015,7,18),3),
                (13, date(2015,7,18),3),
                (11, date(2015,7,18),3),
                (1, date(2015,7,19),6),
        ]  
        db.create_empty_db()
        for t in data:
            db.insert_show(t)
        for t in season:
            db.insert_season(t)
        for t in episodes:
            db.insert_episode(t)

        db.set_season_done(1, 4)
        #print result
        db.cur.execute('''SELECT * FROM episodes''')
        result = db.cur.fetchall()
        expected =[(1, date(2015,7,19),6)]
        self.assertEqual(result, expected)


    def test_set_season_done2(self):
        db = model(':memory:')
        data = [
                (None, 'jdinosour', 'abc', None, date(2015,5,28),1),
                (None, 'sqlite', 'abc', None, date(2015,5,27),1),
                (None, 'option', 'abc', None, date(2015,5,26),1),
                (None, 'justtitle', None, None, date(2015,5,26),1),
                (None, 'justanother', None, None, date(2015,5,25),1),
        ]
        season = [
                (None, 2, date(2015,5,12),1),
                (None, 3, date(2015,5,13),1),
                (None, 4, date(2015,5,13),1),
                (None, 1, date(2015,5,13),1),
                (None, 1, date(2015,5,14),2),
                (None, 2, date(2015,5,15),2),
                (None, 1, date(2015,5,16),3),
                (None, 4, date(2015,5,18),5),
                (None, 3, date(2015,5,19),5),  
                (None, 2, date(2015,5,19),5),
        ]  
        episodes = [
                (14, date(2015,7,17),3),
                (10, date(2015,7,18),3),
                (13, date(2015,7,18),3),
                (11, date(2015,7,18),3),
                (1, date(2015,7,19),6),
        ]  
        db.create_empty_db()
        for t in data:
            db.insert_show(t)
        for t in season:
            db.insert_season(t)
        for t in episodes:
            db.insert_episode(t)

        db.set_season_done(2, 2)
        db.cur.execute('''SELECT * FROM episodes''')
        result = db.cur.fetchall()
        expected =[
                (14, date(2015,7,17),3),
                (10, date(2015,7,18),3),
                (13, date(2015,7,18),3),
                (11, date(2015,7,18),3)]
        self.assertEqual(result, expected)

    def test_delete_show(self):
        db = model(':memory:')
        data = [
                (None, 'jdinosour', 'abc', None, date(2015,5,28),1),
                (None, 'sqlite', 'abc', None, date(2015,5,27),1),
                (None, 'option', 'abc', None, date(2015,5,26),1),
                (None, 'justtitle', None, None, date(2015,5,26),1),
                (None, 'justanother', None, None, date(2015,5,25),1),
        ]
        season = [
                (None, 2, date(2015,5,12),1),
                (None, 3, date(2015,5,13),1),
                (None, 4, date(2015,5,13),1),
                (None, 1, date(2015,5,13),1),
                (None, 1, date(2015,5,14),2),
                (None, 2, date(2015,5,15),2),
                (None, 1, date(2015,5,16),3),
                (None, 4, date(2015,5,18),5),
                (None, 3, date(2015,5,19),5),  
                (None, 2, date(2015,5,19),5),
        ]  
        episodes = [
                (14, date(2015,7,17),3),
                (10, date(2015,7,18),3),
                (13, date(2015,7,18),3),
                (11, date(2015,7,18),3),
                (1, date(2015,7,19),6),
        ]  
        db.create_empty_db()
        for t in data:
            db.insert_show(t)
        for t in season:
            db.insert_season(t)
        for t in episodes:
            db.insert_episode(t)

        db.delete_show(2)

        db.cur.execute('''SELECT * FROM shows''')
        result = db.cur.fetchall()
        expected =[
                (1, 'jdinosour', 'abc', None, date(2015,5,28),1),
                (3, 'option', 'abc', None, date(2015,5,26),1),
                (4, 'justtitle', None, None, date(2015,5,26),1),
                (5, 'justanother', None, None, date(2015,5,25),1),
        ]
        self.assertEqual(result, expected)

        db.cur.execute('''SELECT * FROM seasons''')
        result = db.cur.fetchall()
        expected =[
                (1, 2, date(2015,5,12),1),
                (2, 3, date(2015,5,13),1),
                (3, 4, date(2015,5,13),1),
                (4, 1, date(2015,5,13),1),
                (7, 1, date(2015,5,16),3),
                (8, 4, date(2015,5,18),5),
                (9, 3, date(2015,5,19),5),  
                (10, 2, date(2015,5,19),5),
        ]
        self.assertEqual(result, expected)

        db.cur.execute('''SELECT * FROM episodes''')
        result = db.cur.fetchall()
        expected =[
                (14, date(2015,7,17),3),
                (10, date(2015,7,18),3),
                (13, date(2015,7,18),3),
                (11, date(2015,7,18),3)]
        self.assertEqual(result, expected)

    def test_delete_show_season(self):
        db = model(':memory:')
        data = [
                (None, 'jdinosour', 'abc', None, date(2015,5,28),1),
                (None, 'sqlite', 'abc', None, date(2015,5,27),1),
                (None, 'option', 'abc', None, date(2015,5,26),1),
                (None, 'justtitle', None, None, date(2015,5,26),1),
                (None, 'justanother', None, None, date(2015,5,25),1),
        ]
        season = [
                (None, 2, date(2015,5,12),1),
                (None, 3, date(2015,5,13),1),
                (None, 4, date(2015,5,13),1),
                (None, 1, date(2015,5,13),1),
                (None, 1, date(2015,5,14),2),
                (None, 2, date(2015,5,15),2),
                (None, 1, date(2015,5,16),3),
                (None, 4, date(2015,5,18),5),
                (None, 3, date(2015,5,19),5),  
                (None, 2, date(2015,5,19),5),
        ]  
        episodes = [
                (14, date(2015,7,17),3),
                (10, date(2015,7,18),3),
                (13, date(2015,7,18),3),
                (11, date(2015,7,18),3),
                (1, date(2015,7,19),6),
        ]  
        db.create_empty_db()
        for t in data:
            db.insert_show(t)
        for t in season:
            db.insert_season(t)
        for t in episodes:
            db.insert_episode(t)

        db.delete_show_season(5, 4)
        db.delete_show_season(1, 4)

        db.cur.execute('''SELECT * FROM seasons''')
        result = db.cur.fetchall()
        expected =[
                (1, 2, date(2015,5,12),1),
                (2, 3, date(2015,5,13),1),
                (4, 1, date(2015,5,13),1),
                (5, 1, date(2015,5,14),2),
                (6, 2, date(2015,5,15),2),
                (7, 1, date(2015,5,16),3),
                (9, 3, date(2015,5,19),5),  
                (10, 2, date(2015,5,19),5),
        ]
        self.assertEqual(result, expected)

        db.cur.execute('''SELECT * FROM episodes''')
        result = db.cur.fetchall()
        expected =[
                (1, date(2015,7,19),6)]
        self.assertEqual(result, expected)



    def test_delete_show_episodes(self):
        db = model(':memory:')
        data = [
                (None, 'jdinosour', 'abc', None, date(2015,5,28),1),
                (None, 'sqlite', 'abc', None, date(2015,5,27),1),
                (None, 'option', 'abc', None, date(2015,5,26),1),
                (None, 'justtitle', None, None, date(2015,5,26),1),
                (None, 'justanother', None, None, date(2015,5,25),1),
        ]
        season = [
                (None, 2, date(2015,5,12),1),
                (None, 3, date(2015,5,13),1),
                (None, 4, date(2015,5,13),1),
                (None, 1, date(2015,5,13),1),
                (None, 1, date(2015,5,14),2),
                (None, 2, date(2015,5,15),2),
                (None, 1, date(2015,5,16),3),
                (None, 4, date(2015,5,18),5),
                (None, 3, date(2015,5,19),5),  
                (None, 2, date(2015,5,19),5),
        ]  
        episodes = [
                (14, date(2015,7,17),3),
                (10, date(2015,7,18),3),
                (13, date(2015,7,18),3),
                (11, date(2015,7,18),3),
                (1, date(2015,7,19),6),
        ]  
        db.create_empty_db()
        for t in data:
            db.insert_show(t)
        for t in season:
            db.insert_season(t)
        for t in episodes:
            db.insert_episode(t)

        db.delete_show_episode(2, 2, 1)
        db.delete_show_episode(1, 4, 10)
        db.delete_show_episode(1, 4, 13)

        db.cur.execute('''SELECT * FROM episodes''')
        result = db.cur.fetchall()
        expected =[
                (14, date(2015,7,17),3),
                (11, date(2015,7,18),3)]
        self.assertEqual(result, expected)
if __name__ == "__main__":
    unittest.main()
