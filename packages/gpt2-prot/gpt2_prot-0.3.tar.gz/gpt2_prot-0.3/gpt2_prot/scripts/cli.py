"""
Main entry point for gpt2-prot.
"""

from lightning.pytorch.cli import LightningCLI

from gpt2_prot.callbacks import PreviewCallback  # pylint: disable=unused-import
from gpt2_prot.data_module import BioDataModule
from gpt2_prot.gpt2 import GPT2


def main() -> None:
    """
    Lightning CLI entry point.
    """
    LightningCLI(GPT2, BioDataModule)


if __name__ == "__main__":
    main()
