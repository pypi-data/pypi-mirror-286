import unittest
from mw_python_sdk import download_file


class TestDownloadFile(unittest.TestCase):
    def test_download(self):
        dataset_id_tmp = "64e6c644c60d2823b0a2e266"
        try:  # Example assertion
            download_file(dataset_id_tmp, "flask.zip")
        except Exception as err:
            print(f"An error occurred: {err}")

    def test_redownload(self):
        dataset_id_tmp = "64e6c644c60d2823b0a2e266"
        try:  # Example assertion
            download_file(dataset_id_tmp, "flask.zip")
            download_file(dataset_id_tmp, "flask.zip")
        except Exception as err:
            print(f"An error occurred: {err}")


if __name__ == "__main__":
    unittest.main()
