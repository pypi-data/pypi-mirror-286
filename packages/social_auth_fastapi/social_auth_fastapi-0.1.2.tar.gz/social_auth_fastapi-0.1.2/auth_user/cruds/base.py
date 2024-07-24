#!/usr/bin/env python3
from typing import Any, Dict, Generic, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import Join, Row, and_, delete, func, inspect, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.helper import (
    _add_column_with_prefix,
    _auto_detect_join_condition,
    _extract_matching_columns_from_kwargs,
    _extract_matching_columns_from_schema,
)
from ..models.base import MappedBase

ModelType = TypeVar('ModelType', bound=MappedBase)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)
UpdateSchemaInternalType = TypeVar('UpdateSchemaInternalType', bound=BaseModel)
DeleteSchemaType = TypeVar('DeleteSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Base class for CRUD operations on a model.

    Parameters
    ----------
    model : Type[ModelType]
        The SQLAlchemy model type.
    """

    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model

    async def get_with_condition(self, db: AsyncSession, condition):
        """
        Example:
            condition=[
                Jobs.job_confirmation_code == job_confirmation_code,
                Jobs.status = 1
            ]
        """
        query = select(self.model).filter(*condition)
        groups = await db.execute(query)
        return groups.scalars().first()

    async def get_(
        self,
        db: AsyncSession,
        *,
        pk: int | None = None,
        name: str | None = None,
        status: int | None = None,
        del_flag: int | None = None,
    ) -> ModelType | None:
        """
        Get a piece of data by primary key id or name

        :param db:
        :param pk:
        :param name:
        :param status:
        :param del_flag:
        :return:
        """
        assert (
            pk is not None or name is not None
        ), 'Query error, pk and name parameters cannot be empty at the same time'
        assert pk is None or name is None, 'Query error, pk and name parameters cannot exist at the same time'
        where_list = [self.model.id == pk] if pk is not None else [self.model.name == name]
        if status is not None:
            assert status in (0, 1), 'Query error, status parameter can only be 0 or 1'
            where_list.append(self.model.status == status)
        if del_flag is not None:
            assert del_flag in (0, 1), 'Query error, del_flag parameter can only be 0 or 1'
            where_list.append(self.model.del_flag == del_flag)

        result = await db.execute(select(self.model).where(and_(*where_list)))
        return result.scalars().first()

    async def get_dict_(
        self, db: AsyncSession, schema_to_select: type[BaseModel] | list | None = None, **kwargs: Any
    ) -> dict | None:
        """
        Get a piece of data by primary key id or name

        :param db:
        :param schema_to_select: Union[Type[BaseModel], list, None],
        optional Pydantic schema for selecting specific columns.
        Default is None to select all columns.:
        :return: dict | None The fetched database row or None if not found.
        """
        to_select = _extract_matching_columns_from_schema(model=self.model, schema=schema_to_select)
        stmt = select(*to_select).filter_by(**kwargs)

        db = await db.execute(stmt)
        result: Row = db.first()
        if result:
            out: dict = dict(result._mapping)
            return out

        return None

    async def exists_(self, db: AsyncSession, **kwargs: Any) -> bool:
        """Check if a record exists based on filters.

        Parameters
        ----------
        db : AsyncSession
            The SQLAlchemy async session.
        kwargs : dict
            Filters to apply to the query.

        Returns
        -------
        bool
            True if a record exists, False otherwise.
        """
        to_select = _extract_matching_columns_from_kwargs(model=self.model, kwargs=kwargs)
        stmt = select(*to_select).filter_by(**kwargs).limit(1)

        result = await db.execute(stmt)
        return result.first() is not None

    async def count_(self, db: AsyncSession, **kwargs: Any) -> int:
        """Count the records based on filters.

        Parameters
        ----------
        db : AsyncSession
            The SQLAlchemy async session.
        kwargs : dict
            Filters to apply to the query.

        Returns
        -------
        int
            Total count of records that match the applied filters.

        Note
        ----
        This method provides a quick way to get the count of records without retrieving the actual data.
        """
        if kwargs:
            conditions = [getattr(self.model, key) == value for key, value in kwargs.items()]
            combined_conditions = and_(*conditions)
            count_query = select(func.count()).select_from(self.model).filter(combined_conditions)
        else:
            count_query = select(func.count()).select_from(self.model)

        total_count: int = await db.scalar(count_query)

        return total_count

    async def get_multi_(
        self,
        db: AsyncSession,
        offset: int = 0,
        limit: int = 100,
        schema_to_select: type[BaseModel] | list[type[BaseModel]] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch multiple records based on filters.

        Parameters
        ----------
        db : AsyncSession
            The SQLAlchemy async session.
        offset : int, optional
            Number of rows to skip before fetching. Default is 0.
        limit : int, optional
            Maximum number of rows to fetch. Default is 100.
        schema_to_select : Union[Type[BaseModel], list[Type[BaseModel]], None], optional
            Pydantic schema for selecting specific columns. Default is None to select all columns.
        kwargs : dict
            Filters to apply to the query.

        Returns
        -------
        dict[str, Any]
            Dictionary containing the fetched rows under 'data' key and total count under 'total_count'.
        """
        to_select = _extract_matching_columns_from_schema(model=self.model, schema=schema_to_select)
        stmt = select(*to_select).filter_by(**kwargs).offset(offset).limit(limit)

        result = await db.execute(stmt)
        data = [dict(row) for row in result.mappings()]

        total_count = await self.count_(db=db, **kwargs)

        return {'data': data, 'total_count': total_count}

    async def get_joined_(
        self,
        db: AsyncSession,
        join_model: type[ModelType],
        join_prefix: str | None = None,
        join_on: Join | None = None,
        schema_to_select: type[BaseModel] | list | None = None,
        join_schema_to_select: type[BaseModel] | list | None = None,
        join_type: str = 'left',
        **kwargs: Any,
    ) -> dict | None:
        """Fetches a single record with a join on another model. If 'join_on' is not provided, the method attempts
        to automatically detect the join condition using foreign key relationships.

        Parameters
        ----------
        db : AsyncSession
            The SQLAlchemy async session.
        join_model : Type[ModelType]
            The model to join with.
        join_prefix : Optional[str]
            Optional prefix to be added to all columns of the joined model. If None, no prefix is added.
        join_on : Join, optional
            SQLAlchemy Join object for specifying the ON clause of the join. If None, the join condition is
            auto-detected based on foreign keys.
        schema_to_select : Union[Type[BaseModel], list, None], optional
            Pydantic schema for selecting specific columns from the primary model.
        join_schema_to_select : Union[Type[BaseModel], list, None], optional
            Pydantic schema for selecting specific columns from the joined model.
        join_type : str, default "left"
            Specifies the type of join operation to perform. Can be "left" for a left outer join
            or "inner" for an inner join.
        kwargs : dict
            Filters to apply to the query.

        Returns
        -------
        dict | None
            The fetched database row or None if not found.

        Examples
        --------
        Simple example: Joining User and Tier models without explicitly providing join_on
        ```python
        result = await crud_user.get_joined(
            db=session, join_model=Tier, schema_to_select=UserSchema, join_schema_to_select=TierSchema
        )
        ```

        Complex example: Joining with a custom join condition, additional filter parameters, and a prefix
        ```python
        from sqlalchemy import and_

        result = await crud_user.get_joined(
            db=session,
            join_model=Tier,
            join_prefix="tier_",
            join_on=and_(User.tier_id == Tier.id, User.is_superuser == True),
            schema_to_select=UserSchema,
            join_schema_to_select=TierSchema,
            username="john_doe",
        )
        ```

        Return example: prefix added, no schema_to_select or join_schema_to_select
        ```python
        {
            "id": 1,
            "name": "John Doe",
            "username": "john_doe",
            "email": "johndoe@example.com",
            "hashed_password": "hashed_password_example",
            "profile_image_url": "https://profileimageurl.com/default.jpg",
            "uuid": "123e4567-e89b-12d3-a456-426614174000",
            "created_at": "2023-01-01T12:00:00",
            "updated_at": "2023-01-02T12:00:00",
            "deleted_at": null,
            "is_deleted": false,
            "is_superuser": false,
            "tier_id": 2,
            "tier_name": "Premium",
            "tier_created_at": "2022-12-01T10:00:00",
            "tier_updated_at": "2023-01-01T11:00:00",
        }
        ```
        """
        if join_on is None:
            join_on = _auto_detect_join_condition(self.model, join_model)

        primary_select = _extract_matching_columns_from_schema(model=self.model, schema=schema_to_select)
        join_select = []

        if join_schema_to_select:
            columns = _extract_matching_columns_from_schema(model=join_model, schema=join_schema_to_select)
        else:
            columns = inspect(join_model).c

        for column in columns:
            labeled_column = _add_column_with_prefix(column, join_prefix)
            if f'{join_prefix}{column.name}' not in [col.name for col in primary_select]:
                join_select.append(labeled_column)

        if join_type == 'left':
            stmt = select(*primary_select, *join_select).outerjoin(join_model, join_on)
        elif join_type == 'inner':
            stmt = select(*primary_select, *join_select).join(join_model, join_on)
        else:
            raise ValueError(f"Invalid join type: {join_type}. Only 'left' or 'inner' are valid.")

        for key, value in kwargs.items():
            if hasattr(self.model, key):
                stmt = stmt.where(getattr(self.model, key) == value)

        db_row = await db.execute(stmt)
        result: Row = db_row.first()
        if result:
            out: dict = dict(result._mapping)
            return out

        return None

    async def get_multi_joined_(
        self,
        db: AsyncSession,
        join_model: type[ModelType],
        join_prefix: str | None = None,
        join_on: Join | None = None,
        schema_to_select: type[BaseModel] | list[type[BaseModel]] | None = None,
        join_schema_to_select: type[BaseModel] | list[type[BaseModel]] | None = None,
        join_type: str = 'left',
        offset: int = 0,
        limit: int = 100,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Fetch multiple records with a join on another model, allowing for pagination.

        Parameters
        ----------
        db : AsyncSession
            The SQLAlchemy async session.
        join_model : Type[ModelType]
            The model to join with.
        join_prefix : Optional[str]
            Optional prefix to be added to all columns of the joined model. If None, no prefix is added.
        join_on : Join, optional
            SQLAlchemy Join object for specifying the ON clause of the join. If None, the join condition is
            auto-detected based on foreign keys.
        schema_to_select : Union[Type[BaseModel], list[Type[BaseModel]], None], optional
            Pydantic schema for selecting specific columns from the primary model.
        join_schema_to_select : Union[Type[BaseModel], list[Type[BaseModel]], None], optional
            Pydantic schema for selecting specific columns from the joined model.
        join_type : str, default "left"
            Specifies the type of join operation to perform. Can be "left" for a left outer join
            or "inner" for an inner join.
        offset : int, default 0
            The offset (number of records to skip) for pagination.
        limit : int, default 100
            The limit (maximum number of records to return) for pagination.
        kwargs : dict
            Filters to apply to the primary query.

        Returns
        -------
        dict[str, Any]
            A dictionary containing the fetched rows under 'data' key and total count under 'total_count'.

        Examples
        --------
        # Fetching multiple User records joined with Tier records, using left join
        users = await crud_user.get_multi_joined(
            db=session,
            join_model=Tier,
            join_prefix="tier_",
            schema_to_select=UserSchema,
            join_schema_to_select=TierSchema,
            offset=0,
            limit=10
        )
        """
        if join_on is None:
            join_on = _auto_detect_join_condition(self.model, join_model)

        primary_select = _extract_matching_columns_from_schema(model=self.model, schema=schema_to_select)
        join_select = []

        if join_schema_to_select:
            columns = _extract_matching_columns_from_schema(model=join_model, schema=join_schema_to_select)
        else:
            columns = inspect(join_model).c

        for column in columns:
            labeled_column = _add_column_with_prefix(column, join_prefix)
            if f'{join_prefix}{column.name}' not in [col.name for col in primary_select]:
                join_select.append(labeled_column)

        if join_type == 'left':
            stmt = select(*primary_select, *join_select).outerjoin(join_model, join_on)
        elif join_type == 'inner':
            stmt = select(*primary_select, *join_select).join(join_model, join_on)
        else:
            raise ValueError(f"Invalid join type: {join_type}. Only 'left' or 'inner' are valid.")

        for key, value in kwargs.items():
            if hasattr(self.model, key):
                stmt = stmt.where(getattr(self.model, key) == value)

        stmt = stmt.offset(offset).limit(limit)

        db_rows = await db.execute(stmt)
        data = [dict(row._mapping) for row in db_rows]

        total_count = await self.count_(db=db, **kwargs)

        return {'data': data, 'total_count': total_count}

    async def create_(self, db: AsyncSession, obj_in: CreateSchemaType, user_id: int | None = None) -> None:
        """Create a new record in the database.

        :param db: AsyncSession
        :param obj_in: Pydantic Model class
        :param user_id:
        :return:
        """
        if user_id:
            create_data = self.model(**obj_in.model_dump(), create_user=user_id)
        else:
            create_data = self.model(**obj_in.model_dump())
        db.add(create_data)

    async def update_(
        self, db: AsyncSession, pk: int, obj_in: UpdateSchemaType | Dict[str, Any], user_id: int | None = None
    ) -> int:
        """
        Update a piece of data by primary key id

        :param db:
        :param pk:
        :param obj_in: Pydantic Model class or dictionary corresponding to database fields
        :param user_id:
        :return:
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        if user_id:
            update_data.update({'update_user': user_id})
        result = await db.execute(update(self.model).where(self.model.id == pk).values(**update_data))
        return result.rowcount

    async def delete_(self, db: AsyncSession, pk: int, *, del_flag: int | None = None) -> int:
        """
        Delete a piece of data by primary key id

        :param db:
        :param pk:
        :param del_flag:
        :return:
        """
        if del_flag is None:
            result = await db.execute(delete(self.model).where(self.model.id == pk))
        else:
            assert del_flag == 1, 'Delete error, del_flag parameter can only be 1'
            result = await db.execute(update(self.model).where(self.model.id == pk).values(del_flag=del_flag))
        return result.rowcount
