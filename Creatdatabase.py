import MySQLdb


def create_database():
    conn = MySQLdb.connect("192.168.0.119", "root", "root", "cloud_data", charset="utf8")
    cursor = conn.cursor()
    sql2 = "CREATE TABLE patient_data(" \
                 "number INT(11) NOT NULL AUTO_INCREMENT," \
                 " medical_card_number VARCHAR(100) DEFAULT NULL  ," \
                 " clinic_number VARCHAR(100)  ," \
                 "hospital_number INT(11) ," \
                 "name VARCHAR(100)," \
                 "sex VARCHAR(100) ," \
                 "age VARCHAR(100)," \
                 "department VARCHAR(100) DEFAULT NULL ," \
                 "doctor VARCHAR(100) ," \
                 "bed_number VARCHAR(100) ," \
                 "hospitalized_date DATETIME ," \
                 "typeOfPatients VARCHAR(100) ," \
                 "typeOfInsurance VARCHAR(100) ," \
                 "diagnosis VARCHAR(100) ," \
                 "doctors_advice VARCHAR(100) ," \
                 " primary key (number)) ENGINE = InnoDB default charset=utf8"
    cursor.execute(sql2)
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    create_database()
