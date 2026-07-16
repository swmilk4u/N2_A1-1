# -*- coding: utf-8 -*-
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "prompts.json"

# 1. 기본 프롬프트 데이터 정의 (최소 3개 이상)
# 프로그램 실행 시 처음부터 보여줄 기본 프롬프트 예시 데이터이다.
# 최소 3개 이상 등록되어 있으며, 각 프롬프트는 제목, 내용, 카테고리, 즐겨찾기 여부, 조회수 정보를 포함한다.
# 이 데이터는 prompts.json이 없을 때 사용되며, 앱 실행 초기 화면을 구성하는 기준 데이터 역할을 한다.
default_prompts = [
    {
        "title": "블로그 글 작성 도우미",
        "content": "당신은 10년 경력의 전문 블로거입니다. 주어진 주제에 대해 SEO에 최적화된 블로그 글을 작성해주세요. 서론, 본론, 결론 구조를 갖추고, 독자의 관심을 끄는 제목을 3개 제안해주세요.",
        "category": "텍스트 생성",
        "favorite": True,
        "views": 0
    },
    {
        "title": "제품 썸네일 생성",
        "content": "다음 제품의 매력적인 썸네일 이미지를 생성해주세요. 제품의 핵심 기능이 돋보이고 텍스트는 최소화하며, 밝고 화사한 톤앤매너로 디자인해 주세요.",
        "category": "이미지 생성",
        "favorite": False,
        "views": 0
    },
    {
        "title": "IT 컨설턴트 페르소나",
        "content": "당신은 대기업 IT 전략 컨설턴트입니다. 클라이언트의 디지털 전환 전략에 대해 날카롭고 구체적인 조언을 해주세요. 답변은 항상 전문 용어를 적절히 섞어 3가지 단락으로 요약해 주세요.",
        "category": "페르소나",
        "favorite": False,
        "views": 0
    },
    {
        "title": "뉴스 요약 프롬프트",
        "content": "아래 제공되는 뉴스 기사의 핵심 내용을 3문장으로 요약하고, 각각의 주요 키워드를 해시태그 형식으로 3개 추출해 주세요.",
        "category": "자동화",
        "favorite": True,
        "views": 0
    }
]

prompts = []
CATEGORIES = ["텍스트 생성", "이미지 생성", "영상 생성", "페르소나", "자동화", "기타"]

# 2. JSON 데이터 영속화 함수
# 기존 저장된 프롬프트 데이터를 로드한다.
# 만약 prompts.json이 존재하면 읽어오고, 없으면 기본 데이터로 초기화한다.
def load_data():
    global prompts
    if DB_FILE.exists():
        try:
            with DB_FILE.open("r", encoding="utf-8-sig") as f:
                prompts = json.load(f)
            return
        except Exception as e:
            print(f"[안내] 데이터 로드 오류 ({e}), 기본 데이터를 사용합니다.")
    
    prompts = [dict(p) for p in default_prompts]
    save_data()

# 현재 메모리의 prompts 리스트를 JSON 파일로 저장한다.
# 루트 폴더의 prompts.json에 쓰며, 디렉터리가 없으면 자동으로 생성한다.
def save_data():
    try:
        DB_FILE.parent.mkdir(parents=True, exist_ok=True)
        with DB_FILE.open("w", encoding="utf-8") as f:
            json.dump(prompts, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"[오류] 데이터 저장에 실패했습니다: {e}")

# 3. 메뉴 표시 함수
# 프로그램 실행 시 사용자에게 선택 가능한 메인 메뉴를 출력한다.
def show_menu():
    print("\n=== 나만의 프롬프트 관리 ===")
    print("1. 프롬프트 추가")
    print("2. 프롬프트 목록")
    print("3. 카테고리별 조회")
    print("4. 프롬프트 검색")
    print("5. 프롬프트 상세 보기")
    print("6. 즐겨찾기 관리")
    print("7. 즐겨찾기 목록")
    print("8. 프롬프트 수정/삭제 (CRUD)")
    print("9. 인기 프롬프트 Top 3")
    print("0. 종료")

