import os
from langchain import PromptTemplate, LLMChain
from langchain.llms import HuggingFaceHub

def get_insights_from_notes(notes):
    """
    Constructs a prompt from the given notes and uses LangChain to call a free LLM endpoint
    to provide insights and suggestions on organizing and improving the user's notes.
    
    The prompt is predefined as a "personal assistant" that analyzes the notes and returns
    a summary with insights and suggestions.
    
    Args:
        notes (QuerySet or list): A collection of Note objects.
    
    Returns:
        str: Insights generated by the LLM.
    
    Raises:
        ValueError: If the HUGGINGFACEHUB_API_TOKEN environment variable is not set.
    """
    # Define the prompt template for our personal assistant.
    prompt_template = (
        "You are a personal assistant that helps organize and provide insights about a user's notes. "
        "Analyze the following notes and provide a summary with insights and suggestions on how to organize "
        "and improve them:\n\n"
        "{notes}\n"
        "Please provide your insights."
    )

    # Combine notes into a single string.
    notes_str = ""
    for note in notes:
        notes_str += f"Title: {note.title}\nContent: {note.content}\n\n"

    # Create a prompt template.
    prompt = PromptTemplate(
        input_variables=["notes"],
        template=prompt_template
    )

    # Retrieve the Hugging Face API token from the environment.
    hf_api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    if not hf_api_token:
        raise ValueError(
            "Did not find huggingfacehub_api_token. Please set the environment variable "
            "`HUGGINGFACEHUB_API_TOKEN` with your Hugging Face API token."
        )

    # Initialize the LLM via LangChain's HuggingFaceHub integration.
    llm = HuggingFaceHub(
        repo_id="gpt2",
        huggingfacehub_api_token=hf_api_token,
        model_kwargs={"temperature": 0.7}
    )

    # Create an LLM chain with the prompt template.
    chain = LLMChain(llm=llm, prompt=prompt)

    # Run the chain using the combined notes string.
    insights = chain.run(notes=notes_str)
    return insights
