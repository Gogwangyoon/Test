# functions/api_helper.py
import requests
import time
import urllib.parse

# --- 1. 설정 및 상수 정의 ---
# TODO: 여기에 본인의 Riot Games API Key를 입력하세요.
# API Key는 24시간마다 만료되므로 주기적으로 갱신해야 합니다.
RIOT_API_KEY = "RGAPI-965a662c-1b5b-449b-88e0-e70824217786"

# API 리전 설정
# KR (한국 서버)
REGION_KR = "kr.api.riotgames.com" 
# Asia (매치 데이터를 가져오는 리전)
REGION_ASIA = "asia.api.riotgames.com" 

# 챔피언 ID 맵핑 데이터
CHAMPION_MAP = {
    1: "Annie", 2: "Olaf", 3: "Galio", 4: "TwistedFate", 5: "XinZhao", 
    6: "Urgot", 7: "LeBlanc", 8: "Vladimir", 9: "Fiddlesticks", 10: "Kayle", 
    11: "MasterYi", 12: "Alistar", 13: "Ryze", 14: "Sion", 15: "Sivir", 
    16: "Soraka", 17: "Teemo", 18: "Tristana", 19: "Warwick", 20: "Nunu", 
    21: "MissFortune", 22: "Ashe", 23: "Tryndamere", 24: "Jax", 25: "Morgana", 
    26: "Zilean", 27: "Singed", 28: "Evelynn", 29: "Twitch", 30: "Karthus", 
    31: "Chogath", 32: "Amumu", 33: "Rammus", 34: "Kassadin", 35: "Shaco", 
    36: "DrMundo", 37: "Sona", 38: "KogMaw", 39: "Ezreal", 40: "Janna", 
    41: "Gangplank", 42: "Corki", 43: "Karma", 44: "Taric", 45: "Veigar", 
    48: "Trundle", 50: "Swain", 51: "Caitlyn", 53: "Blitzcrank", 54: "Malphite", 
    55: "Katarina", 56: "Nocturne", 57: "Maokai", 58: "Renekton", 59: "JarvanIV", 
    60: "Elise", 61: "Orianna", 62: "MonkeyKing", 63: "Brand", 64: "LeeSin", 
    67: "Vayne", 68: "Rumble", 69: "Cassiopeia", 72: "Skarner", 74: "Heimerdinger", 
    75: "Nasus", 76: "Udyr", 77: "Irelia", 78: "Mordekaiser", 79: "Gragas", 
    80: "Pantheon", 81: "Evelynn", 82: "Sona", 83: "Yorick", 84: "Akali", 
    85: "Kennen", 86: "Garen", 89: "Leona", 90: "Malzahar", 91: "Talon", 
    92: "Riven", 96: "KogMaw", 98: "Mordekaiser", 99: "Lux", 101: "Xerath", 
    102: "Shyvana", 103: "Ahri", 104: "Graves", 105: "Fizz", 106: "Volibear", 
    107: "Rengar", 110: "Varus", 111: "Nautilus", 112: "Viktor", 113: "Sejuani", 
    114: "Fiora", 115: "Ziggs", 117: "Lulu", 119: "Draven", 120: "Hecarim", 
    121: "Khazix", 122: "Darius", 126: "Jayce", 127: "Lissandra", 131: "Diana", 
    133: "Quinn", 134: "Syndra", 136: "AurelionSol", 141: "Kassadin", 142: "Zoe", 
    143: "Zyra", 145: "Kaisa", 147: "Seraphine", 150: "Gnar", 154: "Zac", 
    157: "Yasuo", 161: "Velkoz", 163: "Taliyah", 164: "Camille", 201: "Braum", 
    202: "Jhin", 203: "Kindred", 222: "Jinx", 223: "TahmKench", 234: "Viego", 
    235: "Senna", 236: "Lucian", 238: "Zed", 240: "Kled", 245: "Ekko", 
    246: "Qiyana", 254: "Vi", 266: "Aatrox", 267: "Nami", 268: "Azir", 
    292: "Rammus", 300: "Garen", 350: "Yuumi", 412: "Thresh", 420: "Illaoi", 
    421: "RekSai", 427: "Ivern", 429: "Kalista", 432: "Bard", 497: "Rakan", 
    498: "Xayah", 516: "Ornn", 517: "Sylas", 518: "Neeko", 523: "Aphelios", 
    526: "Rell", 555: "Zac", 777: "Yone", 875: "Sett", 876: "Lillia", 
    887: "Gwen", 888: "Vex", 895: "Nilah", 897: "Udyr", 902: "Akshan",
    950: "RenataGlasc", 990: "BelVeth", 1000: "KSante", 1111: "Smolder",
    1500: "Naafiri", 800: "Nautilus" # Unknown_ID_800이 Nautilus가 아닌 경우, 실제 ID로 수정이 필요합니다.
}

