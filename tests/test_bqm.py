from click.testing import CliRunner

from bqm.cli import cli


def test_version():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert result.output.startswith("cli, version ")


def test_tables(snapshot):
    runner = CliRunner()

    with runner.isolated_filesystem():
        # need to mock the bq request when using auto_load
        result = runner.invoke(
            cli,
            [
                "tables",
                "--project",
                "project",
                "--dataset",
                "dataset",
                "--select",
                "creation_time_tz",
                "--orderby",
                "days_since_creation desc",
                "-o",
                "size_bytes asc",
                "--dryrun",
            ],
        )

        assert result.exit_code == 0
        assert result.output == snapshot


def test_views(snapshot):
    runner = CliRunner()

    with runner.isolated_filesystem():
        # views command will not auto_load meaning will not request to bq so useful for unit test
        result = runner.invoke(
            cli,
            [
                "views",
                "--project",
                "project",
                "--dataset",
                "dataset",
                "--select",
                "TABLE_SCHeMA,view_definition",
                "--orderby",
                "table_scheMa dEsc",
                "-o",
                "table_catalog aSC",
                "--dryrun",
            ],
        )

        assert result.exit_code == 0
        assert result.output == snapshot
