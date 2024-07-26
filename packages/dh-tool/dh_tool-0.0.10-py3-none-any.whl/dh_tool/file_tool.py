import os
import json
import numpy as np
import pickle
import pandas as pd


def exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"An error occurred in {func.__name__}: {str(e)}")
            return None

    return wrapper


class FileHandler:
    def __init__(self):
        self.load_handlers = {
            "txt": self._load_txt,
            "json": self._load_json,
            "csv": self._load_csv,
            "xlsx": self._load_excel,
            "parquet": self._load_parquet,
            "pkl": self._load_pickle,
            "npz": self._load_npz,
            "npy": self._load_npy,
        }
        self.save_handlers = {
            "txt": self._save_txt,
            "json": self._save_json,
            "csv": self._save_csv,
            "xlsx": self._save_excel,
            "parquet": self._save_parquet,
            "pkl": self._save_pickle,
            "npz": self._save_npz,
            "npy": self._save_npy,
        }

    def load(self, path: str, fn=False):
        try:
            file_name, file_type = os.path.basename(path).split(".")
            file_type = file_type.lower()

            if file_type in self.load_handlers:
                if not fn:
                    return self.load_handlers[file_type](path)
                else:
                    return self.load_handlers[file_type](path), file_name
            else:
                raise ValueError(f"Unsupported file type: {file_type}")

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    @exception_handler
    def save(self, data, path: str):
        try:
            _, file_type = os.path.basename(path).split(".")
            file_type = file_type.lower()

            if file_type in self.save_handlers:
                self.save_handlers[file_type](data, path)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    @exception_handler
    def _load_txt(self, path):
        with open(path, "r", encoding="utf-8") as file:
            return file.read()

    @exception_handler
    def _load_json(self, path):
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    @exception_handler
    def _load_csv(self, path):
        return pd.read_csv(path, encoding="utf-8")

    @exception_handler
    def _load_excel(self, path):
        return pd.read_excel(path)

    @exception_handler
    def _load_parquet(self, path):
        return pd.read_parquet(path)

    @exception_handler
    def _load_pickle(self, path):
        with open(path, "rb") as file:
            return pickle.load(file)

    @exception_handler
    def _load_npz(self, path):
        return np.load(path)

    @exception_handler
    def _load_npy(self, path):
        return np.load(path)

    @exception_handler
    def _save_txt(self, data, path):
        with open(path, "w", encoding="utf-8") as file:
            file.write(data)

    @exception_handler
    def _save_json(self, data, path):
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file)

    @exception_handler
    def _save_csv(self, data, path):
        data.to_csv(path, index=False, encoding="utf-8")

    @exception_handler
    def _save_excel(self, data, path):
        data.to_excel(path, index=False)

    @exception_handler
    def _save_parquet(self, data, path):
        data.to_parquet(path)

    @exception_handler
    def _save_pickle(self, data, path):
        with open(path, "wb") as file:
            pickle.dump(data, file)

    @exception_handler
    def _save_npz(self, data, path):
        np.savez(path, data)

    @exception_handler
    def _save_npy(self, data, path):
        np.save(path, data)
