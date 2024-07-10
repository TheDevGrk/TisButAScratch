from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
  values = []
        
  return render_template("index.html", values = values)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)
