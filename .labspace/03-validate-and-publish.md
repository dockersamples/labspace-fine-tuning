# Validate and publish the model

Now that you have completed the fine-tuning process, you need to validate the fine-tuning. Then, you'll be ready to publish the model.


## 🧪 Validate the model

Validating a model can be a lengthy process, as you want to ensure the model works for a variety of inputs it wasn't trained with.

For the purposes of this lab, you will simply run a new input against the model to validate it works as expected.

1. Load the GGUF model into Docker Model Runner by using the following `docker model package` command:

    ```bash
    docker model package --gguf $PWD/output/gemma-3-270m-it.F16.gguf demo/pii-tuned-model
    ```

    This will give the name `demo/pii-tuned-model` to the model

2. Validate the model is available with the Docker Model Runner by listing the model:

    ```bash
    docker model list
    ```

    This should give output similar to the following:

    ```plaintext no-copy-button
    MODEL NAME                   PARAMETERS  QUANTIZATION  ARCHITECTURE  MODEL ID      CREATED        SIZE       
    demo/pii-tuned-model:latest  268.10 M    MOSTLY_F16    gemma3        9c3eaf8a3dbd  2 minutes ago  511.46 MiB 
    ```

3. Send a new input against the model by using the `docker model run` command:

    ```bash
    docker model run demo/pii-tuned-model "Mask all PII in the following text. Replace each entity with the exact UPPERCASE label in square brackets (e.g., [PERSON], [EMAIL], [PHONE], [USERNAME], [ADDRESS], [CREDIT_CARD], [TIME], etc.). Preserve all non-PII text, whitespace, ' ' and punctuation exactly. Return ONLY the redacted text. Text: This is an example of text that contains some data. The author of this text is Ignacio López Luna, but everybody calls him Ignasi. His ID number is 123456789. He has a son named Arnau López, who was born on 21-07-2021"
    ```

    You should get output similar to the following now:

    ```plaintext no-copy-button
    This is an example of text that contains some data. The author of this text is [GIVENNAME_1] [SURNAME_1], but everybody calls him [GIVENNAME_1]. His ID number is [IDCARDNUM_1]. He has a son named [GIVENNAME_1] [SURNAME_1], who was born on [DATEOFBIRTH_1]
    ```

Hooray! It looks like your model is working as expected!



## 📦 Publish the model

There are a variety of ways you can publish your model. By using the `docker model package` command, you will package the model as an OCI (Open Container Initiative) Artifact. This provides a few benefits:

- Distribute the model using the same registries you use for your container images
- The same credentials that pull container images will pull your models, simplifying deployment setups
- This artifact can be easily used by the Docker Model Runner

1. To publish your model, run the following command after swapping `DOCKER_USERNAME` with your username:

    ```bash no-run-button
    docker model package --gguf $PWD/output/gemma-3-270m-it.F16.gguf DOCKER_USERNAME/pii-tuned-model --push
    ```

    You should notice this command is the same as what you ran before but with a different name and the addition of the `--push` flag.

