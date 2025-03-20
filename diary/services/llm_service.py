import os
from langchain_core.prompts import PromptTemplate
from langchain_community.llms.huggingface_hub import HuggingFaceHub
from langchain.chains import LLMChain
from huggingface_hub.utils import HfHubHTTPError

def extract_insights(response):
    """
    Extract the insights portion from the LLM's response.
    If the response contains the marker "Insights:", return only the text after it.
    Otherwise, return the full response.
    """
    marker = "Insights:"
    if marker in response:
        # Split on the marker and take the text after it.
        return response.split(marker, 1)[1].strip()
    else:
        return response.strip()

def get_insights_from_notes(notes):
    """
    Constructs a prompt from a set of notes and uses LangChain to call an LLM
    to generate a clear, human-readable message with insights and actionable suggestions.
    This version includes post-processing to return only the insights portion.
    """
    prompt_template = (
        """
        Você é um assistente pessoal que ajuda a organizar e melhorar as anotações de um usuário.
        Analise as seguintes anotações e forneça um resumo claro e conciso, com pelo menos um insight ou sugestão prática 
        sobre como organizar melhor e aprimorar as anotações. Sua resposta deve ser amigável e em linguagem simples.
        
        Anotações:
        {notes}
        
        Insights:
        """
    )
    
    # Combine notes into a single string.
    notes_str = ""
    for note in notes:
        notes_str += f"Title: {note.title}\nContent: {note.content}\n\n"
    
    # Create a prompt template instance.
    prompt = PromptTemplate(input_variables=["notes"], template=prompt_template)
    
    # Retrieve the Hugging Face API token.
    hf_api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    if not hf_api_token:
        raise ValueError(
            "Did not find huggingfacehub_api_token. Please set the environment variable "
            "`HUGGINGFACEHUB_API_TOKEN` with your Hugging Face API token."
        )
    
    # Initialize the LLM via LangChain's HuggingFaceHub integration.
    llm = HuggingFaceHub(
        repo_id="tiiuae/falcon-7b-instruct",  # You can change this to another model if desired.
        huggingfacehub_api_token=hf_api_token,
        model_kwargs={"temperature": 0.7, "max_length": 512, "do_sample": True}
    )
    
    # Create an LLM chain with the prompt template.
    chain = LLMChain(llm=llm, prompt=prompt)

    try:
        insights_text = chain.run(notes=notes_str)
    except HfHubHTTPError:
        # Handle errors gracefully.
        insights_text = (
            "Sorry, the LLM service is currently unavailable. "
            "Please try again later."
        )

    # Post-process the output to extract only the insights.
    processed_insights = extract_insights(insights_text)
    
    # Format the output as a human-readable message.
    formatted_message = f"Insights from your indexed notes:\n\n{processed_insights}"
    return formatted_message

# Example usage:
if __name__ == "__main__":
    # Dummy note class for demonstration purposes.
    class Note:
        def __init__(self, title, content):
            self.title = title
            self.content = content

    # Sample notes list.
    sample_notes = [
        Note("Meeting with Team", "Discussed project deadlines and resource allocation."),
        Note("Personal Reflection", "Felt overwhelmed by the number of tasks; need to prioritize.")
    ]

    result = get_insights_from_notes(sample_notes)
    print(result)
