# copyright: skpro developers, BSD-3-Clause License (see LICENSE file)
"""Inverse Gamma probability distribution."""

__author__ = ["meraldoantonio"]

import pandas as pd
from scipy.stats import invgamma, rv_continuous

from skpro.distributions.adapters.scipy import _ScipyAdapter


class InverseGamma(_ScipyAdapter):
    r"""Inverse Gamma Distribution.

    Most methods wrap ``scipy.stats.invgamma``.

    The Inverse Gamma Distribution is parameterized by shape :math:`\alpha` and
    scale :math:`\beta`, such that the pdf is

    .. math:: f(x) = \frac{\beta^{\alpha} x^{-\alpha-1} \exp\left(-\frac{\beta}{x}\right)}{\tau(\alpha)}

    where :math:`\tau(\alpha)` is the Gamma function.
    For all positive integers, :math:`\tau(\alpha) = (\alpha-1)!`.

    Parameters
    ----------
    alpha : float or array of float (1D or 2D)
        It represents the shape parameter.
    beta : float or array of float (1D or 2D)
        It represents the scale parameter.
    index : pd.Index, optional, default = RangeIndex
    columns : pd.Index, optional, default = RangeIndex

    Examples
    --------
    >>> from skpro.distributions.inversegamma import InverseGamma

    >>> d = InverseGamma(beta=[[1, 1], [2, 3], [4, 5]], alpha=2)
    """  # noqa: E501

    _tags = {
        "capabilities:approx": ["energy", "pdfnorm"],
        "capabilities:exact": ["mean", "var", "pdf", "log_pdf", "cdf", "ppf"],
        "distr:measuretype": "continuous",
        "distr:paramtype": "parametric",
        "broadcast_init": "on",
    }

    def __init__(self, alpha, beta, index=None, columns=None):
        self.alpha = alpha
        self.beta = beta

        super().__init__(index=index, columns=columns)

    def _get_scipy_object(self) -> rv_continuous:
        return invgamma

    def _get_scipy_param(self):
        alpha = self._bc_params["alpha"]
        beta = self._bc_params["beta"]
        scale = beta

        return [], {"a": alpha, "scale": scale}

    @classmethod
    def get_test_params(cls, parameter_set="default"):
        """Return testing parameter settings for the estimator."""
        # array case examples
        params1 = {"alpha": [6, 2.5], "beta": [[1, 1], [2, 3], [4, 5]]}
        params2 = {
            "alpha": 2,
            "beta": 3,
            "index": pd.Index([1, 2, 5]),
            "columns": pd.Index(["a", "b"]),
        }
        # scalar case examples
        params3 = {"alpha": 1.5, "beta": 2.1}

        return [params1, params2, params3]
