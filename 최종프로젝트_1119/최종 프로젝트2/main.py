import time
import os
import sys
import pandas as pd
import math
import unicodedata # 💡 추가: 유니코드 처리를 위한 모듈 임포트

# 서브 모듈 임포트
sys.path.append(os.path.join(os.path.dirname(__file__), 'functions'))

import api_helper
import data_manager
import visualize

# 💡 Queue ID 매핑 데이터 정의 (게임 모드)
QUEUE_ID_MAP = {
    420: "개인/2인 랭크",
    430: "일반(솔로)",
    440: "자유 랭크",
    450: "무작위 총력전(칼바람)",
    400: "일반(드래프트)",
    700: "격전",
    800: "AI 대전 (초급)",
    810: "AI 대전 (중급)",
    820: "AI 대전 (고급)",
    900: "URF",
    1020: "단일 챔피언",
    1090: "팀 랭크 (TFT)",
    1100: "랭크 (TFT)",
    1300: "돌격! 넥서스",
    1400: "궁극기 주문서",
    1700: "아레나",
    # 다른 큐 ID는 필요에 따라 추가
}

# 💡 챔피언 이름 (영어 -> 한글) 변환 맵 정의
CHAMPION_NAME_KR_MAP = {
    "Ahri": "아리", "Corki": "코르키", "Taric": "타릭", "Ziggs": "직스",
    "Garen": "가렌", "Thresh": "쓰레쉬", "Annie": "애니", "Zed": "제드", "LeeSin": "리 신", 
    "Ashe": "애쉬", "MasterYi": "마스터 이", "Alistar": "알리스타", "Sivir": "시비르",
    "Olaf": "올라프", "Galio": "갈리오", "TwistedFate": "트위스티드 페이트", "XinZhao": "신 짜오", 
    "Urgot": "우르곳", "LeBlanc": "르블랑", "Vladimir": "블라디미르", "Fiddlesticks": "피들스틱", 
    "Kayle": "케일", "Ryze": "라이즈", "Sion": "사이온", "Soraka": "소라카", 
    "Teemo": "티모", "Tristana": "트리스타나", "Warwick": "워윅", "Nunu": "누누와 윌럼프", 
    "MissFortune": "미스 포츈", "Tryndamere": "트린다미어", "Jax": "잭스", "Morgana": "모르가나", 
    "Zilean": "질리언", "Singed": "신지드", "Evelynn": "이블린", "Twitch": "트위치", 
    "Karthus": "카서스", "Chogath": "초가스", "Amumu": "아무무", "Rammus": "람머스", 
    "Kassadin": "카사딘", "Shaco": "샤코", "DrMundo": "문도 박사", "Sona": "소나", 
    "KogMaw": "코그모", "Ezreal": "이즈리얼", "Janna": "잔나", "Gangplank": "갱플랭크", 
    "Karma": "카르마", "Veigar": "베이가", "Trundle": "트런들", "Swain": "스웨인", 
    "Caitlyn": "케이틀린", "Blitzcrank": "블리츠크랭크", "Malphite": "말파이트", 
    "Katarina": "카타리나", "Nocturne": "녹턴", "Maokai": "마오카이", "Renekton": "레넥톤", 
    "JarvanIV": "자르반 4세", "Elise": "엘리스", "Orianna": "오리아나", 
    "MonkeyKing": "오공", "Brand": "브랜드", "Vayne": "베인", "Rumble": "럼블", 
    "Cassiopeia": "카시오페아", "Skarner": "스카너", "Heimerdinger": "하이머딩거", 
    "Nasus": "나서스", "Udyr": "우디르", "Irelia": "이렐리아", "Mordekaiser": "모르데카이저", 
    "Gragas": "그라가스", "Pantheon": "판테온", "Yorick": "요릭", "Akali": "아칼리", 
    "Kennen": "케넨", "Leona": "레오나", "Malzahar": "말자하", "Talon": "탈론", 
    "Riven": "리븐", "Lux": "럭스", "Xerath": "제라스", "Shyvana": "쉬바나", 
    "Graves": "그레이브즈", "Fizz": "피즈", "Volibear": "볼리베어", "Rengar": "렝가", 
    "Varus": "바루스", "Nautilus": "노틸러스", "Viktor": "빅토르", "Sejuani": "세주아니", 
    "Fiora": "피오라", "Lulu": "룰루", "Draven": "드레이븐", "Hecarim": "헤카림", 
    "Khazix": "카직스", "Darius": "다리우스", "Jayce": "제이스", "Lissandra": "리산드라", 
    "Diana": "다이애나", "Quinn": "퀸", "Syndra": "신드라", "AurelionSol": "아우렐리온 솔", 
    "Zoe": "조이", "Zyra": "자이라", "Kaisa": "카이사", "Seraphine": "세라핀", 
    "Gnar": "나르", "Zac": "자크", "Yasuo": "야스오", "Velkoz": "벨코즈", 
    "Taliyah": "탈리야", "Camille": "카밀", "Braum": "브라움", "Jhin": "진", 
    "Kindred": "킨드레드", "Jinx": "징크스", "TahmKench": "탐 켄치", "Viego": "비에고", 
    "Senna": "세나", "Lucian": "루시안", "Zed": "제드", "Kled": "클레드", 
    "Ekko": "에코", "Qiyana": "키아나", "Vi": "바이", "Aatrox": "아트록스", 
    "Nami": "나미", "Azir": "아지르", "Illaoi": "일라오이", "RekSai": "렉사이", 
    "Ivern": "아이번", "Kalista": "칼리스타", "Bard": "바드", "Rakan": "라칸", 
    "Xayah": "자야", "Ornn": "오른", "Sylas": "사일러스", "Neeko": "니코", 
    "Aphelios": "아펠리오스", "Rell": "렐", "Yuumi": "유미", "Yone": "요네", 
    "Sett": "세트", "Lillia": "릴리아", "Gwen": "그웬", "Vex": "벡스", 
    "Nilah": "닐라", "Akshan": "아크샨", "RenataGlasc": "레나타 글라스크", 
    "BelVeth": "벨베스", "KSante": "크산테", "Smolder": "스몰더", "Naafiri": "나피리"
}


