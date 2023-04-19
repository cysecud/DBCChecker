import json
import os
import shutil
import subprocess
from os import listdir
from os.path import isfile, join

from flask import Flask, send_file
from flask_restful import Api, Resource, abort, reqparse

app = Flask(__name__)
api = Api(app)

# Add and setup the parser
parser = reqparse.RequestParser()
parser.add_argument('DataProverif')
parser.add_argument('DataJsonBigraph')
parser.add_argument('DataJsonIntegrative')
parser.add_argument('VerificationType')

# Models
# Get a list of all models


class Models(Resource):
    def get(self):
        result = subprocess.run(
            ['java', '-jar', '/proverif/serverProverif-1.1.0.jar', 'GetModels'], capture_output=True, text=True)
        if result.stderr != "":
            try:
                var = json.loads(result.stderr)
            except:
                var = result.stderr
                abort(500, Response=var)
            else:
                var = json.loads(result.stderr)
                abort(int(var["code"]), Response=var)
        else:
            return {'Response': json.loads(result.stdout)}, 200

# SingleModel
# Get a model, create a new model and delete a model


class SingleModel(Resource):
    def get(self, model_id):
        result = subprocess.run(['java', '-jar', '/proverif/serverProverif-1.1.0.jar',
                                 'GetModel', '{}'.format(model_id)], capture_output=True, text=True)
        if result.stderr != "":
            try:
                var = json.loads(result.stderr)
            except:
                var = result.stderr
                abort(500, Response=var)
            else:
                var = json.loads(result.stderr)
                abort(int(var["code"]), Response=var)
        else:
            return {'Response': json.loads(result.stdout)}, 200

    def post(self, model_id):
        result = subprocess.run(['java', '-jar', '/proverif/serverProverif-1.1.0.jar',
                                 'PostModel', '{}'.format(model_id)], capture_output=True, text=True)
        if result.stderr != "":
            try:
                var = json.loads(result.stderr)
            except:
                var = result.stderr
                abort(500, Response=var)
            else:
                var = json.loads(result.stderr)
                abort(int(var["code"]), Response=var)
        else:
            return {'Response': json.loads(result.stdout)}, 201

    def delete(self, model_id):
        result = subprocess.run(['java', '-jar', '/proverif/serverProverif-1.1.0.jar',
                                 'DeleteModel', '{}'.format(model_id)], capture_output=True, text=True)
        if result.stderr != "":
            try:
                var = json.loads(result.stderr)
            except:
                var = result.stderr
                abort(500, Response=var)
            else:
                var = json.loads(result.stderr)
                abort(int(var["code"]), Response=var)
        else:
            return {'Response': json.loads(result.stdout)}, 200

# InputModel
# Get a single input model, create a new one, update a model and delete a model


