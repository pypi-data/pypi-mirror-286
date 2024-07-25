from io import BytesIO
import re
from typing import List, Tuple
from openpyxl import Workbook, load_workbook
import requests
from pandas import DataFrame, read_excel, read_csv


class SharePointUtils:
    def __init__(self, client_id: str, client_secret: str, site_id: str, tenant: str):
        """
        Class to aggregate methods for interacting with SharePoint files

        Parameters
        ----------
        * client_id (str): ID of service credentials
        * client_secret (str): secret string of service credentials
        * site_id (str): id of SharePoint site you wish to access
        * tenant (str)
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_base_url = f"https://graph.microsoft.com/beta/sites/{site_id}/"
        self.tenant = tenant.lower()
        self._set_token()

    def _set_token(self):
        get_token_url = f"https://login.microsoftonline.com/{self.tenant}.onmicrosoft.com/oauth2/v2.0/token"
        payload_to_get_token = {
            "Grant_Type": "client_credentials",
            "Scope": "https://graph.microsoft.com/.default",
            "client_id": self.client_id,
            "Client_Secret": self.client_secret,
        }
        token_response = requests.post(get_token_url, data=payload_to_get_token).json()
        self.graph_auth_header = {
            "Authorization": f"{token_response['token_type']} {token_response['access_token']}"
        }

    def _get_id_from_name(self, parent_element_json, name, site=False):
        """Returns id for matching object with given name/displayName in SharePoint API response object"""
        if site:
            var = "displayName"
        else:  # drives, files
            var = "name"
        match = [x["id"] for x in parent_element_json["value"] if x[var] == name]
        assert len(match) == 1
        return match[0].split(",")[-1]

    def _get_subsite_id(self, subsite_name):
        parent_element_json = requests.get(
            self.api_base_url + "sites", headers=self.graph_auth_header
        ).json()
        return self._get_id_from_name(parent_element_json, subsite_name, site=True)

    def _get_drive_id(self, drive, subsite_id=None):
        request_url = (
            self.api_base_url + "drives"
            if subsite_id is None
            else self.api_base_url + f"sites/{subsite_id}/drives"
        )
        parent_element_json = requests.get(
            request_url, headers=self.graph_auth_header
        ).json()
        return self._get_id_from_name(parent_element_json, drive)

    def _get_item_id(self, item_path, drive_id, subsite_id=None):
        request_url = (
            self.api_base_url + f"drives/{drive_id}/root:/{item_path}"
            if subsite_id is None
            else self.api_base_url
            + f"sites/{subsite_id}/drives/{drive_id}/root:/{item_path}"
        )
        response = requests.get(
            request_url,
            headers=self.graph_auth_header,
        )
        assert (
            response.ok
        ), f"Requested item returned status code {response.status_code}"
        return response.json()["id"]

    def request_item(self, drive: str, item_path: str, subsite=None) -> BytesIO:
        """
        Get a SharePoint file

        Parameters
        ----------
        * drive (str): name of drive
        * file_path (str): path to the file
        * subsite (str, optional): name of subsite where file is located, defaults to None

        Returns
        -------
        * BytesIO object with file content
        """
        subsite_id = None if subsite is None else self._get_subsite_id(subsite)
        drive_id = self._get_drive_id(drive, subsite_id=subsite_id)
        request_url = (
            self.api_base_url + f"drives/{drive_id}/root:/{item_path}"
            if subsite is None
            else self.api_base_url
            + f"sites/{subsite_id}/drives/{drive_id}/root:/{item_path}"
        )
        response = requests.get(
            request_url,
            headers=self.graph_auth_header,
        )
        assert (
            response.ok
        ), f"Requested item returned status code {response.status_code}"
        download_url = response.json()["@microsoft.graph.downloadUrl"]
        download_response = requests.get(download_url)
        assert (
            download_response.ok
        ), f"Item download returned status code {download_response.status_code}"
        return BytesIO(download_response.content)

    def write_item(
        self,
        drive: str,
        data,
        content_type: str,
        item_name: str,
        folder_path=None,
        subsite=None,
    ):
        """
        List file names in Sharepoint location

        Parameters
        ----------
        * drive (str): name of drive
        * data (Dictionary, list of tuples, bytes, or file-like object): data content of file
        * content_type (str): file content type (e.g. "text/csv")
        * item_name (str): name of file to write to SharePoint
        * folder_path (str, optional): path/to/sharepoint/folder/in/drive, defaults to None
        * subsite (str, optional): name of subsite where folder is located, defaults to None

        Returns
        -------
        * None
        """
        subsite_id = None if subsite is None else self._get_subsite_id(subsite)
        drive_id = self._get_drive_id(drive, subsite_id=subsite_id)
        request_url = (
            self.api_base_url
            + f"drives/{drive_id}/root:/{folder_path}/{item_name}:/content"
            if subsite is None
            else self.api_base_url
            + f"sites/{subsite_id}/drives/{drive_id}/root:/{folder_path}/{item_name}:/content"
        )
        headers = {**self.graph_auth_header, "Content-Type": content_type}
        response = requests.put(
            request_url,
            headers=headers,
            data=data,
        )
        assert (
            response.ok
        ), f"Attempting to write item returned status code {response.status_code}"

    def get_items_in_path(
        self, drive: str, folder_path=None, subsite=None
    ) -> List[str]:
        """
        List file names in Sharepoint location

        Parameters
        ----------
        * drive (str): name of drive
        * folder_path (str, optional): path/to/sharepoint/folder/in/drive, defaults to None
        * subsite (str, optional): name of subsite where folder is located, defaults to None

        Returns
        -------
        * List of file names as strings
        """
        subsite_id = None if subsite is None else self._get_subsite_id(subsite)
        drive_id = self._get_drive_id(drive, subsite_id=subsite_id)
        if folder_path is None:
            request_url = (
                self.api_base_url + f"drives/{drive_id}/root/children"
                if subsite is None
                else self.api_base_url
                + f"sites/{subsite_id}/drives/{drive_id}/root/children"
            )
        else:
            request_url = (
                self.api_base_url + f"drives/{drive_id}/root:/{folder_path}:/children"
                if subsite is None
                else self.api_base_url
                + f"sites/{subsite_id}/drives/{drive_id}/root:/{folder_path}:/children"
            )
        response = requests.get(
            request_url,
            headers=self.graph_auth_header,
        )
        assert (
            response.ok
        ), f"Request returned status code {response.status_code} for given path"
        return [item["name"] for item in response.json()["value"]]

    def create_folder(
        self,
        drive: str,
        path_parent_folder: str,
        name_new_folder: str,
        subsite=None,
        allow_overwrite: bool = True,
    ):
        """
        Create a new folder on Sharepoint

        Parameters
        ----------
        * drive (str): name of drive
        * path_parent_folder (str): path/to/sharepoint/folder/in/drive
        * name_new_folder (str): name for the new folder being created
        * subsite (str, optional): name of subsite where folder is located, defaults to None
        * allow_overwrite (bool, optional): whether to overwrite an existing folder
            with the creation of a new one, defaults to True

        Returns
        -------
        * None
        """
        subsite_id = None if subsite is None else self._get_subsite_id(subsite)
        drive_id = self._get_drive_id(drive, subsite_id=subsite_id)
        parent_item_id = self._get_item_id(path_parent_folder, drive_id, subsite_id)
        request_url = (
            self.api_base_url + f"drives/{drive_id}/items/{parent_item_id}/children"
            if subsite is None
            else self.api_base_url
            + f"sites/{subsite_id}/drive/items/{parent_item_id}/children"
        )
        headers = {**self.graph_auth_header, "Content-Type": "application/json"}
        drive_item = {
            "name": name_new_folder,
            "folder": {},
            "@microsoft.graph.conflictBehavior": (
                "replace" if allow_overwrite else "fail"
            ),
        }
        response = requests.post(request_url, headers=headers, json=drive_item)
        if allow_overwrite:
            assert (
                response.ok
            ), f"Attempting to move item returned status code {response.status_code}; item not moved"
        else:
            assert response.ok or (
                response.json()["error"]["code"] == "nameAlreadyExists"
            ), f"Attempting to move item returned status code {response.status_code}; no nameAlreadyExists error"

    def move_item(
        self,
        drive: str,
        item_name: str,
        origin_parent_dir=None,
        target_parent_dir=None,
        subsite=None,
        allow_overwrite: bool = True,
    ):
        """
        Move a Sharepoint item from one location to another

        Parameters
        ----------
        * drive (str): name of drive
        * item_name (str): name of the item to be moved
        * origin_parent_dir (str, optional): current path to item, defaults to None
        * target_parent_dir (str, optional): proposed new path to item, defaults to None
        * subsite (str, optional): name of subsite where item is located, defaults to None
        * allow_overwrite (bool, optional): whether to overwrite an existing item when moving, defaults to True

        Returns
        -------
        * None
        """
        subsite_id = None if subsite is None else self._get_subsite_id(subsite)
        drive_id = self._get_drive_id(drive, subsite_id=subsite_id)
        item_path = (
            item_name
            if origin_parent_dir is None
            else f"{origin_parent_dir}/{item_name}"
        )
        request_url = (
            self.api_base_url + f"drives/{drive_id}/root:/{item_path}"
            if subsite is None
            else self.api_base_url
            + f"sites/{subsite_id}/drives/{drive_id}/root:/{item_path}"
        )
        target_folder_id = self._get_item_id(
            target_parent_dir, drive_id, subsite_id=subsite_id
        )
        data = {
            "parentReference": {"id": target_folder_id},
            "name": item_name,
        }
        params = {
            "@microsoft.graph.conflictBehavior": (
                "replace" if allow_overwrite else "fail"
            ),
        }
        response = requests.patch(
            request_url, headers=self.graph_auth_header, json=data, params=params
        )
        if allow_overwrite:
            assert (
                response.ok
            ), f"Attempting to move item returned status code {response.status_code}; item not moved"
        else:
            assert response.ok or (
                response.json()["error"]["code"] == "nameAlreadyExists"
            ), f"Attempting to move item returned status code {response.status_code}; no nameAlreadyExists error"

    def copy_item(
        self,
        drive: str,
        origin_item_name: str,
        target_parent_dir: str,
        origin_parent_dir=None,
        target_item_name=None,
        subsite=None,
        allow_overwrite: bool = True,
    ):
        """
        Copy a Sharepoint item from one location to another

        Parameters
        ----------
        * drive (str): name of drive
        * origin_item_name (str): name of the item to be copied
        * target_parent_dir (str): proposed new path to item
        * origin_parent_dir (str, optional): current path to item, defaults to None
        * target_item_name (str, optional): name for the new copy, defaults to None
        * subsite (str, optional): name of subsite where item is located, defaults to None
        * allow_overwrite (bool, optional): whether to overwrite an existing item when copying, defaults to True

        Returns
        -------
        * None
        """
        subsite_id = None if subsite is None else self._get_subsite_id(subsite)
        drive_id = self._get_drive_id(drive, subsite_id=subsite_id)

        origin_item_path = (
            origin_item_name
            if origin_parent_dir is None
            else f"{origin_parent_dir}/{origin_item_name}"
        )
        origin_item_id = self._get_item_id(origin_item_path, drive_id, subsite_id)
        target_dir_id = self._get_item_id(target_parent_dir, drive_id, subsite_id)

        request_url = (
            self.api_base_url + f"drives/{drive_id}/items/{origin_item_id}/copy"
            if subsite is None
            else self.api_base_url
            + f"sites/{subsite_id}/drive/items/{origin_item_id}/copy"
        )
        drive_item = {
            "parentReference": {"driveId": drive_id, "id": target_dir_id},
            "name": (
                f"{origin_item_name}"
                if target_item_name is None
                else f"{target_item_name}"
            ),
        }
        params = {
            "@microsoft.graph.conflictBehavior": (
                "replace" if allow_overwrite else "fail"
            ),
        }
        response = requests.post(
            request_url, headers=self.graph_auth_header, json=drive_item, params=params
        )
        if allow_overwrite:
            assert (
                response.ok
            ), f"Attempting to move item returned status code {response.status_code}; item not moved"
        else:
            assert response.ok or (
                response.json()["error"]["code"] == "nameAlreadyExists"
            ), f"Attempting to move item returned status code {response.status_code}; no nameAlreadyExists error"

    def get_excel_df(
        self,
        drive: str,
        file_path: str,
        sheet_name=None,
        subsite=None,
        header=0,
        keep_default_na: bool = True,
    ) -> DataFrame:
        """
        Get a Pandas DataFrame from a Sharepoint Excel file

        Parameters
        ----------
        * drive (str): name of drive
        * file_path (str): path to the excel file
        * sheet_name (str, optional): name of the excel sheet to use, defaults to None
        * subsite (str, optional): name of subsite where folder is located, defaults to None
        * header (int, optional): which row to use as column names, defaults to 0
        * keep_default_na (bool, optional): whether to interpret values (e.g., "NA", "None", etc.) as NAs, defaults to True

        Returns
        -------
        * Pandas DataFrame
        """
        excel_content = self.request_item(drive, file_path, subsite=subsite)
        df = read_excel(
            excel_content,
            sheet_name=sheet_name,
            engine="openpyxl",
            header=header,
            keep_default_na=keep_default_na,
        )
        if type(header) is list:
            # Replace column labels starting with "Unnamed:" with empty strings
            df.columns = [
                self._replace_unnamed_vals_for_multiindex_cols(col_val)
                for col_val in df.columns
            ]
        return df

    def _replace_unnamed_vals_for_multiindex_cols(self, col_val: Tuple) -> Tuple:
        return tuple([re.sub(r"^Unnamed:.*", "", val) for val in col_val])

    def get_excel_workbook(self, drive: str, file_path: str, subsite=None) -> Workbook:
        """
        Load a Sharepoint Excel file as an OpenPyXL Workbook

        Parameters
        ----------
        * drive (str): name of drive
        * file_path (str): path to the excel file
        * subsite (str, optional): name of subsite where folder is located, defaults to None

        Returns
        -------
        * OpenPyXL workbook
        """
        excel_content = self.request_item(drive, file_path, subsite=subsite)
        return load_workbook(excel_content)

    def write_excel_workbook(
        self,
        workbook: Workbook,
        drive: str,
        folder_path: str,
        file_name: str,
        subsite=None,
    ):
        """
        Save an OpenPyXL Workbook to Sharepoint as an Excel file

        Parameters
        ----------
        * workbook (OpenPyXL Workbook)
        * drive (str): name of drive
        * folder_path (str): where to save the Excel file
        * file_name (str): what to call the new Excel file
        * subsite (str, optional): name of subsite where folder is located, defaults to None

        Returns
        -------
        * None
        """
        buffer = BytesIO()
        workbook.save(buffer)
        data = buffer.getvalue()
        self.write_item(
            drive,
            data,
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            file_name,
            folder_path,
            subsite=subsite,
        )

    def write_excel_df(
        self,
        df: DataFrame,
        drive: str,
        folder_path: str,
        file_name: str,
        subsite=None,
    ):
        buffer = BytesIO()
        df.to_excel(buffer)
        data = buffer.getvalue()
        self.write_item(
            drive,
            folder_path,
            file_name,
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            data,
            subsite=subsite,
        )

    def get_csv(self, drive: str, file_path: str, subsite=None):
        """
        Get a Pandas DataFrame from a Sharepoint CSV

        Parameters
        ----------
        * drive (str): name of drive
        * file_path (str): path to the CSV file
        * subsite (str, optional): name of subsite where file is located, defaults to None

        Returns
        -------
        * Pandas DataFrame
        """
        csv_content = self.request_item(drive, file_path, subsite=subsite)
        return read_csv(csv_content)

    def write_csv(
        self,
        df: DataFrame,
        drive: str,
        folder_path: str,
        file_name: str,
        subsite=None,
    ):
        """
        Save a Pandas DataFrame to Sharepoint as a CSV

        Parameters
        ----------
        * df (Pandas DataFrame)
        * drive (str): name of drive
        * folder_path (str): where to save the CSV
        * file_name (str): what to call the new CSV
        * subsite (str, optional): name of subsite where file should be located, defaults to None

        Returns
        -------
        * None
        """
        file_data = df.to_csv(index=False).encode("utf-8")
        self.write_item(
            drive, file_data, "text/csv", file_name, folder_path, subsite=subsite
        )

    def get_txt(self, drive: str, file_path: str, subsite=None) -> str:
        """
        Get a SharePoint txt file

        Parameters
        ----------
        * drive (str): name of drive
        * file_path (str): path to the txt file
        * subsite (str, optional): name of subsite where file is located, defaults to None

        Returns
        -------
        * Content of txt file as a string
        """
        txt_content = self.request_item(drive, file_path, subsite=subsite)
        return txt_content.read().decode("utf-8")
