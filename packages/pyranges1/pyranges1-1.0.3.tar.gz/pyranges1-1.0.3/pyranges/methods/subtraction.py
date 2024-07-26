from typing import TYPE_CHECKING

import pandas as pd
from ncls import NCLS  # type: ignore[import]

from pyranges.core.names import TEMP_NUM_COL

if TYPE_CHECKING:
    from pyranges import RangeFrame


def _subtraction(df: "RangeFrame", df2: "RangeFrame", **_) -> pd.DataFrame:
    if df2.empty or df.empty:
        return df

    o = NCLS(df2.Start.to_numpy(), df2.End.to_numpy(), df2.index.to_numpy())

    idx_self, new_starts, new_ends = o.set_difference_helper(
        df.Start.values,
        df.End.values,
        df.index.values,
        df[TEMP_NUM_COL].to_numpy(),
    )

    missing_idx = pd.Index(df.index).difference(idx_self)

    idx_to_drop = new_starts != -1

    new_starts = new_starts[idx_to_drop]
    new_ends = new_ends[idx_to_drop]

    idx_self = idx_self[idx_to_drop]
    new_starts = pd.Series(new_starts, index=idx_self)
    new_ends = pd.Series(new_ends, index=idx_self)

    _df = df.reindex(missing_idx.union(idx_self)).sort_index()
    new_starts = new_starts.sort_index()
    new_ends = new_ends.sort_index()

    if len(idx_self):
        _df.loc[_df.index.isin(idx_self), "Start"] = new_starts.to_numpy()
        _df.loc[_df.index.isin(idx_self), "End"] = new_ends.to_numpy()

    return _df
