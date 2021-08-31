from abc import ABC, abstractmethod


class BaseModel(ABC):
    @classmethod
    @abstractmethod
    def find_by_id(cls, id_: int):
        """
        Method for finding event by its id.
        Returns None when object is not found
        :param id_: int
        """
        pass

    @abstractmethod
    def save_to_db(self) -> None:
        """
        Save object to the database
        :return: None
        """
        pass

    @abstractmethod
    def delete_from_db(self) -> None:
        """
        Delete object from the database
        :return: None
        """
        pass
