import json
from pathlib import Path

import pandas as pd
from fastapi.encoders import jsonable_encoder

from .c_py import di
from .dictionary import DictDefault
from .io.aio import load_from_file_str_async, save_to_file_async
from .io.io import save_to_file
from .utils import _path_suffix_check


class Records(list[dict]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # from
    def from_json(self, path: str | Path):
        with open(path, encoding="utf-8") as file:
            super().extend(json.load(file))
        return self

    async def from_json_async(self, path: str | Path):
        # TODO: Implement async version of from_json
        ret: str = await load_from_file_str_async(path)
        self.from_string(ret)
        return self

    def from_string(self, string: str):
        super().extend(json.loads(string))
        return self

    def from_dataframe(self, df: pd.DataFrame):
        super().extend(df.to_dict(orient="records"))
        return self

    def from_csv(self, path: str | Path):
        # TODO: Implement
        return self

    def from_sqlalchemy_row(self, rows: list):
        records = []
        for row in rows:
            print("Row type:", type(row))
            records.append(row._asdict())

        super().extend(records)
        return self

    def from_sqlalchemy_model(self, models: list):
        models_dict = jsonable_encoder(models)
        super().extend(models_dict)
        return self

    def from_sqlalchemy(self, rows: list):
        if hasattr(rows[0], "_asdict"):
            return self.from_sqlalchemy_row(rows)
        else:
            return self.from_sqlalchemy_model(rows)

    # to
    def to_list(self) -> list:
        return list(self)

    def to_json(
        self,
        path: str | Path | None = None,
        indent: int | None = None,
    ) -> str:
        ret = json.dumps(
            list(self),
            default=str,
            ensure_ascii=False,
            indent=indent,
        )
        if path is not None:
            path = _path_suffix_check(path, suffix=".json")
            save_to_file(ret, path)
        return ret

    async def to_json_async(
        self,
        path: str | Path | None = None,
        indent: int | None = None,
    ) -> str:
        ret = json.dumps(
            list(self),
            default=str,
            ensure_ascii=False,
            indent=indent,
        )
        if path is not None:
            path = _path_suffix_check(path, suffix=".json")
            await save_to_file_async(ret, path)
        return ret

    def to_dict(self, keys: list) -> dict:
        return self.to_dict_default(keys).to_dict()

    def to_defaultdict(self, keys: list) -> dict:
        return self.to_dict_default(keys).to_defaultdict()

    def to_dict_default(self, keys: list) -> DictDefault:
        ret: DictDefault = DictDefault()
        for record in self:
            p = id(ret)
            key_values = [record[key] for key in keys]
            key_values_len = len(key_values)
            for i in range(key_values_len):
                if i < key_values_len - 1:
                    if key_values[i] not in di(p):
                        di(p)[key_values[i]] = {}
                    p = id(di(p)[key_values[i]])
                else:
                    if key_values[i] in di(p):
                        raise ValueError("Keys should be unique in the dataset.")
                    di(p)[key_values[i]] = record

        return ret

    def to_dataframe(
        self,
        index: list | None = None,
        columns: list | None = None,
    ) -> pd.DataFrame:
        df = pd.DataFrame(self)
        if index is not None and len(index) > 0:
            df.set_index(index, inplace=True)
        if columns is not None and len(columns) > 0:
            df = df[columns]
        return df
