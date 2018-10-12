import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
import random
import string
from pydub import AudioSegment
import subprocess
import shutil
from flask import send_file, send_from_directory
from flask import request
from flask import g
from flask_cors import CORS
import pprint
from flask import make_response
from flask import jsonify

pp = pprint.PrettyPrinter(indent=4)

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['mp3'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
CORS(app)


def after_this_request(func):
    if not hasattr(g, 'call_after_request'):
        g.call_after_request = []
    g.call_after_request.append(func)
    return func


@app.after_request
def per_request_callbacks(response):
    for func in getattr(g, 'call_after_request', ()):
        response = func(response)
    return response


def getShowNameFromSeg(filename):
    (dirname, purefilename) = os.path.split(filename)
    arr = purefilename.split('.')
    return arr[0]


def split_wav_by_seg(wav, seg, output):
    showname = getShowNameFromSeg(seg)
    i = 0
    dic = {}

    with open(seg, 'r') as f:
        for line in f:
            if line.startswith(showname):
                line_arr = line.split(' ')
                start = int(line_arr[2]) * 10
                end = int(line_arr[3]) * 10 + start
                dic[start] = end

        for key in sorted(dic):
            i += 1
            newAudio = AudioSegment.from_wav(wav)
            newAudio = newAudio[key:dic[key]]
            newAudio.export(output + "/" + showname + "_split_" + str(i) + ".wav", format="wav")


def rand_post_fix():
    N = 6
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route("/download", methods=['POST'])
def download():
    ppath = request.form.get('path')
    pfilename = request.form.get('filename')

    @after_this_request
    def cleanup(response):
        shutil.rmtree(ppath)
        return response

    return send_from_directory(ppath, pfilename, as_attachment=True)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pp.pprint(request)
        file = request.files['items[]']
        pp.pprint(file)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # make a temporily uploader
            tmpdir = UPLOAD_FOLDER + "/" + file.filename + rand_post_fix()
            if not os.path.exists(tmpdir):
                os.makedirs(tmpdir)
            app.config['UPLOAD_FOLDER'] = tmpdir
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # convert mp3 to wav and save it in the same path
            sound = AudioSegment.from_mp3(tmpdir + "/" + file.filename)
            showName = os.path.splitext(file.filename)[0]
            sound.export(tmpdir + "/" + showName + '.wav', format="wav")
            # execute jar to generate .seg file
            subprocess.call(
                ['java', '-Xmx2024m', '-jar', os.getcwd() + '/lium_spkdiarization-8.4.1.jar', '--fInputMask',
                 tmpdir + "/" + showName + '.wav', '--sOutputMask', tmpdir + "/" + showName + '.seg',
                 '--doCEClustering', '', showName])
            # use wav and .seg file to geneate multiple wav files
            if not os.path.exists(tmpdir + "/out"):
                os.makedirs(tmpdir + "/out")
            split_wav_by_seg(tmpdir + "/" + showName + '.wav', tmpdir + "/" + showName + '.seg', tmpdir + "/out")
            # compress multiple wav files and download to user
            shutil.make_archive(tmpdir + '/' + 'split_audio_' + showName, 'zip', tmpdir + '/out')

            # delete folder just created
            # @after_this_request
            # def cleanup(response):
            #    shutil.rmtree(tmpdir)
            #    return response

            # fname = 'split_audio_'+showName+'.zip'
            # mimetype = 'application/octet-stream'
            di = {}
            di['path'] = tmpdir
            di['filename'] = 'split_audio_' + showName + '.zip'
            return jsonify(result=di)
            # return send_from_directory(tmpdir, showName+'.wav', as_attachment=True, mimetype=mimetype)
            # response = make_response(send_from_directory(tmpdir, 'split_audio_'+showName+'.zip', as_attachment=True))
            # response.headers["Content-Disposition"] = "attachment; filename={split_audio.zip}".format(
            #     fname.encode().decode('latin-1'))
            # response.headers["Access-Control-Allow-Origin"]='*'
            # return response
            # return 'http://www.baidu.com'

            # return redirect(url_for('index'))
    return """
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    <p>%s</p>
    """ % "<br>".join(os.listdir(app.config['UPLOAD_FOLDER'], ))


if __name__ == "__main__":
    app.run(debug=True)