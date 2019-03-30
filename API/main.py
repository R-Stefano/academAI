from flask import Flask, render_template, request

import graph_loader, encoder
import tensorflow as tf
app = Flask(__name__)

isProduction=True
my_sess, x, y, enc=None, None, None, None
#home() function is called when the user hit the landing page(/).
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/checkSetup")
def checkSetup():
    if not(my_sess):
        print('checking setup..')
        setupServer()
    else:
        print('model already loaded')
    return 'model loaded'
#
@app.route('/generate_text', methods=['POST'])
def generate_text():
    if request.method == "POST":
        #Retrieve input
        data=request.json['input']

        response=send_response(data)

        #response='Processing text..'
    else:
        response='Some error occured..'
    return response

def send_response(data):
    #encode the input to feed into the model
    context_tokens = enc.encode(data)
    
    if isProduction:
        #Get the model output (it requires time)
        out = my_sess.run(y, feed_dict={x: [context_tokens for _ in range(1)]})

        out=out[:, len(context_tokens):]
        data = enc.decode(out[0])
    else:
        data = enc.decode(context_tokens)
    return data

def setupServer():
    global my_sess, x, y, enc
    print('Instantiating graph,encoder and session..')
    graph=graph_loader.load_graph('117M', isProduction)
    print('starting session')
    # We access the input and output nodes 
    #Placeholder is an operation. But if you add :0 you retrieve the tensor
    x = graph.get_tensor_by_name('input:0')
    y = graph.get_tensor_by_name('output:0')

    my_sess=tf.Session(graph=graph)

    enc = encoder.get_encoder('117M')
    print('setup ready..')

if __name__ == "__main__":
    app.run(debug=True)