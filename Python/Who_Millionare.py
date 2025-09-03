import json
import random
import os

LETTERS = ["A", "B", "C", "D"]

# --- Lifeline functions ---
def apply_5050(options, correct_idx):
    incorrect = [i for i in range(len(options)) if i != correct_idx and options[i] is not None]
    if len(incorrect) <= 1:
        return options
    to_remove = random.sample(incorrect, 2)
    new_opts = options.copy()
    for i in to_remove:
        new_opts[i] = None
    return new_opts

def audience_poll(options, correct_idx, level):
    reliability = {1: 0.90, 2: 0.75, 3: 0.60, 4: 0.45}
    base = reliability.get(level, 0.6)
    visible_idx = [i for i, o in enumerate(options) if o is not None]
    n = len(visible_idx)
    if n == 0:
        return {LETTERS[i]: 0 for i in range(len(options))}
    remaining_pct = 100
    pct = dict.fromkeys(range(len(options)), 0)
    if correct_idx in visible_idx:
        correct_pct = int(round(base * 100))
        pct[correct_idx] = correct_pct
        remaining_pct -= correct_pct
    wrong_idx = [i for i in visible_idx if i != correct_idx]
    if wrong_idx:
        weights = [random.random() for _ in wrong_idx]
        total_w = sum(weights)
        allocated = 0
        for j, idx in enumerate(wrong_idx):
            if j < len(wrong_idx) - 1:
                p = int(round(remaining_pct * weights[j] / total_w))
                pct[idx] = p
                allocated += p
            else:
                pct[idx] = remaining_pct - allocated
    result = {}
    for i in range(len(options)):
        result[LETTERS[i]] = pct.get(i, 0) if options[i] is not None else 0
    return result

def phone_friend(options, correct_idx, level):
    reliability = {1: 0.85, 2: 0.70, 3: 0.55, 4: 0.40}
    prob = reliability.get(level, 0.6)
    visible_idx = [i for i, o in enumerate(options) if o is not None]
    if random.random() < prob and correct_idx in visible_idx:
        return LETTERS[correct_idx], f"Tôi nghĩ đáp án đúng là {LETTERS[correct_idx]}."
    else:
        wrong_visible = [i for i in visible_idx if i != correct_idx]
        if not wrong_visible:
            return LETTERS[correct_idx], f"Tôi nghĩ đáp án là {LETTERS[correct_idx]}."
        pick = random.choice(wrong_visible)
        return LETTERS[pick], f"Tôi hơi phân vân nhưng có thể là {LETTERS[pick]}."

# --- Helpers ---
def print_question(options):
    for i, opt in enumerate(options):
        if opt is None:
            print(f"  {LETTERS[i]}. ---")
        else:
            print(f"  {LETTERS[i]}. {opt}")
def ask_question(q, lifelines):
    options = q['options'].copy()
    order = list(range(len(options)))
    random.shuffle(order)
    options = [q['options'][i] for i in order]
    correct_idx = options.index(q['answer'])
    level = q.get('level', 1)
    while True:
        print("\n" + "="*40)
        print(f"Câu hỏi: {q['question']}")
        print_question(options)
        print("\nNhập A/B/C/D hoặc '5050', 'call', 'aud'")
        print(f"Quyền còn lại: 50:50={'Có' if lifelines['5050'] else 'X'}, Call={'Có' if lifelines['call'] else 'X'}, Audience={'Có' if lifelines['aud'] else 'X'}")
        ans = input("Lựa chọn: ").strip().upper()
        if ans == "5050":
            if not lifelines['5050']:
                print("Bạn đã dùng 50:50 rồi.")
                continue
            options = apply_5050(options, correct_idx)
            lifelines['5050'] = False
            print("Đã loại 2 đáp án sai.")
        elif ans == "AUD":
            if not lifelines['aud']:
                print("Bạn đã dùng hỏi khán giả rồi.")
                continue
            poll = audience_poll(options, correct_idx, level)
            print("Kết quả khảo sát:")
            for L in LETTERS:
                print(f"  {L}: {poll[L]}%")
            lifelines['aud'] = False
        elif ans == "CALL":
            if not lifelines['call']:
                print("Bạn đã dùng gọi điện rồi.")
                continue
            suggestion, msg = phone_friend(options, correct_idx, level)
            print(f"Bạn bè nói: {msg}")
            lifelines['call'] = False
        elif ans in LETTERS:
            idx = LETTERS.index(ans)
            if options[idx] is None:
                print("Đáp án đã bị loại.")
                continue
            if idx == correct_idx:
                print("✅ ĐÚNG!!!")
                return True
            else:
                print(f"❌ SAI! Đáp án đúng là {LETTERS[correct_idx]}. {options[correct_idx]}")
                return False
        else:
            print("Lựa chọn không hợp lệ.")
def main():
    base_dir = os.path.dirname(__file__)
    with open(os.path.join(base_dir, "questions.json"), "r", encoding="utf-8") as f:
        all_questions = json.load(f)
    selected = random.sample(all_questions, 10)
    lifelines = {'5050': True, 'call': True, 'aud': True}
    score = 0
    for i, q in enumerate(selected, start=1):
        print(f"\n===== Câu số {i} =====")
        if ask_question(q, lifelines):
            score += 1
        else:
            print("Trò chơi kết thúc.")
            break
    print("\n=== KẾT QUẢ ===")
    print(f"Bạn trả lời đúng {score}/{len(selected)} câu.")

if __name__ == "__main__":
    main()
