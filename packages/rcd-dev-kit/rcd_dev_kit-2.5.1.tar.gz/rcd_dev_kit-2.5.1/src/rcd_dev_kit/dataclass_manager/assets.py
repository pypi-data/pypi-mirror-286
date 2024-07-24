import os

import datetime
import pandas as pd
from abc import ABC, abstractmethod
from typing import Dict, Type, Union

from rcd_dev_kit.database_manager import (
    RedshiftOperator,
    read_from_redshift,
    send_to_redshift,
)
from .raw_data_file import RawDataFile
from ..pandas_manager import check_duplication, check_na
from sqlalchemy import (
    inspect,
)
from sqlalchemy.engine.reflection import Inspector


""" Assets """


class DataAsset:
    """
    Base class for managing data assets within the Tekkare environment.

    Attributes:
        __asset_type__ (str): Type of the asset.
        asset_key (str): Key identifying the asset.

    Methods:
        __init__(): Initializes a new instance of the DataAsset class.
        get_asset_key(): Retrieves the asset key.
    """

    __asset_type__: str = NotImplemented
    asset_key: str = NotImplemented

    def __init__(self) -> None:
        pass

    def get_asset_key(self):
        """
        Retrieves the asset key.

        Returns:
            str: The asset key.
        """
        return self.asset_key


""" Table Asset """