# 4. 프롬프트 추가 함수
# 제목, 내용, 카테고리를 입력받아 새로운 프롬프트를 리스트에 추가한다.
# 입력값이 비어 있으면 다시 입력받고, 카테고리는 미리 정해진 목록 또는 직접 입력이 가능하다.
def add_prompt():
    print("\n=== 프롬프트 추가 ===")
    
    # 제목 입력 (비어있으면 재요청)
    while True:
        title = input("제목: ").strip()
        if title:
            break
        print("제목을 입력해주세요. (공백 불가)")
        
    # 내용 입력 (비어있으면 재요청)
    while True:
        content = input("내용: ").strip()
        if content:
            break
        print("내용을 입력해주세요. (공백 불가)")
        
    # 카테고리 선택
    print("\n카테고리 선택:")
    for idx, category in enumerate(CATEGORIES, 1):
        print(f"{idx}) {category}")
    print("7) 직접 입력")
    
    while True:
        cat_choice = input("선택: ").strip()
        if cat_choice.isdigit():
            cat_num = int(cat_choice)
            if 1 <= cat_num <= len(CATEGORIES):
                category = CATEGORIES[cat_num - 1]
                break
            elif cat_num == 7:
                while True:
                    custom_cat = input("직접 입력할 카테고리명: ").strip()
                    if custom_cat:
                        category = custom_cat
                        break
                    print("카테고리명을 입력해주세요.")
                break
        print("잘못된 선택입니다. 1~7 사이의 숫자를 입력해주세요.")
        
    # 프롬프트 추가
    new_prompt = {
        "title": title,
        "content": content,
        "category": category,
        "favorite": False,
        "views": 0
    }
    prompts.append(new_prompt)
    save_data()  # 영속화
    print(f"\n프롬프트가 추가되었습니다!")

# 5. 프롬프트 목록 출력 함수
# 현재 저장된 모든 프롬프트를 번호와 함께 보여준다.
# 즐겨찾기 항목은 [*] 표시로 구분한다.
def show_list():
    print("\n=== 프롬프트 목록 ===")
    if not prompts:
        print("등록된 프롬프트가 없습니다. 프롬프트를 먼저 추가해주세요.")
        return
        
    for idx, p in enumerate(prompts, 1):
        fav_mark = " [*]" if p.get("favorite", False) else ""
        print(f"{idx}. [{p['category']}] {p['title']}{fav_mark}")
        
    print(f"\n총 {len(prompts)}개의 프롬프트")

# 6. 카테고리별 조회 함수
# 사용자가 선택한 카테고리에 해당하는 프롬프트만 필터링하여 보여준다.
def show_by_category():
    print("\n=== 카테고리별 조회 ===")
    print("조회할 카테고리를 선택하세요:")
    for idx, category in enumerate(CATEGORIES, 1):
        print(f"{idx}) {category}")
        
    while True:
        cat_choice = input("선택: ").strip()
        if cat_choice.isdigit():
            cat_num = int(cat_choice)
            if 1 <= cat_num <= len(CATEGORIES):
                target_cat = CATEGORIES[cat_num - 1]
                break
        print(f"잘못된 선택입니다. 1~{len(CATEGORIES)} 사이의 숫자를 입력해주세요.")
        
    filtered = [p for p in prompts if p.get("category") == target_cat]
    
    print(f"\n[{target_cat}] 카테고리 프롬프트:")
    if not filtered:
        print("해당 카테고리에 등록된 프롬프트가 없습니다.")
        return
        
    for idx, p in enumerate(filtered, 1):
        fav_mark = " [*]" if p.get("favorite", False) else ""
        print(f"{idx}. {p['title']}{fav_mark}")
        
    print(f"\n총 {len(filtered)}개의 프롬프트")

