import requests
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime

# Configuración
BASE_URL = "https://www.coretennis.net"
WEEKLY_URLS = [
    "https://www.coretennis.net/majic/pageServer/1z0100000y/en/Junior-Girls.html",
]
# Lista de URLs de torneos específicos para incluir manualmente
SPECIFIC_TOURNAMENT_URLS = [
"https://www.coretennis.net/majic/pageServer/0r0100000c/en/tid/121056/Tournament-Rounds.html",
"https://www.coretennis.net/majic/pageServer/0r0100000c/en/tid/121057/Tournament-Rounds.html",
]
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "es-ES,es;q=0.9"
}

# Mapeo de números de mes a nombres en español
MONTH_NAMES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}

SESSION = requests.Session()
SESSION.headers.update(HEADERS)

def get_country_flag(country_code):
    flag_emojis = {
    'USA': '🇺🇸', 'ARG': '🇦🇷', 'COL': '🇨🇴', 'FRA': '🇫🇷', 
    'ITA': '🇮🇹', 'ESP': '🇪🇸', 'SUI': '🇨🇭', 'JPN': '🇯🇵',
    'RUS': '🇷🇺', 'GER': '🇩🇪', 'BRA': '🇧🇷', 'CHN': '🇨🇳',
    'AUS': '🇦🇺', 'GBR': '🇬🇧', 'CAN': '🇨🇦', 'BEL': '🇧🇪',
    'NED': '🇳🇱', 'SWE': '🇸🇪', 'CZE': '🇨🇿', 'SRB': '🇷🇸',
    'CRO': '🇭🇷', 'UKR': '🇺🇦', 'ROU': '🇷🇴', 'POL': '🇵🇱',
    'SVK': '🇸🇰', 'KAZ': '🇰🇿', 'BLR': '🇧🇾', 'HUN': '🇭🇺',
    'GRE': '🇬🇷', 'TUR': '🇹🇷', 'ISR': '🇮🇱', 'RSA': '🇿🇦',
    'SLO': '🇸🇮', 'BUL': '🇧🇬', 'LAT': '🇱🇻', 'EST': '🇪🇪',
    'TUN': '🇹🇳', 'CYP': '🇨🇾', 'EGY': '🇪🇬', 'UNK': '🏳️',
    'LTU': '🇱🇹', 'IND': '🇮🇳', 'THA': '🇹🇭', 'KOR': '🇰🇷',
    'MDA': '🇲🇩', 'AUT': '🇦🇹', 'GEO': '🇬🇪', 'MEX': '🇲🇽',
    'PER': '🇵🇪', 'CHI': '🇨🇱', 'VEN': '🇻🇪', 'ECU': '🇪🇨',
    'BOL': '🇧🇴', 'PRY': '🇵🇾', 'URY': '🇺🇾', 'PRT': '🇵🇹',
    'NOR': '🇳🇴', 'FIN': '🇫🇮', 'DEN': '🇩🇰', 'IRL': '🇮🇪',
    'ISL': '🇮🇸', 'MAR': '🇲🇦', 'ALG': '🇩🇿', 'NGA': '🇳🇬',
    'KEN': '🇰🇪', 'PHL': '🇵🇭', 'SGP': '🇸🇬', 'MYS': '🇲🇾',
    'IDN': '🇮🇩', 'PAK': '🇵🇰', 'BGD': '🇧🇩', 'NPL': '🇳🇵',
    'LKA': '🇱🇰', 'UAE': '🇦🇪', 'QAT': '🇶🇦', 'SAU': '🇸🇦',
    'NZL': '🇳🇿', 'ZAF': '🇿🇦', 'CMR': '🇨🇲', 'GHA': '🇬🇭',
    'SEN': '🇸🇳', 'CIV': '🇨🇮', 'UGA': '🇺🇬', 'TZA': '🇹🇿',
    'ZWE': '🇿🇼', 'MOZ': '🇲🇿', 'ANG': '🇦🇴', 'NAM': '🇳🇦',
    'JAM': '🇯🇲', 'DOM': '🇩🇴', 'PRI': '🇵🇷', 'CUB': '🇨🇺',
    'HTI': '🇭🇹', 'PAN': '🇵🇦', 'CRI': '🇨🇷', 'NIC': '🇳🇮',
    'HND': '🇭🇳', 'SLV': '🇸🇻', 'GTM': '🇬🇹', 'BLZ': '🇧🇿',
    'MNE': '🇲🇪', 'LBN': '🇱🇧', 'JOR': '🇯🇴', 'IRQ': '🇮🇶',
    'SYR': '🇸🇾', 'YEM': '🇾🇪', 'OMN': '🇴🇲', 'KWT': '🇰🇼',
    'BHR': '🇧🇭', 'ARM': '🇦🇲', 'AZE': '🇦🇿', 'KGZ': '🇰🇬',
    'TJK': '🇹🇯', 'UZB': '🇺🇿', 'TKM': '🇹🇲', 'AFG': '🇦🇫',
    'IRN': '🇮🇷', 'PSE': '🇵🇸', 'LBY': '🇱🇾', 'SDN': '🇸🇩',
    'ETH': '🇪🇹', 'SOM': '🇸🇴', 'DJI': '🇩🇯', 'ERI': '🇪🇷',
    'MDV': '🇲🇻', 'BTN': '🇧🇹', 'MMR': '🇲🇲', 'LAO': '🇱🇦',
    'KHM': '🇰🇭', 'VNM': '🇻🇳', 'TLS': '🇹🇱', 'BRN': '🇧🇳',
    'PNG': '🇵🇬', 'FJI': '🇫🇯', 'SLB': '🇸🇧', 'VUT': '🇻🇺',
    'WSM': '🇼🇸', 'TON': '🇹🇴', 'KIR': '🇰🇮', 'PLW': '🇵🇼',
    'FSM': '🇫🇲', 'MHL': '🇲🇭', 'NRU': '🇳🇷', 'TUV': '🇹🇻',
    'DMA': '🇩🇲', 'GRD': '🇬🇩', 'LCA': '🇱🇨', 'VCT': '🇻🇨',
    'KNA': '🇰🇳', 'ATG': '🇦🇬', 'BRB': '🇧🇧', 'LSO': '🇱🇸',
    'SWZ': '🇸🇿', 'MWI': '🇲🇼', 'COD': '🇨🇩', 'COG': '🇨🇬',
    'CAF': '🇨🇫', 'TCD': '🇹🇩', 'GNQ': '🇬🇶', 'GAB': '🇬🇦',
    'BEN': '🇧🇯', 'TGO': '🇹🇬', 'MLI': '🇲🇱', 'BFA': '🇧🇫',
    'NER': '🇳🇪', 'MRT': '🇲🇷', 'GNB': '🇬🇼', 'CPV': '🇨🇻',
    'STP': '🇸🇹', 'SYC': '🇸🇨', 'COM': '🇰🇲', 'MUS': '🇲🇺',
    'LIE': '🇱🇮', 'SMR': '🇸🇲', 'AND': '🇦🇩', 'MCO': '🇲🇨',
    'VAT': '🇻🇦', 'MAF': '🇲🇫', 'BLM': '🇧🇱', 'SPM': '🇵🇲',
    'WLF': '🇼🇫', 'PYF': '🇵🇫', 'NCL': '🇳🇨', 'COK': '🇨🇰',
    'TKL': '🇹🇰', 'NIU': '🇳🇺', 'PCN': '🇵🇳', 'HMD': '🇭🇲',
    'ATA': '🇦🇶', 'BVT': '🇧🇻', 'IOT': '🇮🇴', 'ATF': '🇹🇫',
    'UMI': '🇺🇲', 'FLK': '🇫🇰', 'SGS': '🇬🇸', 'ESH': '🇪🇭',
    }
    return flag_emojis.get(country_code.upper(), '🏳️')

