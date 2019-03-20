# AcademIA
OpenAI released  a smaller (117M parameter) version of GPT-2.

See more details at [blog post](https://blog.openai.com/better-language-models/).

The code and samples from the paper ["Language Models are Unsupervised Multitask Learners"](https://d4mucfpksywv.cloudfront.net/better-language-models/language-models.pdf).

## Installation

Git clone this repository, and `cd` into directory for remaining commands
```
git clone https://github.com/R-Stefano/gpt-2.git
cd gpt-2
```

On the original repo there is the docker installation guideline. I'm going to use only **virtualenv**

### Installation
First of all, you have been created a virtualenv and activated it.

Download the model data
```
sh download_model.sh 117M
```

Install the required packages
```
pip3 install -r requirements.txt
```

Set the environment variable to override the standard stream settings in UTF-8 mode.
```
export PYTHONIOENCODING=UTF-8
```

Finally, test that it is working running
```
python3 src/interactive_conditional_samples.py
```

### Unconditional sample generation

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

### Conditional sample generation

To give the model custom prompts, you can use:
```
python3 src/interactive_conditional_samples.py --top_k 40
```

To check flag descriptions, use:
```
python3 src/interactive_conditional_samples.py -- --help
```

### Fine tuning on custom datasets

To retrain GPT-2 117M model on a custom text dataset:

```
PYTHONPATH=src ./train --dataset <file|directory|glob>
```

If you want to precompute the dataset's encoding for multiple runs, you can instead use:

```
PYTHONPATH=src ./encode.py <file|directory|glob> /path/to/encoded.npz
PYTHONPATH=src ./train --dataset /path/to/encoded.npz
```

## GPT-2 samples

| WARNING: Samples are unfiltered and may contain offensive content. |
| --- |

While we have not yet released GPT-2 itself, you can see some samples from it in the `gpt-2-samples` folder.
We show unconditional samples with default settings (temperature 1 and no truncation), with temperature 0.7, and with truncation with top_k 40.
We show conditional samples, with contexts drawn from `WebText`'s test set, with default settings (temperature 1 and no truncation), with temperature 0.7, and with truncation with top_k 40.

## Citation

Please use the following bibtex entry:
```
@article{radford2019language,
  title={Language Models are Unsupervised Multitask Learners},
  author={Radford, Alec and Wu, Jeff and Child, Rewon and Luan, David and Amodei, Dario and Sutskever, Ilya},
  year={2019}
}
```

## Future work

We may release code for evaluating the models on various benchmarks.

We are still considering release of the larger models.

## License

MIT