# 7. 프롬프트 검색 함수
# 제목 또는 내용에 입력한 키워드가 포함된 프롬프트를 검색해 결과를 출력한다.
def search_prompt():
    print("\n=== 프롬프트 검색 ===")
    keyword = input("검색어: ").strip()
    if not keyword:
        print("검색어가 입력되지 않았습니다.")
        return
        
    filtered = [p for p in prompts if keyword.lower() in p['title'].lower() or keyword.lower() in p['content'].lower()]
    
    print("\n검색 결과:")
    if not filtered:
        print("검색 결과가 없습니다.")
        return
        
    for idx, p in enumerate(filtered, 1):
        fav_mark = " [*]" if p.get("favorite", False) else ""
        print(f"{idx}. [{p['category']}] {p['title']}{fav_mark}")
        
    print(f"\n총 {len(filtered)}개의 프롬프트를 찾았습니다.")

# 8. 프롬프트 상세 보기 함수
# 사용자가 선택한 프롬프트의 제목, 카테고리, 즐겨찾기 여부, 조회수, 내용을 상세하게 출력한다.
# 상세 보기를 할 때마다 조회수 views를 1씩 증가시킨다.
def show_detail():
    print("\n=== 프롬프트 상세 보기 ===")
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return
        
    show_list()
    
    while True:
        num_input = input("조회할 프롬프트 번호 입력 (이전 메뉴: 0): ").strip()
        if num_input == "0":
            return
        if num_input.isdigit():
            idx = int(num_input) - 1
            if 0 <= idx < len(prompts):
                target = prompts[idx]
                target["views"] = target.get("views", 0) + 1  # 조회수 증가
                save_data()  # 조회수 영속화
                
                fav_str = "[*]" if target.get("favorite", False) else "일반"
                print("\n" + "─" * 40)
                print(f"제목: {target['title']}")
                print(f"카테고리: {target['category']}")
                print(f"즐겨찾기: {fav_str}")
                print(f"조회수: {target.get('views', 0)}회")
                print("─" * 40)
                print("내용:")
                print(target['content'])
                print("─" * 40)
                return
        print(f"잘못된 번호입니다. 1~{len(prompts)} 사이의 숫자를 입력해주세요.")

# 9. 즐겨찾기 관리 함수
# 사용자가 선택한 프롬프트의 즐겨찾기 상태를 추가/해제 토글한다.
def manage_favorites():
    print("\n=== 즐겨찾기 관리 ===")
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return
        
    show_list()
    
    while True:
        num_input = input("즐겨찾기를 추가/해제할 프롬프트 번호 입력 (이전 메뉴: 0): ").strip()
        if num_input == "0":
            return
        if num_input.isdigit():
            idx = int(num_input) - 1
            if 0 <= idx < len(prompts):
                target = prompts[idx]
                target["favorite"] = not target.get("favorite", False)
                save_data()  # 즐겨찾기 상태 저장
                status = "추가" if target["favorite"] else "해제"
                print(f"'{target['title']}' 프롬프트를 즐겨찾기에 {status}했습니다!")
                return
        print(f"잘못된 번호입니다. 1~{len(prompts)} 사이의 숫자를 입력해주세요.")

# 10. 즐겨찾기 목록 출력 함수
# 즐겨찾기 상태로 표시된 프롬프트만 따로 모아 출력한다.
def show_favorites():
    print("\n=== 즐겨찾기 목록 ===")
    filtered = [p for p in prompts if p.get("favorite", False)]
    if not filtered:
        print("즐겨찾기된 프롬프트가 없습니다.")
        return
        
    for idx, p in enumerate(filtered, 1):
        print(f"{idx}. [{p['category']}] {p['title']} [*]")
        
    print(f"\n총 {len(filtered)}개의 즐겨찾기")

