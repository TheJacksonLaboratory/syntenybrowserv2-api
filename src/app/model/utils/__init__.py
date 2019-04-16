from psycopg2 import ProgrammingError as Psycopg2ProgrammingError
from sqlalchemy.exc import ProgrammingError as SqlalchemyProgrammingError
from math import ceil

# Table specific inits
from ..curation_levels_model import populate_curation_level


def init(session, engine, echo_version=False):
    if echo_version:
        print_db_version(engine)
    populate_curation_level(session)


def print_db_version(engine):
    db_ver = "1" if is_original_db(engine) else "2"
    print("\nConnected to database version {}.".format(db_ver))


def is_original_db(engine):
    """
    Check if the application is using the original database, or an sqlalchemy generated database.
    :param engine:
    :return:t
    """
    with engine.connect() as conn:
        try:
            query_results = conn.execute(
                """
                SELECT table_schema, privilege_type
                FROM   information_schema.table_privileges 
                WHERE  grantee = 'ode_remote';
                """
            )
            if query_results:
                schemas, privs = zip(*query_results)
                # Original db segregates into separate schemas, v2 does not
                original_db_schemas = not all((schema == 'public' for schema in schemas))

                # We should only be able to select on the original db, if that's not the case, exit.
                original_db_privs = all((priv == 'SELECT' for priv in privs))
                if original_db_schemas and not original_db_privs:
                    raise RuntimeError("Connected to original db, but not limited to read only")

                result = original_db_schemas
            else:
                result = False

        except (Psycopg2ProgrammingError, SqlalchemyProgrammingError):
            raise RuntimeError("Could not determine if connected to original or generated database")

    return result
