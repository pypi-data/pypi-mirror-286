# gpt2-prot
Train biological language models at single NT or AA resolution.

This is a simple framework for training DNA or protein language models using an easily modifiable GPT-2 architecture. Training data, model hyperparameters and training settings can be easily configured using composable `yaml` config files and extendable using any `pytorch-lightning` settings.

## Features

- Simple and extendable data handling and GPT2 implementation using pytorch lightning
- Supports protein and DNA modelling out of the box
- Underlying torch dataset can download datasets (eg. from Uniprot or NCBI) and caches encoded data into a memory mapped array for handling large numbers of sequences

## Recipes

1. [Cas9 analogue generator](recipes/cas9_analog_generator.yml)
2. [Human genome foundation model](recipes/human_genome_foundation.yml)
3. [Uniref50 protein foundation model](recipes/uniref50_foundation.yml)

Note: These need to be fully tested and final model and data parameters will change.

## Installation

```bash
pip install gpt2_prot
```

## Usage

### From the CLI

```bash
gpt2-prot -h  # Show the CLI help

# Launch tensorboard to view loss, perplexity and model generations during training:
tensorboard --logdir lightning_logs/ &

# Run the demo config for cas9 protein language modelling:
# Since this uses Lightning you can overwrite parameters from the config using the command line
gpt2-prot fit --config recipes/cas9_analogues.yml --max_epochs 10

# Generate new sequences and configure the prompt:
gpt2-prot predict --config cas9_analog_generator.yml --data.prompt MATT --data.n_samples 50
```

### Yaml config (Tiny Cas9 protein language model demo)

```yaml
seed_everything: 0
ckpt_path: last  # Loads the most recent checkpoint in `checkpoints/`

trainer:
  max_epochs: 1000
  log_every_n_steps: 25
  fast_dev_run: false
  enable_checkpointing: true
  
  # Preconfigured TensorBoard logger
  logger:
    - class_path: lightning.pytorch.loggers.TensorBoardLogger
      init_args:
        save_dir: "."

  callbacks: 
    - class_path: lightning.pytorch.callbacks.ModelCheckpoint
      init_args:
        dirpath: "checkpoints/"  # Needs to be set for ckpt_path to correctly load `last`
        save_last: true
    
    # Configurable monitoring of model generations during training:
    - class_path: PreviewCallback
      init_args:
        mode: "aa"
        prompt: "M"
        length: 75
    
    # Inference mode config:
    - class_path: FastaInferenceWriter
      init_args:
        mode: "aa"
        output_file: "predictions.fasta"
        max_tokens: 100
        t: 1.0
        sample: true
        top_k: 5

# Model and optimiser hyperparameters:
model:
  config:
    vocab_size: 24  # mode dependent: aa -> 24, nt -> 5
    window_size: 16
    n_layers: 2
    n_heads: 2
    embed_d: 128
    emb_dropout: 0.1
    attn_dropout: 0.1
    res_dropout: 0.1
    adam_lr: 0.0003
    adam_weight_decay: 0.1
    adam_betas: [0.90, 0.95]

# Lightning datamodule parameters:
data:
  mode: "aa"
  directory: "seqs/"
  batch_size: 1
  max_seq_length: 100
  n_seq_limit: 500
  loader_num_workers: 2

  # The datamodule can also handle downloading datasets: 
  downloads: [
    ["https://rest.uniprot.org/uniprotkb/stream?compressed=true&format=fasta&query=%28gene%3Acas9%29", "uniprot_cas9.fasta.gz"]
  ]
  
  # Optionally set the inference prompt: 
  prompt: "M"
  n_samples: 100
```

## Development

### Installation From source

```bash
micromamba create -f environment.yml  # or conda etc.
micromamba activate gpt2-prot

pip install .  # Basic install
pip install -e ".[dev]"  # Install in editable mode with dev dependencies
pip install ".[test]"  # Install the package and all test dependencies
```

### Running pre-commit hooks

```bash
# Install the hooks:
pre-commit install

# Run all the hooks:
pre-commit run --all-files

# Run unit tests:
pytest
```