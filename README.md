# AI ASSISTANT

This AI assistant is built using Langchain in python and the Cohere large language model(llm).
The model implements Retrieval-Augmented Generation (RAG) which is an advanced AI model architecture that combines two key components: retrieval and generation.

Retrieval: This part involves a large database of text documents or passages, often called a knowledge base. These documents contain vast amounts of information on various topics. RAG employs advanced algorithms to efficiently search through this knowledge base and retrieve relevant passages based on the input query.

Generation: Once relevant passages are retrieved, the generation component comes into play. This part of the model is responsible for understanding the query and synthesizing a response based on the retrieved information. It utilizes state-of-the-art language generation techniques, often based on transformer models like GPT (Generative Pre-trained Transformer), to produce coherent and contextually relevant answers.

However the movel is not conversational and doesnt have conversation memory, that can be added on later.

The Document used in this model is a [pdf](/media/Indie%20Bites%209%20PDF.pdf) which contains an interview with the writer Talli L. Morgan and other short fiction stories.
The AI assistant is succesfully able to answer questions as if it was the one being interviewed and it can also correctly recount events that occoured in the short fiction stories with high accuracy.

The live demo of this model can be found [here](https://aiassistants.site)
