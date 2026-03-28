# Results Directory

This folder stores generated verification artifacts for the firmware regression flow.

## Structure

- `latest/summary.md`: human-readable latest suite summary
- `latest/summary.json`: machine-readable latest suite summary
- `latest/*.log`: per-test simulator console output
- `latest/*.hex`: generated machine-code image used for each test
- `latest/*.vcd`: waveform dump captured for each test

The contents of `latest/` are regenerated when `run_firmware_suite.py` is run.

## License

Generated results are stored alongside a project released under the MIT License. See [`LICENSE`](/c:/Users/moham/OneDrive/Desktop/Projects/RISCV_Project/RISCV_PipelineCore/LICENSE).
