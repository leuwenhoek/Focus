from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():

    download_url = "https://drive.google.com/uc?export=download&id=1qmJPdlCumWFP0g2T_0X5GTzqP6QX0uGL"
    return render_template('home.html', download_url=download_url)

if __name__ == '__main__':
    app.run(debug=True)