import asyncio
import datetime
import json
import logging
from pathlib import Path

import discord
from discord.ext import commands

import sqlite3

def config_load():
    with open('src/data/config.json', 'r', encoding='utf-8-sig') as doc:
        return json.load(doc)


async def run():
    config = config_load()
    bot = Bot(config=config,
              description=config['description'])
    try:
        await bot.start(config['token'])
    except KeyboardInterrupt:
        await bot.logout()


class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(
            command_prefix=self.get_prefix_,
            description=kwargs.pop('description')
        )
        self.start_time = None
        self.app_info = None

        self.loop.create_task(self.track_start())
        self.loop.create_task(self.load_all_extensions())

    async def track_start(self):
        await self.wait_until_ready()
        self.start_time = datetime.datetime.utcnow()

    async def get_prefix_(self, bot, message):
        prefix = ['!']
        return commands.when_mentioned_or(*prefix)(bot, message)

    async def load_all_extensions(self):
        await self.wait_until_ready()
        await asyncio.sleep(1)  # ensure that on_ready has completed and finished printing
        cogs = [x.stem for x in Path('src/cogs').glob('*.py')]
        for extension in cogs:
            try:
                self.load_extension(f'cogs.{extension}')
                print(f'loaded {extension}')
            except Exception as e:
                error = f'{extension}\n {type(e).__name__} : {e}'
                print(f'failed to load extension {error}')
            print('-' * 10)

    async def on_ready(self):
        print('-' * 10)
        self.app_info = await self.application_info()
        print('-' * 10)

    async def on_message(self, message):
        if message.author.bot:
            return  # ignore all bots
        await self.process_commands(message)




if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
