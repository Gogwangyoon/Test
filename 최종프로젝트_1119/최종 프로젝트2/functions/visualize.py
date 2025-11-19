# functions/visualize.py
import pandas as pd
import matplotlib.pyplot as plt
import os
from typing import Optional

# matplotlib에서 한글 폰트 설정을 위한 라이브러리 (macOS, Linux 환경에서 필요)
try:
    from matplotlib import font_manager, rc
    # 시스템에 'Malgun Gothic' 또는 'NanumGothic'이 설치되어 있다고 가정합니다.
    # 사용자 환경에 따라 폰트 이름을 수정해야 할 수 있습니다.
    font_path = 'C:/Windows/Fonts/malgun.ttf' # Windows 예시
    if not os.path.exists(font_path):
        font_path = '/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf' # Linux 예시
    if os.path.exists(font_path):
        font_name = font_manager.FontProperties(fname=font_path).get_name()
        rc('font', family=font_name)
    else:
        print("[경고] 한글 폰트를 찾을 수 없어 그래프의 텍스트가 깨질 수 있습니다.")
except ImportError:
    print("[경고] matplotlib 설정 중 에러가 발생했습니다. (일반적으로 WSL 또는 특수 환경)")


# --- 5. 데이터 시각화 및 통계 ---

def plot_kda_distribution(df: Optional[pd.DataFrame], plot_champion_winrate: bool = True, top_n: int = 10):
    """
    KDA (킬/데스/어시스트) 분포를 막대 그래프로 시각화합니다.
    옵션: plot_champion_winrate=True면 챔피언별 승률 그래프도 표시
    """
    if df is None or df.empty:
        print("[경고] 데이터가 없습니다.")
        return
        
    print("\n[작업] KDA 분포 시각화 준비 중...")
    
    # KDA 데이터 추출
    kda_data = df[['kills', 'deaths', 'assists']]
    
    # 평균 KDA 계산
    total_deaths = kda_data['deaths'].sum()
    total_kills = kda_data['kills'].sum()
    total_assists = kda_data['assists'].sum()

    avg_kda = (total_kills + total_assists) / total_deaths if total_deaths > 0 else total_kills + total_assists
    print(f"[분석] 총 {len(df)}경기 기준 평균 KDA: {avg_kda:.2f}")

    # KDA 막대 그래프
    total_kda = pd.Series([total_kills, total_deaths, total_assists], index=['Kills (킬)', 'Deaths (데스)', 'Assists (어시스트)'])
    plt.figure(figsize=(8,6))
    total_kda.plot(kind='bar', color=['#007bff', '#dc3545', '#ffc107'])
    plt.title(f"최근 {len(df)}경기 KDA (킬/데스/어시스트) 분포", fontsize=15)
    plt.ylabel("총 횟수", fontsize=12)
    plt.xticks(rotation=0)
    for i, v in enumerate(total_kda):
        plt.text(i, v + 5, str(v), ha='center', va='bottom', fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

    # ------------------- 챔피언 승률 분석 -------------------
    if plot_champion_winrate:
        print("\n[작업] 챔피언별 승률 분석 중...")
        champ_stats = df.groupby('champion_name')['win'].agg(['sum','count'])
        champ_stats['win_rate'] = (champ_stats['sum'] / champ_stats['count']) * 100
        champ_stats = champ_stats.sort_values(by='win_rate', ascending=False).head(top_n)

        plt.figure(figsize=(10,6))
        plt.bar(champ_stats.index, champ_stats['win_rate'], color='#28a745')
        plt.ylabel('승률 (%)')
        plt.ylim(0, 100)
        plt.title(f'챔피언별 승률 상위 {top_n}개')
        for i, rate in enumerate(champ_stats['win_rate']):
            plt.text(i, rate + 1, f"{rate:.1f}%", ha='center', va='bottom', fontsize=10)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()