# 💡 게임 시간(초)을 시/분/초 문자열로 변환하는 함수
def format_game_duration(seconds):
    if pd.isna(seconds) or not isinstance(seconds, (int, float)):
        return "N/A"
    
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    
    # 시간이 0이면 '분:초' 형식으로 반환
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"

# --- 출력 포맷팅 유틸리티 함수 (한글 폭 계산) ---
def get_display_width(text):
    """
    한글(전각 문자)을 2칸 폭으로 계산하여 문자열의 출력 너비를 반환합니다.
    """
    width = 0
    for char in str(text):
        if unicodedata.east_asian_width(char) in ('F', 'W', 'A'): # Full-width, Wide, Ambiguous
            width += 2
        else: # Half-width
            width += 1
    return width
# --- 출력 포맷팅 유틸리티 함수 끝 ---


# --- 출력 포맷팅 함수 (글로벌 영역으로 이동) ---
def print_formatted_dataframe(df_head):
    """
    Pandas의 기본 출력 대신 수동으로 포맷팅하여 정렬 문제를 해결합니다. (한글 폭 계산 적용)
    """
    # 1. 각 컬럼의 최대 표시 폭 계산 (헤더 + 데이터)
    col_widths = {}
    for col in df_head.columns:
        # 헤더의 표시 폭 계산
        header_width = get_display_width(col)
        
        # 데이터의 최대 표시 폭 계산
        max_data_width = 0
        for data in df_head[col].astype(str):
            max_data_width = max(max_data_width, get_display_width(data))
        
        # 컬럼 너비는 헤더와 데이터 중 더 큰 값으로 설정
        col_widths[col] = max(header_width, max_data_width)
        
        # 숫자 컬럼 ('킬', '데스', '골드획득' 등)은 최소 너비 확보
        if col in ['킬', '데스', '어시스트', '미니언처치', '골드획득', '게임시간']:
            col_widths[col] = max(col_widths[col], 7) # 최소 7칸 확보 (숫자/시간은 여유 있게)
        
        # 승패 컬럼 ('승리')는 최소 너비 확보 (한글 2글자 = 4칸 + 여백)
        if col == '승리':
            col_widths[col] = max(col_widths[col], 6)

    # 2. 헤더 라인 포매팅
    index_width = len(str(df_head.index.max())) + 1
    header_line = " " * index_width
    separator_line = "-" * index_width
    
    for col in df_head.columns:
        # 헤더 텍스트를 담을 실제 폭
        col_text_width = get_display_width(col)
        width = col_widths[col]
        padding_needed = width - col_text_width
        
        # 헤더는 가운데 정렬 (양쪽 패딩을 나눠서 적용)
        left_pad = padding_needed // 2
        right_pad = padding_needed - left_pad
        header_line += " " * left_pad + col + " " * right_pad + " "
        separator_line += f"{'-' * width} "

    print(header_line.rstrip())
    print(separator_line.rstrip())

    # 3. 데이터 라인 포매팅
    for index, row in df_head.iterrows():
        row_str = f"{index:<{index_width}} "
        for col in df_head.columns:
            value = str(row[col])
            width = col_widths[col]
            value_width = get_display_width(value)
            
            # 숫자 계열 및 승패 컬럼은 가운데 정렬 (보기 좋게)
            if col in ['킬', '데스', '어시스트', '미니언처치', '골드획득', '승리', '게임시간']:
                # 가운데 정렬 (폭 - 값 폭)만큼 패딩을 나눠서 추가
                padding_needed = width - value_width
                left_pad = padding_needed // 2
                right_pad = padding_needed - left_pad
                row_str += " " * left_pad + value + " " * right_pad + " "
            # 텍스트 계열 (게임모드, 챔피언)은 좌측 정렬
            else:
                # 좌측 정렬 (폭 - 값 폭)만큼 뒤에 공백 추가
                row_str += value + " " * (width - value_width) + " "
                
        print(row_str.rstrip())
    print("-" * 50)
