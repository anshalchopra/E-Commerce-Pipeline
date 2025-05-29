from dataset_download import KaggleDataset

if __name__ == "__main__":
    credentials = "./Credentials/Kaggle Settings.json"
    dataset = "retailrocket/ecommerce-dataset"

    kag = KaggleDataset(credentials)
    kag.login()
    kag.download(dataset)