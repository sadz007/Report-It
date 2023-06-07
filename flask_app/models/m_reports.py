from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash,session
from flask_app.models import m_users

class Report:
    def __init__(self,data):
        self.id = data['id']
        self.type = data['type']
        self.location = data['location']
        self.information = data['information']
        self.date_report = data['date_report']
        self.number = data['number']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None


    @staticmethod
    def is_valid_report(report):
        is_valid = True
        if len(report['type'])<1:
            flash("Enter the type of accident")
        if len(report["location"])< 1:
            flash("Location must be specified")
            is_valid = False
        if len(report["information"])<= 0 :
            flash("Details must be provided")
            is_valid = False
        if len(report["date_report"])<= 0 :
            flash("Date is required")
            is_valid = False
        if len(report["number"])<= 0 :
            flash("Reported number of  must be at least 1")
            is_valid = False
        return is_valid 



    @classmethod
    def create_report(cls,report):
        if not cls.is_valid_report(report):
            return False
        
        query = ''' INSERT INTO reports (type,location,information,date_report,number,user_id) 
                    VALUES (%(type)s,%(location)s, %(information)s, %(date_report)s, %(number)s, %(user_id)s);'''
        results = connectToMySQL("python_schema").query_db(query,report)

        return results


    @classmethod
    def get_report_id(cls, report):
        data = {
            "id": report
        }
        query = '''SELECT * FROM reports
                JOIN users ON users.id = reports.user_id
                WHERE reports.id = %(id)s;'''

        results = connectToMySQL("python_schema").query_db(query,data)
        data = results[0]
        report = cls(data)

        report.user = m_users.User({
            "id": data["users.id"],
            "first_name": data["first_name"],
            "last_name": data["last_name"],
            "email": data["email"],
            "password": data["password"],
            "created_at": data["users.created_at"],
            "updated_at": data["users.updated_at"]
        })
        return report 


    @classmethod
    def get_all_reports(cls):
        
        query = "SELECT * FROM reports JOIN users ON users.id = reports.user_id;"
        results = connectToMySQL("python_schema").query_db(query)

        all_reports = []

        for row in results:
            data = cls(row)

            data.user = m_users.User({
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": row["password"],
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"]
            })
            all_reports.append(data)
        return all_reports

    @classmethod
    def update_report(cls,report,session_id):
        data = cls.get_report_id(report["id"])

        if not cls.is_valid_report(report):
            flash("All fields are required")
            return False

        if data.user.id != session_id:
            flash("Can Not Report! Login To Report")
            return False

        query = '''UPDATE reports 
                SET type= %(type)s,location = %(location)s,information = %(information)s,date_report=%(date_report)s,number = %(number)s
                WHERE id = %(id)s;'''
        results = connectToMySQL("python_schema").query_db(query,report)
        return results
    

    @classmethod
    def delete_report(cls,report):
        
        data = {
            "id": report
        }
        query = "DELETE FROM reports WHERE id=%(id)s;"
        results = connectToMySQL("python_schema").query_db(query,data)
        return results
