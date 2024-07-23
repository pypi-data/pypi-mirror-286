import sys
import os
import pickle
import numpy as np
import pythae.models.base.base_utils
import torch
import torch.nn.functional as F
from typing import Tuple, List, Optional
from copy import deepcopy

from transformers import AutoTokenizer, AutoModelForCausalLM
from pythae.trainers import BaseTrainerConfig
from pythae.models.nn import BaseEncoder, BaseDecoder
from pythae.models.base.base_config import BaseAEConfig, EnvironmentConfig
from torch import Tensor
from torch.utils.tensorboard import SummaryWriter
from pythae.models.vae import VAE, VAEConfig
from pythae.trainers.training_callbacks import TrainingCallback


class LangHiddenVAE(VAE):
    """
    A language-oriented Variational Autoencoder (VAE) that can be used for text generation.

    Args:
        model_config (VAEConfig): The configuration of the VAE model.
        encoder (Optional[BaseEncoder]): Language encoder model that processes input data and returns sentence embeddings.
        decoder (Optional[BaseDecoder]): Language decoder model that generates text from latent representations.
    """

    loss_writer = SummaryWriter()

    def __init__(
            self,
            model_config: VAEConfig,
            encoder: Optional[BaseEncoder],
            decoder: Optional[BaseDecoder]
    ):
        super().__init__(model_config=model_config, encoder=encoder, decoder=decoder)
        self.cur_beta: float = 0.0
        self.target_kl = 1.0

        # Logging losses
        self.debug = False
        self._dbg_counter = 0
        self._loss_agg = [0.0, 0.0]