import importlib.util
import os
from typing import List, Optional, Type

import docker
from crewai_tools.tools.base_tool import BaseTool
from pydantic.v1 import BaseModel, Field


class CodeInterpreterSchema(BaseModel):
    """CodeInterpreterTool 的输入"""

    code: str = Field(
        ...,
        description="将在 Docker 容器中解释执行的 Python3 代码。始终打印最终结果和代码的输出",
    )

    libraries_used: List[str] = Field(
        ...,
        description="代码中使用的库列表，使用正确的安装名称，并用逗号分隔。示例：numpy,pandas,beautifulsoup4",
    )


class CodeInterpreterTool(BaseTool):
    name: str = "代码解释器"
    description: str = "解释带有最终打印语句的 Python3 代码字符串。"
    args_schema: Type[BaseModel] = CodeInterpreterSchema
    code: Optional[str] = None

    @staticmethod
    def _get_installed_package_path():
        spec = importlib.util.find_spec("crewai_tools")
        return os.path.dirname(spec.origin)

    def _verify_docker_image(self) -> None:
        """
        验证 Docker 镜像是否可用
        """
        image_tag = "code-interpreter:latest"
        client = docker.from_env()

        try:
            client.images.get(image_tag)

        except docker.errors.ImageNotFound:
            package_path = self._get_installed_package_path()
            dockerfile_path = os.path.join(package_path, "tools/code_interpreter_tool")
            if not os.path.exists(dockerfile_path):
                raise FileNotFoundError(f"在 {dockerfile_path} 中找不到 Dockerfile")

            client.images.build(
                path=dockerfile_path,
                tag=image_tag,
                rm=True,
            )

    def _run(self, **kwargs) -> str:
        code = kwargs.get("code", self.code)
        libraries_used = kwargs.get("libraries_used", [])
        return self.run_code_in_docker(code, libraries_used)

    def _install_libraries(
        self, container: docker.models.containers.Container, libraries: List[str]
    ) -> None:
        """
        在 Docker 容器中安装缺少的库
        """
        for library in libraries:
            container.exec_run(f"pip install {library}")

    def _init_docker_container(self) -> docker.models.containers.Container:
        client = docker.from_env()
        return client.containers.run(
            "code-interpreter",
            detach=True,
            tty=True,
            working_dir="/workspace",
            name="code-interpreter",
        )

    def run_code_in_docker(self, code: str, libraries_used: List[str]) -> str:
        self._verify_docker_image()
        container = self._init_docker_container()
        self._install_libraries(container, libraries_used)

        cmd_to_run = f'python3 -c "{code}"'
        exec_result = container.exec_run(cmd_to_run)

        container.stop()
        container.remove()

        if exec_result.exit_code != 0:
            return f"运行代码时出现错误：\n{exec_result.output.decode('utf-8')}"
        return exec_result.output.decode("utf-8")
    