# --- 출력 포맷팅 함수 끝 ---


# --- 데이터 관리 메뉴 ---
def data_management_menu():
    while True:
        print("\n" + "-" * 30)
        print(" [3] 데이터 관리 (CRUD) 메뉴")
        print("-" * 30)
        print(" 1. 기록 삭제 (Delete)")
        print(" 2. 사용자 메모 수정 (Update)")
        print(" 0. 메인 메뉴로 돌아가기")
        
        choice = input("메뉴 선택: ").strip()
        
        if choice == '0':
            break
        
        df = data_manager.load_match_data_from_csv()
        if df is None:
            continue
            
        if choice == '1':
            data_manager.delete_match_record(df)
        elif choice == '2':
            data_manager.update_match_memo(df)
        else:
            print("[경고] 잘못된 메뉴 선택입니다.")

# --- 통계/시각화 메뉴 ---
def analysis_menu():
    """
    통계 및 시각화 메뉴를 처리합니다.
    """
    while True:
        print("\n" + "-" * 30)
        print(" [2] 데이터 통계/시각화 메뉴")
        print("-" * 30)
        print(" 1. KDA 분포 시각화 (막대 그래프 + 챔피언 승률)")
        print(" 0. 메인 메뉴로 돌아가기")
        
        choice = input("메뉴 선택: ").strip()
        
        if choice == '0':
            break
        
        df = data_manager.load_match_data_from_csv()
        if df is None:
            # CSV가 없거나 비어있으면 안내 후 루프 계속
            print("[경고] 전적 데이터가 없습니다. 먼저 1번 메뉴에서 소환사 전적을 조회/저장하세요.")
            continue
            
        if choice == '1':
            visualize.plot_kda_distribution(df)
        else:
            print("[경고] 잘못된 메뉴 선택입니다.")


