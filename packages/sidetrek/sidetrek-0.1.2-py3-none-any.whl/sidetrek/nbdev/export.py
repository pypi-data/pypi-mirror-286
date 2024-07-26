import os
from pathlib import Path
from nbdev.processors import NBProcessor  # type: ignore
from nbdev.export import scrub_magics  # type: ignore
from sidetrek.nbdev.directives import DbtMaker, ExportDBTProc
from fastcore.foundation import L  # type: ignore


def nb_export_dbt(nb_path, procs=None, debug=False, dbt_maker=DbtMaker, name=None):
    """
    Create dbt files from notebook. Defaults to removing all magics from the cell.

    Example usage:
    nb_export_dbt('path/to/notebook')
    """
    nb_dirname = os.path.dirname(nb_path)
    exp = ExportDBTProc()
    nb = NBProcessor(nb_path, [exp] + L(procs) + L([scrub_magics]), debug=debug)
    nb.process()
    for filepath, cell in exp.file_content.items():
        dest_filepath = str(Path(nb_dirname) / filepath)
        dm = dbt_maker(dest=dest_filepath, nb_path=nb_path)
        dm.make(cell)
