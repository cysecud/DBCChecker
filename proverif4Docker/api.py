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
parser.add_argument('data')
parser.add_argument('type')

# Models
# Get a list of all models


class Models(Resource):
    def get(self):
        path = '/models'
        onlydir = [dI for dI in os.listdir(
            path) if os.path.isdir(os.path.join(path, dI))]
        return {'Models': onlydir}, 200

# SingleModel
# Get a model, create a new model and delete a model


class SingleModel(Resource):
    def get(self, model_id):
        path = '/models/{}'.format(model_id)
        inputPath = '/models/{}/input/text'.format(model_id)
        outputPathText = '/models/{}/output/text'.format(model_id)
        outputPathHtml = '/models/{}/output/html'.format(model_id)
        if os.path.exists(path) and os.path.exists(inputPath) and os.path.exists(outputPathText) and os.path.exists(outputPathHtml):
            inputOnlyfiles = [f for f in os.listdir(
                inputPath) if os.path.isfile(join(inputPath, f))]
            outputOnlyfilesText = [f for f in os.listdir(
                outputPathText) if os.path.isfile(join(outputPathText, f))]
            outputOnlyfilesHtml = [f for f in os.listdir(
                outputPathHtml) if os.path.isfile(join(outputPathHtml, f))]
            return {'Model': model_id, 'Input': inputOnlyfiles, 'OutputText': outputOnlyfilesText, 'OutputHtml': outputOnlyfilesHtml}, 200
        else:
            abort(404, message="Model {} doesn't exist".format(model_id))

    def post(self, model_id):
        path = '/models/{}'.format(model_id)
        if not os.path.exists(path):
            try:
                os.makedirs('/models/{}/input/text'.format(model_id))
                os.makedirs('/models/{}/output/text'.format(model_id))
                os.makedirs('/models/{}/output/html'.format(model_id))
                shutil.copy('/proverifdata/css/cssproverif.css',
                            '/models/{}/output/html'.format(model_id))
                return {'Result': 'Model {} has been created'.format(model_id)}, 201
            except OSError:
                shutil.rmtree('/models/{}'.format(model_id))
                abort(500, message="Fail to create the directories")
        else:
            abort(409, message="Model {} already exists".format(model_id))

    def delete(self, model_id):
        path = '/models/{}'.format(model_id)
        if os.path.exists(path):
            try:
                shutil.rmtree('/models/{}'.format(model_id))
                # OPPURE 204??
                return {'Result': 'Model {} has been deleted'.format(model_id)}, 200
            except OSError:
                abort(500, message="Fail to create the directories")
        else:
            abort(404, message="Model {} doesn't exist".format(model_id))

# InputModel
# Get a single input model, create a new one, update a model and delete a model


class InputModel(Resource):
    def get(self, model_id, file_id):
        path = '/models/{}/input/text/{}.pv'.format(model_id, file_id)
        if os.path.exists(path):
            out_file = open(path, 'r')
            data = out_file.read()
            out_file.close()
            return {'Model': model_id, 'File': file_id, 'Result': data}, 200
        else:
            abort(404, message="File {}.pv of the model {} doesn't exist".format(
                file_id, model_id))

    def post(self, model_id, file_id):
        path = '/models/{}/input/text/{}.pv'.format(model_id, file_id)
        modelpath = '/models/{}/input/text'.format(model_id)
        args = parser.parse_args()
        if args['data'] is not None:
            if os.path.exists(modelpath):
                try:
                    in_file = open(path, 'x')
                    in_file.write(args['data'])
                    in_file.close()
                    return {'Result': "File {}.pv of the model {} has been created".format(file_id, model_id)}, 201
                except FileExistsError as err:
                    abort(
                        409, message="Post input file already performed, to update the resource use put request")
            else:
                abort(404, message="Model {} doesn't exist".format(model_id))
        else:
            abort(415, message="Argument must be a string not null".format(model_id))

    def put(self, model_id, file_id):
        path = '/models/{}/input/text/{}.pv'.format(model_id, file_id)
        args = parser.parse_args()
        if args['data'] is not None:
            if os.path.exists(path):
                in_file = open(path, 'w')
                in_file.write(args['data'])
                in_file.close()
                return {'Result': "File {}.pv of the model {} has been modified".format(file_id, model_id)}, 201
            else:
                abort(404, message="File {}.pv of the model {} doesn't exist".format(
                    file_id, model_id))
        else:
            abort(415, message="Argument must be a string not null".format(model_id))

    def delete(self, model_id, file_id):
        path = '/models/{}/input/text/{}.pv'.format(model_id, file_id)
        if os.path.exists(path):
            os.remove(path)
            return {'Result': 'File {}.pv of the model {} has been deleted'.format(file_id, model_id)}, 200
        else:
            abort(404, message="File {}.pv of the model {} doesn't exist".format(
                file_id, model_id))

# OutputText
# Get an output (text), delete an output


