from backtester.cli import build_parser


def test_cli_parser_accepts_required_args():
    parser = build_parser()
    args = parser.parse_args(["--csv", "x.csv", "--strategy", "ma_crossover"])
    assert args.csv == "x.csv"
    assert args.strategy == "ma_crossover"
