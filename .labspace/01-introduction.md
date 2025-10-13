# Fine tuning models

👋 Welcome to the **Fine tunning models** lab! During this lab, you will learn to do the following:

- Use Docker Offload to fine tune a model
- Package and share the model on Docker Hub
- Run the custom model with Docker Model Runner



## ☑️ Your lab goal

During this lab, you are going to create a fine-tuned model that will detect and redact PII information.

For example, given the following input:

```plaintext no-copy-button
This is an example of text that contains some data. 
The author of this text is Ignacio López Luna, but everybody calls him Ignasi. 
His ID number is 123456789. 
He has a son named Arnau López, who was born on 21-07-2021.
```

The model will present the following output:

```plaintext no-copy-button
This is an example of text that contains some data. 
The author of this text is [MASKED] [MASKED], but everybody calls him [MASKED]. 
His ID number is [MASKED]. 
He has a son named [MASKED], who was born on [MASKED].
```



## 🙋 What is fine-tuning again?

With the increased accessibility of language models, the desire to build specialized and meaningful applications has grown. However, many of these models are trained for general use cases and providing enough context to obtain satisfactory responses.

The process of fine-tuning a model teaches an existing AI model to perform better on a specific task or to behave in a particular way by training it on new examples. The process generally looks like the following:

1. 🧠 **Choose a base model.** Pick a model that already understands the language, images, or code in a general sense.
2. 📋 **Collect a training set.** Gather samples of input and desire output demonstrating how you want the model to behave.
3. 📚 **Train the model.** Use the data to adjust the model's internal weights.
4. 🧪 **Validate and test.** Test the model on new examples to check for undesired behavior.
5. 📦 **Package and deploy.** Package the newly created model and deploy it for broader usage.