class Table(DataAsset):
    """
    Table Asset.

    Represents a dataset table, providing methods to interact with its schema,
    columns, and data.

    Attributes:
    ----------
    __asset_type__ : str
        The type of asset, set to "Dataset".
    is_dictionary : bool
        Indicates if the table is represented as a dictionary format.
    table_name : str
        The name of the table.
    schema_name : str
        The schema of the table.
    model_class : SQLAlchemy model
        The SQLAlchemy model class representing the table structure.
    ro : RedshiftOperator
        RedshiftOperator instance for database operations.
    engine : SQLAlchemy engine
        The engine connected to the database.
    asset_key : str
        Unique key identifying the asset in the format "{schema_name}.{table_name}".
    start_period : None
        Placeholder for the start period of data (not initialized in __init__).
    end_period : None
        Placeholder for the end period of data (not initialized in __init__).
    inspector : Inspector
        SQLAlchemy Inspector for introspecting the table structure.
    dct__python_type : dict
        Dictionary mapping column names to their expected Python types based on SQL types.
    _df : pandas.DataFrame or None
        Internal storage for the DataFrame representation of the table (None by default).

    Properties:
    -----------
    df : pandas.DataFrame or None
        Getter and setter property for the DataFrame representation of the table.
    lst__primary_key : list
        List of primary key column names in the table.
    lst__non_nullable_cols : list
        List of column names that are non-nullable.
    dct__sql_type : dict
        Dictionary mapping column names to their SQLAlchemy column types.
    
    Methods:
    --------
    __init__(self, table_model, is_dictionary: bool = False)
        Initializes the Table instance with table metadata and database connections.
    check_if_table_exists(self)
        Checks if the table exists in the database.
    """
    __asset_type__ = "Dataset"

    def __init__(self, table_model, is_dictionary: bool = False):
        """
        Initialize the Table instance.

        Args:
        ----
        table_model : SQLAlchemy model
            SQLAlchemy model representing the table structure.
        is_dictionary : bool, optional, default=False
            Indicates if the table is represented in dictionary format.

        Initializes attributes including table metadata, database connections,
        and extracts column Python types from SQL types.
        """
        self.is_dictionary = is_dictionary
        
        self.table_name = table_model.__tablename__
        self.schema_name = table_model.__schema__
        self.model_class = table_model
        
        self.ro = RedshiftOperator(database='staging')
        self.ro.schema = table_model.__schema__
        self.ro.table = table_model.__tablename__
        self.engine = self.ro.engine
        
        self.asset_key = f"{self.schema_name}.{self.table_name}"
        self.start_period = None
        self.end_period = None
        super().__init__()
        self.inspector = inspect(self.model_class)
        self.dct__python_type = self.extract_column_types_python()
        self._df = None

    @property
    def df(self):
        """
        pandas.DataFrame or None: Getter and setter property for the DataFrame representation of the table.
        """
        return self._df

    @df.setter
    def df(self, dataframe):
        """
        Setter for the DataFrame representation of the table.

        Args:
        ----
        dataframe : pandas.DataFrame
            DataFrame to set as the representation of the table.
        """
        print("Setting DataFrame")
        self._df = dataframe

    @property
    def lst__primary_key(self):
        """
        list: List of primary key column names in the table.
        """
        return [column.name for column in self.inspector.primary_key]

    @property
    def lst__non_nullable_cols(self):
        """
        list: List of column names that are non-nullable.
        """
        return [
            column.name
            for column in self.inspector.columns.values()
            if not column.nullable
        ]

    @property
    def dct__sql_type(self):
        """
        dict: Dictionary mapping column names to their SQLAlchemy column types.
        """
        # Create an inspector for the model's table
        return {column.name: column.type for column in self.inspector.columns.values()}

    def check_if_table_exists(self):
        """
        Check if the table exists in the database.

        Returns:
        -------
        bool
            True if the table exists, False otherwise.
        """
        insp = Inspector.from_engine(self.engine)
        table_exist = insp.has_table(self.table_name, schema=self.schema_name)
        return table_exist
        
    def extract_column_types_python(self):
        """
        Extract Python types from self.dct__sql_type.

        Returns:
        -------
        dict
            A dictionary mapping column names to their expected Python types based on self.dct__sql_type.
        """
        return {
            column_name: expected_type.python_type
            for column_name, expected_type in self.dct__sql_type.items()
        }

    def check_data_types(self):
        """
        Convert columns in self.df to specified data types in self.dct__python_type.

        Converts each column in self.df according to its specified data type in self.dct__python_type.
        For columns specified as datetime.date, attempts to convert using pd.to_datetime and raises
        a ValueError if conversion fails.

        Returns:
        -------
        pandas.DataFrame
            The DataFrame with columns converted to the specified data types.

        Raises:
        ------
        ValueError
            If there is an error converting a column to datetime.date.
        """

        for col, dtype in self.dct__python_type.items():
            if dtype == datetime.date:
                try:
                    self.df[col] = pd.to_datetime(self.df[col]).dt.date
                except ValueError as e:
                    raise ValueError(f"Error converting column '{col}' to datetime: {str(e)}")
            else:
                self.df[col] = self.df[col].astype(dtype)
        
    def check_non_nullable_columns(self):
        """
        Check for non-nullable columns in the DataFrame.
        """
        nullable_columns = [
            column.name
            for column in self.model_class.__table__.columns
            if not column.nullable
        ]
        missing_values = self.df[nullable_columns].isnull().any()
        if missing_values.any():
            raise ValueError(
                f"Non-nullable columns contain missing values: {missing_values[missing_values].index.tolist()}"
            )

    def check_columns(self):
        """
        Checks if the DataFrame `self.df` contains all expected columns specified 
        in `self.lst__columns`. Raises ValueError if there are extra columns in 
        `self.df` that are not in `self.lst__columns` or if there are missing 
        columns in `self.df` that are expected.

        Raises:
            ValueError: If extra columns are found in `self.df`.
            ValueError: If missing columns are found in `self.df`.
        """
        actual_set = set(self.df.columns)
        expected_set = set(self.lst__columns)
        
        # Check if there are extra columns in the DataFrame
        extra_columns = actual_set - expected_set
        if extra_columns:
            raise ValueError(f"Extra columns found: {', '.join(extra_columns)}")
        
        # Check if there are missing columns in the DataFrame
        missing_columns = expected_set - actual_set
        if missing_columns:
            raise ValueError(f"Missing columns: {', '.join(missing_columns)}")
    
    def validate_dataframe(self):
        """
        Validate the DataFrame against various criteria.
        """
        # self.check_missing_values()
        self.check_data_types()
        self.check_non_nullable_columns()

        check_na(self.df.loc[:, self.lst__non_nullable_cols], raise_error=True)
        check_duplication(self.df, lst_col=self.lst__primary_key, raise_error=True)
        
        

    def create_table(self, database: str = "staging"):
        """Common methods to create table structure"""
        ro = RedshiftOperator(database=database)
        ro.schema = self.schema_name
        ro.table = self.table_name

        self.model_class.metadata.create_all(ro.engine)

    def read_table(self, database: str = "staging"):
        """Common methods to read table"""
        self.df = read_from_redshift(
            database=database,
            schema=self.schema_name,
            table=self.table_name,
            method="auto",
        )

    def extract_periods_from_dataframe(self) -> None:
        """
        Extract start and end periods from _df DataFrame.
        """

        if self.is_dictionary:
            current_year = datetime.datetime.now().year

            self.start_period = str(current_year)
            self.end_period = str(current_year)
        else:
            if self._df is not None:
                try:
                    # Assuming 'period' column exists in _df DataFrame
                    self.start_period = str(self._df["period"].min())
                    self.end_period = str(self._df["period"].max())
                    print(
                        f"Start period: {self.start_period}, End period: {self.end_period}"
                    )
                except KeyError:
                    print("Error: 'period' column not found in _df DataFrame.")
            else:
                print("Error: _df DataFrame is not set.")

    def overwrite_table(self) -> None:
        """Overwrite table in Redshift."""
        if not self.check_if_table_exists():
            self.create_table()
        
        self.dataframe_to_redshift(mode="overwrite")

    def update_table(self) -> None:
        """Update table in Redshift."""
        self.dataframe_to_redshift(mode="merge_update")

    def from_staging_to_prod(self) -> None:
        """
        Transfer data from staging to production.
        """

        self._df = self.read_table()
        self.dataframe_to_redshift(mode="overwrite", database="oip")

    def dataframe_to_redshift(
        self, mode: str = "overwrite", database: str = "staging"
    ) -> None:
        """
        Send DataFrame to Redshift.

        Args:
            mode (str): Mode for writing to Redshift ('overwrite' or 'merge_update').
            database (str): Destination database (default : staging)
        """

        # Retrieve table information
        self.validate_dataframe()
        self.extract_periods_from_dataframe()

        send_to_redshift(
            database=database,
            schema=self.schema_name,
            table=self.table_name,
            mode=mode,
            primary_key=self.lst__primary_key,
            column_pivot=self.lst__primary_key,
            df=self._df,
            start_period=self.start_period,
            end_period=self.end_period,
            dct_aws_type=self.dct__sql_type,
        )


