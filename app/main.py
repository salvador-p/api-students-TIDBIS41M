from email import message
from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse, abort
from flask_pymongo import pymongo
import app.db_config as database

app = Flask(__name__)
api = Api(app)

post_students_args = reqparse.RequestParser()


post_students_args.add_argument("id", type=int, help="Error id value needs to be an integer", required=True)
post_students_args.add_argument("first_name", type=str, help="Error first_name value needs to be an integer", required=True)
post_students_args.add_argument("last_name", type=str, help="Error last_name value needs to be an integer", required=True)
post_students_args.add_argument("image", type=str, help="Error you need to add the image url", required=True)
post_students_args.add_argument("group", type=str, required=False)
post_students_args.add_argument("career", type=str, required=True)




class Test(Resource):

    def get(self):
        database.db.students.find()
        return jsonify({'message': 'You are connected to the database'})

class Student(Resource):

    def get(self,id):
        response = database.db.students.find_one({"id": id})
        del response['_id']
        return jsonify(response)

class Students(Resource):

    def get(self):
        response = list(database.db.students.find())
        students = []
        for student in response:
            del student['_id']
            students.append(student)
        return jsonify({'results' : students})

    def post(self):
        args = post_students_args.parse_args()
        self.abort_if_id_exist(args['id'])
        database.db.students.insert_one({
            'id':args['id'],
            'first_name':args['first_name'],
            'last_name':args['last_name'],
            'image':args['image'],
            'group':args['group'],
            'career':args['career'],
        })
        return jsonify(args)

    def put(self):
        pass

    def patch(self):
        pass

    def delete(self):
        pass

    def abort_if_id_exist(self, id):
        if database.db.students.find_one({'id':id}):
            abort(
                jsonify({'status':'406', 'error': f"the student with the id : {id} already exist"}))

    def abort_if_not_exist(self, id):
        student = database.db.students.find_one({'id':id})
        if not student:
            abort(
                jsonify({'status':'404', 'error': f"the student with the id : {id} already exist"}))
        else:
            return student

api.add_resource(Test, '/test/')
api.add_resource(Students, '/students/')
api.add_resource(Student, '/students/<int:id>/')



if __name__ == '__main__':
    app.run(load_dotenv=True, port=8080)