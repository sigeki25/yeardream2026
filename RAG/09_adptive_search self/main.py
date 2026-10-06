import os

from dotenv import load_dotenv
from langgraph.constants import END

from node_func import get_state, init_answer, router, rag, web, plain, last_answer, init_data

load_dotenv()  # .env 불러오기
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

insert_data("data/")

wf = get_state()

wf.add_node("init_data", init_data)
wf.add_node("init_answer", init_answer)
wf.add_node("router", router)
wf.add_node("rag", rag)
wf.add_node("web", web)
wf.add_node("plain", plain)
wf.add_node("last_answer", last_answer)

wf.set_entry_point("init_data")
wf.add_edge("init_data", "init_answer")
wf.add_conditional_edges(
    "init_answer",
    router,
    {
        "plain": "plain",
        "rag": "rag",
        "web": "web"
    }
)
wf.add_edge("plain", "last_answer")
wf.add_edge("rag", "last_answer")
wf.add_edge("web", "last_answer")
wf.add_edge("last_answer", END)
