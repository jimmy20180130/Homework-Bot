import json
import discord
from discord import option, SlashCommandOptionType
import keep_alive
import os
import datetime
import pytz
from datetime import datetime,  timedelta

intents = discord.Intents().all()
bot = discord.Bot(intents=intents)

with open('settings.json', 'r', encoding='utf-8') as settings:
    setting = json.load(settings)

def open_json():
    with open('hw.json', 'r', encoding='utf-8') as homeworks:
        homework = json.load(homeworks)
    return homework

async def future_time(ctx: discord.AutocompleteContext):
    taipei_timezone = pytz.timezone('Asia/Taipei')
    now_time = datetime.now(taipei_timezone)
    date_list = []
    for i in range(25):
        next_day = now_time + datetime.timedelta(days=i + 1)
        formatted_date = next_day.strftime("%Y/%m/%d")
        date_list.append(formatted_date)
    return date_list
    
async def get_time(ctx: discord.AutocompleteContext):
    homework = open_json()
        
    exist_time = []
    for hw in homework:
        exist_time.append(hw)
        
    return exist_time

async def hw_name(ctx: discord.AutocompleteContext):
    homework = open_json()
    
    hw_time = ctx.options["時間"]
    hw_subject = ctx.options["科目"]
    hw_type = ctx.options["作業種類"]
    
    if hw_time is not None and hw_subject is not None and hw_type is not None:
        hw_names = []
        try:
            for hw_name in homework[hw_time][hw_subject][hw_type]:
                hw_names.append(hw_name)
        except Exception as e:
            print(e)
            return ['找不到此作業']
        
        if hw_names is not None:            
            return hw_names
        else:
            return ['找不到此作業']
    else:
        return ['缺少必要參數']

@bot.event
async def on_ready():
    print(f'機器人已上線({bot.user})')
    
@bot.command(description='新增作業')
@option("科目", description="選擇科目", choices=["班級", "國文","英文","數學","物理","化學","生物","歷史","地理","公民與社會","地球科學","音樂","美術","體育","資訊科技"])
@option("作業類型", description="作業類型", choices=["考試", "讀書", "寫作業", "攜帶物品", "填東西", "提醒"])
@option("作業名稱", description="作業名稱")
@option("作業說明", description="作業說明")
@option("排定時間", description="新增作業的日期", autocomplete=future_time)
@option("附件1", description="檔案附件(建議放圖片)", type=SlashCommandOptionType.attachment)
@option("附件2", description="檔案附件", type=SlashCommandOptionType.attachment)
@option("附件3", description="檔案附件", type=SlashCommandOptionType.attachment)
async def 添加作業(ctx, 科目, 作業類型, 作業名稱, 作業說明, 排定時間=None, 附件1=None, 附件2=None, 附件3=None):
    await ctx.defer()
    if 附件1:
        attachment1_url = 附件1.url
    if 附件2:
        attachment2_url = 附件2.url
    if 附件3:
        attachment3_url = 附件3.url
    
    if 排定時間 is None:
        taipei_timezone = pytz.timezone('Asia/Taipei')
        now_time = datetime.now(taipei_timezone)
        formatted_date = now_time.strftime("%Y/%m/%d")
    else:
        formatted_date = 排定時間
        
    formatted_date = datetime.strptime(formatted_date, "%Y/%m/%d")
    one_day_before = formatted_date - timedelta(days=1)
    formatted_dates = [one_day_before - timedelta(days=i) for i in range(4)]  # 前四天的日期s
    
    homework = open_json()
    
    try:
        for formatted_date in formatted_dates:
            homework.setdefault(formatted_date, {})
            homework[formatted_date].setdefault(科目, {})
            homework[formatted_date][科目].setdefault(作業類型, {})
            if 附件1 is not None and 附件2 is not None and 附件3 is not None:
                homework[formatted_date][科目][作業類型].update({作業名稱: {
                    "description": 作業說明,
                    "uploader": ctx.author.id,
                    "attachment1": attachment1_url,
                    "attachment2": attachment2_url,
                    "attachment3": attachment3_url
                }})
            elif 附件1 is not None and 附件2 is not None and 附件3 is None:
                homework[formatted_date][科目][作業類型].update({作業名稱: {
                    "description": 作業說明,
                    "uploader": ctx.author.id,
                    "attachment1": attachment1_url,
                    "attachment2": attachment2_url,
                    "attachment3": '無'
                }})
            elif 附件1 is not None and 附件2 is None and 附件3 is None:
                homework[formatted_date][科目][作業類型].update({作業名稱: {
                    "description": 作業說明,
                    "uploader": ctx.author.id,
                    "attachment1": attachment1_url,
                    "attachment2": '無',
                    "attachment3": '無'
                }})
            elif (附件1 is None and 附件2 is not None and 附件3 is None) or (附件1 is None and 附件2 is not None and 附件3 is not None) or (附件1 is None and 附件2 is None and 附件3 is not None):
                await ctx.respond('請確認參數是否正確')
                pass
            else:
                homework[formatted_date][科目][作業類型].update({作業名稱: {
                    "description": 作業說明,
                    "uploader": ctx.author.id,
                    "attachment1": '無',
                    "attachment2": '無',
                    "attachment3": '無'
                }})
    except Exception as e:
        print(e)
        await ctx.respond('添加失敗，請確認參數是否正確\n原因: {e}')
        pass
    
    with open('hw.json', 'w', encoding='utf-8') as homeworks:
        json.dump(homework, homeworks, ensure_ascii=False, indent=4)
    
    await ctx.respond('已成功添加')
                
