from typing import Any, Sequence

from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase


class AsyncBaseRepo[M: DeclarativeBase]:
    '''
    Base repository for asynchronous operations with SQLAlchemy models.
    
    How to use: 
    ```python 
    from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
    
    engine = create_async_engine(url)
    async_session = async_sessionmaker(engine)
    
    class UserRepo(AsyncBaseRepo[MyAlchemyModel]):
        model = UserModel
        
    class Repository(AsyncBaseRepoFactory):
        session = SessionLocal
        user: UserRepo
    ```
    '''
    model: type[M]

    def __init__(self, session: AsyncSession):
        self.session = session

    def add_by_model(self, model: M) -> None:
        ''' 
        Add model and return None.
        
        Example: 
        ```python
        async with Repository() as repo: 
            my_model = MyModel(**some_data)
            repo.user.add_by_model(my_model)
        ```
        :param model: An instance of the SQLAlchemy model to be added.
        :return: None
        '''
        self.session.add(model)
    
    async def add_by_kwargs(self, **kwargs: Any) -> M:
        ''' Add an item and return the SQLAlchemy model instance.
        
        :param kwargs: Fields and values for the new record.
        :return: The newly added SQLAlchemy model instance.
        
        Example: 
        
        ```python
        # add new user: 
        async with Repository() as repo: 
            repo.user.add(name="Ivan", surname="Ivanov")
        ```
        '''
        stmt = insert(self.model)\
            .values(**kwargs)\
            .returning(self.model)  # type: ignore
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def delete(self, **by_filter: Any) -> None:
        '''Delete records based on filter criteria.
        
        :param by_filter: Filter criteria as keyword arguments.
        :return: Number of rows deleted.
        
        Example:
        ```python
        async with Repository() as repo:
            # Delete user with id=5
            await repo.user.delete(id=5)
            # Delete users where name="Ivan"
            await repo.user.delete(name="Ivan")
        ```
        '''
        stmt = delete(self.model).filter_by(**by_filter)
        await self.session.execute(stmt)

    async def update_by_id(self, id: int, **new_values: Any) -> M | None:
        '''
        Update values by id.
        
        :param id: The ID of the record to update.
        :param new_values: Fields and new values for the record.
        :return: The updated SQLAlchemy model instance or None if not found.
        
        Example:
        ```python
        async with Repository() as repo:
            await repo.user.update_by_id(id=5, name="Ivan")
        ```
        '''
        stmt = update(self.model)\
            .values(**new_values)\
            .where(self.model.id == id).returning(self.model) # type: ignore  
        item = await self.session.execute(stmt)
        return item.scalar_one_or_none()

    async def get_one_or_none(self, **by_filter: Any) -> M | None:
        '''
        Get a single record based on filter criteria.
        
        :param by_filter: Filter criteria as keyword arguments.
        :return: The SQLAlchemy model instance or None if not found.
        
        Example:
        ```python
        async with Repository() as repo:
            user = await repo.user.get_one_or_none(id=3)
        # >> None
        ```
        Note: Be careful when using filters that couldn't return multiple rows.
        '''
        stmt = select(self.model).filter_by(**by_filter)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_many(self,
                       limit: int | None = None,
                       offset: int | None = None,
                       **by_filter: Any) -> Sequence[M]:
        '''
        Get multiple records based on filter criteria.
        
        :param limit: Maximum number of records to return.
        :param offset: Number of records to skip.
        :param by_filter: Filter criteria as keyword arguments.
        :return: A sequence of SQLAlchemy model instances.
        
        Example:
        ```python
        async with Repository() as repo:
            users = await repo.user.get_many(role="moderator")
        ```
        '''
        stmt = select(self.model)\
            .filter_by(**by_filter)\
            .limit(limit)\
            .offset(offset)
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def count(self, **filter_by: Any) -> int:
        '''
        Get the count of rows in the table based on filter criteria.
        
        :param filter_by: Filter criteria as keyword arguments.
        :return: The number of rows that match the filter criteria.
        
        Example:
        ```python
        async with Repository() as repo:
            # Count documents where role="admin"
            count = await repo.user.count(role="admin")
            # Count all documents in the table
            total_count = await repo.user.count()
        ```
        '''
        stmt = select(func.count()).select_from(self.model).filter_by(**filter_by)
        result = await self.session.execute(stmt)
        return result.scalar_one()