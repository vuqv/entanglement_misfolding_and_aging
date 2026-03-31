import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# file checksum
import hashlib
from pathlib import Path

# Matplotlib setting
BASE_FONTSIZE = 8

def set_nature_style(base_fontsize=8):
    """
    Apply a compact, publication-style Matplotlib theme.

    This helper updates global `matplotlib.rcParams` so subsequent plots use
    a consistent style (font sizes, line widths, tick appearance, and figure
    export defaults) aligned with the project's notebook figures.

    Parameters
    ----------
    base_fontsize : int or float, default=8
        Base font size used for axis labels, titles, ticks, and legends.

    Returns
    -------
    None
        The function mutates Matplotlib global configuration in-place.
    """
    mpl.rcParams.update({
        "font.family": "Arial",
        "font.size": base_fontsize,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,

        "axes.labelsize": base_fontsize,
        "axes.titlesize": base_fontsize,
        "axes.linewidth": 0.8,
        "axes.spines.right": False,
        "axes.spines.top": False,

        "xtick.labelsize": base_fontsize,
        "ytick.labelsize": base_fontsize,
        "xtick.direction": "out",
        "ytick.direction": "out",
        "xtick.major.size": 0,
        "ytick.major.size": 3,
        "xtick.major.width": 0.8,
        "ytick.major.width": 0.8,

        "lines.linewidth": 1.2,
        "lines.markersize": 4,

        "legend.fontsize": base_fontsize,
        "legend.frameon": False,

        "figure.dpi": 300,
        "savefig.dpi": 600,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.02,
    })

# Logging software version
def get_version(module, name):
    """
    Retrieve a module version string safely.

    Parameters
    ----------
    module : object
        Imported module object (for example, `numpy` or `pandas`).
    name : str
        Human-readable module name kept for compatibility with existing calls.
        This argument is currently unused by the function.

    Returns
    -------
    str
        Module version if `module.__version__` exists, `"unknown"` if the
        attribute is missing, or `"not available"` if lookup fails.
    """
    try:
        return getattr(module, "__version__", "unknown")
    except Exception:
        return "not available"

def fmt_p(p):
    """
    Format a p-value for compact reporting.

    Parameters
    ----------
    p : float
        Numeric p-value.

    Returns
    -------
    str
        Scientific notation with 3 decimals for `p < 0.001` (for example,
        `"2.341e-05"`); fixed-point with 3 decimals otherwise (for example,
        `"0.014"`).
    """
    return f"{p:.3e}" if p < 0.001 else f"{p:.3f}"

def summarize_logit(result, alpha=0.05, exponentiate=True):
    """
    Summarize statsmodels Logit/GLM(Binomial) results.

    Parameters
    ----------
    result : statsmodels result object
        Fitted model result with `.params`, `.conf_int()`, and `.pvalues`
        attributes (for example, `LogitResults` or binomial `GLMResults`).
    alpha : float, default=0.05
        Significance level used to compute confidence intervals.
    exponentiate : bool, default=True
        If True, report odds-ratio scale by exponentiating coefficients and
        confidence bounds.

    Returns
    -------
    pandas.DataFrame
        Summary table indexed by model terms.

        - If `exponentiate=True`: columns are
          `coef`, `OR`, `OR_ci_lower`, `OR_ci_upper`, `pvalue`, `p_fmt`.
        - If `exponentiate=False`: columns are
          `coef`, `ci_lower`, `ci_upper`, `pvalue`, `p_fmt`.
    """
    params = result.params
    conf = result.conf_int(alpha=alpha)   # columns: [lower, upper]
    pvals = result.pvalues

    df = pd.DataFrame({
        "coef": params,
        "ci_lower": conf.iloc[:, 0],
        "ci_upper": conf.iloc[:, 1],
        "pvalue": pvals
    })

    if exponentiate:
        df["OR"] = np.exp(df["coef"])
        df["OR_ci_lower"] = np.exp(df["ci_lower"])
        df["OR_ci_upper"] = np.exp(df["ci_upper"])

    # add formatted p-value column
    df["p_fmt"] = df["pvalue"].apply(fmt_p)

    # nicer column order
    if exponentiate:
        df = df[[
            "coef",
            "OR",
            "OR_ci_lower",
            "OR_ci_upper",
            "pvalue",
            "p_fmt"
        ]]
    else:
        df = df[["coef", "ci_lower", "ci_upper", "pvalue", "p_fmt"]]

    return df