@bot.command(description='移除作業')
@option("時間", description="時間", autocomplete=get_time)
@option("科目", description="選擇科目", choices=["班級", "國文","英文","數學","物理","化學","生物","歷史","地理","公民與社會","地球科學","音樂","美術","體育","資訊科技"])
@option("作業種類", description="作業類型", choices=["考試", "讀書", "寫作業", "攜帶物品", "填東西", "提醒"])
@option("名稱", description="作業名稱", autocomplete=hw_name)
async def 移除作業(ctx, 時間, 科目=None, 作業種類=None, 名稱=None):
    homework = open_json()
    try:
        if 科目 is None and 作業種類 is None and 名稱 is None:
            del homework[時間]
        elif  科目 is not None and 作業種類 is None and 名稱 is None:
            del homework[時間][科目]
        elif  科目 is not None and 作業種類 is not None and 名稱 is None:
            del homework[時間][科目][作業種類]
        elif 科目 is not None and 作業種類 is not None and 名稱 is not None:
            del homework[時間][科目][作業種類][名稱]
        elif (科目 is None and 作業種類 is not None and 名稱 is not None) or (作業種類 is None and 名稱 is not None):
            await ctx.respond('請確認參數是否正確')
            pass
    except Exception as e:
        print(e)
        await ctx.respond(f'移除失敗，請確認參數是否正確\n原因: {e}')
        pass
    
    with open('hw.json', 'w', encoding='utf-8') as homeworks:
        json.dump(homework, homeworks, ensure_ascii=False, indent=4)
    
    await ctx.respond('已成功移除')
    
