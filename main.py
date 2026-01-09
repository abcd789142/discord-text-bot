import discord
from discord import app_commands
from discord.ui import Button, View
import os
import asyncio

print("🚀 Discord Bot 启动中...")

# 创建 Bot 实例
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Bot(intents=intents)

# 点击计数器
click_data = {}

# 创建永久按钮视图
class TextButtonView(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(
        label="📝 点击获取文字",
        style=discord.ButtonStyle.primary,
        custom_id="text_button_123",
        emoji="🔢"
    )
    async def button_callback(self, interaction: discord.Interaction, button: Button):
        try:
            # 记录点击次数
            user_id = str(interaction.user.id)
            if user_id not in click_data:
                click_data[user_id] = 0
            click_data[user_id] += 1
            
            # 创建响应消息
            embed = discord.Embed(
                title="✅ 文字获取成功",
                description="您请求的文字内容如下：",
                color=0x00ff00,
                timestamp=interaction.created_at
            )
            
            embed.add_field(
                name="📄 文字内容", 
                value="```123```", 
                inline=False
            )
            
            embed.add_field(
                name="👤 用户信息", 
                value=f"{interaction.user.mention}\n点击次数：{click_data[user_id]}", 
                inline=True
            )
            
            embed.set_footer(text="Koyeb 部署版 v1.0")
            
            # 发送私密响应
            await interaction.response.send_message(embed=embed, ephemeral=True)
            print(f"📨 用户 {interaction.user} 获取了文字内容")
            
        except Exception as e:
            print(f"❌ 按钮点击错误: {e}")
            error_embed = discord.Embed(
                title="❌ 错误",
                description="获取文字时发生错误",
                color=0xff0000
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)

# Bot 启动完成事件
@bot.event
async def on_ready():
    print(f'🎉 {bot.user} 已成功上线！')
    print(f'🆔 Bot ID: {bot.user.id}')
    print(f'📊 已加入服务器数量: {len(bot.guilds)}')
    
    # 设置在线状态
    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name="点击按钮获取文字 | Koyeb部署"
    )
    await bot.change_presence(activity=activity)
    
    # 注册永久按钮
    bot.add_view(TextButtonView())
    
    # 同步斜杠命令
    try:
        synced = await bot.tree.sync()
        print(f"✅ 已同步 {len(synced)} 个斜杠命令")
    except Exception as e:
        print(f"❌ 命令同步错误: {e}")

# 创建按钮命令
@bot.tree.command(name="create_button", description="创建文字获取按钮")
async def create_button(interaction: discord.Interaction):
    """创建文字获取按钮的斜杠命令"""
    try:
        embed = discord.Embed(
            title="📝 文字获取系统 (Koyeb部署)",
            description="点击下方按钮获取预设的文字内容",
            color=0x3498db
        )
        
        embed.add_field(
            name="🎯 功能说明",
            value="• 点击按钮获取文字 **123**\n• 响应仅对点击者可见\n• 自动记录点击次数\n• 24小时在线运行",
            inline=False
        )
        
        embed.set_footer(text="由 Koyeb 云平台驱动")
        
        # 创建按钮视图
        view = TextButtonView()
        
        # 发送消息
        await interaction.response.send_message(embed=embed, view=view)
        print(f"✅ 在服务器 {interaction.guild.name} 创建了按钮")
        
    except Exception as e:
        print(f"❌ 创建按钮错误: {e}")
        await interaction.response.send_message("创建按钮时发生错误，请稍后重试。", ephemeral=True)

# 运行 Bot
if __name__ == "__main__":
    token = os.getenv('DISCORD_BOT_TOKEN')
    
    if not token:
        print("❌ 错误：未找到 DISCORD_BOT_TOKEN 环境变量")
        print("💡 请在 Koyeb 的环境变量中设置正确的 Token")
    else:
        print("🔗 开始连接 Discord...")
        bot.run(token)