import discord
from discord import app_commands
from discord.ui import Button, View
import os
import asyncio

print("🚀 开始启动 Discord Bot...")

# 创建 Bot 实例
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Bot(intents=intents)

# 点击计数器
click_counters = {}

# 创建按钮视图
class TextButtonView(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(
        label="📝 点击获取文字",
        style=discord.ButtonStyle.primary,
        custom_id="text_button",
        emoji="🔢"
    )
    async def callback(self, interaction: discord.Interaction, button: Button):
        user_id = str(interaction.user.id)
        click_counters[user_id] = click_counters.get(user_id, 0) + 1
        
        embed = discord.Embed(
            title="✅ 文字获取成功",
            description="您请求的文字内容：",
            color=0x00ff00
        )
        embed.add_field(name="📄 内容", value="```123```", inline=False)
        embed.add_field(name="👤 用户", value=interaction.user.mention, inline=True)
        embed.add_field(name="🎯 点击次数", value=str(click_counters[user_id]), inline=True)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        print(f"用户 {interaction.user} 获取了文字")

# Bot 启动事件
@bot.event
async def on_ready():
    print(f'🎉 {bot.user} 已成功上线！')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="点击按钮获取文字"))
    
    # 注册永久按钮
    bot.add_view(TextButtonView())
    
    # 同步命令
    try:
        synced = await bot.tree.sync()
        print(f"✅ 已同步 {len(synced)} 个命令")
    except Exception as e:
        print(f"命令同步错误: {e}")

# 创建按钮命令
@bot.tree.command(name="create_button", description="创建文字获取按钮")
async def create_button(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📝 文字获取系统",
        description="点击下方按钮获取文字内容",
        color=0x3498db
    )
    view = TextButtonView()
    await interaction.response.send_message(embed=embed, view=view)

# 运行 Bot
if __name__ == "__main__":
    token = os.getenv('DISCORD_BOT_TOKEN')
    if token:
        bot.run(token)
    else:
        print("❌ 未找到 DISCORD_BOT_TOKEN 环境变量")