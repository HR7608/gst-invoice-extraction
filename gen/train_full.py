from aligntune.core.backend_factory import create_sft_trainer

trainer = create_sft_trainer(
    model_name="Qwen/Qwen2.5-1.5B-Instruct",
    dataset_name="/home/hr768/ps5/data/train_alpaca.jsonl",
    backend="trl",
    output_dir="/home/hr768/ps5/out_full",
    num_epochs=1,
    batch_size=1,
    learning_rate=2e-4,
    max_seq_length=2048,
    max_samples=1000,
    use_peft=True,
    lora_r=16,
    lora_alpha=32,
    lora_target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                         "gate_proj", "up_proj", "down_proj"],
    quantization={"load_in_4bit": True},
)
trainer.train()
