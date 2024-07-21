import asyncio
import pickle

from ceylon.ceylon import AdminAgent, AdminAgentConfig, Processor, MessageHandler, EventHandler
from ceylon.workspace.runner import RunnerInput
from ceylon.ceylon.ceylon import uniffi_set_event_loop


class Admin(AdminAgent, Processor, MessageHandler, EventHandler):

    def __init__(self, name="admin", port=8888):
        super().__init__(config=AdminAgentConfig(name=name, port=port), processor=self, on_message=self, on_event=self)

    async def run(self, inputs: "bytes"):
        pass

    #
    async def on_message(self, agent_id: "str", data: "bytes", time: "int"):
        pass

    async def run_admin(self, inputs, workers):
        uniffi_set_event_loop(asyncio.get_event_loop())
        runner_input = RunnerInput(request=inputs, agents=[], network={})
        await self.start(pickle.dumps(runner_input), workers)

    #
    async def execute_task(self, input):
        pass

    async def on_agent_connected(self, topic: "str", agent_id: "str"):
        pass
