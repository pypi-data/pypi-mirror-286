"""
Composio 工具包装器。
"""

import typing as t

import typing_extensions as te

from crewai_tools.tools.base_tool import BaseTool


class ComposioTool(BaseTool):
    """Composio 工具的包装器。"""

    composio_action: t.Callable

    def _run(self, *args: t.Any, **kwargs: t.Any) -> t.Any:
        """使用给定的参数运行 composio 操作。"""
        return self.composio_action(*args, **kwargs)

    @staticmethod
    def _check_connected_account(tool: t.Any, toolset: t.Any) -> None:
        """检查是否需要连接帐户，如果需要，检查帐户是否存在。"""
        from composio import Action
        from composio.client.collections import ConnectedAccountModel

        tool = t.cast(Action, tool)
        if tool.no_auth:
            return

        connections = t.cast(
            t.List[ConnectedAccountModel],
            toolset.client.connected_accounts.get(),
        )
        if tool.app not in [connection.appUniqueId for connection in connections]:
            raise RuntimeError(
                f"应用程序 `{tool.app}` 没有找到连接的帐户; "
                f"运行 `composio add {tool.app}` 来解决这个问题"
            )

    @classmethod
    def from_action(
        cls,
        action: t.Any,
        **kwargs: t.Any,
    ) -> te.Self:
        """将 composio 工具包装为 crewAI 工具。"""

        from composio import Action, ComposioToolSet
        from composio.constants import DEFAULT_ENTITY_ID
        from composio.utils.shared import json_schema_to_model

        toolset = ComposioToolSet()
        if not isinstance(action, Action):
            action = Action(action)

        action = t.cast(Action, action)
        cls._check_connected_account(
            tool=action,
            toolset=toolset,
        )

        (action_schema,) = toolset.get_action_schemas(actions=[action])
        schema = action_schema.model_dump(exclude_none=True)
        entity_id = kwargs.pop("entity_id", DEFAULT_ENTITY_ID)

        def function(**kwargs: t.Any) -> t.Dict:
            """Composio 操作的包装函数。"""
            return toolset.execute_action(
                action=Action(schema["name"]),
                params=kwargs,
                entity_id=entity_id,
            )

        function.__name__ = schema["name"]
        function.__doc__ = schema["description"]

        return cls(
            name=schema["name"],
            description=schema["description"],
            args_schema=json_schema_to_model(
                action_schema.parameters.model_dump(
                    exclude_none=True,
                )
            ),
            composio_action=function,
            **kwargs,
        )

    @classmethod
    def from_app(
        cls,
        *apps: t.Any,
        tags: t.Optional[t.List[str]] = None,
        use_case: t.Optional[str] = None,
        **kwargs: t.Any,
    ) -> t.List[te.Self]:
        """从应用程序创建工具集。"""
        if len(apps) == 0:
            raise ValueError("您需要至少提供一个应用程序名称")

        if use_case is None and tags is None:
            raise ValueError("`use_case` 和 `tags` 不能同时为 `None`")

        if use_case is not None and tags is not None:
            raise ValueError(
                "不能同时使用 `use_case` 和 `tags` 来过滤操作"
            )

        from composio import ComposioToolSet

        toolset = ComposioToolSet()
        if use_case is not None:
            return [
                cls.from_action(action=action, **kwargs)
                for action in toolset.find_actions_by_use_case(*apps, use_case=use_case)
            ]

        return [
            cls.from_action(action=action, **kwargs)
            for action in toolset.find_actions_by_tags(*apps, tags=tags)
        ]