def plot_odds(
    data=None,
    xlabel="Protein",
    ylabel="Odds of age-associated\nstructural changes",
    figsize=(3.50, 2.80),
    xlim=None,
    ylim=None,
    xtick_labels=None,
    positions=None,
    yticks=None,
    
):
    """
    Plot point estimates with confidence-interval error bars for odds.

    Parameters
    ----------
    data : dict, optional
        Mapping from group label to a 3-element sequence:
        `[estimate, ci_lower, ci_upper]`.
        Example:
        `{"Entangled": [0.43, 0.31, 0.57], "Non-entangled": [0.25, 0.18, 0.34]}`.
        If None, uses zero placeholders for two default groups.
    xlabel : str, default="Protein"
        X-axis label.
    ylabel : str, default="Odds of age-associated\\nstructural changes"
        Y-axis label.
    figsize : tuple, default=(3.50, 2.80)
        Figure size in inches.
    xlim : tuple or None, default=None
        Explicit x-axis limits. Uses `(0, 2.5)` when not provided.
    ylim : tuple or None, default=None
        Explicit y-axis limits. Uses `(0.1, 0.62)` when not provided.
    xtick_labels : list-like or None, default=None
        Labels to display at `positions`. If None, uses keys from `data`.
    positions : list-like or None, default=None
        Numeric x positions for points. If None, uses `[0.7, 1.7]`.
    yticks : list-like or None, default=None
        Custom y ticks. If None, uses `np.arange(0.2, 0.7, 0.2)`.

    Returns
    -------
    tuple
        `(fig, ax)` Matplotlib figure and axes objects.
    """
    if data is None:
        data = {
            "Entangled": [0, 0, 0],
            "Non-entangled": [0, 0, 0]
        }

    states = list(data.keys())
    means = np.array([v[0] for v in data.values()])
    lower = np.array([v[1] for v in data.values()])
    upper = np.array([v[2] for v in data.values()])
    yerr = np.vstack([means - lower, upper - means])

    fig, ax = plt.subplots(figsize=figsize)
    if positions is None:
        positions = [0.7, 1.7]
    ax.errorbar(
        positions, means,
        yerr=yerr,
        fmt="o",
        color="black", ecolor="black",
        elinewidth=1.0,
        capsize=2.5, capthick=1.0,
        markersize=4,
        markeredgewidth=0.8,
        markeredgecolor="black",
        markerfacecolor="black",
    )

    ax.set_xticks(positions)
    if xtick_labels is None:
        ax.set_xticklabels(states, rotation=0, ha="center")
    else:
        ax.set_xticklabels(xtick_labels, rotation=0, ha="center")
    ax.set_xlabel(xlabel, labelpad=2)
    ax.set_ylabel(ylabel, labelpad=3)

    # Apply defaults ONLY if user didn't pass values
    if yticks is not None:
        ax.set_yticks(yticks)
    else:
        ax.set_yticks(np.arange(0.2, 0.7, 0.2))

    if xlim is not None:
        ax.set_xlim(xlim)
    else:
        ax.set_xlim(0, 2.5)

    if ylim is not None:
        ax.set_ylim(ylim)
    else:
        ax.set_ylim(0.1, 0.62)

    ax.tick_params(top=False, right=False)

    return fig, ax

def plot_volcano_lip(df, p_thresh=0.01, xlim=(-13, 13.5), ylim=(0, 7.5), figsize=(3.50, 2.80)):
    """
    Create a volcano-style scatter plot for LiP-MS differential signal.

    Parameters
    ----------
    df : pandas.DataFrame
        Input table containing at least:
        - `log2FC`: log2 fold-change (x-axis)
        - `Pvalue`: p-value (converted to `-log10(Pvalue)` on y-axis)
        - `SC`: class flag (`1` for ASC, non-`1` for NASC)
    p_thresh : float, default=0.01
        P-value threshold used to draw the horizontal significance line.
    xlim : tuple, default=(-13, 13.5)
        X-axis range.
    ylim : tuple, default=(0, 7.5)
        Y-axis range.
    figsize : tuple, default=(3.50, 2.80)
        Figure size in inches.

    Returns
    -------
    tuple
        `(fig, ax)` Matplotlib figure and axes objects.
    """
    # df must have columns: log2FC, Pvalue, SC (1 for ASC, else NASC)
    d = df.copy()
    d["-log10_Pvalue"] = -np.log10(d["Pvalue"].astype(float))

    df_asc = d[d["SC"] == 1]
    df_nasc = d[d["SC"] != 1]

    fig, ax = plt.subplots(figsize=figsize)  # single-column panel

    # Points: small, high density friendly
    ax.scatter(df_nasc["log2FC"], df_nasc["-log10_Pvalue"],
               s=6, c="black", alpha=0.65, linewidths=0, label="NASC", rasterized=True)
    ax.scatter(df_asc["log2FC"], df_asc["-log10_Pvalue"],
               s=6, c="blue", alpha=0.65, linewidths=0, label="ASC", rasterized=True)

    # Threshold lines: thin, dashed
    ax.axvline(0, linestyle="--", linewidth=0.8, color="red")
    ax.axhline(-np.log10(p_thresh), linestyle="--", linewidth=0.8, color="red")

    ax.set_xlabel(r"$\log_2(\mathrm{Normalized\ FC})$")
    ax.set_ylabel(r"$-\log_{10}(P)$")

    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)

    # plt.show()
    return fig, ax
    
