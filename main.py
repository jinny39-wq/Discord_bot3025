import discord
from discord.interactions import Interaction
import requests
import random,threading
import json
import os
from discord.ui import Button, View, Modal, Select
from discord import app_commands,ui

token = "MTE3NTM2MTIzNTQxNjUzMDk5NA.Gy4UMl.wCY0634irIIHRemEYgEZtmocnJZDnpuBD4bjsM" # โทเค็นบอท
serverID = 1175360902233591818 # ไอดีเซิร์ฟเวอร์
phone = "0958816629" # เบอร์รับเงิน
admin = "queesss" # ชื่อแอดมินสำหรับใช้งานคำสั่งบอท

intents = discord.Intents.all()
client = discord.Client(intents=intents)

MYGUILD = discord.Object(id=int(serverID))

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MYGUILD)
        await self.tree.sync(guild=MYGUILD)

intents = discord.Intents.default()
client = MyClient(intents=intents)

class shopping_discord(discord.ui.Modal, title="Rlexzy Store | เติมเงิน"):
	link_angpao = discord.ui.TextInput(label="เติมเงินผ่านซองอั่งเปา", placeholder="ลิ้งค์อั่งเปาของคุณ 💸 | URL", required=True, max_length=100, style=discord.TextStyle.short)
	async def on_submit(self, interaction: discord.Interaction):
		user = interaction.user
		redeem_link = self.link_angpao.value
		response = requests.post("https://restapi.kdkddmdmdd.repl.co/undefined_store/topupwallet",json={"mobile": phone,"link": redeem_link}).json()
		if response["status"] == True:
			money = response["amount"]
			try:
				with open(f"{user.name}.json", "r+") as datame:
					database = json.load(datame)
					last_money = database[f'{user.name}']['amount']
					last_accumulate = database[f'{user.name}']['accumulate']
					update_money = float(last_money) + float(money)
					update_accumulate = float(last_accumulate) + float(money)
					data = {
						f"{user.name}": {
							"id": f"{user.id}",
							"money": float(update_money),
							"accumulate": float(update_accumulate)
						}
					}
					replacedata = json.dumps(data, indent=4)
					with open(f"{user.name}.json", "w+") as datame:
						datame.write(replacedata)
				with open(f"{user.name}.json", "r+") as datame:
					database = json.load(datame)
					lastmoney = database[f'{user.name}']['amount']
					embed = discord.Embed(title="ประวัติการเติมเงิน", description=f"เติมเงินสำเร็จแล้วจำนวนเงิน **{float(money)}0 บาท**", color=0xFCE5CD)
					embed.set_footer(text=f"ยอดเงินคงเหลือ : {lastmoney} บาท")
					await interaction.response.send_message(embed=embed, ephemeral=True)
			except Exception as e:
				data2 = {
					f"{user.name}": {
						"id": f"{user.id}",
						"money": float(money),
						"accumulate": float(money)
					}
				}
				replacedata = json.dumps(data2, indent=4)
				with open(f"{user.name}.json", "w+") as datame2:
					datame2.write(replacedata)
				with open(f"{user.name}.json", "r+") as datame3:
					database = json.load(datame3)
					lastmoney = database[f'{user.name}']['amount']
					embed = discord.Embed(title="ประวัติการเติมเงิน", description=f"เติมเงินสำเร็จแล้วจำนวนเงิน **{float(money)}0 บาท**", color=0xFCE5CD)
					embed.set_footer(text=f"ยอดเงินคงเหลือ : {lastmoney} บาท")
					await interaction.response.send_message(embed=embed, ephemeral=True)
		elif response["reason"] == "VOUCHER_NOT_FOUND":
			embed = discord.Embed(title="\nทำรายการไม่สำเร็จ", description="**ขออภัยเติมเงินไม่สำเร็จหรือลิ้งอังเปาไม่ถูกต้อง!**", color=0xFF0000)
			await interaction.response.send_message(embed=embed, ephemeral=True)
		else:
			embed = discord.Embed(title="\nทำรายการไม่สำเร็จ", description="**ขออภัยเติมเงินไม่สำเร็จลิ้งอังเปาได้มีการรับเงินไปแล้ว!**", color=0xFF0000)
			await interaction.response.send_message(embed=embed, ephemeral=True)
	


@client.event
async def on_ready():
	print(f'We have logged in as {client.user}')
	await client.change_presence(activity=discord.Streaming(name='Discord', url='https://facebook.com/msreyaztv123'))