# --- 메인 프로그램 ---
def main():
    print("=" * 40)
    print("  LoL 전적 분석 시스템 (v1.2)")
    print("=" * 40)
    
    if api_helper.RIOT_API_KEY == "YOUR_RIOT_API_KEY_HERE":
        print("\n[❗필수] RIOT_API_KEY를 설정 후 다시 실행해 주세요.\n")
        return
        
    while True:
        print("\n" + "=" * 40)
        print(" [메인 메뉴]")
        print(" 1. 소환사 전적 조회 및 CSV 저장 (CRUD - Create/Read)")
        print(" 2. 데이터 통계 및 시각화")
        print(" 3. 데이터 관리 (CRUD - Update/Delete)")
        print(" q. 프로그램 종료")
        print("=" * 40)
        
        main_choice = input("메뉴 선택: ").strip()
        
        if main_choice.lower() == 'q':
            print("프로그램을 종료합니다.")
            break
        
        elif main_choice == '1':
            # --------------------------
            # 하드코딩된 소환사 정보 사용
            summoner_info = {
                "puuid": "RQK4iP39WLFMigeczb78DmfHDkEezjok6d26LRYNUIBWvZqTR2WDxbw2CmMJ3Q1zkKcSmIf98ru7zQ",
                "gameName": "MVP",
                "tagLine": "0414"
            }
            puuid = summoner_info['puuid']
            # --------------------------

            # 매치 ID 조회
            match_ids = api_helper.get_match_history_ids(puuid, count=10)
            if not match_ids:
                print("[경고] 해당 소환사의 최근 매치 기록을 찾을 수 없습니다.")
                continue

            all_match_details = []

            print("\n[작업] 매치 상세 정보 조회 및 추출 중...")
            for i, match_id in enumerate(match_ids):
                print(f"  -> {i+1}/{len(match_ids)} 매치 ID: {match_id} 조회 중...", end='\r')
                detail = api_helper.get_match_details(match_id, puuid)
                if detail:
                    all_match_details.append(detail)
                time.sleep(1)

            print("\n[성공] 상세 정보 추출 완료.")
            data_manager.save_match_data_to_csv(all_match_details)

            # -------------------------------
            # 💡 데이터 컬럼명 한글 변환 및 새 CSV 저장 로직
            # -------------------------------
            
            print("\n[작업] 데이터 컬럼명 한글 변환 및 새 CSV 저장 중...")
            
            # CSV 파일 불러오기 (df 변수 정의)
            df = data_manager.load_match_data_from_csv()
            
            if df is None:
                print("[경고] 데이터를 불러올 수 없어 한글 변환을 건너뜁니다.")
                # 'df'가 None일 경우 여기서 continue하여 오류 방지
                continue 

            # 1. 큐 ID를 게임 모드 이름으로 변환
            df['queue_id'] = df['queue_id'].apply(lambda x: QUEUE_ID_MAP.get(x, f"알 수 없음 ({x})"))
            
            # 2. 게임 시간(초)을 시:분:초 문자열로 변환
            df['game_duration'] = df['game_duration'].apply(format_game_duration)
            
            # 3-1. 챔피언 이름 (Unknown_ID_XX -> English Name) 변환 로직
            def convert_champion_id_to_english(champion_str):
                if not isinstance(champion_str, str) or 'Unknown_ID_' not in champion_str:
                    return champion_str # 이미 영어 이름이면 그냥 반환
                
                try:
                    champion_id = int(champion_str.split('_')[-1])
                    # api_helper.py의 CHAMPION_MAP이 English name을 반환한다고 가정
                    eng_name = api_helper.get_champion_name(champion_id)
                    return eng_name if eng_name and 'Unknown' not in eng_name else champion_str
                    
                except Exception:
                    return champion_str 

            df['champion_name'] = df['champion_name'].apply(convert_champion_id_to_english)

            # 3-2. 챔피언 이름 (English Name -> Korean Name) 변환
            df['champion_name'] = df['champion_name'].apply(
                lambda eng_name: CHAMPION_NAME_KR_MAP.get(eng_name, eng_name)
            )
            
            # 💡 3-3. 승패 여부 (True/False)를 한글로 변환
            # True는 '승리', False는 '패배'로 변환합니다. (LoL은 무승부가 없음)
            df['win'] = df['win'].apply(lambda x: '승리' if x else '패배')


            # 4. 컬럼명 한글로 변경 및 'match_id' 제거
            df.rename(columns={
                'match_id': '매치ID',
                'game_duration': '게임시간', 
                'queue_id': '게임모드', 
                'champion_name': '챔피언', # 이제 한글 이름
                'kills': '킬',
                'deaths': '데스',
                'assists': '어시스트',
                'win': '승리', # 컬럼 이름도 '승리'로 변경
                'total_minions_killed': '미니언처치',
                'gold_earned': '골드획득'
            }, inplace=True)
            
            # 5. '매치ID' 컬럼 제거
            df.drop(columns=['매치ID'], inplace=True)


            # CSV로 저장 (새 파일명 사용)
            KR_FILE_PATH = "summoner_match_history_kr.csv"
            df.to_csv(KR_FILE_PATH, index=False, encoding="utf-8-sig")
            print(f"[완료] 한글 컬럼명 데이터가 '{KR_FILE_PATH}'에 저장되었습니다.")
            
            # 💡 수정된 출력 로직: 수동 포매팅 함수 호출
            print_formatted_dataframe(df.head())
            
            # -------------------------------
            
        elif main_choice == '2':
            analysis_menu()
            
        elif main_choice == '3':
            data_management_menu()
            
        else:
            print("[경고] 잘못된 메뉴 선택입니다. 다시 입력해 주세요.")

if __name__ == "__main__":
    main()