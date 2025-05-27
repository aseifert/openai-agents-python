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
                leads = await task
                results.extend(leads)
                num_done += 1
                self.printer.update_item(
                    "progress",
                    f"Processed {num_done}/{len(tasks)} companies",
                )
            self.printer.mark_item_done("progress")
            self.printer.end()
        return results

    async def _process(self, company: str, person: str | None) -> list[LeadInfo]:
        people: list[str]
        if person:
            people = [person]
        else:
            result = await Runner.run(contact_finder_agent, company)
            infos = result.final_output_as(list[ContactInfo])
            people = [info.full_name for info in infos]

        tasks = [
            asyncio.create_task(Runner.run(info_agent, f"Person: {p}\nCompany: {company}"))
            for p in people
        ]

        leads: list[LeadInfo] = []
        for task in asyncio.as_completed(tasks):
            res = await task
            leads.append(res.final_output_as(LeadInfo))
        return leads
