from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.inspection import inspect

class Base(DeclarativeBase):
    """
    Class that allows you to connect objects to tables in the database, in addition to mapping them so that the class becomes a table in the database
    
    If printed, the class will display all its attributes and values ​​(if any)
    """
    def __repr__(self) -> str:
        cls = self.__class__
        column_attrs = inspect(cls).mapper.column_attrs
        columns = {attr.key: getattr(self, attr.key) for attr in column_attrs}
        columns_str = ", ".join(f"{key}={value!r}" for key, value in columns.items())
        return f"{cls.__name__}({columns_str})"
    
    def dict(self) -> dict:
        """
        Converte o objeto para um dicionário, removendo chaves com valores None.
        
        Args:
            None
        Returns:
            Dict[str, Any]: O objeto convertido em dicionário.
        """
        column_attrs = inspect(self.__class__).mapper.column_attrs
        columns = {attr.key: getattr(self, attr.key) for attr in column_attrs}
        columns = {k: v for k, v in columns.items() if v is not None}
        return columns