# functions/data_manager.py
import pandas as pd
import os
import csv
from typing import List, Dict, Optional

# 파일 경로 설정 (평가 요소: 파일 처리)
CSV_FILE_PATH = "summoner_match_history.csv"

# --- 4. 데이터 처리 및 파일 저장/로드 ---

def save_match_data_to_csv(data: List[Dict], file_path: str = CSV_FILE_PATH):
    """
    추출된 매치 데이터를 CSV 파일에 APPEND(추가)합니다.
    (평가 요소: 파일 처리 - CSV, utf-8-sig 인코딩, CRUD - Create)
    """
    if not data:
        print("[경고] 저장할 데이터가 없습니다.")
        return

    # CSV 헤더 정의
    fieldnames = list(data[0].keys())
    
    # 파일이 존재하지 않거나 비어 있다면 헤더를 포함하여 작성
    file_exists = os.path.exists(file_path) and os.path.getsize(file_path) > 0

    try:
        # 'a' (append) 모드로 열고, newline='' 및 encoding='utf-8-sig' 사용
        with open(file_path, mode='a', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            # 파일이 없거나 비어 있을 경우에만 헤더 작성
            if not file_exists:
                writer.writeheader()
            
            # 데이터 쓰기
            writer.writerows(data)
            
        print(f"\n[완료] 매치 데이터 {len(data)}건이 '{file_path}'에 성공적으로 저장되었습니다.")
        
    except IOError as e:
        print(f"[에러] 파일 저장 중 오류 발생: {e}")

def overwrite_csv_from_df(df: pd.DataFrame, file_path: str = CSV_FILE_PATH):
    """
    수정/삭제된 DataFrame을 CSV 파일에 OVERWRITE(덮어쓰기)합니다.
    (평가 요소: 파일 처리, CRUD - Update/Delete 후 저장)
    """
    try:
        # 'w' (write) 모드로 열고, encoding='utf-8-sig' 사용
        df.to_csv(file_path, index=False, encoding='utf-8-sig')
        print(f"[완료] 파일 '{file_path}'이(가) 성공적으로 업데이트되었습니다.")
    except Exception as e:
        print(f"[에러] 파일 덮어쓰기 중 오류 발생: {e}")

def load_match_data_from_csv(file_path: str = CSV_FILE_PATH) -> Optional[pd.DataFrame]:
    """
    CSV 파일에서 데이터를 로드하여 DataFrame으로 반환합니다.
    (평가 요소: 파일 처리 - 불러오기, CRUD - Read)
    """
    if not os.path.exists(file_path):
        print(f"[경고] 파일 '{file_path}'이(가) 존재하지 않습니다. 먼저 전적을 조회/저장하세요.")
        return None
    
    try:
        # utf-8-sig 인코딩으로 파일 로드
        df = pd.read_csv(file_path, encoding='utf-8-sig')
        if df.empty:
            print("[경고] CSV 파일이 비어있습니다. 데이터를 추가해주세요.")
            return None
        return df
    except Exception as e:
        print(f"[에러] CSV 파일 로드 중 오류 발생: {e}")
        return None

# --- 6. 데이터 관리 (CRUD - Update, Delete) ---

def delete_match_record(df: pd.DataFrame):
    """
    특정 match_id를 입력받아 해당 기록을 DataFrame에서 삭제합니다.
    (평가 요소: CRUD - Delete)
    """
    # match_id는 길어서 보여주기 어려우므로, 인덱스 번호를 기반으로 삭제하도록 유도합니다.
    df_display = df.copy()
    df_display['Index'] = df_display.index
    
    print("\n" + "=" * 50)
    print(" [삭제 가능 기록 목록]")
    print(df_display[['Index', 'champion_name', 'win', 'match_id']].head(10).to_string())
    print("-" * 50)
    print(f" (총 {len(df)}건의 기록이 있습니다. 인덱스 10번까지만 표시)")
    
    try:
        index_to_delete = input("삭제할 기록의 'Index' 번호를 입력하세요 (취소: 'c'): ").strip()
        if index_to_delete.lower() == 'c':
            print("[취소] 기록 삭제를 취소합니다.")
            return

        index_to_delete = int(index_to_delete)
        
        if index_to_delete not in df.index:
            print(f"[경고] 인덱스 번호 {index_to_delete}에 해당하는 기록이 없습니다.")
            return

        # 삭제 전 확인 메시지
        record_info = df.loc[index_to_delete, ['champion_name', 'match_id']].to_dict()
        print(f"[확인] {record_info['champion_name']} (Match ID: {record_info['match_id'][:10]}...) 기록을 삭제합니다.")

        # DataFrame에서 해당 인덱스 삭제
        df.drop(index_to_delete, inplace=True)
        
        # 파일에 덮어쓰기
        overwrite_csv_from_df(df)
        
    except ValueError:
        print("[경고] 유효하지 않은 인덱스 번호입니다.")
    except Exception as e:
        print(f"[에러] 기록 삭제 중 오류 발생: {e}")


def update_match_memo(df: pd.DataFrame):
    """
    특정 match_id에 사용자 메모를 추가하거나 수정합니다.
    (평가 요소: CRUD - Update)
    """
    # 'user_memo' 컬럼이 없으면 추가하고 NaN으로 초기화
    if 'user_memo' not in df.columns:
        df['user_memo'] = ''

    df_display = df.copy()
    df_display['Index'] = df_display.index
    
    print("\n" + "=" * 50)
    print(" [메모 수정 가능 기록 목록]")
    print(df_display[['Index', 'champion_name', 'win', 'user_memo']].head(10).to_string())
    print("-" * 50)
    
    try:
        index_to_update = input("메모를 수정/추가할 기록의 'Index' 번호를 입력하세요 (취소: 'c'): ").strip()
        if index_to_update.lower() == 'c':
            print("[취소] 메모 수정을 취소합니다.")
            return

        index_to_update = int(index_to_update)
        
        if index_to_update not in df.index:
            print(f"[경고] 인덱스 번호 {index_to_update}에 해당하는 기록이 없습니다.")
            return

        current_memo = df.loc[index_to_update, 'user_memo']
        # pd.notna(current_memo) and current_memo: NaN이 아니고 값이 있는 경우
        print(f"\n[현재 메모] {current_memo if pd.notna(current_memo) and current_memo else '없음'}")
        
        new_memo = input("새로운 메모를 입력하세요 (현재 메모 덮어쓰기): ").strip()
        
        # DataFrame에 메모 업데이트
        df.loc[index_to_update, 'user_memo'] = new_memo
        
        # 파일에 덮어쓰기
        overwrite_csv_from_df(df)

    except ValueError:
        print("[경고] 유효하지 않은 인덱스 번호입니다.")
    except Exception as e:
        print(f"[에러] 메모 수정 중 오류 발생: {e}")