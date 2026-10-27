"""dbt SQL units and cyclomatic complexity, read through dbtsql.

A model's units are its top-level CTEs and the final select, `main`. A macro
file's units are its macros. The namespace is the file name, which dbt keeps
unique per project. Jinja is masked first; its `if`, `elif`, `for`, `and`, and
`or` count as decisions alongside the SQL ones.
"""

from crapper.model import Function


def functions_in_source(
    source: str, path: str, source_root: str | None = None
) -> list[Function]:
    from dbtsql.units import namespace, units

    found: list[Function] = []
    for unit in units(source):
        found.append(
            Function(
                name=unit.name,
                namespace=namespace(path),
                complexity=unit.complexity,
                start_line=unit.start_line,
                end_line=unit.end_line,
                path=path,
                language="sql",
                start_byte=len(source[: unit.start].encode("utf-8")),
                end_byte=len(source[: unit.end].encode("utf-8")),
            )
        )
    return found
