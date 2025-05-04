import discord
from discord.ext import commands
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

def obter_ultimos_resultados_furia(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    resultados = []


    eventos = soup.find_all('thead')
    for evento in eventos:

        th = evento.find('th', class_='text-ellipsis')
        if not th:
            continue
        torneio = th.get_text(strip=True)

        tbody = evento.find_next_sibling('tbody')
        if not tbody:
            continue

        for row in tbody.find_all('tr', class_='team-row'):
            cols = row.find_all('td')
            if len(cols) < 2:
                continue

            date_span = cols[0].find('span')
            if date_span and date_span.has_attr('data-unix'):
                timestamp = int(date_span['data-unix']) / 1000
                date = datetime.fromtimestamp(timestamp).strftime('%d/%m/%Y')
            else:
                date = 'Data desconhecida'

            team_cells = cols[1].find_all('div', class_='team-flex')
            if len(team_cells) < 2:
                continue
            team1 = team_cells[0].find('a', class_='team-name').get_text(strip=True)
            team2 = team_cells[1].find('a', class_='team-name').get_text(strip=True)

            score_cell = cols[1].find('div', class_='score-cell')
            if score_cell:
                scores = score_cell.find_all('span', class_='score')
                if len(scores) >= 2:
                    score1 = scores[0].get_text(strip=True)
                    score2 = scores[1].get_text(strip=True)
                    resultado = f'**{score1}**:{score2}'
                else:
                    resultado = 'Placar indisponível'
            else:
                resultado = 'Placar indisponível'

            if team1.upper() == 'FURIA':
                adversario = team2
                placar1 = score1
                placar2 = score2
            else:
                adversario = team1
                placar1 = score2
                placar2 = score1

            resultados.append({
                'data': date,
                'adversario': adversario,
                'placar1': placar1,
                'placar2': placar2,
                'torneio': torneio
            })

    return resultados

def obter_ranking_furia(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    try:
        ranking_tags = soup.find_all('div', class_='profile-team-stat')

        valve_ranking = None
        world_ranking = None

        for tag in ranking_tags:
            if tag.find('b') and 'Valve ranking' in tag.find('b').text:
                valve_ranking = tag.find('span', class_='right').get_text(strip=True)

            if tag.find('b') and 'World ranking' in tag.find('b').text:
                world_ranking = tag.find('span', class_='right').get_text(strip=True)

        if valve_ranking and world_ranking:
            return f"Ranking da Valve: {valve_ranking}\nRanking Mundial: {world_ranking}"
        else:
            return "Erro ao obter o ranking. Verifique se as tags mudaram no site."

    except Exception as e:
        return f"Erro ao obter o ranking: {e}"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

bot.remove_command('help')

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
    html_content = '''(<table class="table-container match-table">
                  <thead>
                    <tr>
                      <th class="date-cell">Date</th>
                      <th class="team-center-cell">Matches</th>
                      <th class="stats-button-cell"></th>
                    </tr>
                  </thead>
                  <thead>
                    <tr class="event-header-cell">
                      <th class="text-ellipsis" colspan="3"><a href="/events/8044/pgl-bucharest-2025" class="a-reset">PGL Bucharest 2025 - 12-14th</a></th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr class="team-row">
                      <td class="date-cell"><span data-time-format="dd/MM/yyyy" data-unix="1744203000000">09/04/2025</span></td>
                      <td class="team-center-cell">
                        <div class="team-flex lost"><a href="/team/8297/furia" class="team-name team-1">FURIA</a><span class="team-logo-container"><a href="/team/8297/furia"><img alt="FURIA" src="https://img-cdn.hltv.org/teamlogo/mvNQc4csFGtxXk5guAh8m1.svg?ixlib=java-2.1.0&amp;s=11e5056829ad5d6c06c5961bbe76d20c" class="team-logo" title="FURIA"></a></span></div>
                        <div class="score-cell"><span class="score lost">0</span><span class="score-divider">:</span><span class="score ">2</span></div>
                        <div class="team-flex "><span class="team-logo-container"><a href="/team/6248/the-mongolz"><img alt="The MongolZ" src="https://img-cdn.hltv.org/teamlogo/bRk2sh_tSTO6fq1GLhgcal.png?ixlib=java-2.1.0&amp;w=50&amp;s=8b08e53858eb817852ae74b30a30151d" class="team-logo" title="The MongolZ"></a></span><a href="/team/6248/the-mongolz" class="team-name team-2">The MongolZ</a></div>
                      </td>
                      <td class="stats-button-cell"><a href="/matches/2381321/furia-vs-the-mongolz-pgl-bucharest-2025" class="stats-button">Match</a></td>
                    </tr>
                    <tr class="team-row">
                      <td class="date-cell"><span data-time-format="dd/MM/yyyy" data-unix="1744103100000">08/04/2025</span></td>
                      <td class="team-center-cell">
                        <div class="team-flex lost"><a href="/team/8297/furia" class="team-name team-1">FURIA</a><span class="team-logo-container"><a href="/team/8297/furia"><img alt="FURIA" src="https://img-cdn.hltv.org/teamlogo/mvNQc4csFGtxXk5guAh8m1.svg?ixlib=java-2.1.0&amp;s=11e5056829ad5d6c06c5961bbe76d20c" class="team-logo" title="FURIA"></a></span></div>
                        <div class="score-cell"><span class="score lost">0</span><span class="score-divider">:</span><span class="score ">2</span></div>
                        <div class="team-flex "><span class="team-logo-container"><a href="/team/5378/virtuspro"><img alt="Virtus.pro" src="https://img-cdn.hltv.org/teamlogo/yZ6Bpuui1rW3jocXQ68XgZ.svg?ixlib=java-2.1.0&amp;s=f39be1d3e7baf30a4e7f0b1216720875" class="team-logo" title="Virtus.pro"></a></span><a href="/team/5378/virtuspro" class="team-name team-2">Virtus.pro</a></div>
                      </td>
                      <td class="stats-button-cell"><a href="/matches/2381310/furia-vs-virtuspro-pgl-bucharest-2025" class="stats-button">Match</a></td>
                    </tr>
                    <tr class="team-row">
                      <td class="date-cell"><span data-time-format="dd/MM/yyyy" data-unix="1744034700000">07/04/2025</span></td>
                      <td class="team-center-cell">
                        <div class="team-flex lost"><a href="/team/8297/furia" class="team-name team-1">FURIA</a><span class="team-logo-container"><a href="/team/8297/furia"><img alt="FURIA" src="https://img-cdn.hltv.org/teamlogo/mvNQc4csFGtxXk5guAh8m1.svg?ixlib=java-2.1.0&amp;s=11e5056829ad5d6c06c5961bbe76d20c" class="team-logo" title="FURIA"></a></span></div>
                        <div class="score-cell"><span class="score lost">1</span><span class="score-divider">:</span><span class="score ">2</span></div>
                        <div class="team-flex "><span class="team-logo-container"><a href="/team/5005/complexity"><img alt="Complexity" src="https://img-cdn.hltv.org/teamlogo/mYH7ldcjUjr02R21SLk_pE.png?ixlib=java-2.1.0&amp;w=50&amp;s=32d8d589138305e40137163405e3d598" class="team-logo day-only" title="Complexity"><img alt="Complexity" src="https://img-cdn.hltv.org/teamlogo/HP3QlPseFLIDHNmZjeyA9A.png?ixlib=java-2.1.0&amp;w=50&amp;s=1501bcedcd47063f56d6611756d1b80a" class="team-logo night-only" title="Complexity"></a></span><a href="/team/5005/complexity" class="team-name team-2">Complexity</a></div>
                      </td>
                      <td class="stats-button-cell"><a href="/matches/2381306/furia-vs-complexity-pgl-bucharest-2025" class="stats-button">Match</a></td>
                    </tr>
                    <tr class="team-row">
                      <td class="date-cell"><span data-time-format="dd/MM/yyyy" data-unix="1743953700000">06/04/2025</span></td>
                      <td class="team-center-cell">
                        <div class="team-flex "><a href="/team/8297/furia" class="team-name team-1">FURIA</a><span class="team-logo-container"><a href="/team/8297/furia"><img alt="FURIA" src="https://img-cdn.hltv.org/teamlogo/mvNQc4csFGtxXk5guAh8m1.svg?ixlib=java-2.1.0&amp;s=11e5056829ad5d6c06c5961bbe76d20c" class="team-logo" title="FURIA"></a></span></div>
                        <div class="score-cell"><span class="score ">2</span><span class="score-divider">:</span><span class="score lost">0</span></div>
                        <div class="team-flex lost"><span class="team-logo-container"><a href="/team/12916/betclic"><img alt="Betclic" src="https://img-cdn.hltv.org/teamlogo/iX5wi-ZLkdHTARnXcMEvZF.png?ixlib=java-2.1.0&amp;w=50&amp;s=d543c7f38ede96ef911a66c407b6b6cd" class="team-logo" title="Betclic"></a></span><a href="/team/12916/betclic" class="team-name team-2">Betclic</a></div>
                      </td>
                      <td class="stats-button-cell"><a href="/matches/2381258/furia-vs-betclic-pgl-bucharest-2025" class="stats-button">Match</a></td>
                    </tr>
                    <tr class="tr-seperator"></tr>
                  </tbody>
                  <thead>
                    <tr class="event-header-cell">
                      <th class="text-ellipsis" colspan="3"><a href="/events/7904/blast-open-lisbon-2025" class="a-reset">BLAST Open Lisbon 2025 - 13-16th</a></th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr class="team-row">
                      <td class="date-cell"><span data-time-format="dd/MM/yyyy" data-unix="1742649600000">22/03/2025</span></td>
                      <td class="team-center-cell">
                        <div class="team-flex lost"><a href="/team/8297/furia" class="team-name team-1">FURIA</a><span class="team-logo-container"><a href="/team/8297/furia"><img alt="FURIA" src="https://img-cdn.hltv.org/teamlogo/mvNQc4csFGtxXk5guAh8m1.svg?ixlib=java-2.1.0&amp;s=11e5056829ad5d6c06c5961bbe76d20c" class="team-logo" title="FURIA"></a></span></div>
                        <div class="score-cell"><span class="score lost">1</span><span class="score-divider">:</span><span class="score ">2</span></div>
                        <div class="team-flex "><span class="team-logo-container"><a href="/team/12376/m80"><img alt="M80" src="https://img-cdn.hltv.org/teamlogo/U6ziW17pgYxsxR_WQJ_9-V.png?ixlib=java-2.1.0&amp;w=50&amp;s=c26471695a9e28f1c08dd5cf856ecb55" class="team-logo" title="M80"></a></span><a href="/team/12376/m80" class="team-name team-2">M80</a></div>
                      </td>
                      <td class="stats-button-cell"><a href="/matches/2380117/m80-vs-furia-blast-open-lisbon-2025" class="stats-button">Match</a></td>
                    </tr>
                    <tr class="team-row">
                      <td class="date-cell"><span data-time-format="dd/MM/yyyy" data-unix="1742499900000">20/03/2025</span></td>
                      <td class="team-center-cell">
                        <div class="team-flex lost"><a href="/team/8297/furia" class="team-name team-1">FURIA</a><span class="team-logo-container"><a href="/team/8297/furia"><img alt="FURIA" src="https://img-cdn.hltv.org/teamlogo/mvNQc4csFGtxXk5guAh8m1.svg?ixlib=java-2.1.0&amp;s=11e5056829ad5d6c06c5961bbe76d20c" class="team-logo" title="FURIA"></a></span></div>
                        <div class="score-cell"><span class="score lost">0</span><span class="score-divider">:</span><span class="score ">2</span></div>
                        <div class="team-flex "><span class="team-logo-container"><a href="/team/4608/natus-vincere"><img alt="Natus Vincere" src="https://img-cdn.hltv.org/teamlogo/9iMirAi7ArBLNU8p3kqUTZ.svg?ixlib=java-2.1.0&amp;s=4dd8635be16122656093ae9884675d0c" class="team-logo" title="Natus Vincere"></a></span><a href="/team/4608/natus-vincere" class="team-name team-2">Natus Vincere</a></div>
                      </td>
                      <td class="stats-button-cell"><a href="/matches/2380007/natus-vincere-vs-furia-blast-open-lisbon-2025" class="stats-button">Match</a></td>
                    </tr>
                    <tr class="tr-seperator"></tr>
                  </tbody>
                  <thead>
                    <tr class="event-header-cell">
                      <th class="text-ellipsis" colspan="3"><a href="/events/8292/esl-pro-league-season-21" class="a-reset">ESL Pro League Season 21 - 12-14th</a></th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr class="team-row">
                      <td class="date-cell"><span data-time-format="dd/MM/yyyy" data-unix="1741629600000">10/03/2025</span></td>
                      <td class="team-center-cell">
                        <div class="team-flex lost"><a href="/team/8297/furia" class="team-name team-1">FURIA</a><span class="team-logo-container"><a href="/team/8297/furia"><img alt="FURIA" src="https://img-cdn.hltv.org/teamlogo/mvNQc4csFGtxXk5guAh8m1.svg?ixlib=java-2.1.0&amp;s=11e5056829ad5d6c06c5961bbe76d20c" class="team-logo" title="FURIA"></a></span></div>
                        <div class="score-cell"><span class="score lost">1</span><span class="score-divider">:</span><span class="score ">2</span></div>
                        <div class="team-flex "><span class="team-logo-container"><a href="/team/11283/falcons"><img alt="Falcons" src="https://img-cdn.hltv.org/teamlogo/4eJSkDQINNM6Tbs4WvLzkN.png?ixlib=java-2.1.0&amp;w=50&amp;s=d8c857ea47046f61eca695beab0d12ef" class="team-logo" title="Falcons"></a></span><a href="/team/11283/falcons" class="team-name team-2">Falcons</a></div>
                      </td>
                      <td class="stats-button-cell"><a href="/matches/2380068/falcons-vs-furia-esl-pro-league-season-21" class="stats-button">Match</a></td>
                    </tr>
                    <tr class="team-row">
                      <td class="date-cell"><span data-time-format="dd/MM/yyyy" data-unix="1741539600000">09/03/2025</span></td>
                      <td class="team-center-cell">
                        <div class="team-flex "><a href="/team/8297/furia" class="team-name team-1">FURIA</a><span class="team-logo-container"><a href="/team/8297/furia"><img alt="FURIA" src="https://img-cdn.hltv.org/teamlogo/mvNQc4csFGtxXk5guAh8m1.svg?ixlib=java-2.1.0&amp;s=11e5056829ad5d6c06c5961bbe76d20c" class="team-logo" title="FURIA"></a></span></div>
                        <div class="score-cell"><span class="score ">2</span><span class="score-divider">:</span><span class="score lost">1</span></div>
                        <div class="team-flex lost"><span class="team-logo-container"><a href="/team/9215/mibr"><img alt="MIBR" src="https://img-cdn.hltv.org/teamlogo/sVnH-oAf1J5TnMwoY4cxUC.png?ixlib=java-2.1.0&amp;w=50&amp;s=b0ef463fa0f1638bce72a89590fbaddf" class="team-logo day-only" title="MIBR"><img alt="MIBR" src="https://img-cdn.hltv.org/teamlogo/m_JQ624LNFHWiUY-25uuaE.png?ixlib=java-2.1.0&amp;w=50&amp;s=80a1e479dd1b15b974d3e2d5588763af" class="team-logo night-only" title="MIBR"></a></span><a href="/team/9215/mibr" class="team-name team-2">MIBR</a></div>
                      </td>
                      <td class="stats-button-cell"><a href="/matches/2380061/furia-vs-mibr-esl-pro-league-season-21" class="stats-button">Match</a></td>
                    </tr>
                    <tr class="team-row">
                      <td class="date-cell"><span data-time-format="dd/MM/yyyy" data-unix="1741454400000">08/03/2025</span></td>
                      <td class="team-center-cell">
                        <div class="team-flex lost"><a href="/team/8297/furia" class="team-name team-1">FURIA</a><span class="team-logo-container"><a href="/team/8297/furia"><img alt="FURIA" src="https://img-cdn.hltv.org/teamlogo/mvNQc4csFGtxXk5guAh8m1.svg?ixlib=java-2.1.0&amp;s=11e5056829ad5d6c06c5961bbe76d20c" class="team-logo" title="FURIA"></a></span></div>
                        <div class="score-cell"><span class="score lost">0</span><span class="score-divider">:</span><span class="score ">2</span></div>
                        <div class="team-flex "><span class="team-logo-container"><a href="/team/5973/liquid"><img alt="Liquid" src="https://img-cdn.hltv.org/teamlogo/JMeLLbWKCIEJrmfPaqOz4O.svg?ixlib=java-2.1.0&amp;s=c02caf90234d3a3ebac074c84ba1ea62" class="team-logo" title="Liquid"></a></span><a href="/team/5973/liquid" class="team-name team-2">Liquid</a></div>
                      </td>
                      <td class="stats-button-cell"><a href="/matches/2380054/liquid-vs-furia-esl-pro-league-season-21" class="stats-button">Match</a></td>
                    </tr>
                    <tr class="team-row">
                      <td class="date-cell"><span data-time-format="dd/MM/yyyy" data-unix="1741358700000">07/03/2025</span></td>
                      <td class="team-center-cell">
                        <div class="team-flex lost"><a href="/team/8297/furia" class="team-name team-1">FURIA</a><span class="team-logo-container"><a href="/team/8297/furia"><img alt="FURIA" src="https://img-cdn.hltv.org/teamlogo/mvNQc4csFGtxXk5guAh8m1.svg?ixlib=java-2.1.0&amp;s=11e5056829ad5d6c06c5961bbe76d20c" class="team-logo" title="FURIA"></a></span></div>
                        <div class="score-cell"><span class="score lost">1</span><span class="score-divider">:</span><span class="score ">2</span></div>
                        <div class="team-flex "><span class="team-logo-container"><a href="/team/4494/mouz"><img alt="MOUZ" src="https://img-cdn.hltv.org/teamlogo/IejtXpquZnE8KqYPB1LNKw.svg?ixlib=java-2.1.0&amp;s=7fd33b8def053fbfd8fdbb58e3bdcd3c" class="team-logo" title="MOUZ"></a></span><a href="/team/4494/mouz" class="team-name team-2">MOUZ</a></div>
                      </td>
                      <td class="stats-button-cell"><a href="/matches/2380042/mouz-vs-furia-esl-pro-league-season-21" class="stats-button">Match</a></td>
                    </tr>
                    <tr class="tr-seperator"></tr>
                  </tbody>
                  <thead>
                    <tr class="event-header-cell">
                      <th class="text-ellipsis" colspan="3"><a href="/events/8035/esl-pro-league-season-21-stage-1" class="a-reset">ESL Pro League Season 21 Stage 1 - 6-8th</a></th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr class="team-row">
                      <td class="date-cell"><span data-time-format="dd/MM/yyyy" data-unix="1741204200000">05/03/2025</span></td>
                      <td class="team-center-cell">
                        <div class="team-flex "><a href="/team/8297/furia" class="team-name team-1">FURIA</a><span class="team-logo-container"><a href="/team/8297/furia"><img alt="FURIA" src="https://img-cdn.hltv.org/teamlogo/mvNQc4csFGtxXk5guAh8m1.svg?ixlib=java-2.1.0&amp;s=11e5056829ad5d6c06c5961bbe76d20c" class="team-logo" title="FURIA"></a></span></div>
                        <div class="score-cell"><span class="score ">2</span><span class="score-divider">:</span><span class="score lost">1</span></div>
                        <div class="team-flex lost"><span class="team-logo-container"><a href="/team/12376/m80"><img alt="M80" src="https://img-cdn.hltv.org/teamlogo/U6ziW17pgYxsxR_WQJ_9-V.png?ixlib=java-2.1.0&amp;w=50&amp;s=c26471695a9e28f1c08dd5cf856ecb55" class="team-logo" title="M80"></a></span><a href="/team/12376/m80" class="team-name team-2">M80</a></div>
                      </td>
                      <td class="stats-button-cell"><a href="/matches/2380038/furia-vs-m80-esl-pro-league-season-21-stage-1" class="stats-button">Match</a></td>
                    </tr>
                    <tr class="team-row">
                      <td class="date-cell"><span data-time-format="dd/MM/yyyy" data-unix="1741116300000">04/03/2025</span></td>
                      <td class="team-center-cell">
                        <div class="team-flex "><a href="/team/8297/furia" class="team-name team-1">FURIA</a><span class="team-logo-container"><a href="/team/8297/furia"><img alt="FURIA" src="https://img-cdn.hltv.org/teamlogo/mvNQc4csFGtxXk5guAh8m1.svg?ixlib=java-2.1.0&amp;s=11e5056829ad5d6c06c5961bbe76d20c" class="team-logo" title="FURIA"></a></span></div>
                        <div class="score-cell"><span class="score ">2</span><span class="score-divider">:</span><span class="score lost">1</span></div>
                        <div class="team-flex lost"><span class="team-logo-container"><a href="/team/6673/nrg"><img alt="NRG" src="https://img-cdn.hltv.org/teamlogo/SJZaPBCyZssru-pUDS3aZe.png?ixlib=java-2.1.0&amp;w=50&amp;s=5f4ca255d90b4ea7092882834bbf1bdc" class="team-logo" title="NRG"></a></span><a href="/team/6673/nrg" class="team-name team-2">NRG</a></div>
                      </td>
                      <td class="stats-button-cell"><a href="/matches/2380035/furia-vs-nrg-esl-pro-league-season-21-stage-1" class="stats-button">Match</a></td>
                    </tr>
                    <tr class="team-row">
                      <td class="date-cell"><span data-time-format="dd/MM/yyyy" data-unix="1741015200000">03/03/2025</span></td>
                      <td class="team-center-cell">
                        <div class="team-flex lost"><a href="/team/8297/furia" class="team-name team-1">FURIA</a><span class="team-logo-container"><a href="/team/8297/furia"><img alt="FURIA" src="https://img-cdn.hltv.org/teamlogo/mvNQc4csFGtxXk5guAh8m1.svg?ixlib=java-2.1.0&amp;s=11e5056829ad5d6c06c5961bbe76d20c" class="team-logo" title="FURIA"></a></span></div>
                        <div class="score-cell"><span class="score lost">0</span><span class="score-divider">:</span><span class="score ">2</span></div>
                        <div class="team-flex "><span class="team-logo-container"><a href="/team/9215/mibr"><img alt="MIBR" src="https://img-cdn.hltv.org/teamlogo/sVnH-oAf1J5TnMwoY4cxUC.png?ixlib=java-2.1.0&amp;w=50&amp;s=b0ef463fa0f1638bce72a89590fbaddf" class="team-logo day-only" title="MIBR"><img alt="MIBR" src="https://img-cdn.hltv.org/teamlogo/m_JQ624LNFHWiUY-25uuaE.png?ixlib=java-2.1.0&amp;w=50&amp;s=80a1e479dd1b15b974d3e2d5588763af" class="team-logo night-only" title="MIBR"></a></span><a href="/team/9215/mibr" class="team-name team-2">MIBR</a></div>
                      </td>
                      <td class="stats-button-cell"><a href="/matches/2380026/furia-vs-mibr-esl-pro-league-season-21-stage-1" class="stats-button">Match</a></td>
                    </tr>
                    <tr class="team-row">
                      <td class="date-cell"><span data-time-format="dd/MM/yyyy" data-unix="1740925800000">02/03/2025</span></td>
                      <td class="team-center-cell">
                        <div class="team-flex lost"><a href="/team/8297/furia" class="team-name team-1">FURIA</a><span class="team-logo-container"><a href="/team/8297/furia"><img alt="FURIA" src="https://img-cdn.hltv.org/teamlogo/mvNQc4csFGtxXk5guAh8m1.svg?ixlib=java-2.1.0&amp;s=11e5056829ad5d6c06c5961bbe76d20c" class="team-logo" title="FURIA"></a></span></div>
                        <div class="score-cell"><span class="score lost">1</span><span class="score-divider">:</span><span class="score ">2</span></div>
                        <div class="team-flex "><span class="team-logo-container"><a href="/team/10567/saw"><img alt="SAW" src="https://img-cdn.hltv.org/teamlogo/9vOlYp2U_z0vXPb9aLK-4r.png?ixlib=java-2.1.0&amp;w=50&amp;s=22abd048c4d198e504696f27e8ff68d1" class="team-logo day-only" title="SAW"><img alt="SAW" src="https://img-cdn.hltv.org/teamlogo/9vOlYp2U_z0vXPb9aLK-4r.png?invert=true&amp;ixlib=java-2.1.0&amp;sat=-100&amp;w=50&amp;s=6013ee655368f0f1a69cd0c2183ba332" class="team-logo night-only" title="SAW"></a></span><a href="/team/10567/saw" class="team-name team-2">SAW</a></div>
                      </td>
                      <td class="stats-button-cell"><a href="/matches/2380018/furia-vs-saw-esl-pro-league-season-21-stage-1" class="stats-button">Match</a></td>
                    </tr>
                    <tr class="team-row">
                      <td class="date-cell"><span data-time-format="dd/MM/yyyy" data-unix="1740841800000">01/03/2025</span></td>
                      <td class="team-center-cell">
                        <div class="team-flex "><a href="/team/8297/furia" class="team-name team-1">FURIA</a><span class="team-logo-container"><a href="/team/8297/furia"><img alt="FURIA" src="https://img-cdn.hltv.org/teamlogo/mvNQc4csFGtxXk5guAh8m1.svg?ixlib=java-2.1.0&amp;s=11e5056829ad5d6c06c5961bbe76d20c" class="team-logo" title="FURIA"></a></span></div>
                        <div class="score-cell"><span class="score ">2</span><span class="score-divider">:</span><span class="score lost">0</span></div>
                        <div class="team-flex lost"><span class="team-logo-container"><a href="/team/8840/lynn-vision"><img alt="Lynn Vision" src="https://img-cdn.hltv.org/teamlogo/vO_s8NWgDhLzqFsj6p9xTt.png?ixlib=java-2.1.0&amp;w=50&amp;s=1fd5c4b19dd9d173c7d1981614ba0094" class="team-logo" title="Lynn Vision"></a></span><a href="/team/8840/lynn-vision" class="team-name team-2">Lynn Vision</a></div>
                      </td>
                      <td class="stats-button-cell"><a href="/matches/2379996/furia-vs-lynn-vision-esl-pro-league-season-21-stage-1" class="stats-button">Match</a></td>
                    </tr>
                    <tr class="tr-seperator"></tr>
                  </tbody>
                  <thead>
                    <tr class="event-header-cell">
                      <th class="text-ellipsis" colspan="3"><a href="/events/8034/iem-katowice-2025" class="a-reset">IEM Katowice 2025 - 13-16th</a></th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr class="team-row">
                      <td class="date-cell"><span data-time-format="dd/MM/yyyy" data-unix="1738594800000">03/02/2025</span></td>
                      <td class="team-center-cell">
                        <div class="team-flex lost"><a href="/team/8297/furia" class="team-name team-1">FURIA</a><span class="team-logo-container"><a href="/team/8297/furia"><img alt="FURIA" src="https://img-cdn.hltv.org/teamlogo/mvNQc4csFGtxXk5guAh8m1.svg?ixlib=java-2.1.0&amp;s=11e5056829ad5d6c06c5961bbe76d20c" class="team-logo" title="FURIA"></a></span></div>
                        <div class="score-cell"><span class="score lost">1</span><span class="score-divider">:</span><span class="score ">2</span></div>
                        <div class="team-flex "><span class="team-logo-container"><a href="/team/6665/astralis"><img alt="Astralis" src="https://img-cdn.hltv.org/teamlogo/9bgXHp-oh1oaXr7F0mTGmd.svg?ixlib=java-2.1.0&amp;s=f567161ab183001be33948b98c4b2067" class="team-logo" title="Astralis"></a></span><a href="/team/6665/astralis" class="team-name team-2">Astralis</a></div>
                      </td>
                      <td class="stats-button-cell"><a href="/matches/2378901/furia-vs-astralis-iem-katowice-2025" class="stats-button">Match</a></td>
                    </tr>
                    <tr class="tr-seperator"></tr>
                  </tbody>
                </table>)''' 

    resultados = obter_ultimos_resultados_furia(html_content)
    if not resultados:
        await ctx.send("Não foi possível obter os resultados recentes da FURIA.")
        return

    mensagem = "**Últimos resultados da FURIA:**\n"
    for r in resultados:
        mensagem += f"{r['data']} - FURIA (**{r['placar1']}**) VS {r['adversario']} (**{r['placar2']}**) - {r['torneio']}\n"

    await ctx.send(mensagem)

@bot.command()
async def ranking(ctx):
    html_content = '''(<div class="standard-box profileTopBox clearfix">
                <div class="flex">
                  <div class="profile-team-container text-ellipsis">
                    <div class="profile-team-logo-container"><img alt="FURIA" src="https://img-cdn.hltv.org/teamlogo/mvNQc4csFGtxXk5guAh8m1.svg?ixlib=java-2.1.0&amp;s=11e5056829ad5d6c06c5961bbe76d20c" class="teamlogo" title="FURIA"></div>
                    <div class="profile-team-info">
                      <div class="team-country text-ellipsis"><img alt="Brazil" src="/img/static/flags/30x20/BR.gif" class="flag flag" title="Brazil"> Brazil</div>
                      <h1 class="profile-team-name text-ellipsis">FURIA</h1>
                    </div>
                  </div>
                  <div class="socialMediaButtons"><a href="https://www.twitter.com/i/user/894704535037513729" target="_blank"><i class="socialmedia custom-x"></i></a><a href="https://www.twitch.tv/furiatv" target="_blank"><i class="socialmedia fa twitch fa-twitch"></i></a><a href="https://www.instagram.com/furiagg" target="_blank"><i class="socialmedia fa instagram fa-instagram"></i></a></div>
                </div>
                <div class="profile-team-stats-container">
                  <div class="profile-team-stat-50-50">
                    <div class="profile-team-stat"><img src="/img/static/gfx/ranking/valve.png" loading="lazy" height="14" width="14" alt="Valve logo">
                      <div class="regional-wrapper"><b>Valve ranking</b>
                        <div class="regional-beta">Beta</div>
                      </div>
<span class="right"><a href="/valve-ranking/teams?teamId=8297">#20</a></span></div>
                    <div class="profile-team-stat"><img src="/img/static/gfx/ranking/hltv_day.png" class="day-only" loading="lazy" height="14" width="14" alt="HLTV logo"><img src="/img/static/gfx/ranking/hltv_night.png" class="night-only" loading="lazy" height="14" width="14" alt="HLTV logo"><b>World ranking</b><span class="right"><a href="/ranking/teams/2025/april/28/details/8297">#17</a></span></div>
                  </div>
                  <div class="profile-team-stat"><b>Weeks in top30 for core</b><span class="right">95</span></div>
                  <div class="profile-team-stat"><b>Average player age</b><span class="right">26.2</span></div>
                  <div class="profile-team-stat"><b>Coach</b><a href="/coach/24267/sidde" class="a-reset right"><img alt="Brazil" src="/img/static/flags/30x20/BR.gif" class="flag" title="Brazil"> Sid <span class="bold a-default">'sidde'</span> Macedo</a></div>
                </div>
              </div>)'''
    
    ranking = obter_ranking_furia(html_content)
    if not ranking:
        await ctx.send("Não foi possível obter o ranking atual da FURIA.")
        return
    
    await ctx.send(f"O ranking atual da FURIA é:\n{ranking}")


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

bot.run(TOKEN)
