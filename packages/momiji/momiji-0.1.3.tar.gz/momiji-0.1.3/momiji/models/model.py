import torch.nn as nn


class MyModel(nn.Module):
    def __init__(
        self, in_dim: int, out_dim: int, clock_name: str, features: list
    ):
        """A simple linear model for testing aging clock prediction.
        Args:
            in_dim (int): input dimension
            out_dim (int): output dimension
            clock_name (str): clock name to predict. Must to be in the adata.
            features (list): feature names of adata.var.index
        """
        super(MyModel, self).__init__()

        self.linear = nn.Linear(in_dim, out_dim)
        self.features = features
        self.metadata = {"clock_name": clock_name}

    def forward(self, x):
        return self.linear(x)


__all__ = ["MyModel"]
