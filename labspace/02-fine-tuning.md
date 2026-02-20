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

The :fileLink[data/training_data.json]{path="data/training_data.json"} file contains a large dataset of ~35k samples. These provide a very large sampling of the ways in which PII might be represented in text.

> [!TIP]
> Another valid use case for LLMs is to help generate these large datasets for training. You can craft prompts that can generate samples, after which you can validate the data and use it in fine-tuning



## 📚 Train the model

With a base model chosen and starting data, it's time to perform the actual fine-tuning.

The [`unsloth/unsloth`](https://hub.docker.com/r/unsloth/unsloth) container image provides all of the tools required in order to perform fine-tuning. It even provides a Jupyter Notebook interface to let you explore and experiment with your setup.

However, since you already have a data set and the fine-tuning code have been provided, you are going to write a Dockerfile that will perform the fine-tuning in a reproducible manner.

1. Create a file named `Dockerfile` with the following contents:

    ```dockerfile save-as=Dockerfile
    FROM unsloth/unsloth:stable

    # Install libcurl4-openssl-dev which is required by llama.cpp to save GGUF files and
    # update the unsloth libraries to bring in some fixes related to saving to GGUF files
    USER root
    RUN apt update && \
        apt install libcurl4-openssl-dev -y && \
        rm -rf /var/lib/apt/lists/*
    RUN pip install --upgrade unsloth-zoo && \
        pip install --upgrade unsloth

    WORKDIR /usr/local/app

    COPY --link finetune.py ./
    ENTRYPOINT [ ]
    CMD ["python", "finetune.py"]
    ```

2. Build the container image using the following command:

    ```bash
    docker build -t fine-tuning .
    ```

    It will likely take a few moments to download the base image and perform all the required updates.

3. Create a directory for the model output to be placed when completed:

    ```bash
    mkdir output
    ```

4. Start a container using the newly created image and mounting the `gguf_output` directory (where the script will put the final GGUF file):

    ```bash
    docker run -ti \
        --gpus all \
        -v ./output:/usr/local/app/gguf_output \
        -v ./data:/usr/local/app/data \
        fine-tuning
    ```

    You will see the fine-tuning process kick off, which may have moments where it appears the output has frozen. The full model training takes about 12 minutes to run.

5. Once the fine-tuning finishes, you should see the GGUF file in the `output` directory:

    ```bash
    ls output/
    ```

    You should see a file named `gemma-3-270m-it.F16.gguf`

Hooray! You now have a model!