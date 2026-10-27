from crapper.discover import iter_source_files, language_of
from crapper.languages.sql import functions_in_source

MODEL = """{{ config(materialized='view') }}
with orders as (
    select * from {{ ref('raw') }} where amount > 0 and status = 'ok'
)
select * from orders
"""


def test_a_model_scores_each_cte_and_its_final_select():
    found = functions_in_source(MODEL, "models/stg/orders.sql")
    assert [(f.namespace, f.name, f.complexity, f.start_line, f.end_line) for f in found] == [
        ("orders", "orders", 3, 2, 4),
        ("orders", "main", 1, 5, 5),
    ]
    assert MODEL.encode()[found[1].start_byte : found[1].end_byte] == b"select * from orders"


def test_sql_files_are_found_but_not_in_dbt_packages(tmp_path):
    (tmp_path / "models").mkdir()
    (tmp_path / "models" / "a.sql").write_text("select 1")
    (tmp_path / "dbt_packages" / "dbt_utils").mkdir(parents=True)
    (tmp_path / "dbt_packages" / "dbt_utils" / "b.sql").write_text("select 1")
    (tmp_path / "logs").mkdir()
    (tmp_path / "logs" / "query_log.sql").write_text("select 1")
    assert language_of("models/a.sql") == "sql"
    assert [path.name for path in iter_source_files([tmp_path])] == ["a.sql"]
