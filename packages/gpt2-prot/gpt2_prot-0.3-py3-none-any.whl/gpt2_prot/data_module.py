"""
Character tokenizers and Lightning DataModule for handling biological datasets.
"""

import gzip
from pathlib import Path

import lightning as L
import numpy as np
import requests
import torch
from Bio import SeqIO
from torch.utils.data import DataLoader, Dataset
from tqdm import tqdm


class CharTokenizer:
    """
    Simple single character tokenizer superclass.

    Params:
        vocab: List of characters to be used as the vocabulary.
        pad_char: Character to use for padding.
    Returns:
        None
    """

    def __init__(
        self,
        vocab: list[str],
        pad_char: str = "X",
    ) -> None:
        # pylint: disable=unnecessary-comprehension

        assert pad_char in vocab

        self.vocab = vocab
        self.pad_char = pad_char

        self.encoder = {v: i for i, v in enumerate(vocab)}
        self.decoder = {i: v for i, v in enumerate(vocab)}

    def __call__(self, data: str, pad_to: int | None = None) -> list[int]:
        return self.encode(data, pad_to)

    def __len__(self) -> int:
        return len(self.vocab)

    def encode(self, data: str, pad_to: int | None = None) -> list[int]:
        """
        Call the encoder, padding and cropping to the desired length.

        Params:
            data (str): Sequence to encode.
            pad_to (int): Length to pad or crop to.
        Returns:
            list[int]: Encoded sequence.
        """
        if pad_to is not None:
            data = data[:pad_to]
            data += self.pad_char * (pad_to - len(data))
        return [self.encoder[c] for c in data]

    def decode(self, data: torch.Tensor) -> str:
        """
        Decode an encoded sequence.

        TODO: Correct type hint.

        Params:
            data (torch.Tensor): Encoded sequence.
        Returns:
            str: Decoded sequence.
        """
        return "".join([self.decoder[int(i)] for i in data])


class NTTokenizer(CharTokenizer):
    """
    DNA nucleotide character tokenizer.

    Uses IUPAC nucleotide codes and `N` for padding. (Vocab size = 5)
    """

    def __init__(self) -> None:
        super().__init__(list("ATCGN"), "N")


class AATokenizer(CharTokenizer):
    """
    Protein amino acid character tokenizer.

    Uses standard AAs, `ZBU` non-canonical AAs and `X` for padding.
    (Vocab size = 26)
    """

    def __init__(self) -> None:
        super().__init__(list("ACDEFGHIKLMNPQRSTVWYZBUX"), "X")


class FastaDataset(Dataset):
    """
    Pytorch Dataset for loading, encoding and serving sequences from fasta files.

    Params:
        directory (Path): Path to a directory containing .fa or .fasta files (can be gzipped).
        tokenizer (CharTokenizer): Tokenizer to use for encoding sequences.
        max_len (int): Maximum sequence length to crop and pad sequences to.
        limit (int): Maximum number of sequences to load.
        bin_name (Path): Path to a binary file to where the encoded data is stored.
    Returns:
        None

    Note: If `bin_name` already exists, it will be overwritten.
    """

    def __init__(
        self,
        directory: Path,
        tokenizer: CharTokenizer,
        max_len: int,
        limit: int,
        bin_name: Path = Path("train.bin"),
    ) -> None:
        # pylint: disable=too-many-arguments,consider-using-with, unspecified-encoding

        print("Initializing FastaDataset...")
        self.files = (
            list(directory.glob("*.fasta"))
            + list(directory.glob("*.fa"))
            + list(directory.glob("*.fasta.gz"))
            + list(directory.glob("*.fa.gz"))
        )
        self.bin_name = bin_name
        self.tokenizer = tokenizer
        self.max_len = max_len

        assert np.iinfo(np.uint8).max >= len(tokenizer)  # Ensure vocab fits into 256 tokens

        # Init memmap to hold the maximum number of sequences of length max_len:
        self.data = np.memmap(self.bin_name, dtype=np.uint8, mode="w+", shape=(limit, max_len))

        # Loop through files and sequences, tokenise and store in the memmap:
        n_seqs = 0
        for file in self.files:
            print(f"Loading: {file}...")

            if file.suffix == ".gz":
                handle = gzip.open(file, "rt")
            else:
                handle = open(file, "r")

            for record in SeqIO.parse(handle, "fasta"):
                seq = str(record.seq).upper()[:max_len]
                self.data[n_seqs] = tokenizer(seq, max_len)
                n_seqs += 1
                if n_seqs >= limit:
                    break

            handle.close()

        print(f"Finished: loaded {n_seqs} sequences ({max_len*n_seqs} tokens)")
        self._len = n_seqs

        # Resize the memmap to the actual number of sequences:
        self.data = np.memmap(self.bin_name, dtype=np.uint8, mode="r+", shape=(n_seqs, max_len))

    def __len__(self) -> int:
        return self._len

    def __getitem__(self, idx: int) -> torch.Tensor:
        data = self.data[idx]
        return torch.LongTensor(data)

    def cleanup(self) -> None:
        """
        Flush and remove the dataset mmap binary.
        """
        self.data.flush()
        self.bin_name.unlink()


