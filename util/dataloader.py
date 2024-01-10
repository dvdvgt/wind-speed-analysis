import os
from bs4 import BeautifulSoup
import requests as rq
import zipfile
import pickle

class Loader:
    ZIP_NAME = "data.zip"
    DATA_BASE_URL = "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes"
    # KINDS = ["wind", "air_temperature", "precipitation", "solar"]

    def __init__(self, metrics: list, data_folder: str, station_id: str = "02115"):
        """
        metrics is a list of "wind", "air_temperature", "precipitation" and/or "solar"
        """
        self.station_id = station_id
        self.metrics = metrics
        self.data_folder = data_folder
        self.loaded = False
        self.contents_path = os.path.join(data_folder, "contents.pickle")
        self.metric_urls = { metric: f"{self.DATA_BASE_URL}/{metric}/historical/" for metric in metrics }

    def query_metric(self, metric) -> tuple: 
        def seach_refs(soup, keyword) -> list:
            return [a.get("href") for a in soup.find_all("a", href=True) if a.get("href").__contains__(keyword)]

        url = self.metric_urls[metric]
        desc_url = f"{self.DATA_BASE_URL}/{metric}/"

        desc_soup = BeautifulSoup(rq.get(desc_url).text, "html.parser")
        descs = seach_refs(desc_soup, "pdf")
        desc_resps = [rq.get(desc_url + d) for d in descs]
        descs_d = { desc: desc_resp for desc, desc_resp in zip(descs, desc_resps) }

        data_soup = BeautifulSoup(rq.get(url).text, "html.parser")
        csvs = seach_refs(data_soup, self.station_id)
        csv_resps = [rq.get(url + link) for link in csvs]
        csvs_d = { csv: csv_resp for csv, csv_resp in zip(csvs, csv_resps) }

        return descs_d, csvs_d
    
    def download_metric(self, metric):
        descs, csvs = self.query_metric(metric)
        save_path = os.path.join(self.data_folder, metric)
        os.makedirs(save_path, exist_ok=True)

        # save dataset description pdfs
        desc_file_paths = []
        for descr, resp in descs.items():
            desc_file_path = os.path.join(save_path, descr)
            with open(desc_file_path, "wb") as file:
                file.write(resp.content)
            desc_file_paths.append(desc_file_path)

        # save dataset csvs
        csv_file_paths = []
        for csv, csv_resp in csvs.items():
            zip_path = os.path.join(self.data_folder, metric, csv)

            # write zip to disk
            with open(zip_path, "wb") as z:
                z.write(csv_resp.content)

            # extract zip contents
            with zipfile.ZipFile(zip_path) as zip_file:
                for filename in zip_file.namelist():
                    csv_file_paths.append(os.path.abspath(os.path.join(save_path, filename)))
                zip_file.extractall(save_path)

            os.remove(zip_path)

        return desc_file_paths, csv_file_paths


    def download_all_metrics(self): 
        metric_files = { metric : [] for metric in self.metrics }

        # download data only the first time
        if not self.loaded:
            os.makedirs(self.data_folder, exist_ok=True)

            for metric in self.metrics:
                m_desc_path, m_csv_path = self.download_metric(metric)
                metric_files[metric] =  m_csv_path

            with open(os.path.join(self.contents_path), "wb") as fh:
                pickle.dump(metric_files, fh, protocol=pickle.HIGHEST_PROTOCOL)

            self.loaded = True
        # only load the dictionary containing abs. file paths for the csv files for each metric
        else:
            with open(self.contents_path) as fh:
                metric_files = pickle.load(fh)

        return metric_files
