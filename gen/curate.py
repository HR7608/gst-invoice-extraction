from curatorkit import Curator, CuratorConfig

result = Curator(CuratorConfig(
    dataset="/home/hr768/ps5/data/train_alpaca.jsonl",
    dedup="minhash",
    clean=True,
    export_formats=["alpaca"],
    output_dir="/home/hr768/ps5/curated",
)).run()

result.print_summary()
