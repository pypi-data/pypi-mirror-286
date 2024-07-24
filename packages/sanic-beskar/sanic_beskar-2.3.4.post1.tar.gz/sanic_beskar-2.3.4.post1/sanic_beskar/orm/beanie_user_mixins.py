from typing import Optional

from beanie import Document
from bson.objectid import ObjectId


class BeanieUserMixin(Document):
    """
    A short-cut providing required methods and attributes for a user class
    implemented with `tortoise-orm <https://tortoise.github.io/>`_. Makes
    many assumptions about how the class is defined.

    ASSUMPTIONS:

    * The model has an ``id`` column that uniquely identifies each instance
    * The model has a ``roles`` column that contains the roles for the
      user instance as a comma separated list of roles
    * The model has a ``username`` column that is a unique string for each instance
    * The model has a ``password`` column that contains its hashed password

    """

    @property
    def identity(self) -> str:
        """
        *Required Attribute or Property*

        sanic-beskar requires that the user class has an :py:meth:`identity`
        instance attribute or property that provides the unique id of the user
        instance

        :returns: Provided :py:class:`User.id`
        :rtype: str
        """
        return str(self.id)

    @property
    def rolenames(self) -> list:
        """
        *Required Attribute or Property*

        sanic-beskaruires that the user class has a
        :py:attr:`rolenames` instance attribute or property that
        provides a list of strings that describe the roles attached to
        the user instance.

        This can be a separate table (probably sane), so long as this attribute
        or property properly returns the associated values for the user as a
        RBAC dict, as:
        {'rolename', ['permissions'],}

        :returns: Provided :py:class:`User`'s current ``roles``
        :rtype: list
        """

        _roles: list = self.roles.split(",") if self.roles else []
        return _roles

    @classmethod
    async def lookup(
        cls, username: Optional[str] = None, email: Optional[str] = None
    ) -> Optional[Document]:
        """
        *Required Method*

        sanic-beskar requires that the user class implements a :py:meth:`lookup()`
        class method that takes a single :py:data:`username` or :py:data:`email`
        argument and returns a user instance if there is one that matches or
        ``None`` if there is not.

        :param username: `username` of the user to lookup
        :type username: Optional[str]
        :param email: `email` of the user to lookup
        :type email: Optional[str]

        :returns: ``None`` or :py:class:`User` of the found user
        :rtype: :py:class:`User`
        """
        if username:
            return await cls.find({"username": username}).first_or_none()
        if email:
            return await cls.find({"email": email}).first_or_none()

        return None

    @classmethod
    async def identify(cls, id: str) -> Optional[Document]:
        """
        *Required Attribute or Property*

        sanic-beskar requires that the user class implements an
        :py:meth:`identify()` class method that takes a single
        :py:data:`id` argument and returns user instance if
        there is one that matches or ``None`` if there is not.

        :param self: a :py:class:`User` object
        :type self: :py:class:`User`

        :returns: Provided :py:class:`User` ``id``
        :rtype: str, None
        """
        return await cls.find({"_id": ObjectId(id)}).first_or_none()
