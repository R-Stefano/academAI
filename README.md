# AcademIA
<p align="center"><img src="https://github.com/R-Stefano/academIA/blob/master/img.png" /></p>

The project borns with the idea of developing an Intelligent Scientific creative engine able to providing insights about a scientific area of interest scanning and learning the related literature. 


The agent is a variation of a small (117M parameter) version of GPT-2.O developed by [**openAI**](https://openai.com/).
See more details at [blog post](https://blog.openai.com/better-language-models/).

The code and samples from the paper ["Language Models are Unsupervised Multitask Learners"](https://d4mucfpksywv.cloudfront.net/better-language-models/language-models.pdf).

## Contributing
The idea excites you and you are interested in *Natural Language Processing*? 

Why not contributing?

Join us to Slack https://academai.slack.com  
## Installation
irst of all, you have to create a virtualenv and activate it.
On the original repo there is the docker installation guideline as well. 

Git clone this repository, and `cd` into the directory
```
git clone https://github.com/R-Stefano/gpt-2.git
cd gpt-2
```

Download the model data

```
sh download_model.sh 117M
```

Install the required packages
```
python3 -m pip install -r requirements.txt
```

Set the environment variable to override the standard stream settings in UTF-8 mode.
```
export PYTHONIOENCODING=UTF-8
```

Finally, test that it is working running
```
python3 src/interactive_conditional_samples.py
```
## Get Started
You could start running it on [**Google Colab**](https://colab.research.google.com/gist/R-Stefano/db6b50d73bec98186b1ab5c726869585/gpt_2.ipynb)

### 1. Unconditional sample generation

To generate unconditional samples from the small model:
```
python3 src/generate_unconditional_samples.py | tee /tmp/samples
```
There are various flags for controlling the samples:
```
python3 src/generate_unconditional_samples.py --top_k 40 --temperature 0.7 | tee /tmp/samples
```

To check flag descriptions, use:
```
python3 src/generate_unconditional_samples.py -- --help
```

### 2. Conditional sample generation

To give the model custom prompts, you can use:
```
python3 src/interactive_conditional_samples.py --top_k 40
```

To check flag descriptions, use:
```
python3 src/interactive_conditional_samples.py -- --help
```

### 3. Fine tuning on custom datasets

To retrain GPT-2 117M model on a custom text dataset:

```
PYTHONPATH=src ./train.py --dataset data/
```

If you want to precompute the dataset's encoding for multiple runs, you can instead use:

```
PYTHONPATH=src ./encode.py <file|directory|glob> /path/to/encoded.npz
PYTHONPATH=src ./train --dataset /path/to/encoded.npz
```

## Citation

Please use the following bibtex entry:
```
@article{radford2019language,
  title={Language Models are Unsupervised Multitask Learners},
  author={Radford, Alec and Wu, Jeff and Child, Rewon and Luan, David and Amodei, Dario and Sutskever, Ilya},
  year={2019}
}
```

## License

MIT
