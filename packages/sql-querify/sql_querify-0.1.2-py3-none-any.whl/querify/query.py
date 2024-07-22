import colorama
import tabulate
import typing
import sys
import sql_metadata

from . import database
from . import exceptions
from . import sources


def query(
    query=None,
):
    if query is None:
        raise exceptions.ValidationError('Missing query')

    query = query.lower()

    try:
        if trimed(query) == trimed('show tables'):
            return display(
                columns=[
                    'table_name',
                ],
                rows=[
                    (
                        source_name,
                    )
                    for source_name in sources.sources
                ],
            )

        if is_describe_table_query(
            query=query,
        ):
            _, source_name = query.split(' ')

            return describe_source(
                source=sources.get_source_by_name(
                    source_name=source_name,
                )
            )

        parsed_query = sql_metadata.Parser(query)
        source = sources.get_source_by_name(
            source_name=parsed_query.tables[0],
        )

        with database.client.DB() as db:
            db.create_source_table(
                source=source,
            )

            db.insert_source_data(
                source=source,
            )

            columns, rows = db.query(
                query=query,
            )

            display(
                columns=columns,
                rows=rows,
            )
    except Exception as exception:
        raise exceptions.QuerifyError(str(exception))


def is_describe_table_query(
    query: str,
) -> bool:
    if query.startswith('desc'):
        describe, _ = query.split(' ')

        return any(
            describe == valid_describe
            for valid_describe in (
                'desc',
                'describe',
            )
        )

    return False


def describe_source(
    source: sources.base_source.BaseSource,
):
    source_fields = [
        (
            field,
            field_type.__name__,
        )
        for field, field_type in typing.get_type_hints(source.model).items()
    ]

    display(
        columns=[
            'field_name',
            'data_type',
        ],
        rows=source_fields,
    )


def display(
    columns: list[str],
    rows: list[typing.Any],
):
    print(
        tabulate.tabulate(
            rows,
            [
                colorama.Style.BRIGHT +
                f'{column}' +
                colorama.Style.RESET_ALL
                for column
                in columns
            ],
            tablefmt='psql',
        )
    )


def trimed(
    x: str,
) -> str:
    return x.replace(' ', '')


def main():
    query(*sys.argv[1:])


if __name__ == '__main__':
    main()
