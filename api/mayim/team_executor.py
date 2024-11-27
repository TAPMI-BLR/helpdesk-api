from mayim import PostgresExecutor


class TeamExecutor(PostgresExecutor):
    generic_prefix = ""
    path = "./queries/teams/"
