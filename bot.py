import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
from datetime import datetime


# Função para converter o timestamp Unix para formato de data
def converter_timestamp_unix(timestamp):
    return datetime.utcfromtimestamp(int(timestamp) / 1000).strftime('%d/%m/%Y %H:%M')

# Função para obter os últimos resultados da FURIA
def obter_ultimos_resultados_furia():
    url = "https://www.hltv.org/team/8297/furia#tab-matchesBox"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # Requisição à página
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontrar as linhas de jogo
        matches = soup.find_all('tr', class_='team-row')

        resultados = []
        for match in matches:
            try:
                # Data da partida
                date = match.find('td', class_='date-cell').text.strip()
                
                # Time da FURIA
                team_furia = match.find('a', class_='team-name team-1').text.strip()
                team_furia_logo = match.find('img', class_='team-logo')['src']
                
                # Time adversário
                team_adversario = match.find('a', class_='team-name team-2').text.strip()
                team_adversario_logo = match.find('img', class_='team-logo')['src']
                
                # Placar
                scores = match.find_all('span', class_='score')
                score_furia = scores[0].text.strip() if len(scores) > 0 else 'N/A'
                score_adversario = scores[1].text.strip() if len(scores) > 1 else 'N/A'
                
                # Link para a página do jogo
                match_link = match.find('a', class_='stats-button')['href']
                
                # Formatar os resultados para exibição
                resultado = (f"Data: {date}\n"
                             f"Time FURIA: {team_furia} - {team_furia_logo}\n"
                             f"Time Adversário: {team_adversario} - {team_adversario_logo}\n"
                             f"Placar: {score_furia} : {score_adversario}\n"
                             f"Link para detalhes: https://www.hltv.org{match_link}\n"
                             f"{'-' * 50}")
                resultados.append(resultado)
                
            except Exception as e:
                continue

        return "\n".join(resultados) if resultados else "Não foi possível encontrar os últimos resultados."
    
    else:
        return "Não foi possível acessar a página."


def obter_torneio_atual_furia():
    url = "https://www.hltv.org/team/8297/furia#tab-matchesBox"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        torneio_section = soup.find('div', class_='matchmaking-title')
        if torneio_section:
            return f"Torneio atual da FURIA: {torneio_section.text.strip()}"
        else:
            return "Não foi possível encontrar o torneio atual."
    else:
        return "Não foi possível acessar a página."
    

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

bot.remove_command('help')  # Remove o comando help padrão


@bot.event
async def on_ready():
    print(f'Bot {bot.user} conectado com sucesso!')

@bot.command()
async def visaogeral(ctx):
    parte1 = """
**FURIA Esports** é uma organização brasileira de esports fundada em 2017. Conhecida por suas atuações de destaque no cenário competitivo, a FURIA é uma das maiores e mais respeitadas organizações de esports do Brasil e do mundo. 
A FURIA compete em diversos jogos, com especial destaque para **Counter-Strike: Global Offensive (CS:GO)** e **Counter-Strike 2 (CS2)**, mas também está presente em outras modalidades de esports.

**Áreas de Atuação**:
- **Counter-Strike: Global Offensive (CS:GO)**: A FURIA se tornou uma das principais equipes do Brasil e do mundo, com participações em grandes torneios internacionais como ESL Pro League e DreamHack.
- **Counter-Strike 2 (CS2)**: A FURIA é uma das equipes pioneiras no novo título da franquia, com grande expectativa para o futuro.
- **Valorant**: A organização também investiu no jogo Valorant, participando de torneios no cenário competitivo.
"""
    parte2 = """
- **Rainbow Six Siege**: A FURIA tem uma equipe de destaque no jogo de tiro tático da Ubisoft.
- **Free Fire**: A organização também tem presença no jogo mobile Free Fire, com uma base de fãs significativa no Brasil.

**Filosofia e Valores**:
A FURIA Esports tem como missão promover o crescimento do cenário de esports no Brasil e no mundo, investindo em atletas, coaches e infraestrutura de ponta. A organização valoriza a inovação, o trabalho em equipe e o desenvolvimento contínuo. Além disso, a FURIA está comprometida em criar um impacto positivo na sociedade por meio de projetos educacionais e sociais, como o **FURIA Academy**, uma iniciativa que busca formar novos talentos do mundo dos esports.

**Principais Conquistas**:
- **CS:GO**: A FURIA tem se destacado em competições de alto nível, conquistando vitórias importantes e sendo reconhecida como uma das melhores equipes do cenário mundial.
- **Valorant**: A equipe tem se consolidado entre as melhores no cenário competitivo de Valorant, com participações de destaque em torneios regionais e internacionais.
- **Rainbow Six Siege**: A FURIA também é reconhecida por suas boas performances no jogo, ganhando destaque em torneios da Ubisoft. 
"""
    await ctx.send(parte1)
    await ctx.send(parte2)


@bot.command()
async def mascote(ctx):
    await ctx.send("Nosso mascote é o FURIA! 🦊")

@bot.command()
async def membros(ctx):
    membros = (
        "**Elenco atual da FURIA CS:**\n"
        "• YEKINDAR\n"
        "• molodoy-\n"
        "• KSCERATO\n"
        "• yuurih\n"
        "• FalleN (capitão)\n"
        "• sidde (coach)"
    )
    await ctx.send(membros)

@bot.command()
async def redes(ctx):
    redes_sociais = (
        "**🌐 Redes Sociais da FURIA:**\n"
        "🔵 Twitter: https://twitter.com/furia\n"
        "📸 Instagram: https://www.instagram.com/furia\n"
        "📺 YouTube: https://www.youtube.com/@FURIA\n"
        "🎮 Twitch: https://www.twitch.tv/furia\n"
    )
    await ctx.send(redes_sociais)

@bot.command()
async def projetos(ctx):
    await ctx.send("A FURIA investe em projetos como o FURIA Academy, iniciativas educacionais e sociais, além de promover a cultura gamer no Brasil.")

@bot.command()
async def ultimosresultados(ctx):
    ultimos_resultados = obter_ultimos_resultados_furia()
    await ctx.send(f"Últimos resultados da FURIA:\n{ultimos_resultados}")

@bot.command()
async def torneioatual(ctx):
    torneio_atual = obter_torneio_atual_furia()  # Corrigido o nome da função
    await ctx.send(f"Torneio atual da FURIA:\n{torneio_atual}")

@bot.command(name='help')
async def custom_help(ctx):
    ajuda = (
        "**🤖 Comandos disponíveis do FURIA Bot:**\n\n"
        "🔹 !visaogeral - Visão geral sobre a FURIA Esports.\n"
        "🔹 !membros - Lista atual dos jogadores da equipe de CS.\n"
        "🔹 !ultimosresultados - Mostra os últimos resultados da FURIA (dinâmico).\n"
        "🔹 !torneioatual - Mostra o torneio atual da FURIA (dinâmico).\n"
        "🔹 !projetos - Fala sobre os projetos e iniciativas da FURIA.\n"
        "🔹 !redes - Mostra as redes sociais oficiais da FURIA.\n"
        "🔹 !mascote - Mostra o mascote da FURIA.\n"
        "\n*Use ! antes de cada comando para ativar.*"
    )
    await ctx.send(ajuda)

# Rodando o bot com o token (AQUI você precisa colocar o token do seu bot)
bot.run('MTM2NzE1NjQ4OTE1NTc3MjUyOA.GpZFeX.wV5mUi5pA5-7lzEWCzwn_43PLiQgClp7qXuBig')