class InferenceDataset(Dataset):
    """Simple dataset to serve the model the tokenised prompt during inference."""

    def __init__(self, prompt: str, tokenizer: CharTokenizer, n_samples) -> None:
        self.prompt = prompt
        self.tokenizer = tokenizer

        self.x = [self.tokenizer(self.prompt)] * n_samples

    def __len__(self) -> int:
        return len(self.x)

    def __getitem__(self, idx: int) -> torch.Tensor:
        return torch.LongTensor(self.x[idx])


class BioDataModule(L.LightningDataModule):
    """
    Pytorch Lightning DataModule for loading, encoding and serving sequences from fasta files.

    Params:
        mode (str): Either "nt" or "aa" to indicate the type of sequences to loadu
        directory (Path): Path to a directory containing .fa or .fasta files (can be gzipped).
        batch_size (int): Batch size to use for training.
        max_seq_length (int): Maximum sequence length to crop and pad sequences to.
        n_seq_limit (int): Maximum number of sequences to load.
        loader_num_workers (int): Number of workers to use for the torch DataLoader.
        downloads (list[tuple[str, str]]): List of tuples containing URLs and filenames to download.
    Returns:
        None
    """

    # pylint: disable=too-many-instance-attributes

    def __init__(
        self,
        mode: str,
        directory: Path,
        batch_size: int,
        max_seq_length: int,
        n_seq_limit: int,
        loader_num_workers: int,
        downloads: list[tuple[str, str]] | None,
        prompt: str | None = None,
        n_samples: int | None = None,
    ) -> None:

        # pylint: disable=too-many-arguments
        super().__init__()

        assert mode in ["nt", "aa"]

        self.mode = mode
        self.directory = directory
        self.batch_size = batch_size
        self.max_seq_length = max_seq_length
        self.n_seq_limit = n_seq_limit
        self.loader_num_workers = loader_num_workers
        self.downloads = downloads

        # Predict mode settings:
        self.prompt = prompt
        self.n_samples = n_samples

        if self.downloads is not None:
            for url, filename in self.downloads:
                self.download_dataset(url, filename)

        self.tokenizer = NTTokenizer() if self.mode == "nt" else AATokenizer()
        self.train_dataset = FastaDataset(
            self.directory, self.tokenizer, self.max_seq_length, self.n_seq_limit
        )

    def download_dataset(self, url: str, filename: str, chunk_size: int = 1024 * 10) -> None:
        """
        Download a file from a URL to a local file.

        Params:
            url (str): URL to download from.
            filename (str): Filename to save the file as.
            chunk_size (int): Chunk size to use for downloading.
        Returns:
                None
        """
        assert self.downloads is not None
        download_path = self.directory / filename

        if download_path.exists():
            print(f"Downloaded dataset already exists: {download_path}")
            return

        print(f"Downloading dataset from: {url}")
        self.directory.mkdir(exist_ok=True)
        response = requests.get(url, stream=True, timeout=None)

        size_mb = int(response.headers.get("content-length", 0)) / (1024**2)
        progress_bar = tqdm(total=int(size_mb), unit="MB")
        with open(download_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    progress_bar.update(chunk_size / (1024**2))

    def train_dataloader(self) -> DataLoader:
        """Return the DataLoader for training."""
        return DataLoader(
            self.train_dataset,
            batch_size=self.batch_size,
            num_workers=self.loader_num_workers,
        )

    def teardown(self, stage: str | None = None) -> None:
        """Call the cleanup method of the train dataset."""
        _ = stage
        self.train_dataset.cleanup()

    def predict_dataloader(self) -> DataLoader:
        """Return the DataLoader for inference."""
        assert self.prompt is not None

        dataset = InferenceDataset(self.prompt, self.tokenizer, self.n_samples)
        return DataLoader(dataset, batch_size=1, num_workers=self.loader_num_workers)


if __name__ == "__main__":
    pass
