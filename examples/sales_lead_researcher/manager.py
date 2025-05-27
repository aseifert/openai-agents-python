from __future__ import annotations

import asyncio

from rich.console import Console

from agents import Runner, gen_trace_id, trace

from .agents.contact_finder_agent import ContactInfo, contact_finder_agent
from .agents.info_agent import LeadInfo, info_agent
from .printer import Printer


class SalesLeadResearcher:
    def __init__(self) -> None:
        self.console = Console()
        self.printer = Printer(self.console)

    async def run(self, targets: list[tuple[str, str | None]]) -> list[LeadInfo]:
        trace_id = gen_trace_id()
        with trace("Sales lead research", trace_id=trace_id):
            self.printer.update_item(
                "trace_id",
                f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}",
                is_done=True,
                hide_checkmark=True,
            )
            tasks = [
                asyncio.create_task(self._process(company, person)) for company, person in targets
            ]
            results: list[LeadInfo] = []
            num_done = 0
            for task in asyncio.as_completed(tasks):
                result = await task
                results.append(result)
                num_done += 1
                self.printer.update_item("progress", f"Processed {num_done}/{len(tasks)} leads")
            self.printer.mark_item_done("progress")
            self.printer.end()
        return results

    async def _process(self, company: str, person: str | None) -> LeadInfo:
        if not person:
            result = await Runner.run(contact_finder_agent, company)
            info = result.final_output_as(ContactInfo)
            person = info.full_name
        input_data = f"Person: {person}\nCompany: {company}"
        result = await Runner.run(info_agent, input_data)
        return result.final_output_as(LeadInfo)
