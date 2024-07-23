from sqlbox.creat_db import Database
from sqlbox.table import table
from typing import Optional, Union, Dict, Tuple, List
from sqlbox.exception_ import TableNotFoundError
    

_SQL_TYPE=dict(
        int_primary_key='INTEGER PRIMARY KEY',
        text_primary_key='TEXT PRIMARY KEY',
        int='INTEGER',
        float='FLOAT',
        text='TEXT',
        blob='BLOB',
        null='NULL',    
    )


class sqlbox(Database):
    def __init__(
            self,
            *,
            database_name:str
        ) -> None:
        """
        Initializes a new instance of the `sqlbox` class.

        Args:
            database_name (str): The name of the database.

        Returns:
            None
        """
        
        super().__init__(database=database_name) # type: ignore
        self.database_name=database_name
        self._creat_database()

    def create_table(
            self, 
            table_name:str,
            columns:Union[Dict[str, _SQL_TYPE]],  # type: ignore
            ) -> None: 
        """
        Creates a table in the database with the given `table_name` and `columns`.

        Args:
            table_name (str): The name of the table to be created.
            columns (Dict[str, _SQL_TYPE]): A dictionary mapping column names to their corresponding SQL types.

        Returns:
            None

        Raises:
            None

        Notes:
            - This function connects to the database, creates a table with the given name and columns, and commits the changes.
            - If the table already exists, it will not be recreated.
            - The function closes the database connection after committing the changes.
        """
        
        self.table_name=table_name
        if isinstance(columns, dict):
            self._connect_database()
            v=','.join(tuple((f'{c} {_SQL_TYPE[t]}'  for c, t in columns.items())))
            self.cur.execute(f'''
                    CREATE TABLE IF NOT EXISTS {table_name} (
                        {v}
                    )
                    ''')
            
        self.con.commit()
        self.con.close()

    def insert_into(
                self, 
                *, 
                field:tuple, 
                value:tuple
            ) -> table:
        """
        Inserts a new row into the table with the specified field values.

        Args:
            field (tuple): The field names to insert data into.
            value (tuple): The corresponding values to insert into the fields.

        Returns:
            table: The table instance after inserting the new row.

        Raises:
            TableNotFoundError: If the table does not exist in the database.
        """

        if self.table_name:
            self._connect_database()
            self.cur.execute(f'INSERT INTO {self.table_name} {field} VALUES ({(t:=','.join('?'*len(value)))})', value)
            self.con.commit()
            self.con.close()

        else:
            raise TableNotFoundError("Table not found")

        return table
    
    def get(
            self,
            field_name:Optional[str]=None,
            all:bool=True
        ) -> tuple:
        """
    	Retrieves data from the table based on the specified field name and whether to fetch all rows or not.
    	
    	Args:
    	    field_name (Optional[str]): The name of the field to retrieve data from.
    	    all (bool): A flag to determine whether to fetch all rows or not.
    	
    	Returns:
    	    The rows of data fetched based on the specified criteria.
    	"""

        if all and self.table_name:
            self._connect_database()
            self.cur.execute(f'SELECT * FROM {self.table_name}')
            rows=self.cur.fetchall()
            self.cur.close()
            return rows

        elif not all and self.table_name:
            self._connect_database()
            self.cur.execute(f'SELECT {field_name} FROM {self.table_name}')
            rows=self.cur.fetchall()
            self.cur.close()
            return rows
        
    def update(
            self,
            *,
            field_name:Union[List, Tuple],
            value:Union[List, Tuple]
        ) -> None:
        """
        Updates a row in the table with the specified field name and value.

        Args:
            field_name (Union[List, Tuple]): A tuple containing the field name to update and the new value.
            value (Union[List, Tuple]): A tuple containing the current value of the field and the new value.

        Raises:
            TableNotFoundError: If the table does not exist in the database.

        Returns:
            None
        """

        if  self.table_name:
            self._connect_database()
            self.cur.execute(f'UPDATE {self.table_name} SET {field_name[1]} = ? WHERE {field_name[0]} = ?', (value[1], value[0]))
            self.con.commit()
            self.con.close()

        else:
            raise TableNotFoundError("Table not found")
        
    def delete(
            self,
            *,
            field:str,
            value
        ) -> None:
        """
        Deletes a row from the table based on the specified field and value.

        Args:
            field (str): The name of the field to filter the deletion.
            value: The value of the specified field to delete.

        Raises:
            TableNotFoundError: If the table does not exist in the database.

        Returns:
            None
        """
        if  self.table_name:
            self._connect_database()
            self.cur.execute(f'DELETE FROM {self.table_name} WHERE {field} = ?', (value,))
            self.con.commit()
            self.con.close()

        else:
            raise TableNotFoundError("Table not found")
        
    def table(self):
        """
        Retrieves a table object based on the database name and table name provided.

        Parameters:
            self (object): The instance of the class.

        Returns:
            Either a table object representing the specified table or raises a TableNotFoundError if the table is not found.
        """
        return table(database_name=self.database_name, table_name=self.table_name) if self.table_name else TableNotFoundError("Table not found")