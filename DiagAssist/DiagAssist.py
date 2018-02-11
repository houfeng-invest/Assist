from flask import Flask,request,make_response
from flask_restful import  Resource,Api,reqparse
import random
#from flaskext.mysql import  MySQL
import pymysql
import pymysql.cursors

app = Flask(__name__,static_folder='static')
app.config['MYSQL_DATABASE_USER'] = 'houfeng'
app.config['MYSQL_DATABASE_PASSWORD'] = 'houfengabc123'
app.config['MYSQL_DATABASE_DB'] = 'diagassist'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

# mysql = MySQL()
# mysql.init_app(app)

config = {
          'host':'127.0.0.1',
          'port':3306,
          'user':'houfeng',
          'password':'houfengabc123',
          'db':'diagassist',
          'charset':'utf8',
          'cursorclass':pymysql.cursors.DictCursor,
          }

#connection = pymysql.connect(**config)

#cursor = connection.cursor()
#cursor.execute("insert into customer (identity,name) values ('1002','houfeng02')")
#connection.commit()



api = Api(app)
parser = reqparse.RequestParser()
@app.route("/")
def hello():
    return "Hello World!"


class RLDiagAssistAction(Resource):
    def get(self):
        print(request.url)
        print(request.headers)
        results =  app.send_static_file(self.__class__.__name__+'.json')
        print(results)
        return results
    def delete(self):
        print(request.url)
        print(request.headers)
        results =  {
            "results": {
            "api_version": "2.0",
            "return_code": "SUCCESS",
            "result_datas": {

                }
            }
        }
        print(results)
        return results
    def post(self):
        print(request.url)
        print(request.headers)
        print(request.get_json())
        results =  app.send_static_file(self.__class__.__name__+'.json')
        print(results)
        return results
    def put(self):
        print(request.url)
        print(request.headers)
        print(request.get_json())
        results =  app.send_static_file(self.__class__.__name__+'.json')
        print(results)
        return results



class RLDiagAssistGetConfigVersionsAction(RLDiagAssistAction):
    def get(self):
        return super().get()


class RLDiagGetFatigueAssessmentConfigAction(RLDiagAssistAction):
    def get(self,version):
        print(version)
        return super().get()


class RLDiagAssistGetBodypartRelatedConfigAction(RLDiagAssistAction):
    def get(self,version):
        print(version)
        return super().get()


class RLDiagAssistGetDiseaseConfigAction(RLDiagAssistAction):
    def get(self,version):
        print(version)
        return super().get()





class RLDiagAssistAddMedicalRecordAction(RLDiagAssistAction):
    def post(self):
        print(request.get_json())
        results =  {
            "results": {
            "api_version": "2.0",
            "return_code": "SUCCESS",
            "result_datas": {

                }
            }
        }
        medical_record_id = random.randint(1,100)
        results["results"]["result_datas"] = {"medical_record_id":medical_record_id}
        print(results)
        return results



class RLDiagAssistGetMedicalRecordAction(RLDiagAssistAction):
    def post(self):
        print(request.get_json())
        results =  {
            "results": {
            "api_version": "2.0",
            "return_code": "SUCCESS",
            "result_datas": {

                }
            }
        }
        medical_record_id = random.randint(1,100)
        results["results"]["result_datas"] = {"medical_record_id":medical_record_id}
        print(results)
        return results



class RLDiagAssistFatigueAssessmentPreviewAction(RLDiagAssistAction):
    def post(self):
        print(request.get_json())
        results =  {
            "results": {
            "api_version": "2.0",
            "return_code": "SUCCESS",
            "result_datas": {

                }
            }
        }
        medical_record_id = random.randint(1,100)
        results["results"]["result_datas"] = {"medical_record_id":medical_record_id}
        #print(results)
        return super().post()

#/api/v3/da/prediagnosis/fatigueAssessment/medicalRecord
class RLDiagAssistGetFatigueAssessmentAction(RLDiagAssistAction):
    def get(self,id):
        print(id)
        return super().get()

class RLDiagAssistFatigueAssessmentAction(RLDiagAssistAction):
    def post(self):
        print(request.url)
        print(request.get_json())
        results =  {
            "results": {
            "api_version": "2.0",
            "return_code": "SUCCESS",
            }
        }
        print(results)
        return results
    def put(self):
        print(request.url)
        print(request.get_json())
        results =  {
            "results": {
            "api_version": "2.0",
            "return_code": "SUCCESS",
            }
        }
        print(results)
        return results



class RLDiagAssistGetCurrentMedicalRecordsAction(RLDiagAssistAction):
    def get(self,id):
        print(id)
        return super().get()



class RLDiagAssistGetCurrentMedicalRecordAction(RLDiagAssistAction):
    def get(self,id):
        print(id)
        return super().get()



class RLDiagAssistImageAction(Resource):
    def get(self,name):
        print(name)
        img = app.send_static_file("image/"+name)
        return img


class RLTest(Resource):
    def get(self):
        return app.send_static_file('a.xlsx')

class RLIp(Resource):
    def get(self):
        return request.remote_addr

api.add_resource(RLTest,'/api/test')
api.add_resource(RLDiagAssistGetConfigVersionsAction,'/api/v3/da/config')
api.add_resource(RLDiagGetFatigueAssessmentConfigAction,'/api/v3/da/config/fatigueAssessment/version/<string:version>')
api.add_resource(RLDiagAssistGetCurrentMedicalRecordsAction,'/api/v3/da/prediagnosis/currentMedicalRecord/customer/<string:id>')
api.add_resource(RLDiagAssistGetCurrentMedicalRecordAction,'/api/v3/da/prediagnosis/currentMedicalRecord/<string:id>')

api.add_resource(RLDiagAssistAddMedicalRecordAction,'/api/v3/da/medicalrecord')
api.add_resource(RLDiagAssistGetMedicalRecordAction,'/api/v3/da/medicalrecord/customer')

api.add_resource(RLDiagAssistFatigueAssessmentPreviewAction,'/api/v3/da/prediagnosis/fatigueAssessment/preview')
api.add_resource(RLDiagAssistFatigueAssessmentAction,'/api/v3/da/prediagnosis/fatigueAssessment')
api.add_resource(RLDiagAssistGetFatigueAssessmentAction,'/api/v3/da/prediagnosis/fatigueAssessment/medicalRecord/<string:id>')

api.add_resource(RLDiagAssistGetBodypartRelatedConfigAction,'/api/v3/da/config/bodypartRelated/version/<string:version>')
api.add_resource(RLDiagAssistGetDiseaseConfigAction,'/api/v3/da/config/disease/version/<string:version>')

api.add_resource(RLDiagAssistImageAction,'/healthy/da/config/muscle/images/<string:name>')

api.add_resource(RLIp,'/ip/')



@app.route('/api/v3/da/config/test',methods=['GET', 'POST'])
def testConfig():
    print(request.url)
    if request.method == 'POST':
        print(request.data)
    elif request.method == 'GET':
        print(request.args)
    return app.send_static_file('RLDiagAssistGetConfigVersionsAction.json')

#ssl_context='adhoc'
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=8080)



