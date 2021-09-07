from fpl import FPL
import aiohttp
import asyncio
import csv
import os.path

#Edit below 3 fields
email='youremail@address.com'
password='yourPassword'
filename = 'thefilenameyouprefer.csv'

async def main(indexNum):
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        await fpl.login(email, password)
        classic_league = await fpl.get_classic_league(155040)
        details = await classic_league.get_standings(indexNum)
        file_exists = os.path.isfile('./'+filename)
        with open(filename, 'a', encoding="utf-8") as csvfile:
            fieldnames=['id','event_total','player_name','rank','last_rank','rank_sort','total','entry','entry_name']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            for player in details["results"]:
                writer.writerow(player)
                print(str(player["id"])+ "Added")
        if details['has_next'] == True:
            print('doing new page \n\n\n\n')
            await main(indexNum+1)

print('working')
# Python 3.7+
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main(1))
