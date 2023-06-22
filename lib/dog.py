import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    
    def __init__(self, name, breed, id=None):
        self.id = id
        self.name = name
        self.breed = breed 

    @classmethod 
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs(
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            );
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod 
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS dogs;
        """
        CURSOR.execute(sql)
        CONN.commit()
    
    def save(self):
        sql = """
            INSERT INTO dogs (name, breed)
            VALUES (?,?);
        """
        CURSOR.execute(sql,(self.name, self.breed))
        CONN.commit()

        self.id = CURSOR.lastrowid
        return self
    
    @classmethod 
    def create(cls, name, breed):
        dog = Dog(name, breed)
        return dog.save()

    @classmethod 
    def new_from_db(cls, row):
        return Dog(row[1], row[2], row[0])

    @classmethod 
    def get_all(cls):
        sql = """
            SELECT * from dogs
            """
        rows = CURSOR.execute(sql).fetchall()
        return [cls.new_from_db(r) for r in rows]

    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT * FROM dogs WHERE name = ? LIMIT 1
            """
        row = CURSOR.execute(sql, (name,)).fetchone()
        if not row:
            return None 
        return Dog(row[1], row[2], row[0])

    @classmethod 
    def find_by_id(cls, id):
        sql = """
            SELECT * FROM dogs WHERE id = ? LIMIT 1
            """
        row = CURSOR.execute(sql, (id,)).fetchone()
        return Dog(row[1], row[2], row[0])

    @classmethod
    def find_or_create_by(cls, name, breed):
        sql = """
            SELECT * FROM dogs WHERE name = ? AND breed = ? LIMIT 1
            """
        row = CURSOR.execute(sql, (name, breed)).fetchone()

        if not row:
            return cls.create(name, breed)
        
        return cls.new_from_db(row)

    def update(self):
        sql = """
            UPDATE dogs SET name = ?, breed = ? where id = ?;
            """
        row = CURSOR.execute(sql, (self.name,self.breed, self.id))
        CONN.commit()