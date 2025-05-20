import typer
from typing import Optional,List
from phi.assistant import Assistant
from phi.storage.assistant.postgres import PgAssistantStorage
from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.vectordb.pgvector import PgVector2
from phi.embedder.sentence_transformer import SentenceTransformerEmbedder
from phi.model.groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")


db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"
#kb to take pdfurls convert to embeds and store in vectordb
# Load a local embedding model (no OpenAI)
embedder = SentenceTransformerEmbedder(
    model_name="all-MiniLM-L6-v2",
    dimensions=384   # model dims = 384
)
print(embedder.dimensions)

# Create vector DB connection
vector_db = PgVector2(collection="recipes_v2", db_url=db_url, embedder=embedder)

# Create knowledge base with custom embedder
knowledge_base = PDFUrlKnowledgeBase(
    urls=["https://phi-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
    vector_db=vector_db,
)
knowledge_base.load(recreate=True, upsert=True)
#this one is used for session storage, so that agent doesnt lose context
storage = PgAssistantStorage(table_name="pdf_assistant",db_url=db_url)

def pdf_assistant(new = False, user = "user"):
    run_id = None

    if not new:
        existing_run_ids = storage.get_all_run_ids(user)
        if len(existing_run_ids) > 0:
            run_id = existing_run_ids[0]

    assistant = Assistant(
        name = "Vector db assistant",
        llm= {"provider": "groq", "model": "llama3-70b-8192"},
        run_id=run_id,
        user_id = user,
        knowledge_base=knowledge_base,
        storage=storage,
        show_tool_calls= True,
        search_knowledge=True,
        read_chat_history=True,
        
    )
    if run_id is None:
        run_id = assistant.run_id
        print(f"Started Run: {run_id}\n")
    else:
        print(f"Continuing Run: {run_id}\n")

    assistant.cli_app(markdown=True, stream=False)

if __name__ == "__main__":
    typer.run(pdf_assistant)            