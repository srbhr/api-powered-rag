from langchain_community.document_loaders import PyPDFLoader
from langchain_ollama import ChatOllama
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate


def summarize_pdf(pdf_file_path: str, model_name: str = "llama3"):
    """
    Extracts text from a PDF and uses a local Ollama model to generate a detailed summary.
    """
    try:
        llm = ChatOllama(model=model_name, temperature=0)

        prompt_template = """Write a concise summary of the following text.
        Aim for a summary that is about 4-5 sentences long.
        After the summary, provide 2-3 key takeaways as bullet points.

        Text:
        "{text}"

        CONCISE SUMMARY AND KEY TAKEAWAYS:"""

        PROMPT = PromptTemplate(template=prompt_template, input_variables=["text"])
        loader = PyPDFLoader(pdf_file_path)
        docs = loader.load()
        chain = load_summarize_chain(
            llm, chain_type="map_reduce", map_prompt=PROMPT, combine_prompt=PROMPT
        )
        summary_result = chain.invoke(docs)

        return summary_result["output_text"]

    except FileNotFoundError:
        return f"Error: The file was not found at {pdf_file_path}"
    except Exception as e:
        return f"An error occurred during summarization: {e}. Please ensure Ollama is running and the PDF file is valid."
