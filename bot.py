# bot_fusion_embed.py
import discord
from discord import app_commands
from discord.ext import commands
import asyncio

# =========================================================
# 🔧 CONFIGURATION
# =========================================================
TOKEN = "MTQzMTA1NTEzMzU4NzgwNDIzNA.GqnIW4.nYdqeCyUvftJny4PNXUnCqjBTFKrllkKkALgq0"
ROLE_NAME = "Mini Piper"
SEND_DELAY_SECONDS = 1.0

# =========================================================
# 🚀 CONFIGURATION DU BOT
# =========================================================
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# =========================================================
# 🔄 SYNC AUTOMATIQUE (GLOBAL)
# =========================================================
@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"✅ Commandes globales synchronisées ({len(synced)}).")
    except Exception as e:
        print(f"⚠️ Erreur de synchronisation : {e}")
    print(f"🤖 Connecté en tant que {bot.user} (ID: {bot.user.id})")

# =========================================================
# 💬 COMMANDE /dm-optin (slash command)
# =========================================================
@bot.tree.command(name="dm-optin", description="Envoie un DM à tous les membres avec le rôle défini (Admins seulement)")
@app_commands.describe(message="Le message à envoyer aux membres")
async def dm_optin(interaction: discord.Interaction, message: str):
    if not interaction.user.guild_permissions.administrator:
        embed = discord.Embed(title="❌ Permission refusée",
                              description="Tu dois être administrateur pour utiliser cette commande.",
                              color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    guild = interaction.guild
    if guild is None:
        embed = discord.Embed(title="❌ Erreur",
                              description="Cette commande doit être utilisée dans un serveur.",
                              color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    role = discord.utils.get(guild.roles, name=ROLE_NAME)
    if role is None:
        embed = discord.Embed(title="⚠️ Rôle manquant",
                              description=f"Le rôle `{ROLE_NAME}` n'existe pas. Crée-le d'abord.",
                              color=discord.Color.orange())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    embed = discord.Embed(title="📨 Envoi des DM",
                          description=f"Envoi des DM aux membres avec le rôle `{ROLE_NAME}`...",
                          color=discord.Color.blue())
    await interaction.response.send_message(embed=embed, ephemeral=True)

    sent, failed, skipped = 0, 0, 0

    async for member in guild.fetch_members(limit=None):
        if member.bot or role not in member.roles:
            skipped += 1
            continue
        try:
            dm_embed = discord.Embed(title="💌 Message du serveur",
                                     description=message,
                                     color=discord.Color.green())
            await member.send(embed=dm_embed)
            sent += 1
        except discord.Forbidden:
            failed += 1
        except discord.HTTPException:
            failed += 1
        await asyncio.sleep(SEND_DELAY_SECONDS)

    summary_embed = discord.Embed(title="✅ Envoi terminé",
                                  description=f"Messages envoyés : {sent}\nÉchecs : {failed}\nIgnorés : {skipped}",
                                  color=discord.Color.gold())
    await interaction.followup.send(embed=summary_embed, ephemeral=True)

# =========================================================
# 🧪 COMMANDE /test (slash command)
# =========================================================
@bot.tree.command(name="test", description="Vérifie si le bot fonctionne")
async def test(interaction: discord.Interaction):
    embed = discord.Embed(title="✅ Bot actif",
                          description="Slash command fonctionne !",
                          color=discord.Color.green())
    await interaction.response.send_message(embed=embed, ephemeral=True)

# =========================================================
# ➕ COMMANDE !add-role (texte classique)
# =========================================================
@bot.command(name="add-role")
async def add_role(ctx, role_id: int, member: discord.Member):
    role = ctx.guild.get_role(role_id)
    if role is None:
        embed = discord.Embed(title="❌ Rôle introuvable",
                              description=f"Aucun rôle avec l'ID `{role_id}`",
                              color=discord.Color.red())
        await ctx.send(embed=embed)
        return
    try:
        await member.add_roles(role)
        embed = discord.Embed(title="✅ Rôle ajouté",
                              description=f"Le rôle `{role.name}` a été ajouté à `{member.display_name}`",
                              color=discord.Color.green())
        await ctx.send(embed=embed)
    except discord.Forbidden:
        embed = discord.Embed(title="❌ Permission refusée",
                              description="Je n'ai pas la permission d'ajouter ce rôle.",
                              color=discord.Color.red())
        await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(title="❌ Erreur",
                              description=str(e),
                              color=discord.Color.red())
        await ctx.send(embed=embed)

# =========================================================
# ▶️ LANCEMENT DU BOT
# =========================================================
if __name__ == "__main__":
    if not TOKEN or TOKEN == "TON_TOKEN_ICI":
        print("⚠️ Erreur : tu dois mettre ton token dans la variable TOKEN.")
    else:
        bot.run(TOKEN)
