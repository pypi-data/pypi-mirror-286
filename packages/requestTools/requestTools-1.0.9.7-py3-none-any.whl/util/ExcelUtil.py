import pandas as pd

class XlsxUtil:
    """
    A utility class for handling operations related to Excel files.
    """

    @staticmethod
    def saveExcel(datas,path,fileName):
        """
        Save data to an Excel file.

        Args:
            datas (list or dict): The data to be saved, which could be a list of dictionaries or a dictionary of lists.
            path (str): The directory path where the Excel file will be saved.
            fileName (str): The name of the Excel file (without the extension).

        Returns:
            None

        Example usage：
            XlsxUtil.saveExcel(data, '/path/to/save/', 'example_filename')
        """

        df = pd.DataFrame(datas)
        df.to_excel(path+fileName+'.xlsx',sheet_name='sheet0', index=False)