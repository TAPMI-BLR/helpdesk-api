from mayim import PostgresExecutor


class SLAExecutor(PostgresExecutor):
    generic_prefix = ""
    path = "./queries/SLAs/"
