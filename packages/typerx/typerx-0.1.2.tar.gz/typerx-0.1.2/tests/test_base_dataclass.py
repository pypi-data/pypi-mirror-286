from typer.testing import CliRunner
import typer

runner = CliRunner()


def test_app():
    from examples.base_dataclass import main
    app = typer.Typer()
    app.command()(main)
    result = runner.invoke(app, ["--data.hi", "2", "--data.ho", "2"])
    assert result.exit_code == 0
    assert result.output == "Data(hi=2, ho='2')\n"
