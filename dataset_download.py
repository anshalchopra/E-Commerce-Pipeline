import kagglehub
import json
import os
from pathlib import Path


class KaggleDataset:
    def __init__(self, credentials_path: str):
        self.credentials_path = Path(credentials_path)
        self.credentials = self._load_credentials()

    def _load_credentials(self) -> dict:
        if not self.credentials_path.exists():
            raise FileNotFoundError(f"[ERROR] Credentials file not found at: {self.credentials_path}")

        try:
            with open(self.credentials_path, 'r') as f:
                creds = json.load(f)
                if "username" not in creds or "key" not in creds:
                    raise KeyError("Missing 'username' or 'key' in credentials file.")
                return creds
        except json.JSONDecodeError:
            raise ValueError(f"[ERROR] Invalid JSON in credentials file: {self.credentials_path}")
        except Exception as e:
            raise RuntimeError(f"[ERROR] Failed to load credentials: {e}")

    def login(self):
        os.environ["KAGGLE_USERNAME"] = self.credentials["username"]
        os.environ["KAGGLE_KEY"] = self.credentials["key"]
        print(f"[INFO] Logged in as {self.credentials['username']}")

    def download(self, dataset_id: str, target_path: str = "./Datasets"):
        target_dir = Path(target_path)
        target_dir.mkdir(parents=True, exist_ok=True)

        try:
            path = kagglehub.dataset_download(dataset_id)
            print(f"[INFO] Dataset downloaded to: {path}")
            command = f'cp -r "{path}" "{target_path}"'
            result = os.system(command)
            if result == 0:
                print(f"[INFO] Successfully copied from {path} to {target_path}")
            else:
                print(f"[ERROR] Copy failed with exit code: {result}")
        except Exception as e:
            raise RuntimeError(f"[ERROR] Failed to download Datasets: {e}")