""" ETL Asset """


class ETLOperator(DataAsset, ABC):
    """
    Base class for ETL (Extract, Transform, Load) operators.

    Attributes:
        __asset_type__ (str): Type identifier for ETL processes.
        asset_key (str): Key for identifying the asset.
        dct_input (Dict[str, Union[RawDataFile, Type[RawDataFile]]]): Input data sources.
        output (DataAsset): Output data asset.
    """

    __asset_type__: str = "etl_process"
    asset_key: str = NotImplemented
    dct_input: Dict[str, Union[RawDataFile, Type[DataAsset]]] = NotImplemented
    dct_output: Dict[str, Union[RawDataFile, Type[DataAsset]]] = NotImplemented

    def __init__(self):
        """
        Initialize the ETL operator and validate input/output.
        """
        self._validate_input()
        self._validate_output()
        super().__init__()

    @classmethod
    def _validate_input(cls) -> None:
        """
        Validate the input data sources.

        Raises:
            TypeError: If input is not a DataAsset or a subclass of RawDataFile.
        """
        for key, source in cls.dct_input.items():
            if not isinstance(source, DataAsset) and not (
                isinstance(source, RawDataFile) or issubclass(type(source), RawDataFile)
            ):
                raise TypeError(
                    f"Value associated with key '{key}' must be an instance of DataAsset or a subclass of RawDataFile"
                )

    @classmethod
    def _validate_output(cls) -> None:
        """
        Validate the input data sources.

        Raises:
            TypeError: If input is not a DataAsset or a subclass of RawDataFile.
        """
        for key, source in cls.dct_output.items():
            if not isinstance(source, DataAsset) and not (
                isinstance(source, RawDataFile) or issubclass(type(source), RawDataFile)
            ):
                raise TypeError(
                    f"Value associated with key '{key}' must be an instance of DataAsset or a subclass of RawDataFile"
                )

    def process(self):
        """
        Perform the ETL process: get raw data, transform, and load.
        """
        self.get_raw_data()
        self.transform()
        self.load()

    @abstractmethod
    def get_raw_data(self):
        """
        Abstract method to extract raw data.
        """
        pass

    @abstractmethod
    def transform(self):
        """
        Abstract method to transform the data.
        """
        pass

    @abstractmethod
    def load(self):
        """
        Abstract method to load the transformed data.

        Also sends metadata to Directus.
        """
        self.send_metadata_to_directus()

    def get_metadata(self):
        """
        Extract metadata about input, process, and output.

        Returns:
            Dict: Metadata dictionary.
        """
        lst_source = []

        for key, source in self.dct_input.items():
            if isinstance(source, RawDataFile):
                dct_source = {
                    "asset_type": "RawDataFile",
                    "asset_value": {
                        "source_uuid": source.source_uuid,
                        "file_name": source.file_name,
                    },
                }
            elif isinstance(source, DataAsset):
                dct_source = {
                    "asset_type": source.__asset_type__,
                    "asset_key": source.get_asset_key(),
                }
            else:
                raise ValueError("Data Asset source type not recognized")

            lst_source.append(dct_source)

        return {
            "lst_input": self.get_metadata_info(self.dct_input),
            "etl_process": {
                "asset_key": self.get_asset_key(),
                "asset_type": self.__asset_type__,
            },
            "output": self.get_metadata_info(self.dct_output),
        }

    def get_metadata_info(self, dct_asset: dict):
        """
        Extract metadata about input, process, and output.

        Returns:
        """
        lst_metadata = []

        for key, source in dct_asset.items():
            if isinstance(source, RawDataFile):
                dct_metadata = {
                    "asset_type": "RawDataFile",
                    "asset_value": {
                        "source_uuid": source.source_uuid,
                        "file_name": source.file_name,
                    },
                }
            elif isinstance(source, DataAsset):
                dct_metadata = {
                    "asset_type": source.__asset_type__,
                    "asset_key": source.get_asset_key(),
                }
            else:
                raise ValueError("Data Asset source type not recognized")

            lst_metadata.append(dct_metadata)
