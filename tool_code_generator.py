from typing import Dict, Any
from llama_index.core.tools import FunctionTool
from langchain_openai import ChatOpenAI
from llama_index.llms.langchain import LangChainLLM
from llama_index.llms.ollama import Ollama
from prompts import CODE_GENERATION_PROMPT

api_key = "本地模型 API"
base_url = "API 链接"


def create_code_generator_tool(
        model_name: str = "模型名XXX"
) -> FunctionTool:
    """创建代码生成工具"""

    def generate_python_code(
            task_description: str,
            user_id: str = "default",
            task_id: str = None,
            additional_context: str = ""
    ) -> str:
        """
        根据任务描述生成Python代码

        Args:
            task_description (str): 任务描述
            user_id (str): 用户ID
            task_id (str): 任务ID
            additional_context (str): 额外的上下文信息

        Returns:
            str: 生成的Python代码
        """
        # llm = Ollama(model=model_name, base_url="http://localhost:11434")
        llm = LangChainLLM(ChatOpenAI(model=model_name, openai_api_key=api_key, openai_api_base=base_url))

        prompt = f"""{CODE_GENERATION_PROMPT}

用户ID: {user_id}
任务ID: {task_id}
任务描述：{task_description}
额外上下文：{additional_context}

请直接返回代码，无需其他解释。
"""

        response = llm.complete(prompt)
        return response.text.strip()

    return FunctionTool.from_defaults(
        fn=generate_python_code,
        name="code_generator",
        description="根据任务描述生成Python代码的工具。需要提供user_id和task_id，返回可执行的Python代码字符串。"
    )
