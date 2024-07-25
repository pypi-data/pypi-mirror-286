"""
Lightning callback to inspect model generations during training.
"""

import hashlib
from pathlib import Path

import lightning as L
import torch
from lightning.pytorch.callbacks import BasePredictionWriter

from gpt2_prot.data_module import AATokenizer, NTTokenizer
from gpt2_prot.gpt2 import PredictConfig


class PreviewCallback(L.Callback):
    """
    Callback to print a preview of the models generation.

    Params:
        mode (str): Run in protein (aa) or nucleotide mode.
        prompt (str): The prompt to generate from.
        length (int): Sequence length to generate.
    Returns:
        None
    """

    # pylint: disable=too-few-public-methods

    def __init__(self, mode: str, prompt: str, length: int = 50) -> None:
        super().__init__()
        assert mode in ["aa", "nt"]
        self.mode = mode
        self.prompt = prompt
        self.length = length

    def on_train_epoch_end(self, trainer: L.Trainer, pl_module: L.LightningModule) -> None:
        """
        Logic to run the model generation, additionally logs to tensorboard.

        Params:
            trainer (L.Trainer): The trainer object.
            pl_module (L.LightningModule): The LightningModule object.
        Returns:
            None
        """
        pl_module.eval()

        if self.mode == "aa":
            tok = AATokenizer()
        else:
            tok = NTTokenizer()

        prompt_enc = torch.LongTensor(tok(self.prompt)).unsqueeze(0).to(pl_module.device)

        generate_arguments = [
            {"t": 1.0, "sample": False, "top_k": None},
            {"t": 1.0, "sample": True, "top_k": None},
            {"t": 1.2, "sample": True, "top_k": 5},
        ]

        tag = "Model generation previews:"
        message = ""

        for args in generate_arguments:
            response_enc = pl_module.generate(prompt_enc, self.length, **args)
            seq = tok.decode(response_enc.flatten().tolist())
            message += f"({args}): {seq}\n"

        tensorboard = pl_module.logger.experiment  # type: ignore
        tensorboard.add_text(tag, message, trainer.global_step)

        print(tag, "\n", message)


class FastaInferenceWriter(BasePredictionWriter):
    """
    Callback to configure the model and write generated sequences to a fasta file.

    Params:
        output_file (Path): The path to the output file.
        mode (str): Run in protein (aa) or nucleotide mode.
        max_tokens (int): Maximum number of tokens to generate per sequence.
        t (float): Temperature parameter to use during inference.
        sample (bool): Whether to sample from model logits during inference.
        top_k (int | None): Top k parameter to use during inference.
    Returns:
        None
    """

    # pylint: disable=abstract-method, too-many-arguments
    def __init__(
        self,
        output_file: Path,
        mode: str,
        max_tokens: int,
        t: float,
        sample: bool,
        top_k: int | None,
    ):
        super().__init__(write_interval="epoch")
        self.output_file = output_file
        assert mode in ["aa", "nt"]
        self.mode = mode

        self.predict_config = PredictConfig(max_tokens=max_tokens, t=t, sample=sample, top_k=top_k)

        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        self.output_file.touch(exist_ok=True)

    def on_predict_start(self, trainer: L.Trainer, pl_module: L.LightningModule):
        """
        Configure the model with inference parameters before predicting.

        Params:
            trainer (L.Trainer): The trainer object (UNUSED).
            pl_module (L.LightningModule): The LightningModule object.
        Returns:
            None
        """
        _ = trainer
        pl_module.predict_config = self.predict_config

    @staticmethod
    def _hash_sequence(sequence: str) -> str:
        return hashlib.sha256(sequence.encode("utf-8")).hexdigest()[:8]

    def write_on_epoch_end(
        self,
        trainer: L.Trainer,
        pl_module: L.LightningModule,
        predictions: list[torch.Tensor],
        batch_indices: list[int],
    ):
        """
        Decode the tokenised model generations and write to a fasta file.

        Params:
            trainer (L.Trainer): The trainer object (UNUSED).
            pl_module (L.LightningModule): The LightningModule object (UNUSED).
            predictions (list[torch.Tensor]): The model predictions.
            batch_indices (list[int]): The batch indices (UNUSED).
        Returns:
            None
        """
        _ = trainer, pl_module, batch_indices

        if self.mode == "aa":
            tok = AATokenizer()
        else:
            tok = NTTokenizer()

        out_file = self.output_file.open("a")

        for pred in predictions:
            seq = tok.decode(pred.flatten())
            print(f">{self._hash_sequence(seq)}\n{seq}", file=out_file)

        out_file.close()


if __name__ == "__main__":
    pass
