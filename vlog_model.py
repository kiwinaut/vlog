import sqlite3, os
from datetime import date
from gi.repository import GObject
import assets_vlog
from collections import namedtuple

Row = namedtuple('Row', ['id', 'title', 'season', 'episode', 'date'])
def namedtuple_factory(cursor, row):
    return Row(*row)

class DateMax:
    def __init__(self):
        self.max = None
    def step(self, value):
        if self.max == None:
            self.max = value
        if value > self.max:
            self.max = value
    def finalize(self):
        return self.max


class VlogModel(GObject.GObject):
    __gsignals__ = {'error': (GObject.SIGNAL_RUN_FIRST, None,(str,))}

    def __init__(self, name = None):
        GObject.GObject.__init__(self)
        self.db_name = assets_vlog.Assets.get_db() if name == None else name
        self.last_show_row_id = None
        self.ERROR = 'DB: '
        try:
            self.conn = sqlite3.connect(self.db_name, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
            #self.conn.row_factory = namedtuple_factory
            self.conn.create_aggregate('datemax', 1, DateMax)
            self.cur = self.conn.cursor()
        except sqlite3.Error as e:
            self.emit('error',e.args[0])


    def commit(self):
        self.conn.commit()

    def create_empty_db(self):
        #'''id, title, torrent, subtitle, date'''
        #'''id, season_number, season_complete, season_add_date, season_complete_date, show_id'''
        #'''episode_number, episode_add_date, season_id'''
        try:
            self.cur.execute('''
                    CREATE TABLE shows
                    (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        title TEXT UNIQUE NOT NULL, 
                        torrent TEXT, 
                        subtitle TEXT, 
                        date DATE,
                        tag INTEGER
                    )''')
            self.cur.execute('''
                    CREATE TABLE seasons
                    (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        number INTEGER, 
                        date DATE, 
                        show_id INTEGER
                    )''')
            self.cur.execute('''
                    CREATE UNIQUE INDEX sea_idx
                    ON seasons(number, show_id)
                    ''')
            self.cur.execute('''
                    CREATE TABLE episodes
                    (
                        number INTEGER, 
                        date DATE, 
                        season_id INTEGER
                    )''')
            self.cur.execute('''
                    CREATE UNIQUE INDEX epi_idx
                    ON episodes(number, season_id)
                    ''')
        except sqlite3.Error as e:
            print self.ERROR + e.args[0]



    
    def get_show_list_towatch(self):
        try:
            self.cur.execute('''
                SELECT shows.id, shows.title, NULL, NULL, shows.date, shows.tag
                FROM shows
                LEFT OUTER JOIN seasons
                ON seasons.show_id = shows.id 
                WHERE seasons.id IS NULL
            ''')
            result=self.cur.fetchall()
            return result
        except sqlite3.Error as e:
            self.emit('error',self.ERROR + e.args[0])

    def get_show_list_completed(self):
        try:
            self.cur.execute('''
                SELECT sh.id, sh.title, se2.number, NULL, se2.date, sh.tag
                FROM seasons AS se2
                LEFT OUTER JOIN episodes AS ep2
                    ON se2.id = ep2.season_id 
                JOIN shows AS sh
                    ON sh.id = se2.show_id
                    AND se2.id = (SELECT se3.id
                                   FROM seasons AS se3
                                   WHERE se3.date  = (SELECT se4.date
                                                        FROM seasons AS se4
                                                        WHERE se4.show_id  = sh.id
                                                        ORDER BY se4.date DESC
                                                        LIMIT 1
                                                        )
                                   AND se3.show_id = sh.id
                                   ORDER BY se3.number DESC
                                   LIMIT 1
                                   )
                WHERE ep2.number IS NULL
                AND se2.show_id NOT IN
                            (
                            SELECT DISTINCT se3.show_id
                            FROM seasons AS se3
                            LEFT OUTER JOIN episodes AS ep3
                                ON se3.id = ep3.season_id 
                            WHERE ep3.number IS NOT NULL
                            )
            ''')
            result=self.cur.fetchall()
            return result
        except sqlite3.Error as e:
            self.emit('error',self.ERROR + e.args[0])

    def get_show_list_active(self):
        try:
            self.cur.execute('''
                SELECT sh.id, sh.title, se.number, ep.number, ep.date, sh.tag
                FROM shows AS sh
                JOIN
                    seasons AS se
                    ON se.show_id = sh.id
                JOIN
                    episodes AS ep
                    ON ep.season_id = se.id
                    AND ep.number = (SELECT ep2.number
                                     FROM episodes AS ep2
                                     WHERE ep2.date = (SELECT ep3.date
                                                       FROM episodes AS ep3
                                                       WHERE ep3.season_id = se.id
                                                       ORDER BY ep3.date DESC
                                                       LIMIT 1
                                                       )
                                     AND ep2.season_id = se.id
                                     ORDER BY ep2.number DESC
                                     LIMIT 1
                                     )

            ''')
            result=self.cur.fetchall()
            return result
        except sqlite3.Error as e:
            self.emit('error',self.ERROR + e.args[0])

    def get_show_list(self):
        result = []
        result.extend(self.get_show_list_completed())
        result.extend(self.get_show_list_active())
        result.extend(self.get_show_list_towatch())
        return result

    def search(self, keyword):
        try:
            self.cur.execute('''
                SELECT sh.id, sh.title, se.number, ep.number, ep.date as "ep.date [DATE]", sh.tag
                FROM shows AS sh
                JOIN
                    seasons AS se
                    ON se.show_id = sh.id
                JOIN
                    episodes AS ep
                    ON ep.season_id = se.id
                    AND ep.number = (SELECT ep2.number
                                     FROM episodes AS ep2
                                     WHERE ep2.date = (SELECT ep3.date
                                                       FROM episodes AS ep3
                                                       WHERE ep3.season_id = se.id
                                                       ORDER BY ep3.date DESC
                                                       LIMIT 1
                                                       )
                                     AND ep2.season_id = se.id
                                     ORDER BY ep2.number DESC
                                     LIMIT 1
                                     )
                WHERE sh.title LIKE ?
                UNION
                SELECT sh.id, sh.title, se2.number, NULL, se2.date as "se2.date [DATE]", sh.tag
                FROM seasons AS se2
                LEFT OUTER JOIN episodes AS ep2
                    ON se2.id = ep2.season_id 
                JOIN shows AS sh
                    ON sh.id = se2.show_id
                    AND se2.id = (SELECT se3.id
                                   FROM seasons AS se3
                                   WHERE se3.date  = (SELECT se4.date
                                                        FROM seasons AS se4
                                                        WHERE se4.show_id  = sh.id
                                                        ORDER BY se4.date DESC
                                                        LIMIT 1
                                                        )
                                   AND se3.show_id = sh.id
                                   ORDER BY se3.number DESC
                                   LIMIT 1
                                   )
                WHERE ep2.number IS NULL
                AND sh.title LIKE ?
                AND se2.show_id NOT IN
                            (
                            SELECT DISTINCT se3.show_id
                            FROM seasons AS se3
                            LEFT OUTER JOIN episodes AS ep3
                                ON se3.id = ep3.season_id 
                            WHERE ep3.number IS NOT NULL
                            )
                UNION
                SELECT shows.id, shows.title, NULL, NULL, shows.date as "shows.date [DATE]", shows.tag
                FROM shows
                LEFT OUTER JOIN seasons
                ON seasons.show_id = shows.id 
                WHERE seasons.id IS NULL
                AND shows.title LIKE ?

            ''',(keyword + '%',keyword + '%',keyword + '%',))
            result=self.cur.fetchall()
            return result
        except sqlite3.Error as e:
            self.emit('error',self.ERROR + e.args[0])

    def get_show(self, id):
        try:
            self.cur.execute('''
                SELECT sh.id, sh.title, se.number, ep.number, ep.date as "ep.date [DATE]", sh.tag
                FROM shows AS sh
                JOIN
                    seasons AS se
                    ON se.show_id = sh.id
                JOIN
                    episodes AS ep
                    ON ep.season_id = se.id
                    AND ep.number = (SELECT ep2.number
                                     FROM episodes AS ep2
                                     WHERE ep2.date = (SELECT ep3.date
                                                       FROM episodes AS ep3
                                                       WHERE ep3.season_id = se.id
                                                       ORDER BY ep3.date DESC
                                                       LIMIT 1
                                                       )
                                     AND ep2.season_id = se.id
                                     ORDER BY ep2.number DESC
                                     LIMIT 1
                                     )
                WHERE sh.id = ?
                UNION
                SELECT sh.id, sh.title, se2.number, NULL, se2.date as "se2.date [DATE]", sh.tag
                FROM seasons AS se2
                LEFT OUTER JOIN episodes AS ep2
                    ON se2.id = ep2.season_id 
                JOIN shows AS sh
                    ON sh.id = se2.show_id
                    AND se2.id = (SELECT se3.id
                                   FROM seasons AS se3
                                   WHERE se3.date  = (SELECT se4.date
                                                        FROM seasons AS se4
                                                        WHERE se4.show_id  = sh.id
                                                        ORDER BY se4.date DESC
                                                        LIMIT 1
                                                        )
                                   AND se3.show_id = sh.id
                                   ORDER BY se3.number DESC
                                   LIMIT 1
                                   )
                WHERE ep2.number IS NULL
                AND sh.id = ?
                AND se2.show_id NOT IN
                            (
                            SELECT DISTINCT se3.show_id
                            FROM seasons AS se3
                            LEFT OUTER JOIN episodes AS ep3
                                ON se3.id = ep3.season_id 
                            WHERE ep3.number IS NOT NULL
                            )
                UNION
                SELECT shows.id, shows.title, NULL, NULL, shows.date as "shows.date [DATE]", shows.tag
                FROM shows
                LEFT OUTER JOIN seasons
                ON seasons.show_id = shows.id 
                WHERE seasons.id IS NULL
                AND shows.id = ?

            ''',(id, id, id,))
            result=self.cur.fetchall()
            return result
        except sqlite3.Error as e:
            self.emit('error',self.ERROR + e.args[0])


    def get_show_shallow(self, id):
        #'''data sample (title,torrent,subtitle,[(season1,[episodes,]), (season2,[episodes,]] )'''
        try:
            self.cur.execute('''
                    SELECT id, title, torrent, subtitle, date, tag 
                    FROM shows 
                    WHERE id=?
                    ''', (id,))
            title = self.cur.fetchone()
            return title
        except sqlite3.Error as e:
            self.emit('error',self.ERROR + e.args[0])

    def get_show_deep(self, id):
        #'''data sample (title,torrent,subtitle,[(season1,[episodes,]), (season2,[episodes,]] )'''
        try:
            self.cur.execute('''
                    SELECT id, title, torrent, subtitle, date, tag 
                    FROM shows 
                    WHERE id=?
                    ''', (id,))
            show = self.cur.fetchone()
            all = []
            all.extend(show)
            self.cur.execute('''
                    SELECT seasons.id, seasons.number, seasons.date 
                    FROM seasons 
                    WHERE show_id=?
                    ''', (id,))
            seasons = self.cur.fetchall()

            sealist = []
            for sea in seasons:
                '''[(1,d,[(11,d),(12,d)]),] '''
                self.cur.execute('''
                        SELECT episodes.number, episodes.date 
                        FROM episodes 
                        WHERE season_id=?
                        ''', (sea[0],))
                epis = self.cur.fetchall()
                unit = (sea[1],sea[2],epis)
                sealist.append(unit)
            all.append(sealist)
            return all

        except sqlite3.Error as e:
            self.emit('error',self.ERROR + e.args[0])

    def set_season_done(self, id, sea):
        self.delete_show_episodes(id, sea)

    def delete_show(self, id):
        try:
            self.cur.execute('''DELETE 
                                FROM shows 
                                WHERE id=?''', (id,))
            self.cur.execute('''DELETE 
                                FROM episodes 
                                WHERE season_id IN (
                                                    SELECT id
                                                    FROM seasons
                                                    WHERE show_id = ?
                                                    )
                                ''', (id,))
            self.cur.execute('''DELETE 
                                FROM seasons 
                                WHERE id IN (
                                            SELECT id
                                            FROM seasons
                                            WHERE show_id = ?
                                            )
                                ''', (id,))
        except sqlite3.Error as e:
            self.emit('error',self.ERROR + e.args[0])
            print e.args

    def delete_show_season(self, id ,sea):
        try:
            self.cur.execute('''DELETE 
                                FROM episodes 
                                WHERE season_id IN (
                                                    SELECT id
                                                    FROM seasons
                                                    WHERE show_id = ?
                                                    AND number = ?
                                                    )
                                ''', (id,sea,))
            self.cur.execute('''DELETE 
                                FROM seasons 
                                WHERE id IN (
                                            SELECT id
                                            FROM seasons
                                            WHERE show_id = ?
                                            AND number = ?
                                            )
                                ''', (id,sea,))
        except sqlite3.Error as e:
            self.emit('error',self.ERROR + e.args[0])
            print e.args

    def delete_show_episode(self, id ,sea,epi):
        try:
            self.cur.execute('''DELETE 
                                FROM episodes 
                                WHERE season_id IN (
                                                    SELECT id
                                                    FROM seasons
                                                    WHERE show_id = ?
                                                    AND number = ?
                                                    )
                                AND number = ?
                                ''', (id,sea,epi,))
        except sqlite3.Error as e:
            self.emit('error',self.ERROR + e.args[0])
            print e.args

    def delete_show_episodes(self, id ,sea):
        try:
            self.cur.execute('''
                    DELETE FROM episodes 
                    WHERE season_id IN (SELECT id 
                                        FROM seasons 
                                        WHERE number=? AND show_id=?)
            ''', (sea, id,))
        except sqlite3.Error as e:
            self.emit('error',self.ERROR + e.args[0])
            print e.args

    def update_show(self, id,tor,sub):
        try:
            self.cur.execute('''
                    UPDATE shows 
                    SET torrent=?,subtitle=? 
                    WHERE id=?
                    ''', (tor,sub,id,))
        except sqlite3.Error as e:
            self.emit('error',self.ERROR + e.args[0])
            print e.args

    def update_tag(self, id, code):
        try:
            self.cur.execute('''
                    UPDATE shows 
                    SET tag=?
                    WHERE id=?
                    ''', (code,id,))
        except sqlite3.Error as e:
            self.emit('error',self.ERROR + e.args[0])
            print e.args

    def insert_show(self, tuple):
        self.cur.execute('''
                INSERT OR REPLACE INTO shows 
                VALUES(?,?,?,?,?,?)
                ''', tuple)

    def insert_season(self, tuple):
        self.cur.execute('''
                INSERT OR REPLACE INTO seasons 
                VALUES(?,?,?,?)
                ''', tuple)

    def insert_episode(self, tuple):
        self.cur.execute('''
                INSERT OR REPLACE INTO episodes 
                VALUES(?,?,?)
                ''', tuple)

    def insert_bundle(self, data):
        #'''data sample (title,torrent,subtitle,[(season1,[episodes,]), (season2,[episodes,]] )'''
        try:
            self.insert_show((None,data[0],data[1],data[2],date.today(),data[3]) )
            ss = self.cur.lastrowid
            self.last_show_row_id = ss
            if data[4] is not None and len(data[4]):
                for sea in data[4]:
                    self.insert_season((None, sea[0],  date.today(), ss,) )
                    kk = self.cur.lastrowid
                    if sea[1] is not None or len(sea[1]):
                        for e in sea[1]:
                            self.insert_episode((e, date.today(), kk,) )

        except sqlite3.Error as e:
            self.emit('error',self.ERROR + e.args[0])
            print e.args

    def insert_show_season(self,id, data):
        #'''data sample [(season1,[episodes,]), (season2,[episodes,]] '''
        try:
            for sea in data:
                '''(season1,[episodes,])'''
                self.insert_season((None, sea[0],  date.today(), id,) )
                kk = self.cur.lastrowid
                for num in sea[1]:
                    self.insert_episode((num, date.today(), kk,) )
        except sqlite3.Error as e:
            self.emit('error',self.ERROR + e.args[0])
            print e.args

    def insert_show_episode(self, id, sea, data):
        #'''data sample [episodes,]'''
        try:
            self.cur.execute('''
                    SELECT id 
                    FROM seasons 
                    WHERE number=? AND show_id=?
                    ''', (sea,id,))
            sea_id = self.cur.fetchone()[0]
            for num in data:
                self.insert_episode((num, date.today(), sea_id,) )
        except sqlite3.Error as e:
            self.emit('error',self.ERROR + e.args[0])
            print e.args

    def insert_phony(self,data):
        #'''data sample (title,torrent,subtitle,[(season1,[episodes,]), (season2,[episodes,]] )'''
        try:
            self.insert_show((None,data[0],data[1],data[2],date.today(),) )
            ss = self.cur.lastrowid
            for sea in data[3]:
                self.insert_season((None, sea[0],  date(2015,4,12), None, ss,) )
                kk = self.cur.lastrowid
                for e in sea[1]:
                    self.insert_episode((e, date(2015,5,18), kk,) )
            self.conn.commit()
        except sqlite3.Error as e:
            self.emit('error',e.args[0])
            print e.args[0]

    def get_last_show_id(self):
        return self.last_show_row_id

    def add_column(self):
        try:
            self.cur.execute('''
                    ALTER TABLE shows
                    ADD COLUMN tag INTEGER
                    ''')
        except sqlite3.Error as e:
            self.emit('error',self.ERROR + e.args[0])
            print e.args


    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    db = VlogModel()
    #db.create_empty_db()
    db.add_column()


