"""
When setting up a Docker in Snowflake Container Services
we discovered that Snowflake doesn't like using an RSA key for authentication.
Instead, Snowflake Containers make stuff available via the os environment variables
"""
import os
import functools
from snowflake.connector import connect
from sqlalchemy import create_engine


def get_container_login_token():
    with open('/snowflake/session/token', 'r') as f:
        return f.read()


def get_container_connection():
    return connect(
        host=os.getenv('SNOWFLAKE_HOST'),
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        token=get_container_login_token(),
        authenticator='oauth'
    )


def snowflake_container_sql_engine():
    """ Connection to Snowflake via the SQL Alchemy Engine Method. """
    return create_engine("snowflake://not@used/db", creator=get_container_connection)


def container_connect_decorator(func):
    """
    Snowflake Container Service Connection Wrapper

    Designed to wrap around snowflake_connect when we may use a Snowflake Container Service Connection.
    Point is to check the os.environ to see if we are in a container service.
    If we are then run a specialist container functions rather than the original function.
    """

    # the extra decorator means we can still use help etc.
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # we know if we are in a Snowflake container if 'SNOWFLAKE_HOST' in the os.environ
        if 'SNOWFLAKE_HOST' in os.environ.keys():
            return get_container_connection().raw_connection()
        else:
            return func(*args, **kwargs)

    return wrapper


def container_engine_decorator(func):
    """
    Snowflake Container Service Engine Wrapper

    Designed to wrap around snowflake_sql_engine when we may use a Snowflake Container Service Connection.
    Point is to check the os.environ to see if we are in a container service.
    If we are then run a specialist container functions rather than the original function.
    """

    # the extra decorator means we can still use help etc.
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # we know if we are in a Snowflake container if 'SNOWFLAKE_HOST' in the os.environ
        if 'SNOWFLAKE_HOST' in os.environ.keys():
            return snowflake_container_sql_engine().raw_connection()
        else:
            return func(*args, **kwargs)

    return wrapper