# 11. [보너스] 프롬프트 수정 및 삭제 (CRUD) 함수
# 기존 프롬프트를 수정하거나 삭제할 수 있다.
# 수정 시 제목, 내용, 카테고리를 변경할 수 있고, 삭제 시 y/n 확인을 거친다.
def modify_or_delete_prompt():
    print("\n=== 프롬프트 수정/삭제 (CRUD) ===")
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return
        
    show_list()
    
    while True:
        num_input = input("수정/삭제할 프롬프트 번호 입력 (이전 메뉴: 0): ").strip()
        if num_input == "0":
            return
        if num_input.isdigit():
            idx = int(num_input) - 1
            if 0 <= idx < len(prompts):
                target = prompts[idx]
                break
        print(f"잘못된 번호입니다. 1~{len(prompts)} 사이의 숫자를 입력해주세요.")
        
    print(f"\n선택된 프롬프트: '{target['title']}'")
    print("1. 수정 (Modify)")
    print("2. 삭제 (Delete)")
    print("0. 취소")
    
    while True:
        action = input("선택: ").strip()
        if action == "0":
            return
        elif action == "1":
            print("\n--- 프롬프트 수정 (입력하지 않고 Enter 입력 시 기존 값 유지) ---")
            new_title = input(f"새 제목 (기존: {target['title']}): ").strip()
            new_content = input(f"새 내용 (기존: {target['content'][:20]}...): ").strip()
            
            print(f"기존 카테고리: {target['category']}")
            print("새 카테고리 선택 (엔터 입력 시 기존 유지):")
            for i, cat in enumerate(CATEGORIES, 1):
                print(f"{i}) {cat}")
            print("7) 직접 입력")
            
            while True:
                cat_input = input("선택: ").strip()
                if not cat_input:
                    new_category = target['category']
                    break
                if cat_input.isdigit():
                    cat_num = int(cat_input)
                    if 1 <= cat_num <= len(CATEGORIES):
                        new_category = CATEGORIES[cat_num - 1]
                        break
                    elif cat_num == 7:
                        custom_cat = input("직접 입력할 카테고리명: ").strip()
                        if custom_cat:
                            new_category = custom_cat
                            break
                        print("카테고리명을 입력해주세요.")
                        continue
                print("잘못된 입력입니다. 엔터를 누르거나 1~7 숫자를 입력하세요.")
                
            if new_title:
                target['title'] = new_title
            if new_content:
                target['content'] = new_content
            target['category'] = new_category
            
            save_data()
            print("프롬프트가 수정되었습니다!")
            return
            
        elif action == "2":
            confirm = input(f"정말로 '{target['title']}' 프롬프트를 삭제하시겠습니까? (y/n): ").strip().lower()
            if confirm == 'y':
                prompts.pop(idx)
                save_data()
                print("프롬프트가 삭제되었습니다.")
            else:
                print("삭제가 취소되었습니다.")
            return
        print("잘못된 입력입니다. 0, 1, 2 중에서 선택해주세요.")

# 12. [보너스] 인기 프롬프트 Top 3 조회 함수 (조회수 기준 정렬)
# 조회수 views가 높은 순으로 상위 3개 프롬프트를 출력한다.
def show_top_prompts():
    print("\n=== 인기 프롬프트 Top 3 ===")
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return
        
    # 조회수(views) 기준 내림차순 정렬
    sorted_prompts = sorted(prompts, key=lambda x: x.get("views", 0), reverse=True)
    top_n = sorted_prompts[:3]
    
    for idx, p in enumerate(top_n, 1):
        fav_mark = " [*]" if p.get("favorite", False) else ""
        print(f"{idx}위. [{p['category']}] {p['title']}{fav_mark} (조회수: {p.get('views', 0)}회)")

# 13. 메인 실행 함수
# 프로그램의 전체 흐름을 제어한다.
# 메뉴 선택에 따라 각 기능 함수들을 호출하고, 종료를 선택하면 루프를 빠져나간다.
def main():
    load_data()  # 시작 시 데이터 로드
    while True:
        show_menu()
        try:
            choice = input("선택: ").strip()
        except KeyboardInterrupt:
            print("\n프로그램을 종료합니다.")
            break
            
        if choice == "0":
            print("프로그램을 종료합니다. 이용해 주셔서 감사합니다.")
            break
        elif choice == "1":
            add_prompt()
        elif choice == "2":
            show_list()
        elif choice == "3":
            show_by_category()
        elif choice == "4":
            search_prompt()
        elif choice == "5":
            show_detail()
        elif choice == "6":
            manage_favorites()
        elif choice == "7":
            show_favorites()
        elif choice == "8":
            modify_or_delete_prompt()
        elif choice == "9":
            show_top_prompts()
        else:
            print("잘못된 입력입니다. 0~9 사이의 숫자를 입력해주세요.")

# 프로그램 실행 진입점
if __name__ == "__main__":
    main()