class InputModel(Resource):
    def get(self, model_id, file_id):
        result = subprocess.run(['java', '-jar', '/proverif/serverProverif-1.1.0.jar', 'GetInput',
                                 '{}'.format(model_id), '{}'.format(file_id)], capture_output=True, text=True)
        if result.stderr != "":
            try:
                var = json.loads(result.stderr)
            except:
                var = result.stderr
                abort(500, Response=var)
            else:
                var = json.loads(result.stderr)
                abort(int(var["code"]), Response=var)
        else:
            return {'Response': json.loads(result.stdout)}, 200

    def post(self, model_id, file_id):
        args = parser.parse_args()
        if args['DataProverif'] is not None:
            dataProverif = str(args['DataProverif']).replace(
                '\n', ' ').replace('\t', ' ')
            if args['DataJsonBigraph'] is None and args['DataJsonIntegrative'] is None:
                result = subprocess.run(['java', '-jar', '/proverif/serverProverif-1.1.0.jar', 'PostInputRaw', '{}'.format(
                    model_id), '{}'.format(file_id), '{}'.format(dataProverif)], capture_output=True, text=True)
                if result.stderr != "":
                    try:
                        var = json.loads(result.stderr)
                    except:
                        var = result.stderr
                        abort(500, Response=var)
                    else:
                        var = json.loads(result.stderr)
                        abort(int(var["code"]), Response=var)
                else:
                    return {'Response': json.loads(result.stdout)}, 201
            else:
                abort(
                    415, message="Arguments DataJsonBigraph and DataJsonIntegrative must be null if DataProverif is not null")
        elif args['DataProverif'] is None:
            if args['DataJsonBigraph'] is not None and args['DataJsonIntegrative'] is not None:
                dataJsonBigraph = str(args['DataJsonBigraph']).replace(
                    '\n', ' ').replace('\t', ' ')
                dataJsonIntegrative = str(args['DataJsonIntegrative']).replace(
                    '\n', ' ').replace('\t', ' ')
                result = subprocess.run(['java', '-jar', '/proverif/serverProverif-1.1.0.jar', 'PostInput', '{}'.format(
                    model_id), '{}'.format(file_id), dataJsonBigraph, dataJsonIntegrative], capture_output=True, text=True)
                if result.stderr != "":
                    try:
                        var = json.loads(result.stderr)
                    except:
                        var = result.stderr
                        abort(500, Response=var)
                    else:
                        var = json.loads(result.stderr)
                        abort(int(var["code"]), Response=var)
                else:
                    return {'Response': json.loads(result.stdout)}, 201
            else:
                abort(
                    415, message="Arguments DataJsonBigraph and DataJsonIntegrative must be not if DataProverif is null null")
        else:
            abort(415, message="Some argument must be a string not null")

    def put(self, model_id, file_id):
        args = parser.parse_args()
        if args['DataProverif'] is not None:
            dataProverif = str(args['DataProverif']).replace(
                '\n', ' ').replace('\t', ' ')
            if args['DataJsonBigraph'] is None and args['DataJsonIntegrative'] is None:
                result = subprocess.run(['java', '-jar', '/proverif/serverProverif-1.1.0.jar', 'PutInputRaw', '{}'.format(
                    model_id), '{}'.format(file_id), '{}'.format(dataProverif)], capture_output=True, text=True)
                if result.stderr != "":
                    try:
                        var = json.loads(result.stderr)
                    except:
                        var = result.stderr
                        abort(500, Response=var)
                    else:
                        var = json.loads(result.stderr)
                        abort(int(var["code"]), Response=var)
                else:
                    return {'Response': json.loads(result.stdout)}, 201
            else:
                abort(
                    415, message="Arguments DataJsonBigraph and DataJsonIntegrative must be null if DataProverif is not null")
        elif args['DataProverif'] is None:
            if args['DataJsonBigraph'] is not None and args['DataJsonIntegrative'] is not None:
                dataJsonBigraph = str(args['DataJsonBigraph']).replace(
                    '\n', ' ').replace('\t', ' ')
                dataJsonIntegrative = str(args['DataJsonIntegrative']).replace(
                    '\n', ' ').replace('\t', ' ')
                result = subprocess.run(['java', '-jar', '/proverif/serverProverif-1.1.0.jar', 'PutInput', '{}'.format(
                    model_id), '{}'.format(file_id), dataJsonBigraph, dataJsonIntegrative], capture_output=True, text=True)
                if result.stderr != "":
                    try:
                        var = json.loads(result.stderr)
                    except:
                        var = result.stderr
                        abort(500, Response=var)
                    else:
                        var = json.loads(result.stderr)
                        abort(int(var["code"]), Response=var)
                else:
                    return {'Response': json.loads(result.stdout)}, 201
            else:
                abort(
                    415, message="Arguments DataJsonBigraph and DataJsonIntegrative must be not if DataProverif is null null")
        else:
            abort(415, message="Some argument must be a string not null")

    def delete(self, model_id, file_id):
        result = subprocess.run(['java', '-jar', '/proverif/serverProverif-1.1.0.jar', 'DeleteInput',
                                 '{}'.format(model_id), '{}'.format(file_id)], capture_output=True, text=True)
        if result.stderr != "":
            try:
                var = json.loads(result.stderr)
            except:
                var = result.stderr
                abort(500, Response=var)
            else:
                var = json.loads(result.stderr)
                abort(int(var["code"]), Response=var)
        else:
            return {'Response': json.loads(result.stdout)}, 200

# OutputText
# Get an output (text), delete an output