class OutputText(Resource):
    def get(self, model_id, file_id):
        path = '/models/{}/output/text/{}.txt'.format(model_id, file_id)
        if os.path.exists(path):
            out_file = open(path, 'r')
            data = out_file.read()
            out_file.close()
            return {'Model': model_id, 'File': file_id, 'Result': data}, 200
        else:
            abort(404, message="File {}.txt of the model {} doesn't exist".format(
                file_id, model_id))

    def delete(self, model_id, file_id):
        path = '/models/{}/output/text/{}.txt'.format(model_id, file_id)
        if os.path.exists(path):
            os.remove(path)
            return {'Result': 'File {}.txt of the model {} has been deleted'.format(file_id, model_id)}, 200
        else:
            abort(404, message="File {}.txt of the model {} doesn't exist".format(
                file_id, model_id))

# OutputHtml
# Get an output (html), delete an output


class OutputHtml(Resource):
    def get(self, model_id, file_id):
        path = '/models/{}/output/html/{}'.format(model_id, file_id)
        if os.path.exists(path):
            try:
                return send_file(path)
            except Exception as e:
                abort(500, message="Fail to serve the file")
        else:
            abort(404, message="File {}.html of the model {} doesn't exist".format(
                file_id, model_id))

    def delete(self, model_id, file_id):
        path = '/models/{}/output/html/{}'.format(model_id, file_id)
        if os.path.exists(path):
            folder = '/models/{}/output/html/'.format(model_id)
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    abort(500, message='Failed to delete %s. Reason: %s' %
                          (file_path, e))
            shutil.copy('/proverifdata/css/cssproverif.css',
                        '/models/{}/output/html'.format(model_id))
            return {'Result': 'All output html files of the model {} has been deleted'.format(model_id)}, 200
        else:
            abort(404, message="File {}.html of the model {} doesn't exist".format(
                file_id, model_id))

# Verify
# Verify with Proverif a model


class Verify(Resource):
    def post(self, model_id, file_id):
        args = parser.parse_args()
        pathInput = '/models/{}/input/text/{}.pv'.format(model_id, file_id)
        if os.path.exists(pathInput):
            if args['type'] is not None:
                typeVerify = str(args['type'])
                if typeVerify == 'text' or 'html':
                    if typeVerify == 'html':
                        pathOutputHtml = '/models/{}/output/html/'.format(
                            model_id, file_id)
                        if os.path.isfile(pathOutputHtml + 'index.html'):
                            abort(
                                409, message="Post verify already performed, to update the resource use put request")
                        else:
                            process = subprocess.Popen(
                                ['/proverifdata/script/runproverif.sh', pathInput, pathOutputHtml, str(typeVerify)], stdout=subprocess.PIPE)
                            stdout = process.communicate()[0]
                            return {'Result': 'The script finish', 'Log': '{}'.format(stdout)}
                    else:
                        pathOutputText = '/models/{}/output/text/{}.txt'.format(
                            model_id, file_id)
                        if os.path.isfile(pathOutputText):
                            abort(
                                409, message="Post verify already performed, to update the resource use put request")
                        else:
                            process = subprocess.Popen(
                                ['/proverifdata/script/runproverif.sh', pathInput, pathOutputText, str(typeVerify)], stdout=subprocess.PIPE)
                            stdout = process.communicate()[0]
                            return {'Result': 'The script finish', 'Log': '{}'.format(stdout)}
                else:
                    abort(415, message="type must be html or text")
            else:
                abort(415, message="type must be declare: choose between html or text")
        else:
            abort(404, message="File {}.pv of the model {} doesn't exist".format(
                file_id, model_id))

    def put(self, model_id, file_id):
        args = parser.parse_args()
        pathInput = '/models/{}/input/text/{}.pv'.format(model_id, file_id)
        if os.path.exists(pathInput):
            if args['type'] is not None:
                typeVerify = str(args['type'])
                if typeVerify == 'text' or 'html':
                    if typeVerify == 'html':
                        pathOutputHtml = '/models/{}/output/html/'.format(
                            model_id, file_id)
                        # Delete existing files
                        folder = pathOutputHtml
                        for filename in os.listdir(folder):
                            file_path = os.path.join(folder, filename)
                            try:
                                if os.path.isfile(file_path) or os.path.islink(file_path):
                                    os.unlink(file_path)
                                elif os.path.isdir(file_path):
                                    shutil.rmtree(file_path)
                            except Exception as e:
                                abort(500, message='Failed to delete %s. Reason: %s. Delete html result and verify again' % (
                                    file_path, e))
                        shutil.copy('/proverifdata/css/cssproverif.css',
                                    '/models/{}/output/html'.format(model_id))
                        # End Delete existing files
                        process = subprocess.Popen(
                            ['/proverifdata/script/runproverif.sh', pathInput, pathOutputHtml, str(typeVerify)], stdout=subprocess.PIPE)
                        stdout = process.communicate()[0]
                        return {'Result': 'The script finish', 'Log': '{}'.format(stdout)}
                    else:
                        pathOutputText = '/models/{}/output/text/{}.txt'.format(
                            model_id, file_id)
                        process = subprocess.Popen(
                            ['/proverifdata/script/runproverif.sh', pathInput, pathOutputText, str(typeVerify)], stdout=subprocess.PIPE)
                        stdout = process.communicate()[0]
                        return {'Result': 'The script finish', 'Log': '{}'.format(stdout)}
                else:
                    abort(415, message="type must be html or text")
            else:
                abort(415, message="type must be declare: choose between html or text")
        else:
            abort(404, message="File {}.pv of the model {} doesn't exist".format(
                file_id, model_id))


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
    app.run(host='0.0.0.0', port=5001, debug=True)
