# Labspace starter

This repository is intended to server as a template to help bootstrap a new Labspace.

## Instructions

1. Create a new repository using this repo as the template ([docs here](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template)).

    **NOTE:** After creating the repo, a GHA workflow will run to do some additional bootstrapping. The bootstrapping workflow file will be removed during bootstrapping.

2. Clone your newly created repo to your local machine

3. Start the local development mode:

    ```bash
    # On Mac/Linux
    CONTENT_PATH=$PWD docker compose -f oci://dockersamples/labspace-content-dev -f .labspace/compose.override.yaml up

    # On Windows with PowerShell
    $Env:CONTENT_PATH = (Get-Location).Path; docker compose -f oci://dockersamples/labspace-content-dev -f .labspace/compose.override.yaml up
    ```

4. Update the `labspace.yaml` with your Labspace's title and description

5. Write your Labspace! Being in dev mode, your changes should be visible in the interface without a restart. Feel free to edit either on your host machine or in the Labspace itself!

    Add any supporting application files or resources directly into the Labspace. This repo will be cloned into the Labspace at startup.

    Be sure to check out the [docs](https://github.com/dockersamples/labspace-infra/tree/main/docs) for additional information and guidelines.



### Setting up the deployment pipeline

The template repo contains a workflow file to make it easy to publish your Labspace.

1. Add GitHub Action Secrets in your new repo for the following:

    - `DOCKERHUB_USERNAME` - the username to authenticate to Docker Hub with
    - `DOCKERHUB_TOKEN` - a personal or organization access token to use for authentication

2. In the `.github/workflows/publish-labspace.yaml.temp` file, update the `DOCKERHUB_REPO` with the name of the Docker Hub repo you want to publish to.

3. Rename the workflow file to remove the `.temp` extension.

    ```bash
    mv .github/workflows/publish-labspace.yaml.temp .github/workflows/publish-labspace.yaml
    ```

## Acknowledgements

This repository contains an example of fine-tuning a language model for PII (Personally Identifiable Information) masking using the Unsloth framework.

Special thanks to AI4Privacy for providing the comprehensive PII masking dataset that makes this fine-tuning example possible.

### Dataset Source

The training dataset `pii_redaction_train.json` used in this example was created from the **AI4Privacy PII Masking 400k Dataset**:

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

