import torch
from torch import nn, Tensor
from transformers import AutoTokenizer, AutoModelForTextEncoding, PreTrainedTokenizer
from pythae.models.nn import BaseEncoder
from pythae.models.base.base_utils import ModelOutput


class HiddenStateEncoder(BaseEncoder):
    """
    Encoder class for LLM hidden states.


    """

    def __init__(self, latent_size: int,
                 device: str = "cpu",
                 args=None):  # Args is a ModelConfig instance
        """
        Initializes the SentenceEncoder with a specified model, latent size, tokenizers, and device.

        Args:
            model_path (str): Path/locator to the pre-trained model.
            latent_size (int): Size of the latent space.
            decoder_tokenizer (PreTrainedTokenizer): Tokenizer for decoding input tensors.
            device (str): Device to allocate model and data (e.g., 'cpu', 'cuda').
            args (ModelConfig, optional): Additional configuration arguments.
        """
        BaseEncoder.__init__(self)
        self.linear = nn.Linear(self.encoder.config.hidden_size, 2 * latent_size, bias=False, device=device)

    def forward(self, x: Tensor) -> ModelOutput:
        """
        Processes the input tensor through the encoder and linear transformation to produce latent variables.

        Args:
            x (Tensor): Input tensor containing token IDs.

        Returns:
            ModelOutput: Object containing the latent embedding and log covariance.
        """
        x = torch.squeeze(x).to(self.device)

        # Fix for pythae device allocation bug
        self._encoder[0] = self._encoder[0].to(self.device)
        self.linear = self.linear.to(self.device)

        tok_ids = torch.argmax(x, dim=-1)
        input = self.decoder_tokenizer.batch_decode(tok_ids, clean_up_tokenization_spaces=False, skip_special_tokens=True)
        enc_toks = self.tokenizer(input, padding=True, truncation=True, return_tensors='pt')
        enc_attn_mask = enc_toks["attention_mask"].to(self.device)

        encoded = self.encoder(input_ids=enc_toks["input_ids"].to(self.device), attention_mask=enc_attn_mask)
        pooled = mean_pooling(encoded, enc_attn_mask)
        mean, logvar = self.linear(pooled).chunk(2, -1)
        output = ModelOutput(
            embedding=mean,
            log_covariance=logvar
        )

        # Debug print (inputs)
        if (self.debug):
            if (self._dbg_counter % 100 == 0):
                with open(self.output_log_filepath, "w", encoding="utf-8") as enc_log_file:
                    # print("\n".join(input[:2]))
                    print("\n".join(self.tokenizer.batch_decode(enc_toks["input_ids"])), file=enc_log_file)
                    print("\n", "-" * 40, "\n", file=enc_log_file)
            self._dbg_counter += 1

        return output
