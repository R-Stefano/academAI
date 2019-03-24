import tensorflow as tf
import os 
from google.cloud import storage

def load_graph(model_name, isProduction):
    if isProduction:
        client = storage.Client()
        bucket = client.get_bucket('academai-235417.appspot.com')
        blob = bucket.get_blob('models/frozen_model.pb')
        graph_str = blob.download_as_string()

        graph_def = tf.GraphDef()
        graph_def.ParseFromString(graph_str)

    else:
        # We load the protobuf file from the disk and parse it to retrieve the 
        # unserialized graph_def
        with tf.gfile.GFile(os.path.join('models', model_name, 'frozen_model.pb'), "rb") as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())

    # Then, we import the graph_def into a new Graph and returns it 
    with tf.Graph().as_default() as graph:
        # The name var will prefix every op/nodes in your graph
        # Since we load everything in a new graph, this is not needed
        tf.import_graph_def(graph_def, name='')
    
    return graph

#for op in graph.get_operations():
#    if op.name=='Placeholder':
#        print(op)
#    print(op.name)