class OutputText(Resource):
    def get(self, model_id, file_id):
        result = subprocess.run(['java', '-jar', '/proverif/serverProverif-1.1.0.jar', 'GetOutputText',
                                 '{}'.format(model_id), '{}'.format(file_id)], capture_output=True, text=True)
        if result.stderr != "":
            try:
                var = json.loads(result.stderr)
            except:
                var = result.stderr
                abort(500, Response=var)
            else:
                var = json.loads(result.stderr)
                abort(int(var["code"]), Response=var)
        else:
            return {'Response': json.loads(result.stdout)}, 200

    def delete(self, model_id, file_id):
        result = subprocess.run(['java', '-jar', '/proverif/serverProverif-1.1.0.jar', 'DeleteOutputText',
                                 '{}'.format(model_id), '{}'.format(file_id)], capture_output=True, text=True)
        if result.stderr != "":
            try:
                var = json.loads(result.stderr)
            except:
                var = result.stderr
                abort(500, Response=var)
            else:
                var = json.loads(result.stderr)
                abort(int(var["code"]), Response=var)
        else:
            return {'Response': json.loads(result.stdout)}, 200

# OutputHtml
# Get an output (html), delete an output


class OutputHtml(Resource):
    def get(self, model_id, file_id):
        result = subprocess.run(['java', '-jar', '/proverif/serverProverif-1.1.0.jar', 'GetOutputHtml',
                                 '{}'.format(model_id), '{}'.format(file_id)], capture_output=True, text=True)
        if result.stderr != "":
            try:
                var = json.loads(result.stderr)
            except:
                var = result.stderr
                abort(500, Response=var)
            else:
                var = json.loads(result.stderr)
                abort(int(var["code"]), Response=var)
        else:
            return {'Response': json.loads(result.stdout)}, 200

    def delete(self, model_id, file_id):
        result = subprocess.run(['java', '-jar', '/proverif/serverProverif-1.1.0.jar', 'DeleteOutputHtml',
                                 '{}'.format(model_id), '{}'.format(file_id)], capture_output=True, text=True)
        if result.stderr != "":
            try:
                var = json.loads(result.stderr)
            except:
                var = result.stderr
                abort(500, Response=var)
            else:
                var = json.loads(result.stderr)
                abort(int(var["code"]), Response=var)
        else:
            return {'Response': json.loads(result.stdout)}, 200

# Verify
# Verify with Proverif a model


