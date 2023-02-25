import json
import pandas as pd
from abc import ABC, abstractmethod
from typing import Dict, Any


class loader(ABC):

    @abstractmethod
    def load_data(self) -> Dict[str, Any]:
        """Method responsible to load any spatial data type to json type"""
        pass

    @abstractmethod
    def normalize(self, json_data: Dict[str, Any]) -> pd.DataFrame:
        """Converting the json data to pandas dataframe"""
        pass

class GoogleEarthLoader(loader):
    
    def load_data(self, filePath: str) -> None:

        with open(filePath) as f:
            self.json_data = json.load(f)


    def normalize(self) -> pd.DataFrame:
        json_df = pd.json_normalize(self.json_data['features'], sep = '_').drop(['properties_description', 'geometry_type', 'type'], axis = 1)

        return json_df


class formatter(ABC):

    @abstractmethod
    def apply_format(self):
        pass


class GoogleEarthFormatter(formatter):
    def __init__(self, Data_Frame: pd.DataFrame) -> None:
        self.DataFrame = Data_Frame
    
    def _swapper(self, Series2Swap) -> None:
            
        def _swapPositions(list_, pos1 = 0, pos2 = 1):
 
            # Storing the two elements
            # as a pair in a tuple variable get
            get = list_[pos1], list_[pos2]
      
            # unpacking those elements
            list_[pos2], list_[pos1] = get
      
            return list_

        def _swap_latLon(list_of_list):
    
            # Swap the position of all the elements of list of list 
            swapped = list(map(_swapPositions, list_of_list))
    
            return swapped

        self.DataFrame[Series2Swap].apply(_swap_latLon)

    @staticmethod
    def _str_concat(list_elements):
        to_str = [list(map(str, i)) for i in list_elements]
        l_str = [','.join(i) for i in to_str]
        complete_str = ';'.join(l_str)

        return complete_str

    def apply_format(self):
        self._swapper('geometry_coordinates')
        self.DataFrame['coordinate_set'] = self.DataFrame['geometry_coordinates'].map(self._str_concat)
        self.DataFrame.drop(columns='geometry_coordinates', inplace=True)

        geo_dict = self.DataFrame.set_index('properties_Name').T.to_dict('list')

        return geo_dict
