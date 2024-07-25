"""
General purpose GPT2 implementation in pytorch lightning.
"""

from math import sqrt
from typing import NamedTuple

import lightning as L
import torch
from torch import nn
from torch.nn import functional as F
from torcheval.metrics.functional.text import perplexity


class GPT2Config(NamedTuple):
    """Hyperparameters for GPT2."""

    vocab_size: int
    window_size: int

    n_layers: int
    n_heads: int
    embed_d: int

    emb_dropout: float
    attn_dropout: float
    res_dropout: float

    adam_lr: float
    adam_weight_decay: float
    adam_betas: tuple[float, float]


class PredictConfig(NamedTuple):
    """Parameters for model generations."""

    max_tokens: int = 100
    sample: bool = False
    t: float = 1.0
    top_k: int | None = None


class TransformerBlock(nn.Module):
    """
    Decoder only GPT2 transformer block.

    Params:
        embed_d (int): Internal embedding dimension.
        n_heads (int): Number of attention heads.
        attn_dropout (float): Dropout rate for attention weights.
        res_dropout (float): Dropout rate for residual connections.
    Returns:
        None
    """

    # pylint: disable=too-few-public-methods

    def __init__(
        self,
        embed_d: int,
        n_heads: int,
        attn_dropout: float,
        res_dropout: float,
    ) -> None:
        super().__init__()

        self.ln1 = nn.LayerNorm(embed_d)
        self.qkv = nn.Linear(embed_d, 3 * embed_d)
        self.attn = nn.MultiheadAttention(embed_d, n_heads, attn_dropout, batch_first=True)
        self.ln2 = nn.LayerNorm(embed_d)
        self.mlp = nn.Sequential(
            nn.Linear(embed_d, 4 * embed_d),
            nn.GELU(),
            nn.Linear(4 * embed_d, embed_d),
            nn.Dropout(res_dropout),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass through the transformer block."""
        q, k, v = self.qkv(self.ln1(x)).split(self.ln1.normalized_shape[0], dim=2)
        mask = self._lookahead_mask(x.size(1)).to(x.device) if self.training else None
        x_, _ = self.attn(q, k, v, attn_mask=mask, need_weights=False)
        x = x + x_
        x = x + self.mlp(self.ln2(x))
        return x

    @staticmethod
    def _lookahead_mask(d: int) -> torch.Tensor:
        """Generate a lookahead attention mask for a given dimension."""
        mask = torch.triu(torch.ones(d, d), diagonal=1)
        mask[mask.bool()] = -float("inf")
        return mask


class GPT2(L.LightningModule):
    """
    GPT2 language model.

    Params:
        config (GPT2Config): Hyperparameters for GPT2.
    Returns:
        None
    """

    def __init__(self, config: GPT2Config) -> None:
        super().__init__()
        self.config = config
        self.predict_config: PredictConfig = PredictConfig()

        transformer_blocks = [
            TransformerBlock(
                config.embed_d,
                config.n_heads,
                config.attn_dropout,
                config.res_dropout,
            )
            for _ in range(config.n_layers)
        ]

        self.transformer = nn.ModuleDict(
            {
                "tok_emb": nn.Embedding(config.vocab_size, config.embed_d),
                "pos_emb": nn.Embedding(config.window_size, config.embed_d),
                "dropout": nn.Dropout(config.emb_dropout),
                "blocks": nn.ModuleList(transformer_blocks),
                "ln": nn.LayerNorm(config.embed_d),
            }
        )
        self.lm_head = nn.Linear(config.embed_d, config.vocab_size, bias=False)

        self.apply(self._init_weights)
        for pn, p in self.named_parameters():
            if pn.endswith("mlp.2.weight"):
                torch.nn.init.normal_(p, mean=0.0, std=0.02 / sqrt(2 * config.n_layers))

    def _init_weights(self, module: nn.Module) -> None:
        """
        Initialise model weights with GPT2 defaults.

        TODO: Test what difference this makes as cribbed from Karpathy.

        Params:
            module (nn.Module): Module to initialise.
        Returns:
            None
        """

        if isinstance(module, nn.Linear):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)
            if module.bias is not None:
                torch.nn.init.zeros_(module.bias)
        if isinstance(module, nn.MultiheadAttention):
            torch.nn.init.normal_(module.in_proj_weight, mean=0.0, std=0.02)
            torch.nn.init.zeros_(module.in_proj_bias)
            torch.nn.init.normal_(module.out_proj.weight, mean=0.0, std=0.02)
            torch.nn.init.zeros_(module.out_proj.bias)
        elif isinstance(module, nn.Embedding):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)
        elif isinstance(module, nn.LayerNorm):
            torch.nn.init.zeros_(module.bias)
            torch.nn.init.ones_(module.weight)

    def configure_optimizers(self) -> torch.optim.AdamW:
        """
        Configure AdamW optimizer with some modules experiencing weight decay.

        Returns:
            torch.optim.AdamW: Configured optimizer.
        """

        decay = set()
        for mn, m in self.named_modules():
            if isinstance(m, (torch.nn.Linear, torch.nn.MultiheadAttention)):
                for pn, _ in m.named_parameters():
                    if pn.endswith("weight"):
                        decay.add(f"{mn}.{pn}" if mn else pn)

        param_dict = dict(self.named_parameters())
        all_params = set(param_dict.keys())
        no_decay = all_params - decay
        assert len(decay & no_decay) == 0
        assert len(param_dict.keys() - (decay | no_decay)) == 0

        optim_groups = [
            {
                "params": [param_dict[pn] for pn in sorted(list(decay))],
                "weight_decay": self.config.adam_weight_decay,
            },
            {
                "params": [param_dict[pn] for pn in sorted(list(no_decay))],
                "weight_decay": 0.0,
            },
        ]
        return torch.optim.AdamW(optim_groups, lr=self.config.adam_lr, betas=self.config.adam_betas)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Model forward pass."""
        # pylint: disable=arguments-differ

        _, t = x.size()
        pos = torch.arange(0, t, dtype=torch.long, device=x.device).unsqueeze(0)
        pos_emb = self.transformer.pos_emb(pos)
        tok_emb = self.transformer.tok_emb(x)
        x = self.transformer.dropout(tok_emb + pos_emb)
        for tblock in self.transformer.blocks:
            x = tblock(x)
        x = self.transformer.ln(x)
        return self.lm_head(x)

    def training_step(self, batch: torch.Tensor, batch_idx: torch.Tensor) -> torch.Tensor:
        """
        Lightning training step configuration.

        Params:
            batch (torch.Tensor): Batch of training data.
            batch_idx (torch.Tensor): Index of the batch (UNUSED).
        """
        # pylint: disable=arguments-differ

        _ = batch_idx
        y = batch[:, 1:]
        y_hat = torch.zeros(y.shape[0], 0, self.config.vocab_size, device=y.device)

        for i in range(1, batch.size(1)):
            start = i - self.config.window_size if i >= self.config.window_size else 0
            x = batch[:, start:i]
            x = self.forward(x)
            x = x[:, -1:, :]
            y_hat = torch.cat((y_hat, x), dim=1)

        loss = F.cross_entropy(y_hat.permute(0, 2, 1), y)
        perp = perplexity(y_hat, y)
        self.log("loss", loss, prog_bar=True)
        self.log("perplexity", perp, prog_bar=True)

        return loss

    @torch.no_grad()
    def generate(
        self,
        x: torch.Tensor,
        max_tokens: int,
        t: float = 1.0,
        sample: bool = False,
        top_k: int | None = None,
    ) -> torch.Tensor:
        """
        Generate from a given tokenised input.

        Params:
            x (torch.Tensor): Tokenised input sequence.
            max_tokens (int): Maximum number of tokens to generate.
            t (float): Temperature parameter.
            sample (bool): Sample from the distribution or take the largest probability.
            top_k (int | None): Top-k sampling parameter.
        """
        # pylint: disable=too-many-arguments

        for _ in range(max_tokens):
            if x.size(1) <= self.config.window_size:
                x_trunc = x
            else:
                x_trunc = x[:, -self.config.window_size :]

            logits = self.forward(x_trunc)
            logits = logits[:, -1, :] / t

            if top_k is not None:
                v, _ = torch.topk(logits, top_k)
                logits[logits < v[:, [-1]]] = -float("Inf")

            probs = F.softmax(logits, dim=-1)

            if sample:
                next_ = torch.multinomial(probs, num_samples=1)
            else:
                _, next_ = torch.topk(probs, k=1, dim=-1)

            x = torch.cat((x, next_), dim=-1)
        return x

    def predict_step(self, batch: torch.Tensor, batch_idx: torch.Tensor) -> torch.Tensor:
        """
        Lightning predict step configuration.

        Params:
            batch (torch.Tensor): Batch of training data.
            batch_idx (torch.Tensor): Index of the batch (UNUSED).
        """
        _ = batch_idx

        return self.generate(
            batch,
            max_tokens=self.predict_config.max_tokens,
            t=self.predict_config.t,
            sample=self.predict_config.sample,
            top_k=self.predict_config.top_k,
        )


if __name__ == "__main__":
    pass
