import os, argparse
import json

import tensorflow as tf

#used to create the model
import sample, model

'''
I can't use the meta data because there are hiperparams to set 
manually that are not stored in the file.
'''
dir = os.path.dirname(os.path.realpath(__file__))

def freeze_graph(model_dir, output_node_names):
    """Extract the sub graph defined by the output nodes and convert 
    all its variables into constant 
    Args:
        model_dir: the root folder containing the checkpoint state file
        output_node_names: a string, containing all the output node's names, 
                            comma separated
    """
    if not tf.gfile.Exists(model_dir):
        raise AssertionError(
            "Export directory doesn't exists. Please specify an export "
            "directory: %s" % model_dir)

    if not output_node_names:
        print("You need to supply the name of a node to --output_node_names.")
        return -1
    
    #Create the frozen graph in the same folder of the model weights
    output_graph = model_dir + "/frozen_model.pb"

    # We clear devices to allow TensorFlow to control on which device it will load operations
    clear_devices = True

    # We start a session using a temporary fresh Graph
    with tf.Session(graph=tf.Graph()) as sess:
        #1. Set hyperparams
        print('Setting hyperparams..')
        hparams = model.default_hparams()
        with open(model_dir+'/hparams.json') as f:
            hparams.override_from_dict(json.load(f))

        batch_size=1
        length = hparams.n_ctx // 2
        temperature=1
        top_k=0
        #2. Create the graph
        print('Creating the graph..')
        #input
        context = tf.placeholder(tf.int32, [batch_size, None], name='input')
        #output
        output = sample.sample_sequence(
            hparams=hparams, length=length,
            context=context,
            batch_size=batch_size,
            temperature=temperature, top_k=top_k
        )
        #3. Restore weights
        print('Restoring weights..')
        saver = tf.train.Saver()
        ckpt = tf.train.latest_checkpoint(model_dir)
        saver.restore(sess, ckpt)

        #Add another operation called output to easily retrieve the output
        output=tf.identity(output, name='output')

        print('Freezing model..')
        # We use a built-in TF helper to export variables to constants
        output_graph_def = tf.graph_util.convert_variables_to_constants(
            sess, # The session is used to retrieve the weights
            tf.get_default_graph().as_graph_def(), # The graph_def is used to retrieve the nodes 
            output_node_names.split(",") # The output node names are used to select the usefull nodes
        ) 

        print('Saving frozen model into', output_graph)
        # Finally we serialize and dump the output graph to the filesystem
        with tf.gfile.GFile(output_graph, "wb") as f:
            f.write(output_graph_def.SerializeToString())
        print("%d ops in the final graph." % len(output_graph_def.node))

    return output_graph_def

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_dir", type=str, default="models/117M", help="Model folder to export")
    parser.add_argument("--output_node_names", type=str, default="input,output", help="The name of the output nodes, comma separated.")
    args = parser.parse_args()

    freeze_graph(args.model_dir, args.output_node_names)