# plot contingency table
def draw_contingency_table(
    counts=((0, 0),
            (0, 0)),
    row_labels=("Yes", "No"),
    col_labels=("Yes", "No"),
    title_top="Age-associated structural change",
    title_left="Entangled protein",
    figsize=(3.50, 2.80),  # match panel b height
):
    """
    Draw a 2x2 contingency table as a formatted Matplotlib panel.

    Parameters
    ----------
    counts : tuple of tuple, default=((0, 0), (0, 0))
        2x2 count matrix in row-major form:
        `((YY, YN), (NY, NN))`.
    row_labels : tuple of str, default=("Yes", "No")
        Labels shown on table rows.
    col_labels : tuple of str, default=("Yes", "No")
        Labels shown on table columns.
    title_top : str, default="Age-associated structural change"
        Column-axis title displayed above the table.
    title_left : str, default="Entangled protein"
        Row-axis title displayed to the left of the table.
    figsize : tuple, default=(3.50, 2.80)
        Figure size in inches.

    Returns
    -------
    tuple
        `(fig, ax)` Matplotlib figure and axes objects.

    Notes
    -----
    The function calls `plt.show()` before returning.
    """
    # Counts is contingency table: 
    # YY YN
    # NY NN
    fig, ax = plt.subplots(figsize=figsize)
    ax.axis("off")

    # Keep geometry stable across panels
    bbox = [0.30, 0.34, 0.58, 0.38]

    table = ax.table(
        cellText=[[f"{x:,}" for x in row] for row in counts],
        cellLoc="center",
        loc="center",
        bbox=bbox,
    )
    table.auto_set_font_size(False)
    table.set_fontsize(BASE_FONTSIZE)

    # Match stroke weight to axes linewidth scale (not too heavy)
    for cell in table.get_celld().values():
        cell.set_edgecolor("black")
        cell.set_linewidth(0.8)
        cell.set_facecolor("white")
        cell.PAD = 0.16

    # Column labels (tight to table)
    for i, label in enumerate(col_labels):
        x = bbox[0] + (i + 0.5) * bbox[2] / 2
        y = bbox[1] + bbox[3] + 0.03
        ax.text(x, y, label, ha="center", va="bottom", fontsize=BASE_FONTSIZE)

    # Column title
    ax.text(
        bbox[0] + bbox[2] / 2,
        bbox[1] + bbox[3] + 0.12,
        title_top,
        ha="center",
        va="bottom",
        fontsize=BASE_FONTSIZE,
    )

    # Row labels (closer to table)
    for i, label in enumerate(row_labels):
        y = bbox[1] + bbox[3] - (i + 0.5) * bbox[3] / 2
        x = bbox[0] - 0.03
        ax.text(x, y, label, ha="right", va="center", fontsize=BASE_FONTSIZE)

    # Left title (push further left to increase spacing from Yes/No)
    ax.text(
        bbox[0] - 0.14,
        bbox[1] + bbox[3] / 2,
        title_left,
        ha="center",
        va="center",
        rotation=90,
        fontsize=BASE_FONTSIZE,
    )


    plt.show()
    return fig, ax


# File checksum
def file_checksum(filepath, algorithm="sha256", block_size=65536):
    """
    Compute a cryptographic checksum for a file.

    Parameters
    ----------
    filepath : str or pathlib.Path
        Path to the target file.
    algorithm : str, default="sha256"
        Hash algorithm name accepted by `hashlib.new()` (for example,
        `"sha256"`, `"md5"`, `"sha1"`).
    block_size : int, default=65536
        Number of bytes read per chunk while hashing.

    Returns
    -------
    str
        Hex digest string of the computed checksum.
    """
    filepath = Path(filepath)
    
    h = hashlib.new(algorithm)
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(block_size), b""):
            h.update(chunk)
    
    return h.hexdigest()
    
def file_info(filepath):
    """
    Return lightweight metadata and checksum for a file.

    Parameters
    ----------
    filepath : str or pathlib.Path
        Path to the target file.

    Returns
    -------
    dict
        If file does not exist:
        `{"path": <path>, "exists": False}`.

        If file exists:
        `{"path": <path>, "size_bytes": <int>, "sha256": <str>}`.
    """
    p = Path(filepath)
    
    if not p.exists():
        return {"path": str(p), "exists": False}
    
    return {
        "path": filepath,
        "size_bytes": p.stat().st_size,
        "sha256": file_checksum(p)
    }
