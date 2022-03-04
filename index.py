from flask import Flask
from flask import Flask, render_template, redirect, url_for, request, session, send_file
import requests
from pytube import YouTube
from youtube_dl import *
from io import BytesIO



app = Flask(__name__)



@app.route('/', methods=['POST', 'GET'])
def homepage():
    return render_template('index.html')



@app.route('/contact', methods=['GET', 'POST'])
def contact():
    msg = ''
    url = 'https://docs.google.com/forms/u/0/d/e/1FAIpQLSdzTI0wDvoCKF13qeA1Zg6c0mOZWT_pAuC6FWVS_6SbR-QyxA/formResponse'
    if request.method == "POST":
        name = request.form['name'].strip()
        mail = request.form['mail'].strip()
        msgs = request.form['msgs'].strip()
        param = f"entry.1127945278={name}&entry.1233515303={mail}&entry.1184040836={msgs}"
        try:
            requests.post(url, params = param)
            msg = 'ĐÃ GỬI, TEAM SẼ LIÊN HỆ VỚI BẠN TRONG THỜI GIAN SỚM NHẤT'
        except:
            msg = 'ĐÃ CÓ LỖI XẢY RA, VUI LÒNG THỬ LẠI!!!'
    return render_template('index.html', msg=msg)



@app.route('/download_youtube', methods=['GET', 'POST'])
def find_video():
    global embed_url
    embed_url = ''
    if request.method == "POST":
        id_ = request.form['url'].strip().split('watch?v=')[1]
        embed_url = f'https://www.youtube.com/embed/{id_}'
    return render_template('download_youtube.html', embed_url=embed_url)


@app.route('/mp4_download', methods=['GET', 'POST'])
def mp4_download():
    error_msg = ''
    if request.method == "POST":
        try:
            buffer = BytesIO()
            video = YouTube(embed_url).streams.get_by_itag(22)
            video.stream_to_buffer(buffer)
            buffer.seek(0)
            return send_file(buffer, as_attachment=True, download_name="Video - YT2Video.mp4")
        except:
            error_msg = 'CÓ LỖI XẢY RA, VUI LÒNG THỬ LẠI!'
    return render_template('download_youtube.html', error_msg=error_msg)


@app.route('/mp3_download', methods=['GET', 'POST'])
def mp3_download():
    error_msg = ''
    if request.method == "POST":
        try:
            v_info=YoutubeDL().extract_info(url=embed_url,download=False)
            f_mp3=f"{v_info['title']}.mp3"
            options={
                'format':'bestaudio/best',
                'keepvideo':False,
                'outtmpl':f_mp3,}
            with YoutubeDL(options) as ydl:
                buffer = BytesIO()
                ydl.stream_to_buffer(buffer).download([embed_url])
                buffer.seek(0)
                return send_file(buffer, as_attachment=True, download_name="Video - YT2Video.mp3")
        except:
            error_msg = 'CÓ LỖI XẢY RA, VUI LÒNG THỬ LẠI!'
    return render_template('download_youtube.html', error_msg=error_msg)


@app.errorhandler()
def notfound

# ===============================================================

if __name__ == '__main__':
    app.run(debug=True)