class Verify(Resource):
    def post(self, model_id, file_id):
        args = parser.parse_args()
        if args['VerificationType'] is not None:
            typeVerify = str(args['VerificationType'])
            if typeVerify == 'both':
                if args['DataJsonBigraph'] is not None and args['DataJsonIntegrative'] is not None:
                    dataJsonBigraph = str(args['DataJsonBigraph']).replace(
                        '\n', ' ').replace('\t', ' ')
                    dataJsonIntegrative = str(args['DataJsonIntegrative']).replace(
                        '\n', ' ').replace('\t', ' ')
                    result = subprocess.run(['java', '-jar', '/proverif/serverProverif-1.1.0.jar', 'PostVerify', dataJsonBigraph, dataJsonIntegrative,
                                             '{}'.format(model_id), '{}'.format(file_id)], capture_output=True, text=True)
                    if result.stderr != "":
                        try:
                            var = json.loads(result.stderr)
                        except:
                            var = result.stderr
                            abort(500, Response=var)
                        else:
                            var = json.loads(result.stderr)
                            abort(int(var["code"]), Response=var)
                    else:
                        return {'Response': json.loads(result.stdout)}, 200
                else:
                    abort(
                        415, Response="If VerificationType is set on both, DataJsonBigraph and DataJsonIntegrative must be specified")
            elif typeVerify == 'text':
                if args['DataJsonBigraph'] is not None and args['DataJsonIntegrative'] is not None:
                    dataJsonBigraph = str(args['DataJsonBigraph']).replace(
                        '\n', ' ').replace('\t', ' ')
                    dataJsonIntegrative = str(args['DataJsonIntegrative']).replace(
                        '\n', ' ').replace('\t', ' ')
                    result = subprocess.run(['java', '-jar', '/proverif/serverProverif-1.1.0.jar', 'PostVerifyText', dataJsonBigraph, dataJsonIntegrative,
                                             '{}'.format(model_id), '{}'.format(file_id)], capture_output=True, text=True)
                    if result.stderr != "":
                        try:
                            var = json.loads(result.stderr)
                        except:
                            var = result.stderr
                            abort(500, Response=var)
                        else:
                            var = json.loads(result.stderr)
                            abort(int(var["code"]), Response=var)
                    else:
                        return {'Response': json.loads(result.stdout)}, 200
                elif args['DataJsonBigraph'] is None and args['DataJsonIntegrative'] is None:
                    result = subprocess.run(['java', '-jar', '/proverif/serverProverif-1.1.0.jar', 'PostVerText',
                                             '{}'.format(model_id), '{}'.format(file_id)], capture_output=True, text=True)
                    if result.stderr != "":
                        try:
                            var = json.loads(result.stderr)
                        except:
                            var = result.stderr
                            abort(500, Response=var)
                        else:
                            var = json.loads(result.stderr)
                            abort(int(var["code"]), Response=var)
                    else:
                        return {'Response': json.loads(result.stdout)}, 200
                else:
                    abort(
                        415, Response="DataJsonBigraph and DataJsonIntegrative must be both null or both not null")
            elif typeVerify == 'html':
                if args['DataJsonBigraph'] is not None and args['DataJsonIntegrative'] is not None:
                    dataJsonBigraph = str(args['DataJsonBigraph']).replace(
                        '\n', ' ').replace('\t', ' ')
                    dataJsonIntegrative = str(args['DataJsonIntegrative']).replace(
                        '\n', ' ').replace('\t', ' ')
                    result = subprocess.run(['java', '-jar', '/proverif/serverProverif-1.1.0.jar', 'PostVerifyHtml', dataJsonBigraph, dataJsonIntegrative,
                                             '{}'.format(model_id), '{}'.format(file_id)], capture_output=True, text=True)
                    if result.stderr != "":
                        try:
                            var = json.loads(result.stderr)
                        except:
                            var = result.stderr
                            abort(500, Response=var)
                        else:
                            var = json.loads(result.stderr)
                            abort(int(var["code"]), Response=var)
                    else:
                        return {'Response': json.loads(result.stdout)}, 200
                elif args['DataJsonBigraph'] is None and args['DataJsonIntegrative'] is None:
                    result = subprocess.run(['java', '-jar', '/proverif/serverProverif-1.1.0.jar', 'PostVerHtml',
                                             '{}'.format(model_id), '{}'.format(file_id)], capture_output=True, text=True)
                    if result.stderr != "":
                        try:
                            var = json.loads(result.stderr)
                        except:
                            var = result.stderr
                            abort(500, Response=var)
                        else:
                            var = json.loads(result.stderr)
                            abort(int(var["code"]), Response=var)
                    else:
                        return {'Response': json.loads(result.stdout)}, 200
                else:
                    abort(
                        415, Response="DataJsonBigraph and DataJsonIntegrative must be both null or both not null")
            else:
                abort(415, Response="VerificationType must be both, html or text")
        else:
            abort(
                415, message="VerificationType must be declare: choose between both, text or html")

    def put(self, model_id, file_id):
        args = parser.parse_args()
        if args['VerificationType'] is not None:
            typeVerify = str(args['VerificationType'])
            if typeVerify == 'both':
                if args['DataJsonBigraph'] is not None and args['DataJsonIntegrative'] is not None:
                    dataJsonBigraph = str(args['DataJsonBigraph']).replace(
                        '\n', ' ').replace('\t', ' ')
                    dataJsonIntegrative = str(args['DataJsonIntegrative']).replace(
                        '\n', ' ').replace('\t', ' ')
                    result = subprocess.run(['java', '-jar', '/proverif/serverProverif-1.1.0.jar', 'PutVerify', dataJsonBigraph, dataJsonIntegrative,
                                             '{}'.format(model_id), '{}'.format(file_id)], capture_output=True, text=True)
                    if result.stderr != "":
                        try:
                            var = json.loads(result.stderr)
                        except:
                            var = result.stderr
                            abort(500, Response=var)
                        else:
                            var = json.loads(result.stderr)
                            abort(int(var["code"]), Response=var)
                    else:
                        return {'Response': json.loads(result.stdout)}, 200
                else:
                    abort(
                        415, Response="If VerificationType is set on both, DataJsonBigraph and DataJsonIntegrative must be specified")
            elif typeVerify == 'text':
                if args['DataJsonBigraph'] is not None and args['DataJsonIntegrative'] is not None:
                    dataJsonBigraph = str(args['DataJsonBigraph']).replace(
                        '\n', ' ').replace('\t', ' ')
                    dataJsonIntegrative = str(args['DataJsonIntegrative']).replace(
                        '\n', ' ').replace('\t', ' ')
                    result = subprocess.run(['java', '-jar', '/proverif/serverProverif-1.1.0.jar', 'PutVerifyText', dataJsonBigraph, dataJsonIntegrative,
                                             '{}'.format(model_id), '{}'.format(file_id)], capture_output=True, text=True)
                    if result.stderr != "":
                        try:
                            var = json.loads(result.stderr)
                        except:
                            var = result.stderr
                            abort(500, Response=var)
                        else:
                            var = json.loads(result.stderr)
                            abort(int(var["code"]), Response=var)
                    else:
                        return {'Response': json.loads(result.stdout)}, 200
                elif args['DataJsonBigraph'] is None and args['DataJsonIntegrative'] is None:
                    result = subprocess.run(['java', '-jar', '/proverif/serverProverif-1.1.0.jar', 'PutVerText',
                                             '{}'.format(model_id), '{}'.format(file_id)], capture_output=True, text=True)
                    if result.stderr != "":
                        try:
                            var = json.loads(result.stderr)
                        except:
                            var = result.stderr
                            abort(500, Response=var)
                        else:
                            var = json.loads(result.stderr)
                            abort(int(var["code"]), Response=var)
                    else:
                        return {'Response': json.loads(result.stdout)}, 200
                else:
                    abort(
                        415, Response="DataJsonBigraph and DataJsonIntegrative must be both null or both not null")
            elif typeVerify == 'html':
                if args['DataJsonBigraph'] is not None and args['DataJsonIntegrative'] is not None:
                    dataJsonBigraph = str(args['DataJsonBigraph']).replace(
                        '\n', ' ').replace('\t', ' ')
                    dataJsonIntegrative = str(args['DataJsonIntegrative']).replace(
                        '\n', ' ').replace('\t', ' ')
                    result = subprocess.run(['java', '-jar', '/proverif/serverProverif-1.1.0.jar', 'PutVerifyHtml', dataJsonBigraph, dataJsonIntegrative,
                                             '{}'.format(model_id), '{}'.format(file_id)], capture_output=True, text=True)
                    if result.stderr != "":
                        try:
                            var = json.loads(result.stderr)
                        except:
                            var = result.stderr
                            abort(500, Response=var)
                        else:
                            var = json.loads(result.stderr)
                            abort(int(var["code"]), Response=var)
                    else:
                        return {'Response': json.loads(result.stdout)}, 200
                elif args['DataJsonBigraph'] is None and args['DataJsonIntegrative'] is None:
                    result = subprocess.run(['java', '-jar', '/proverif/serverProverif-1.1.0.jar', 'PutVerHtml',
                                             '{}'.format(model_id), '{}'.format(file_id)], capture_output=True, text=True)
                    if result.stderr != "":
                        try:
                            var = json.loads(result.stderr)
                        except:
                            var = result.stderr
                            abort(500, Response=var)
                        else:
                            var = json.loads(result.stderr)
                            abort(int(var["code"]), Response=var)
                    else:
                        return {'Response': json.loads(result.stdout)}, 200
                else:
                    abort(
                        415, Response="DataJsonBigraph and DataJsonIntegrative must be both null or both not null")
            else:
                abort(415, Response="VerificationType must be both, html or text")
        else:
            abort(
                415, message="VerificationType must be declare: choose between both, text or html")


##
# Actually setup the Api resource routing here
##
api.add_resource(Models, '/models')
api.add_resource(SingleModel, '/models/<model_id>')
api.add_resource(InputModel, '/models/<model_id>/input/text/<file_id>')
api.add_resource(OutputText, '/models/<model_id>/output/text/<file_id>')
api.add_resource(OutputHtml, '/models/<model_id>/output/html/<file_id>')
api.add_resource(Verify, '/models/<model_id>/verify/<file_id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
