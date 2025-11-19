LoL 전적 분석 시스템 (LoL Analyst)

프로젝트 개요

이 프로젝트는 Riot Games의 API를 활용하여 특정 소환사의 리그 오브 레전드(LoL) 전적을 조회하고, 이를 로컬 CSV 파일에 저장하여 관리 및 분석하는 콘솔 애플리케이션입니다.

주요 기능

전적 조회 및 저장 (CRUD: Create/Read): Riot API를 통해 최신 매치 기록을 가져와 로컬 CSV 파일에 추가합니다.

데이터 통계 및 시각화:

저장된 데이터를 기반으로 소환사의 KDA(킬/데스/어시스트) 분포를 matplotlib 그래프로 시각화합니다.

(확장 예정) 챔피언별 승률 등의 추가 통계를 제공합니다.

데이터 관리 (CRUD: Update/Delete):

불필요한 매치 기록을 파일에서 삭제합니다.

특정 매치에 대한 사용자 메모를 추가하거나 수정합니다.

프로젝트 구조

코드는 역할별로 모듈화되어 관리됩니다.

main.py: 애플리케이션의 메인 루프, 사용자 인터페이스(메뉴), 그리고 모듈 간의 연결을 담당합니다.

functions/api_helper.py: Riot API 키, 엔드포인트 설정 및 모든 API 통신(소환사 검색, 매치 기록 획득) 로직을 처리합니다.

functions/data_manager.py: 로컬 CSV 파일 I/O(저장, 로드) 및 CRUD 작업(데이터 삭제/수정)을 담당합니다. pandas를 사용합니다.

functions/visualize.py: matplotlib을 사용하여 데이터 분석 결과를 그래프로 출력하는 로직을 담당합니다.