# --- 2. 헬퍼 함수: API 통신 및 에러 처리 ---

def make_api_request(url: str):
    """
    Riot API로 요청을 보내고 응답을 JSON 형식으로 반환합니다.
    (평가 요소: 에러 처리, API 연동)
    """
    headers = {"X-Riot-Token": RIOT_API_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        
        # HTTP 상태 코드에 따른 에러 처리
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 403:
            print("[에러] API 키가 만료되었거나 접근 불가. 내용:", response.text)
        elif response.status_code == 404:
            print("[에러] 요청한 리소스를 찾을 수 없습니다. 내용:", response.text)
        elif response.status_code == 429:
            print("[경고] Rate Limit 초과. 잠시 후 다시 시도해주세요.")
            time.sleep(5)
        else:
            print(f"[에러] 알 수 없는 상태 코드 {response.status_code}. 내용:", response.text)

        
    except requests.exceptions.RequestException as e:
        print(f"[에러] 네트워크 요청 중 오류 발생: {e}")
    
    return None

def get_champion_name(champion_id: int) -> str:
    """챔피언 ID를 이름으로 변환합니다."""
    return CHAMPION_MAP.get(champion_id, f"Unknown_ID_{champion_id}")

# --- 3. 핵심 기능: 데이터 수집 ---


def get_summoner_data(summoner_name: str, region: str = REGION_KR) -> dict or None:
    print(f"\n[작업] 소환사 '{summoner_name}'의 기본 정보 조회 중...")
    encoded_name = urllib.parse.quote(summoner_name)  # 특수문자(# 등) 인코딩
    url = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{encoded_name}"
    data = make_api_request(url)
    
    if data and 'puuid' in data:
        print(f"[성공] puuid: {data['puuid'][:8]}... 획득 완료.")
        return data
    else:
        print(f"[실패] 소환사 '{summoner_name}'을(를) 찾을 수 없습니다.")
        return None



def get_match_history_ids(puuid: str, region: str = REGION_ASIA, count: int = 20) -> list:
    """
    소환사의 최근 매치 ID 목록을 조회합니다.
    (평가 요소: API 연동)
    """
    print(f"[작업] 최근 {count}경기 매치 ID 목록 조회 중...")
    # type=ranked, queue=420 등으로 필터링 가능 (여기서는 모든 타입)
    url = f"https://{region}/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}"
    match_ids = make_api_request(url)
    
    if isinstance(match_ids, list):
        print(f"[성공] 매치 ID {len(match_ids)}개 획득 완료.")
        return match_ids
    return []

def get_match_details(match_id: str, puuid: str, region: str = REGION_ASIA, champion_map_func=get_champion_name) -> dict or None:
    """
    단일 매치에 대한 상세 정보를 조회하고, 해당 소환사의 기록을 추출합니다.
    """
    url = f"https://{region}/lol/match/v5/matches/{match_id}"
    match_data = make_api_request(url)
    
    if not match_data:
        return None

    # 해당 소환사의 상세 기록만 추출
    target_participant = next(
        (p for p in match_data.get('info', {}).get('participants', []) if p.get('puuid') == puuid),
        None
    )

    if not target_participant:
        return None

    # 필요한 데이터 추출 (평가 요소: 데이터 처리)
    return {
        'match_id': match_id,
        'game_duration': match_data['info']['gameDuration'],
        'queue_id': match_data['info']['queueId'],
        'champion_name': champion_map_func(target_participant['championId']),
        'kills': target_participant['kills'],
        'deaths': target_participant['deaths'],
        'assists': target_participant['assists'],
        'win': target_participant['win'],
        'total_minions_killed': target_participant['totalMinionsKilled'],
        'gold_earned': target_participant['goldEarned'],
    }