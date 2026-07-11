# 02_source/main.py

# 1. 기본 프롬프트 데이터 정의 (최소 3개 이상)
prompts = [
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

CATEGORIES = ["텍스트 생성", "이미지 생성", "영상 생성", "페르소나", "자동화", "기타"]

# 2. 메뉴 표시 함수
def show_menu():
    print("\n=== 나만의 프롬프트 관리 ===")
    print("1. 프롬프트 추가")
    print("2. 프롬프트 목록")
    print("3. 카테고리별 조회")
    print("4. 프롬프트 검색")
    print("5. 프롬프트 상세 보기")
    print("6. 즐겨찾기 관리")
    print("7. 즐겨찾기 목록")
    print("0. 종료")

# 3. 프롬프트 추가 함수
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
    print(f"\n프롬프트가 추가되었습니다!")

# 4. 프롬프트 목록 출력 함수
def show_list():
    print("\n=== 프롬프트 목록 ===")
    if not prompts:
        print("등록된 프롬프트가 없습니다. 프롬프트를 먼저 추가해주세요.")
        return
        
    for idx, p in enumerate(prompts, 1):
        fav_mark = " ⭐" if p.get("favorite", False) else ""
        print(f"{idx}. [{p['category']}] {p['title']}{fav_mark}")
        
    print(f"\n총 {len(prompts)}개의 프롬프트")

# 5. 카테고리별 조회 함수
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
        fav_mark = " ⭐" if p.get("favorite", False) else ""
        print(f"{idx}. {p['title']}{fav_mark}")
        
    print(f"\n총 {len(filtered)}개의 프롬프트")

# 6. 프롬프트 검색 함수
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
        fav_mark = " ⭐" if p.get("favorite", False) else ""
        print(f"{idx}. [{p['category']}] {p['title']}{fav_mark}")
        
    print(f"\n총 {len(filtered)}개의 프롬프트를 찾았습니다.")

# 7. 프롬프트 상세 보기 함수
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
                
                fav_str = "⭐" if target.get("favorite", False) else "일반"
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

# 8. 즐겨찾기 관리 함수
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
                # 즐겨찾기 상태 토글
                target["favorite"] = not target.get("favorite", False)
                status = "추가" if target["favorite"] else "해제"
                print(f"'{target['title']}' 프롬프트를 즐겨찾기에 {status}했습니다!")
                return
        print(f"잘못된 번호입니다. 1~{len(prompts)} 사이의 숫자를 입력해주세요.")

# 9. 즐겨찾기 목록 출력 함수
def show_favorites():
    print("\n=== 즐겨찾기 목록 ===")
    filtered = [p for p in prompts if p.get("favorite", False)]
    if not filtered:
        print("즐겨찾기된 프롬프트가 없습니다.")
        return
        
    for idx, p in enumerate(filtered, 1):
        print(f"{idx}. [{p['category']}] {p['title']} ⭐")
        
    print(f"\n총 {len(filtered)}개의 즐겨찾기")

# 10. 메인 실행 함수
def main():
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
        else:
            print("잘못된 입력입니다. 0~7 사이의 숫자를 입력해주세요.")

if __name__ == "__main__":
    main()
