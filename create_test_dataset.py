import json

dataset=[
    {
        "question": "What is a neuron?",
        "answer": "The neuron is the basic working unit of the brain, a specialized cell designed to transmit information to other nerve cells, muscle, or gland cells. Neurons are cells within the nervous system that transmit information to other nerve cells, muscle, or gland cells. Most neurons have a cell body, an axon, and dendrites."
    },

    {
        "question": "What is the role of the hippocampus in episodic memory?",
        "answer": "The formation of new episodic memories requires the medial temporal lobe, a structure that includes the hippocampus. Without the medial temporal lobe, one is able to form new procedural memories (such as playing the piano) but cannot remember the events during which they happened (See the hippocampus and memory)."
    }
]

with open('test_dataset.json', 'w') as outfile:  
    json.dump(dataset, outfile)