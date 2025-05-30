import discord
from discord.ext import commands, tasks
import asyncio
from datetime import datetime, timedelta

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)

ping_tracker = {}  

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")
    reset_ping_counts.start()  


@bot.tree.command(name="new_slot")
async def slo(interaction: discord.Interaction, vendeur: discord.Member, nom: str, category: discord.CategoryChannel, ping_max_here: int, ping_max_everyone: int):
    guild = interaction.guild
    

    channel = await guild.create_text_channel(name=nom, category=category)
    await channel.set_permissions(vendeur, read_messages=True, send_messages=True)
    await channel.set_permissions(guild.default_role, read_messages=True, send_messages=False)


    ping_tracker[channel.id] = {
        "max_here": ping_max_here,
        "current_here": 0,
        "max_everyone": ping_max_everyone,
        "current_everyone": 0,
        "vendeur": vendeur
    }

    embed = discord.Embed(
        title="Nouveau Slot",
        description=f"""
> Le nombre de ping **@here** autorisé est de {ping_max_here}.
> Le nombre de ping **@everyone** autorisé est de {ping_max_everyone}.
> Le vendeur à qui appartient le slot est {vendeur.mention}""",
        color=0xFFFFFF
    )
    embed.set_footer(text=f"Créé par {interaction.user.name}")
    msg = await channel.send(embed=embed)
    await interaction.response.send_message(f"Slot créé {channel.mention}", ephemeral=True)
    await msg.add_reaction("🛒")

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    channel = message.channel

    if channel.id not in ping_tracker:
        await bot.process_commands(message)
        return

    tracker = ping_tracker[channel.id]
    deleted = False
    if "@everyone" in message.content:
        tracker["current_everyone"] += 1
        if tracker["current_everyone"] > tracker["max_everyone"]:
            await message.delete()
            await channel.send(f"{message.author.mention} vous avez dépassé le nombre de `@everyone` autorisé dans ce slot.")
            await channel.set_permissions(tracker["vendeur"], read_messages=True, send_messages=False)
            await channel.set_permissions(message.author, read_messages=True, send_messages=False)
            deleted = True
        else:
            restant = tracker["max_everyone"] - tracker["current_everyone"]
            await channel.send(f"{message.author.mention} il vous reste {restant} ping(s) `@everyone` autorisé(s).")

    if "@here" in message.content:
        tracker["current_here"] += 1
        if tracker["current_here"] > tracker["max_here"]:
            if not deleted:
                await message.delete()
            await channel.send(f"{message.author.mention} vous avez dépassé le nombre de `@here` autorisé dans ce slot.")
            await channel.set_permissions(tracker["vendeur"], read_messages=True, send_messages=False)
            await channel.set_permissions(message.author, read_messages=True, send_messages=False)
        else:
            restant = tracker["max_here"] - tracker["current_here"]
            await channel.send(f"{message.author.mention} il vous reste {restant} ping(s) `@here` autorisé(s).")

    await bot.process_commands(message)


async def wait_until_midnight():
    now = datetime.now()
    tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    wait_seconds = (tomorrow - now).total_seconds()
    await asyncio.sleep(wait_seconds)


@tasks.loop(hours=24)
async def reset_ping_counts():
    for channel_id, tracker in ping_tracker.items():
        tracker["current_here"] = 0
        tracker["current_everyone"] = 0
    print("[RESET] Compteurs de pings remis à zéro")

@reset_ping_counts.before_loop
async def before_reset():
    await bot.wait_until_ready()
    await wait_until_midnight()



bot.run("YOURTOKEN")
