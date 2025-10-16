# Labspace - Fine tuning

This Labspace provides a hands-on walkthrough on fine-tuning models using Docker Offload, Docker Model Runner, and Unsloth.

## Learning objectives

This Labspace will teach you the following:

- Use Docker Offload to fine tune a model
- Package and share the model on Docker Hub
- Run the custom model with Docker Model Runner

## Launch the Labspace

To launch the Labspace, run the following command:

```bash
docker compose -f oci://dockersamples/labspace-fine-tuning up -d
```

And then open your browser to http://localhost:3030.

### Using the Docker Desktop extension

If you have the Labspace extension installed (`docker extension install dockersamples/labspace-extension` if not), you can also click [this link](https://open.docker.com/dashboard/extension-tab?extensionId=dockersamples/labspace-extension&location=dockersamples/labspace-fine-tuning&title=Fine-tuning%20local%20models) to launch the Labspace.


## Acknowledgements

This repository contains an example of fine-tuning a language model for PII (Personally Identifiable Information) masking using the Unsloth framework.

Special thanks to AI4Privacy for providing the comprehensive PII masking dataset that makes this fine-tuning example possible.

### Dataset Source

The training dataset `data/training_data.json` used in this example was created from the **AI4Privacy PII Masking 400k Dataset**:

- **Original Dataset**: [ai4privacy/pii-masking-400k](https://huggingface.co/datasets/ai4privacy/pii-masking-400k)
- **Dataset Description**: World's largest open dataset for privacy masking with 406,896 entries
- **Languages Supported**: English, Italian, French, German, Dutch, Spanish
- **PII Classes**: 17 different types of PII in the public dataset

### Licensing and Attribution

#### Important License Notice

The original dataset is provided by AI4Privacy under a custom license with the following requirements:

- **Academic Use**: Encouraged with proper citation
- **Commercial Use**: Requires licensing from AI4Privacy
  - Contact: licensing@ai4privacy.com
- **Attribution**: This project uses data derived from the ai4privacy/pii-masking-400k dataset

#### Citation

If you use this dataset or derivatives in academic work, please cite:
```
@dataset{ai4privacy_pii_masking_400k,
  title={PII Masking 400k Dataset},
  author={AI4Privacy},
  year={2024},
  publisher={Hugging Face},
  url={https://huggingface.co/datasets/ai4privacy/pii-masking-400k}
}
```

### Data Preparation Process

The dataset was prepared using the `prepare_pii_masking_for_unsloth.py` script, which:

1. **Loads the original dataset** from HuggingFace: `ai4privacy/pii-masking-400k`
2. **Transforms the data** into a format suitable for fine-tuning with Unsloth
3. **Creates instruction-following pairs** with two modes:
   - **Redaction mode**: Maps source text to masked text with PII labels
   - **Spans mode**: Extracts PII spans with their positions and labels

#### Using the Data Preparation Script

```bash
# Basic usage - creates redaction mode dataset
python prepare_pii_masking_for_unsloth.py --outdir data_out

# Filter by languages (e.g., English and Spanish)
python prepare_pii_masking_for_unsloth.py --langs en es --outdir data_out_en_es

# Filter by locales (e.g., US and GB)
python prepare_pii_masking_for_unsloth.py --locales US GB --outdir data_out_us_gb

# Use spans mode instead of redaction
python prepare_pii_masking_for_unsloth.py --mode spans --outdir spans_out

# Add custom EOS token
python prepare_pii_masking_for_unsloth.py --outdir data_out --eos "</s>"

# Sample a subset for testing
python prepare_pii_masking_for_unsloth.py --outdir data_out --sample_train 1000 --sample_val 200
```

### Fine-Tuning Process

The `finetune.py` script demonstrates how to:

1. Load a pre-trained model (Gemma-3-270M-IT)
2. Prepare the dataset for instruction fine-tuning
3. Configure LoRA adapters for efficient training
4. Train the model using the SFTTrainer from TRL
5. Save the fine-tuned model

