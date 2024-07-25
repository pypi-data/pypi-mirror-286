import glob
import pandas as pd

class DataAcquisition(object):
    @classmethod
    def get_data_from_dir(cls, DATA_DIR_PATH):
        """
        Parameters
        ----------
        DATA_DIR_PATH (string): the location of the data files (.txt, .csv)

        Returns
        -------
        df (pandas.DataFrame): data in pandas dataframe format
        """
        print ("data dir path : "+DATA_DIR_PATH)
        files = sorted(glob.glob(DATA_DIR_PATH+"/200*"))
        print ("length of files : ", len(files))
        df = pd.read_csv(files[0], sep='\t', header=None, names=(['0','1','2','3']))
        for i in range(1, len(files)):
            df = pd.concat([df, pd.read_csv(files[i], sep='\t', header=None, names=(['0','1','2','3']))], axis=0)
        return df

    @classmethod
    def get_data_from_file(cls, DATA_FILE_PATH):
        """
        Parameters
        ----------
        DATA_FILE_PATH (string): the location of the single data file (.txt, .csv)

        Returns
        -------
        df (pandas.DataFrame): data in pandas dataframe format
        """
        df = pd.read_csv(DATA_FILE_PATH, sep='\t', header=None, names=(['0','1','2','3']))

        return df
