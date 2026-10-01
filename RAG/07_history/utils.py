import contextlib
import io


def retrieve_to_text(docs):
    text = ""
    for doc in docs:
        text += doc.page_content + "\n"
    return text

def python_code_parser(text: str):
    # 대답중에서 ```python 으로 감싸진 부분만 받아오는 함수
    # ```python -> ``` -> [```,code내용,```]
    code_list = text.replace("```python", "```").strip().split("```")

    # ``` 이 없어서 끊지 못한경우 코드를 그대로 내보낸다.
    if len(code_list) == 1:
        return code_list[0]
    return code_list[1]

def run_code(df_name: str, df, input_code: str):
    output = io.StringIO()

    try:
        with contextlib.redirect_stdout(output):
            exec(input_code, {df_name: df})
    except Exception as e:
        print(f"Error : {e}", file=output)
    return output.getvalue()