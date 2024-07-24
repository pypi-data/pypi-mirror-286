import unittest
from mw_python_sdk import download_dir


class TestDownloadFile(unittest.TestCase):
    def test_download(self):
        dataset_id_tmp = "64e6c644c60d2823b0a2e266"
        try:
            download_dir(dataset_id_tmp)
        except Exception as err:
            print(f"An error occurred: {err}")

    def test_redownload(self):
        dataset_id_tmp = "64e6c644c60d2823b0a2e266"
        try:
            print(download_dir(dataset_id_tmp))
            print(download_dir(dataset_id_tmp))
        except Exception as err:
            print(f"An error occurred: {err}")


if __name__ == "__main__":
    unittest.main()
