"""
This file contains the basic dataset functions.
"""
from typing import Dict, List, Optional, Union

import pandas as pd

from hyfi.utils.logging import LOGGING
from hyfi.utils.types import DictLike, ListLike

logger = LOGGING.getLogger(__name__)


class DSBasic:
    @staticmethod
    def dataframe_select_columns(
        data: pd.DataFrame,
        columns: Union[List[str], str],
        verbose: bool = False,
    ) -> pd.DataFrame:
        """
        Select columns from a dataframe.

        Args:
            data (pd.DataFrame): The dataframe to select columns from.
            columns (List[str]): The columns to select.
            verbose (bool, optional): Whether to print verbose output. Defaults to False.

        Returns:
            pd.DataFrame: The dataframe with the columns selected.

        Examples:
            >>> import pandas as pd
            >>> from hyfi.utils.datasets.basic import DSBasic
            >>> data = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
            >>> DSBasic.dataframe_select_columns(data, columns=["a"])
               a
            0  1
            1  2
            2  3
        """
        columns = [columns] if isinstance(columns, str) else columns
        columns = [c for c in columns if c in data.columns]
        if verbose:
            logger.info("Selecting columns: %s", columns)
        return data[columns]

    @staticmethod
    def dataframe_drop_columns(
        data: pd.DataFrame,
        columns: Union[List[str], str],
        level: Optional[int] = None,
        errors: str = "raise",
        verbose: bool = False,
    ) -> pd.DataFrame:
        """
        Drop columns from a dataframe.

        Args:
            data (pd.DataFrame): The dataframe to drop columns from.
            columns (List[str]): The columns to drop.
            level (int, optional): The level to drop columns from. Defaults to None.
            errors (str, optional): Whether to raise an error if the column does not exist. Defaults to "raise".
            verbose (bool, optional): Whether to print verbose output. Defaults to False.

        Returns:
            pd.DataFrame: The dataframe with the columns dropped.

        Examples:
            >>> import pandas as pd
            >>> from hyfi.utils.datasets.basic import DSBasic
            >>> data = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
            >>> DSBasic.dataframe_drop_columns(data, columns=["a"])
                b
            0   4
            1   5
            2   6
        """
        if verbose:
            logger.info("Dropping columns %s", columns)
        if isinstance(columns, str):
            columns = [columns]
        data.drop(columns=columns, level=level, errors=errors, inplace=True)
        return data

    @staticmethod
    def dataframe_drop(
        data: pd.DataFrame,
        labels: Union[List[str], str],
        axis: int = 1,
        level: Optional[int] = None,
        errors: str = "raise",
        verbose: bool = False,
    ) -> pd.DataFrame:
        """
        Drop columns from a dataframe.

        Args:
            data (pd.DataFrame): The dataframe to drop columns from.
            labels (List[str]): The columns or index to drop.
            axis (int, optional): The axis to drop from. Defaults to 1.
            level (int, optional): The level to drop columns from. Defaults to None.
            errors (str, optional): Whether to raise an error if the column does not exist. Defaults to "raise".
            verbose (bool, optional): Whether to print verbose output. Defaults to False.

        Returns:
            pd.DataFrame: The dataframe with the columns dropped.
        """
        if verbose:
            logger.info("Dropping labels %s", labels)
        if isinstance(labels, str):
            labels = [labels]
        data.drop(labels=labels, axis=axis, level=level, errors=errors, inplace=True)
        return data

    @staticmethod
    def dataframe_split_str_column(
        data: pd.DataFrame,
        column: str,
        sep: str,
        new_column_name: Optional[str] = None,
        drop_old_column: bool = False,
        verbose: bool = False,
    ) -> pd.DataFrame:
        """
        Split a column of strings into a new column.

        Args:
            data (pd.DataFrame): The dataframe to split.
            column (str): The column to split.
            sep (str): The string to split on.
            new_column_name (str): The name of the new column.
            drop_old_column (bool, optional): Whether to drop the old column. Defaults to False.
            verbose (bool, optional): Whether to print verbose output. Defaults to False.

        Returns:
            pd.Dataframe: The dataframe with the new column.

        Examples:
            >>> import pandas as pd
            >>> from hyfi.utils.datasets.basic import DSBasic
            >>> data = pd.DataFrame({"a": ["1,2", "3,4", "5,6"]})
            >>> DSBasic.dataframe_split_str_column(data, column="a", sep=",")
                a_1
            0   1
            1   3
            2   5
        """
        if new_column_name is None:
            new_column_name = column
            drop_old_column = False
        if verbose:
            logger.info(
                "Splitting column %s on %s into new column %s",
                column,
                sep,
                new_column_name,
            )
        data[new_column_name] = data[column].str.split(sep)
        if drop_old_column:
            data.drop(column, axis=1, inplace=True)
        return data

    @staticmethod
    def dataframe_combine_str_columns(
        data: pd.DataFrame,
        columns: List[str],
        sep: str,
        fillna: Optional[str] = None,
        new_column_name: Optional[str] = None,
        drop_old_columns: bool = False,
        verbose: bool = False,
    ) -> pd.DataFrame:
        """
        Combine columns of strings into a new column.

        Args:
            data (pd.DataFrame): The dataframe to combine.
            columns (List[str]): The columns to combine.
            sep (str): The string to combine on.
            fillna (str, optional): The string to fill NaN values with. Defaults to None.
            new_column_name (str): The name of the new column.
            drop_old_columns (bool, optional): Whether to drop the old columns. Defaults to False.
            verbose (bool, optional): Whether to print verbose output. Defaults to False.

        Returns:
            pd.Dataframe: The dataframe with the new column.

        Examples:
            >>> import pandas as pd
            >>> from hyfi.utils.datasets.basic import DSBasic
            >>> data = pd.DataFrame({"a": ["1", "3", "5"], "b": ["2", "4", "6"]})
            >>> DSBasic.dataframe_combine_str_columns(data, columns=["a", "b"], sep=",")
                a_b
            0   1,2
            1   3,4
            2   5,6

        """
        if new_column_name is None:
            new_column_name = "_".join(columns)
            drop_old_columns = False
        if verbose:
            logger.info(
                "Combining columns %s into new column %s",
                columns,
                new_column_name,
            )
        if fillna:
            data[new_column_name] = data[columns].fillna(fillna).agg(sep.join, axis=1)
        else:
            data[new_column_name] = data[columns].agg(sep.join, axis=1)
        if drop_old_columns:
            data.drop(columns, axis=1, inplace=True)
        return data

    @staticmethod
    def dataframe_eval_columns(
        data: pd.DataFrame,
        expressions: Union[Dict[str, str], List[str]],
        engine: str = "python",
        verbose: bool = False,
    ) -> pd.DataFrame:
        """
        Evaluate columns in a dataframe.

        Args:
            data (pd.DataFrame): The dataframe to evaluate.
            expressions (Union[Dict[str, str], List[str]]): The expressions to evaluate.
            engine (str, optional): The engine to use. Defaults to "python".
            verbose (bool, optional): Whether to print verbose output. Defaults to False.

        Returns:
            pd.DataFrame: The dataframe with the evaluated columns.

        Examples:
            >>> import pandas as pd
            >>> from hyfi.utils.datasets.basic import DSBasic
            >>> data = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
            >>> DSBasic.dataframe_eval_columns(data, expressions={"c": "a + b"})
                a   b   c
            0   1   4   5
            1   2   5   7
            2   3   6   9

        """
        if isinstance(expressions, DictLike):
            for column in expressions:
                if verbose:
                    logger.info("Evaluating column %s", column)
                data[column] = data.eval(expressions[column], engine=engine)
        elif isinstance(expressions, ListLike):
            for expression in expressions:
                if verbose:
                    logger.info("Evaluating expression %s", expression)
                data = data.eval(expression, engine=engine)
        return data

    @staticmethod
    def dataframe_eval_columns_with_pd_eval(
        data: pd.DataFrame,
        expressions: Union[Dict[str, str], List[str]],
        engine: str = "python",
        verbose: bool = False,
    ) -> pd.DataFrame:
        """
        Evaluate columns in a dataframe using the pandas eval function.

        Args:
            data (pd.DataFrame): The dataframe to evaluate.
            expressions (Union[Dict[str, str], List[str]]): The expressions to evaluate.
            engine (str, optional): The engine to use. Defaults to "python".
            verbose (bool, optional): Whether to print verbose output. Defaults to False.

        Returns:
            pd.DataFrame: The dataframe with the evaluated columns.

        Examples:
            >>> import pandas as pd
            >>> from hyfi.utils.datasets.basic import DSBasic
            >>> data = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
            F>>> DSBasic.dataframe_eval_columns_with_pd_eval(data, expressions={"c": "data.a + data.b"})
                a   b   c
            0   1   4   5
            1   2   5   7
            2   3   6   9

        """
        if isinstance(expressions, DictLike):
            for column in expressions:
                if verbose:
                    logger.info("Evaluating column %s", column)
                data[column] = pd.eval(expressions[column], engine=engine, target=data)
        elif isinstance(expressions, ListLike):
            for expression in expressions:
                if verbose:
                    logger.info("Evaluating expression %s", expression)
                data = pd.eval(expression, engine=engine, target=data)
        return data

    # @staticmethod
    # def dataframe_eval_columns_with_eval(
    #     data: pd.DataFrame,
    #     expressions: Dict[str, str],
    #     verbose: bool = False,
    # ) -> pd.DataFrame:
    #     """
    #     Evaluate columns in a dataframe using the built-in eval function.

    #     Args:
    #         data (pd.DataFrame): The dataframe to evaluate.
    #         expressions (Union[Dict[str, str], List[str]]): The expressions to evaluate.
    #         engine (str, optional): The engine to use. Defaults to "python".
    #         verbose (bool, optional): Whether to print verbose output. Defaults to False.

    #     Returns:
    #         pd.DataFrame: The dataframe with the evaluated columns.

    #                 Examples:
    #         >>> import pandas as pd
    #         >>> from hyfi.utils.datasets.basic import DSBasic
    #         >>> data = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    #         F>>> DSBasic.dataframe_eval_columns_with_eval(data, expressions={"c": "data.a + data.b"})
    #             a   b   c
    #         0   1   4   5
    #         1   2   5   7
    #         2   3   6   9
    #     """
    #     for column in expressions:
    #         if verbose:
    #             logger.info("Evaluating column %s", column)
    #         data[column] = eval(expressions[column])
    #     return data

    @staticmethod
    def dataframe_print_head_and_tail(
        data: pd.DataFrame,
        num_heads: Optional[int] = 5,
        num_tails: Optional[int] = 5,
        columns: Optional[Union[List[str], str]] = None,
        verbose: bool = False,
    ) -> pd.DataFrame:
        """
        Print the head and tail of a dataframe.

        Args:
            data (pd.DataFrame): The dataframe to print.
            num_heads (int, optional): The number of rows to print from the head. Defaults to 5.
            num_tails (int, optional): The number of rows to print from the tail. Defaults to 5.
            verbose (bool, optional): Whether to print verbose output. Defaults to False.

        Returns:
            pd.DataFrame: The dataframe.

        Examples:
            >>> import pandas as pd
            >>> from hyfi.utils.datasets.basic import DSBasic
            >>> data = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
            >>> DSBasic.dataframe_print_head_and_tail(data, num_heads=1, num_tails=1)
                a   b
            0   1   4
            2   3   6
        """
        if not columns:
            columns = data.columns
        elif isinstance(columns, str):
            columns = [columns]
        if verbose:
            logger.info("Printing head and tail of dataframe")
        if num_heads:
            if verbose:
                logger.info("Head:")
            print(data[columns].head(num_heads))
        if num_tails:
            if verbose:
                logger.info("Tail:")
            print(data[columns].tail(num_tails))
        return data