@bot.command(description='作業列表')
@option("時間", description="時間", autocomplete=get_time)
@option("科目", description="科目", choices=["班級", "國文","英文","數學","物理","化學","生物","歷史","地理","公民與社會","地球科學","音樂","美術","體育","資訊科技"])
@option("作業種類", description="作業種類", choices=["考試", "讀書", "寫作業", "攜帶物品", "填東西", "提醒"])
@option("名稱", description="作業名稱", autocomplete=hw_name)
async def 作業列表(ctx, 時間=None, 科目=None, 作業種類=None, 名稱=None):
    homework = open_json()
    if not (時間 is None and (科目 is not None or 作業種類 is not None or 名稱 is not None)) or (時間 is not None and 科目 is None and 作業種類 is not None):
        if not 時間:
            # 如果未提供時間參數，顯示所有天數的所有作業
            for date, subjects in homework.items():
                taipei_timezone = pytz.timezone('Asia/Taipei')
                current_date = datetime.now(taipei_timezone).date()
                provided_date = datetime.strptime(date, '%Y/%m/%d').date()
                if provided_date >= current_date:
                    embed = discord.Embed(title=f"作業列表 - {date}", color=discord.Color.blue())
                    for subject, types in subjects.items():
                        for hw_type, hw_data in types.items():
                            for hw_name, hw_info in hw_data.items():
                                if hw_info['attachment1'].endswith('.png') or hw_info['attachment1'].endswith('.jpg') or hw_info['attachment1'].endswith('.jpeg') or hw_info['attachment1'].endswith('.gif') or hw_info['attachment1'].endswith('.bmp'):
                                    embed.set_image(url=hw_info['attachment1'])
                                if not hw_info['attachment1'] == '無':
                                    if not hw_info['attachment2'] == '無':
                                        if not hw_info['attachment3'] == '無':
                                            embed.add_field(name=f"{subject} - {hw_type} - {hw_name}",
                                                            value=f"說明: {hw_info['description']}\n上傳者: <@{hw_info['uploader']}>\n附件1: [檔案點我]({hw_info['attachment1']})\n附件2: [檔案點我]({hw_info['attachment2']})\n附件3: [檔案點我]({hw_info['attachment3']})",
                                                            inline=False)
                                        else:
                                            embed.add_field(name=f"{subject} - {hw_type} - {hw_name}",
                                                            value=f"說明: {hw_info['description']}\n上傳者: <@{hw_info['uploader']}>\n附件1: [檔案點我]({hw_info['attachment1']})\n附件2: [檔案點我]({hw_info['attachment2']})",
                                                            inline=False)
                                    else:
                                        embed.add_field(name=f"{subject} - {hw_type} - {hw_name}",
                                                            value=f"說明: {hw_info['description']}\n上傳者: <@{hw_info['uploader']}>\n附件1: [檔案點我]({hw_info['attachment1']})",
                                                            inline=False)
                                        
                                else:
                                    embed.add_field(name=f"{subject} - {hw_type} - {hw_name}",
                                                        value=f"說明: {hw_info['description']}\n上傳者: <@{hw_info['uploader']}>",
                                                        inline=False)
                    await ctx.respond(embed=embed)
        elif 時間 in homework:
            if not 科目:
                # 如果只提供時間參數，但未提供科目，顯示當天的所有作業
                embed = discord.Embed(title=f"作業列表 - {時間}", color=discord.Color.blue())
                subjects = homework[時間]
                for subject, types in subjects.items():
                    for hw_type, hw_data in types.items():
                        for hw_name, hw_info in hw_data.items():
                            if hw_info['attachment1'].endswith('.png') or hw_info['attachment1'].endswith('.jpg') or hw_info['attachment1'].endswith('.jpeg') or hw_info['attachment1'].endswith('.gif') or hw_info['attachment1'].endswith('.bmp'):
                                embed.set_image(url=hw_info['attachment1'])
                            if not hw_info['attachment1'] == '無':
                                if not hw_info['attachment2'] == '無':
                                    if not hw_info['attachment3'] == '無':
                                        embed.add_field(name=f"{subject} - {hw_type} - {hw_name}",
                                                        value=f"說明: {hw_info['description']}\n上傳者: <@{hw_info['uploader']}>\n附件1: [檔案點我]({hw_info['attachment1']})\n附件2: [檔案點我]({hw_info['attachment2']})\n附件3: [檔案點我]({hw_info['attachment3']})",
                                                        inline=False)
                                    else:
                                        embed.add_field(name=f"{subject} - {hw_type} - {hw_name}",
                                                        value=f"說明: {hw_info['description']}\n上傳者: <@{hw_info['uploader']}>\n附件1: [檔案點我]({hw_info['attachment1']})\n附件2: [檔案點我]({hw_info['attachment2']})",
                                                        inline=False)
                                else:
                                    embed.add_field(name=f"{subject} - {hw_type} - {hw_name}",
                                                        value=f"說明: {hw_info['description']}\n上傳者: <@{hw_info['uploader']}>\n附件1: [檔案點我]({hw_info['attachment1']})",
                                                        inline=False)
                                    
                            else:
                                embed.add_field(name=f"{subject} - {hw_type} - {hw_name}",
                                                    value=f"說明: {hw_info['description']}\n上傳者: <@{hw_info['uploader']}>",
                                                    inline=False)
                await ctx.respond(embed=embed)
            elif 科目 in homework[時間]:
                if not 作業種類:
                    # 如果提供時間和科目參數，但未提供作業類型，顯示當天特定科目的所有作業
                    embed = discord.Embed(title=f"作業列表 - {時間} - {科目}", color=discord.Color.blue())
                    types = homework[時間][科目]
                    for hw_type, hw_data in types.items():
                        for hw_name, hw_info in hw_data.items():
                            if hw_info['attachment1'].endswith('.png') or hw_info['attachment1'].endswith('.jpg') or hw_info['attachment1'].endswith('.jpeg') or hw_info['attachment1'].endswith('.gif') or hw_info['attachment1'].endswith('.bmp'):
                                embed.set_image(url=hw_info['attachment1'])
                            if not hw_info['attachment1'] == '無':
                                if not hw_info['attachment2'] == '無':
                                    if not hw_info['attachment3'] == '無':
                                        embed.add_field(name=f"{subject} - {hw_type} - {hw_name}",
                                                        value=f"說明: {hw_info['description']}\n上傳者: <@{hw_info['uploader']}>\n附件1: [檔案點我]({hw_info['attachment1']})\n附件2: [檔案點我]({hw_info['attachment2']})\n附件3: [檔案點我]({hw_info['attachment3']})",
                                                        inline=False)
                                    else:
                                        embed.add_field(name=f"{subject} - {hw_type} - {hw_name}",
                                                        value=f"說明: {hw_info['description']}\n上傳者: <@{hw_info['uploader']}>\n附件1: [檔案點我]({hw_info['attachment1']})\n附件2: [檔案點我]({hw_info['attachment2']})",
                                                        inline=False)
                                else:
                                    embed.add_field(name=f"{subject} - {hw_type} - {hw_name}",
                                                        value=f"說明: {hw_info['description']}\n上傳者: <@{hw_info['uploader']}>\n附件1: [檔案點我]({hw_info['attachment1']})",
                                                        inline=False)
                                    
                            else:
                                embed.add_field(name=f"{subject} - {hw_type} - {hw_name}",
                                                    value=f"說明: {hw_info['description']}\n上傳者: <@{hw_info['uploader']}>",
                                                    inline=False)
                    await ctx.respond(embed=embed)
                elif 作業種類 in homework[時間][科目]:
                    if not 名稱:
                        # 如果提供時間、科目和作業類型，但未提供作業名稱，顯示當天特定科目和作業類型的所有作業
                        embed = discord.Embed(title=f"作業列表 - {時間} - {科目} - {作業種類}", color=discord.Color.blue())
                        hw_data = homework[時間][科目][作業種類]
                        for hw_name, hw_info in hw_data.items():
                            if hw_info['attachment1'].endswith('.png') or hw_info['attachment1'].endswith('.jpg') or hw_info['attachment1'].endswith('.jpeg') or hw_info['attachment1'].endswith('.gif') or hw_info['attachment1'].endswith('.bmp'):
                                embed.set_image(url=hw_info['attachment1'])
                            if not hw_info['attachment1'] == '無':
                                if not hw_info['attachment2'] == '無':
                                    if not hw_info['attachment3'] == '無':
                                        embed.add_field(name=f"{subject} - {hw_type} - {hw_name}",
                                                        value=f"說明: {hw_info['description']}\n上傳者: <@{hw_info['uploader']}>\n附件1: [檔案點我]({hw_info['attachment1']})\n附件2: [檔案點我]({hw_info['attachment2']})\n附件3: [檔案點我]({hw_info['attachment3']})",
                                                        inline=False)
                                    else:
                                        embed.add_field(name=f"{subject} - {hw_type} - {hw_name}",
                                                        value=f"說明: {hw_info['description']}\n上傳者: <@{hw_info['uploader']}>\n附件1: [檔案點我]({hw_info['attachment1']})\n附件2: [檔案點我]({hw_info['attachment2']})",
                                                        inline=False)
                                else:
                                    embed.add_field(name=f"{subject} - {hw_type} - {hw_name}",
                                                        value=f"說明: {hw_info['description']}\n上傳者: <@{hw_info['uploader']}>\n附件1: [檔案點我]({hw_info['attachment1']})",
                                                        inline=False)
                                    
                            else:
                                embed.add_field(name=f"{subject} - {hw_type} - {hw_name}",
                                                    value=f"說明: {hw_info['description']}\n上傳者: <@{hw_info['uploader']}>",
                                                    inline=False)
                        await ctx.respond(embed=embed)
                    elif 名稱 in homework[時間][科目][作業種類]:
                        # 如果提供時間、科目、作業類型和作業名稱，顯示特定作業的詳細信息
                        hw_info = homework[時間][科目][作業種類][名稱]
                        embed = discord.Embed(title=f"作業詳細信息 - {時間} - {科目} - {作業種類} - {名稱}",
                                            color=discord.Color.blue())
                        if hw_info['attachment1'].endswith('.png') or hw_info['attachment1'].endswith('.jpg') or hw_info['attachment1'].endswith('.jpeg') or hw_info['attachment1'].endswith('.gif') or hw_info['attachment1'].endswith('.bmp'):
                                    embed.set_image(url=hw_info['attachment1'])
                        if not hw_info['attachment1'] == '無':
                            if not hw_info['attachment2'] == '無':
                                if not hw_info['attachment3'] == '無':
                                    embed.add_field(name=f"{subject} - {hw_type} - {hw_name}",
                                                    value=f"說明: {hw_info['description']}\n上傳者: <@{hw_info['uploader']}>\n附件1: [檔案點我]({hw_info['attachment1']})\n附件2: [檔案點我]({hw_info['attachment2']})\n附件3: [檔案點我]({hw_info['attachment3']})",
                                                    inline=False)
                                else:
                                    embed.add_field(name=f"{subject} - {hw_type} - {hw_name}",
                                                    value=f"說明: {hw_info['description']}\n上傳者: <@{hw_info['uploader']}>\n附件1: [檔案點我]({hw_info['attachment1']})\n附件2: [檔案點我]({hw_info['attachment2']})",
                                                    inline=False)
                            else:
                                embed.add_field(name=f"{subject} - {hw_type} - {hw_name}",
                                                    value=f"說明: {hw_info['description']}\n上傳者: <@{hw_info['uploader']}>\n附件1: [檔案點我]({hw_info['attachment1']})",
                                                    inline=False)
                                
                        else:
                            embed.add_field(name=f"{subject} - {hw_type} - {hw_name}",
                                                value=f"說明: {hw_info['description']}\n上傳者: <@{hw_info['uploader']}>",
                                                inline=False)
                        await ctx.respond(embed=embed)
                    else:
                        await ctx.respond("找不到指定的作業名稱。")
                else:
                    await ctx.respond("找不到指定的作業類型。")
            else:
                await ctx.respond("找不到指定的科目。")
        else:
            await ctx.respond("找不到指定的日期。")
    else:
        await ctx.respond("請確認參數是否正確")

if __name__ == '__main__':
    keep_alive.keep_alive()
    bot.run(setting['token'])