@client.tree.command(description="shopping")
async def shop(interaction: discord.Interaction):
	uid = str(interaction.user.name)
	if uid == admin:
		async def button_callback(interaction: discord.Interaction):
			await interaction.response.send_modal(shopping_discord())
		
		async def button_callback2(interaction: discord.Interaction):
			user = interaction.user
			try:
				with open(f"{user.name}.json", "r+") as data:
					db = json.load(data)
					money = db[f'{user.name}']['amount']
					accumulate = db[f'{user.name}']['accumulate']
					embed = discord.Embed(title="ข้อมูลบัญชีของคุณ", description=f"ยอดเงินคงเหลือ : **{money}0 บาท**\nยอดเงินสะสมรวม : **{accumulate}0 บาท**", color=0xFCE5CD)
					await interaction.response.send_message(embed=embed, ephemeral=True)
			except:
				embed = discord.Embed(title="ไม่พบบัญชีของคุณ ❗", description=f"คุณยังไม่มีบัญชีกรุณาเติมเงินก่อนทำรายการ", color=0xFCE5CD)
				await interaction.response.send_message(embed=embed, ephemeral=True)
	
		
		
		components = Select(
			placeholder="🛒 เลือกสินค้าที่คุณต้องการซื้อ",
			options=[
				discord.SelectOption(
					label="ทดสอบ 1",
					emoji="📦",
					description="100.00 บาท",
					value="1"
				),
				discord.SelectOption(
					label="ทดสอบ 2",
					emoji="📦",
					description="20.00 บาท",
					value="2"
				),
				discord.SelectOption(
					label="รายการสินค้าว่างเปล่า",
					emoji="📦",
					description="30.00 บาท",
					value="3"
				)
			]
		)
		
		
		async def my_callback(interaction: discord.Interaction):
			user = interaction.user
			if components.values[0] == "1":
				try:
					with open(f"{user.name}.json", "r+") as file:
						data = json.load(file)
						money = data[f'{user.name}']['amount']
						if float(money) < float(100.0):
							embed = discord.Embed(title="ไม่สามารถซื้อสินค้าได้❗", description=f"ยอดเงินของคุณคงเหลือไม่เพียงพอสำหรับใช้จ่ายสินค้านี้ (ยอดเงินคงเหลือ {money}0 บาท)", color=0xFCE5CD)
							await interaction.response.send_message(embed=embed, ephemeral=True)
						else:
							with open(f"{user.name}.json", "r+") as file:
								data = json.load(file)
								money = data[f'{user.name}']['amount']
								accumulate = data[f'{user.name}']['accumulate']
								update_money = float(money) - float(100.0)
								
								data = {
									f"{user.name}": {
										"id": f"{user.id}",
										"amount": float(update_money),
										"accumulate": float(accumulate)
									}
								}
								newupdate = json.dumps(data, indent=4)
								with open(f"{user.name}.json", "w+") as file:
									file.write(newupdate)
							
							with open(f"{user.name}.json", "r+") as file:
								data = json.load(file)
								money = data[f'{user.name}']['amount']
								embed = discord.Embed(title="ประวัติการซื้อสินค้า", description=f"ซื้อสินค้าสำเร็จลิ้งค์โหลดสินค้า\nxxxxxxxxxxxx", color=0xFCE5CD)
								embed.set_footer(text=f"ยอดเงินคงเหลือ : {money}0 บาท")
								await interaction.response.send_message(embed=embed, ephemeral=True)
				except:
					embed = discord.Embed(title="ไม่พบบัญชีของคุณ ❗", description=f"คุณยังไม่มีบัญชีกรุณาเติมเงินก่อนทำรายการ", color=0xFCE5CD)
					await interaction.response.send_message(embed=embed, ephemeral=True)
			if components.values[0] == "2":
				try:
					with open(f"{user.name}.json", "r+") as file:
						data = json.load(file)
						money = data[f'{user.name}']['amount']
						if float(money) < float(20.0):
							embed = discord.Embed(title="ไม่สามารถซื้อสินค้าได้❗", description=f"ยอดเงินของคุณคงเหลือไม่เพียงพอสำหรับใช้จ่ายสินค้านี้ (ยอดเงินคงเหลือ {money}0 บาท)", color=0xFCE5CD)
							await interaction.response.send_message(embed=embed, ephemeral=True)
						else:
							with open(f"{user.name}.json", "r+") as file:
								data = json.load(file)
								money = data[f'{user.name}']['amount']
								accumulate = data[f'{user.name}']['accumulate']
								update_money = float(money) - float(20.0)
								
								data = {
									f"{user.name}": {
										"id": f"{user.id}",
										"amount": float(update_money),
										"accumulate": float(accumulate)
									}
								}
								newupdate = json.dumps(data, indent=4)
								with open(f"{user.name}.json", "w+") as file:
									file.write(newupdate)
								
							with open(f"{user.name}.json", "r+") as file:
								data = json.load(file)
								money = data[f'{user.name}']['amount']
								embed = discord.Embed(title="ประวัติการซื้อสินค้า", description=f"ซื้อสินค้าสำเร็จลิ้งค์โหลดสินค้า\nxxxxxxxxxxxx", color=0xFCE5CD)
								embed.set_footer(text=f"ยอดเงินคงเหลือ : {money}0 บาท")
								await interaction.response.send_message(embed=embed, ephemeral=True)
				except:
					embed = discord.Embed(title="ไม่พบบัญชีของคุณ ❗", description=f"คุณยังไม่มีบัญชีกรุณาเติมเงินก่อนทำรายการ", color=0xFCE5CD)
					await interaction.response.send_message(embed=embed, ephemeral=True)
			if components.values[0] == "3":
				await interaction.response.send_message("ยังไม่มีสินค้า !",ephemeral=True)
			
			
		
		embed = discord.Embed(title="**ร้านค้ายอดนิยม**", description=f"[+] เติมเงินเข้าบัญชี\n[+] เลือกสินค้าที่ต้องการ\n[+] สั่งซื้อสินค้าและรับของ", color=0xFCE5CD)
		embed.set_image(url="https://media.discordapp.net/attachments/1175342810589822996/1175346468467511357/dsfsdf.png?width=600&height=600")
		button = Button(label="เติมเงิน", style=discord.ButtonStyle.green, emoji="🧧")
		button2 = Button(label="เช็คยอดเงิน", style=discord.ButtonStyle.green, emoji="📁")
		button.callback = button_callback
		button2.callback = button_callback2
		components.callback = my_callback
		view = View(timeout=None)
		view.add_item(components)
		view.add_item(button)
		view.add_item(button2)
		await interaction.response.send_message(embed=embed, view=view)
	else:
		embed = discord.Embed(title="\nไม่สามารถใช้คำสั่งได้", description=f"เนื่องจากคุณไม่มีสิทธิ์ใช้งานคำสั่งนี้", color=0xFCE5CD)
		await interaction.response.send_message(embed=embed, ephemeral=True)
	
		

client.run(token)
