from flask import Flask, render_template, request

app = Flask(__name__)

#home() function is called when the user hit the landing page(/).
@app.route("/")
def home():
    return render_template("home.html")

#
@app.route('/generate_text', methods=['POST'])
def generate_text():
    if request.method == "POST":
         #perform action here
        data=request.json['input']
    else:
        data='Invalid request'
    return data


if __name__ == "__main__":
    app.run(debug=True)