def clean_tournament_name(name):
    """Extrae solo el nombre básico del torneo para el archivo de salida"""
    name = re.sub(r'\(.*?\)', '', name)
    name = re.sub(r',\s*\d{4}-\d{2}-\d{2}', '', name)
    name = re.sub(r'Tennis Results$', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    
    category = ""
    if "J500" in name: category = "(J500)"
    if "J300" in name: category = "(J300)"
    elif "J200" in name: category = "(J200)"
    elif "J100" in name: category = "(J100)"
    elif "J60" in name: category = "(J60)"
    elif "J30" in name: category = "(J30)"
    elif "Australian Open" in name: category = "(Australian Open) 🏆"
    elif "Roland Garros" in name: category = "(Roland Garros) 🏆"
    elif "Wimbledon" in name: category = "(Wimbledon) 🏆"
    elif "US Open" in name: category = "(US Open) 🏆"
    
    main_name = name.replace(category, "").strip()
    main_name = re.sub(r',.*$', '', main_name).strip()
    
    return f"{main_name} {category}"

def get_tournament_name(soup):
    title_tag = soup.find('title')
    if title_tag:
        return clean_tournament_name(title_tag.text.split('|')[0].strip())
    return "TORNEO DESCONOCIDO"

def get_tournament_links(url):
    """Obtiene los enlaces de los torneos desde la página principal"""
    print(f"\nObteniendo enlaces de torneos de: {url}")
    
    try:
        response = SESSION.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        full_results_links = []
        for link in soup.find_all('a', class_='fullResults'):
            href = link.get('href')
            if href:
                full_link = href if href.startswith('http') else f"{BASE_URL}{href}"
                full_results_links.append(full_link)
        
        print(f"Se encontraron {len(full_results_links)} torneos")
        return full_results_links
    
    except Exception as e:
        print(f"Error al obtener enlaces de torneos: {str(e)}")
        return []

def extract_champion(soup):
    """Extrae a la campeona de la tabla de la final"""
    final_tables = soup.select('div.tabcontent table.round')
    if not final_tables:
        final_tables = soup.select('table.round')
    
    if not final_tables:
        return None
    
    final_table = final_tables[-1]
    
    # Buscar la fila del ganador (contiene td.winner)
    winner_row = None
    for row in final_table.select('tr'):
        if row.select_one('td.winner'):
            winner_row = row
            break
    
    if not winner_row:
        return None
    
    winner_cell = winner_row.select_one('td.winner a') or winner_row.select_one('td.player a')
    if not winner_cell:
        return None
    
    try:
        # Extraer nombre completo
        name_parts = winner_cell.get_text(strip=True).split(',')
        if len(name_parts) >= 2:
            last_name, first_name = [x.strip() for x in name_parts[:2]]
            full_name = f"{first_name} {last_name}"
        else:
            full_name = winner_cell.get_text(strip=True)
            last_name, first_name = full_name.split(' ', 1) if ' ' in full_name else (full_name, '')
        
        # Buscar la fila ORIGINAL del jugador para obtener su país
        player_row = None
        for row in final_table.select('tr'):
            player_link = row.select_one('td.player a')
            if player_link:
                player_name = player_link.get_text(strip=True)
                if (player_name == f"{last_name}, {first_name}" or 
                    player_name == full_name or 
                    (first_name and player_name.startswith(last_name))):
                    player_row = row
                    break
        
        country_code = "UNK"
        if player_row:
            country_span = player_row.select_one('td.ctry')
            if country_span:
                match = re.search(r'\[([A-Z]{3})\]', country_span.get_text(strip=True))
                if match:
                    country_code = match.group(1)
                else:
                    # Intentar extraer el código del país de otra forma
                    country_img = country_span.find('img')
                    if country_img and 'title' in country_img.attrs:
                        country_title = country_img['title'].upper()
                        if len(country_title) == 3:
                            country_code = country_title
        
        # Obtener año de nacimiento
        birth_year = None
        href = winner_cell.get('href', '')
        if href:
            if isinstance(href, list):
                href = href[0] if href else ''
            profile_url = f"{BASE_URL}{href}" if not href.startswith('http') else href
            
            try:
                profile_response = SESSION.get(profile_url, timeout=10)
                if profile_response.status_code == 200:
                    profile_soup = BeautifulSoup(profile_response.text, 'html.parser')
                    birth_text = profile_soup.get_text()
                    if "Born in" in birth_text:
                        match = re.search(r"Born in.*?(\d{4})", birth_text)
                        if match:
                            birth_year = match.group(1)
            except:
                pass
        
        return {
            'name': full_name,
            'country_code': country_code,
            'birth_year': birth_year or "N/A"
        }
    except Exception as e:
        print(f"Error extrayendo campeona: {str(e)}")
        return None

def process_tournament(url):
    """Procesa un torneo individual para extraer la campeona"""
    try:
        response = SESSION.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        tournament_name = get_tournament_name(soup)
        
        print(f"\nProcesando torneo: {tournament_name}")
        
        champion_data = extract_champion(soup)
        
        if champion_data:
            flag = get_country_flag(champion_data['country_code'])
            if champion_data['birth_year'] != "N/A":
                output_content = f"{flag} {champion_data['name']} [{champion_data['birth_year']}] {tournament_name.split()[-1]}"
            else:
                output_content = f"{flag} {champion_data['name']} {tournament_name.split()[-1]}"
            return output_content
        
        return None
        
    except Exception as e:
        print(f"Error procesando torneo: {str(e)}")
        return None

def get_month_from_url(url):
    """Extrae el mes de la URL"""
    match = re.search(r'date=(\d{4})(\d{2})', url)
    if match:
        year, month = int(match.group(1)), int(match.group(2))
        return MONTH_NAMES.get(month, f"Mes {month}")
    return "Fecha desconocida"

def main():
    print("Iniciando proceso completo...")
    
    # Diccionario para almacenar campeonas por mes y semana
    champions_data = {}
    
    for week_url in WEEKLY_URLS:
        month = get_month_from_url(week_url)
        if month not in champions_data:
            champions_data[month] = []
        
        print(f"\nProcesando semana: {week_url}")
        
        # Obtener enlaces de torneos para esta semana
        tournament_urls = get_tournament_links(week_url)
        
        if not tournament_urls:
            print(f"No se encontraron torneos para esta semana")
            champions_data[month].append([])  # Lista vacía para mantener el orden
            continue
        
        # Procesar cada torneo de esta semana
        week_champions = []
        for tournament_url in tournament_urls:
            champion = process_tournament(tournament_url)
            if champion:
                week_champions.append(champion)
        
        champions_data[month].append(week_champions)
    
    # Generar el output organizado por meses y semanas
    all_output = ""
    for month, weeks in champions_data.items():
        if any(weeks):  # Solo agregar meses con datos
            all_output += f"\n{month}:\n\n"
            
            for week in weeks:
                if week:  # Solo agregar semanas con campeonas
                    all_output += "\n".join(week) + "\n\n"
    
    if all_output:
        filename = "campeonas_junior_semanales.txt"
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(all_output)
        print(f"\n🎉 Resultados guardados en: {filename}")
        print("\n📄 Contenido del archivo:\n")
        print(all_output)
    else:
        print("\n⚠️ No se encontraron campeonas válidas en los torneos procesados")

if __name__ == "__main__":
    main()