# Fine-tuning a model

In this section, you're going to:

1. 🧠 **Choose a base model**
2. 📋 **Collect a training set**
3. 📚 **Train the model**

With that, let's get started!



## 🧠 Choosing a model

When choosing a base model, there are a few considerations to keep in mind:

- **General purpose versus domain-specific** - if your use case involves specialized domains (such as legal, medical, or engineering), starting with a model that is already exposes to that domain may reduce the amount of fine-tuning you need to perform
- **Modalities** - ensure the model both works with the input and output types (text, vision, code, audio, etc.) that you want to work with
- **Context length** - every model has limits on the amount of data they can process, so ensure your model fits your needs
- **Reasoning and tool-calling requirements** - only certain models support reasoning, tool calling, and other advanced capabilities
- **Licensing** - some models have restrictions on commercial usage

> [!NOTE]
> If you want to read more about considerations and additional insights, be sure to check out Unsloth's documentation on [What Model Should I Use?](https://docs.unsloth.ai/get-started/fine-tuning-llms-guide/what-model-should-i-use)

Using the criteria previously mentioned, your model's use case has the following needs:

- General purpose - no specific domains have been specified for this sample app
- Text-only modalities
- No context length has been specified
- No need for reasoning or tool calling

Based on this criterion, the [**Gemma3 270M model**](https://hub.docker.com/r/ai/gemma3) looks like a great choice.



## 📋 Collect a training set

In order to fine-tune a model, you need a large collection of sample inputs and desired outputs. What's this look like?

The following JSON snippet provides an example, where `prompt` captures the input and `response` captures the desired output:

```json
{
  "prompt": "Mask all PII in the following text. Replace each entity with the exact UPPERCASE label in square brackets (e.g., [PERSON], [EMAIL], [PHONE], [USERNAME], [ADDRESS], [CREDIT_CARD], [TIME], etc.). Preserve all non-PII text, whitespace, and punctuation exactly. Return ONLY the redacted text.\n\nText:\n<p>My child faozzsd379223 (DOB: May/58) will undergo treatment with Dr. faozzsd379223, office at Hill Road. Our ZIP code is 28170-6392. Consult policy M.UE.227995. Contact number: 0070.606.322.6244. Handle transactions with 6225427220412963. Queries? Email: faozzsd379223@outlook.com.</p>",
  "response": "<p>My child [USERNAME_2] (DOB: [DATEOFBIRTH_1]) will undergo treatment with Dr. [USERNAME_1], office at [STREET_1]. Our ZIP code is [ZIPCODE_1]. Consult policy M.UE.227995. Contact number: [TELEPHONENUM_1]. Handle transactions with [CREDITCARDNUMBER_1]. Queries? Email: [EMAIL_1].</p>"
},
```

The :fileLink[pii_redaction_train.json]{path="pii_redaction_train.json"} file contains a large dataset of ~35k samples. These provide a very large sampling of the ways in which PII might be represented in text.

> [!TIP]
> Another valid use case for LLMs is to help generate these large datasets for training. You can craft prompts that can generate samples, after which you can validate the data and use it in fine-tuning



## 📚 Train the model

With a base model chosen and starting data, it's time to perform the actual fine-tuning.

1. Start a container using the `unsloth/unsloth` container, giving it access to all available GPUs:

    ```bash
    docker run -dp 8888:8888 \
        --gpus all \
        -v ./:/workspace/work \
        --name unsloth \
        unsloth/unsloth
    ```

    This will likely take a moment to download as the image is a few GB in size.

2. Once the container has started, exec into the container by running the following command:

    ```bash
    docker exec -ti unsloth bash
    ```

3. Inside the container, run the following command to kick off the fine-tuning:

    ```bash
    python finetune.py
    ```