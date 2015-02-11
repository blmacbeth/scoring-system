''' This is the utility file for working with SQL databases for the 
main program. It will allow for persistent data regarding the judges,
routines, competitors, etc.
'''

import sqlite3 as SQL
import logging

LOG_FILENAME = 'logging_example.out'
logging.basicConfig(filename=LOG_FILENAME)

init_db = '''
CREATE TABLE IF NOT EXISTS judges(
    id   INT    PRIMARY KEY,
    name STRING NOT NULL
);

CREATE TABLE IF NOT EXISTS competitors(
    bib  INT    PRIMARY KEY,
    name STRING NOT NULL
);

CREATE TABLE IF NOT EXISTS routines(
    id       INT PRIMARY KEY,
    leader   INT NOT NULL,
    follower INT NOT NULL
);
'''

## Add things to the db
add_judge      = '''INSERT INTO judges      VALUES(?,?)'''
add_competitor = '''INSERT INTO competitors VALUES(?,?)'''
add_routine    = '''INSERT INTO routines    VALUES(?,?,?)'''
## get info from the db
get_judge_by_id   = '''SELECT * FROM judges WHERE id=?'''
get_judge_by_name = '''SELECT * FROM judges WHERE name=?'''
get_all_judges    = '''SELECT * FROM judges'''

get_competitor_by_bib  = '''SELECT * FROM competitors WHERE bib=?'''
get_competitor_by_name = '''SELECT * FROM competitors WHERE name=?'''
get_all_cometitors     = '''SELECT * FROM competitors'''

get_routine_by_id       = '''SELECT * FROM routines WHERE id=?'''
get_routine_by_leader   = '''SELECT * FROM routines WHERE leader=?'''
get_routine_by_follower = '''SELECT * FROM routines WHERE follower=?'''
get_all_routines        = '''SELECT * FROM routines'''

## utility functions
class Database:
    '''A general purpose DB for the software'''
    def __init__(self, db, new_db=True):
        self.db = db
        if new_db:
            with SQL.connect(self.db) as conn:
                cur = conn.cursor()
                cur.executescript(init_db)
                conn.commit()

    def add_judge(self, id, name):
        with SQL.connect(self.db) as conn:
            cur = conn.cursor()
            cur.execute(add_judge, (id, name,))
            conn.commit()

    def add_competitor(self, bib, name):
        with SQL.connect(self.db) as conn:
            cur = conn.cursor()
            cur.execute(add_competitor, (bib, name,))
            conn.commit()

    def add_routine(self, id, leader, follower):
        with SQL.connect(self.db) as conn:
            cur = conn.cursor()
            cur.execute(add_routine, (id, leader, follower,))
            conn.commit()

    def get_judge_by_id(self, id):
        with SQL.connect(self.db) as conn:
            cur = conn.cursor()
            cur.execute(get_judge_by_id, (id,))
            return cur.fetchone()
        logging.debug('Falied to get judge')

    def get_judge_by_name(self, name):
        with SQL.connect(self.db) as conn:
            cur = conn.cursor()
            cur.execute(get_judge_by_name, (name,))
            return cur.fetchone()
        logging.debug('Falied to get judge')

    def get_all_judges(self):
        with SQL.connect(self.db) as conn:
            cur = conn.cursor()
            cur.execute(get_all_judges)
            return cur.fetchall()
        logging.debug('Falied to get judges')

    def get_competitor_by_bib(self, bib):
        with SQL.connect(self.db) as conn:
            cur = conn.cursor()
            cur.execute(get_competitor_by_bib, (bib,))
            return cur.fetchone()
        logging.debug('Falied to get competitor')

    def get_competitor_by_name(self, name):
        with SQL.connect(self.db) as conn:
            cur = conn.cursor()
            cur.execute(get_competitor_by_name, (name,))
            return cur.fetchone()
        logging.debug('Falied to get competitor')

    def get_all_cometitors(self):
        with SQL.connect(self.db) as conn:
            cur = conn.cursor()
            cur.execute(get_all_cometitors)
            return cur.fetchall()
        logging.debug('Falied to get competitors')

    def get_routine_by_id(self, id):
        with SQL.connect(self.db) as conn:
            cur = conn.cursor()
            cur.execute(get_routine_by_id, (id,))
            return cur.fetchone()
        logging.debug('Falied to get routine')

    def get_routine_by_leader(self, leader):
        with SQL.connect(self.db) as conn:
            cur = conn.cursor()
            cur.execute(get_judge_by_name, (leader,))
            return cur.fetchone()
        logging.debug('Falied to get routine')

    def get_routine_by_follower(self, follower):
        with SQL.connect(self.db) as conn:
            cur = conn.cursor()
            cur.execute(get_judge_by_name, (follower,))
            return cur.fetchone()
        logging.debug('Falied to get routine')

    def get_all_routines(self):
        with SQL.connect(self.db) as conn:
            cur = conn.cursor()
            cur.execute(get_all_judges)
            return cur.fetchall()
        logging.debug('Falied to get routines')

if __name__ == '__main__':
    db = 'test.db'
    database = Database(db, False)
    ##database.add_judge(2, 'Alexa MacBeth')
    print database.get_all_judges()