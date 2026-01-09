import discord
import os
import sys

# 强制使用 discord.py 2.x
try:
    from discord import app_commands
    from discord.ui import Button, View
    print("✅ discord.py 2.x 版本检测通过")
except ImportError as e:
    print(f"❌ 错误：{e}")
    print("💡 请确保安装了 discord.py 2.x 版本")
    sys.exit(1)

print(f"🎯 Discord.py 版本: {discord.__version__}")

# 创建 Bot 实例
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Bot(intents=intents)

# 点击计数器
click_data = {}

# 创建按钮视图
class TextButtonView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="📝 点击获取文字", style=discord.ButtonStyle.primary, custom_id="text_button")
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = str(interaction.user.id)
        click_data[user_id] = click_data.get(user_id, 0) + 1
        
        embed = discord.Embed(
            title="✅ 文字获取成功",
            description="```123```",
            color=0x00ff00
        )
        embed.add_field(name="👤 用户", value=interaction.user.mention)
        embed.add_field(name="🎯 点击次数", value=str(click_data[user_id]))
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.event
async def on_ready():
    print(f'🎉 {bot.user} 已上线！')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="点击按钮获取文字"))
    
    # 注册永久按钮
    bot.add_view(TextButtonView())
    
    # 同步命令
    try:
        synced = await bot.tree.sync()
        print(f"✅ 已同步 {len(synced)} 个命令")
    except Exception as e:
        print(f"❌ 命令同步错误: {e}")

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
token = os.getenv('DISCORD_BOT_TOKEN')
if token:
    print("🔗 开始连接 Discord...")
    bot.run(token)
else:
    print("❌ 未找到 DISCORD_BOT_TOKEN 环境变量")
