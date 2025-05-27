import asyncio

from .manager import SalesLeadResearcher


async def main() -> None:
    print("Enter targets as 'Company, Person' or just 'Company'. Enter an empty line to finish.")
    targets: list[tuple[str, str | None]] = []
    while True:
        line = input()
        if not line.strip():
            break
        if "," in line:
            company, person = [part.strip() for part in line.split(",", 1)]
        else:
            company, person = line.strip(), None
        targets.append((company, person))

    results = await SalesLeadResearcher().run(targets)
    print("\n=====RESULTS=====")
    for res in results:
        print(res.json())


if __name__ == "__main__":
    asyncio.run(main())
