# Sales lead researcher

This example shows how to build a small multi‑agent workflow for gathering sales leads. The flow mirrors the `research_bot` example but is specialized for collecting CRM information about publishing contacts.

Run it with:

```bash
python -m examples.sales_lead_researcher.main
```

You will be prompted to enter company and person pairs. Provide either `Company, Person` or just the company name. The agents will search the web (LinkedIn and company websites) in parallel and return structured lead information.
