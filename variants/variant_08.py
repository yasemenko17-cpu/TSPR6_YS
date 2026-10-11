def level_plan(tasks: list, capacity: list, plan: list) -> dict:
    """Вирівнює план під ємність спринтів з урахуванням залежностей."""
    # 1. Перевірка повторних id у tasks
    task_ids = set()
    for t in tasks:
        tid = t['id']
        if tid in task_ids:
            raise ValueError(f"Повторний id: {tid}")
        task_ids.add(tid)
        
    # Створюємо словник для швидкого доступу до задач
    task_map = {t['id']: t for t in tasks}

    # 2. Перевірка невідомих залежностей у tasks
    for t in tasks:
        for dep in t['depends_on']:
            if dep not in task_map:
                raise ValueError(f"Невідома залежність: {t['id']} -> {dep}")

    # 3. Перевірка циклів залежностей (DFS)
    visited = {} # 0: visiting, 1: visited
    def check_cycle(tid):
        if visited.get(tid) == 0:
            raise ValueError("Цикл залежностей")
        if visited.get(tid) == 1:
            return
        visited[tid] = 0
        for dep in task_map[tid]['depends_on']:
            check_cycle(dep)
        visited[tid] = 1

    for t in tasks:
        if t['id'] not in visited:
            check_cycle(t['id'])

    # 4. Перевірки плану (plan)
    plan_task_ids = []
    seen_in_plan = set()
    for sprint_list in plan:
        for tid in sprint_list:
            if tid not in task_map:
                raise ValueError(f"Невідома задача в плані: {tid}")
            if tid in seen_in_plan:
                raise ValueError(f"Задача в плані двічі: {tid}")
            seen_in_plan.add(tid)
            plan_task_ids.append(tid)

    # 5. Задача є в tasks, але відсутня в плані
    for t in tasks:
        if t['id'] not in seen_in_plan:
            raise ValueError(f"Задача не в плані: {t['id']}")

    # Максимальна ємність (беремо останню з list)
    max_cap = capacity[-1]

    # 6. Перевірка чи задача не більша за максимальну ємність
    for t in tasks:
        if t['points'] > max_cap:
            raise ValueError(f"Задача {t['id']} більша за ємність")

    # --- Алгоритм вирівнювання плану ---
    # Збираємо всі задачі в чергу кандидатів з початкового плану
    # Перетворюємо plan у зручну структуровану чергу початкових списків спринтів
    
    # Сформуємо список задач, які ще не розміщені
    # Для цього промоделюємо процес розкладки згідно з правилами:
    
    # Зберігаємо початковий розподіл задач по спринтах для визначення moved
    original_sprint_map = {}
    for s_idx, sprint_tasks in enumerate(plan):
        for tid in sprint_tasks:
            original_sprint_map[tid] = s_idx + 1

    placed_tasks = set()
    sprints_result = []
    load_result = []
    
    # Черга очікування для відкладених задач
    pending_queue = []
    
    # Щоб обробляти спринти один за одним:
    current_sprint_idx = 0
    
    # Потрібно пройтися по всіх задачах, поки всі не будуть розміщені
    total_tasks_count = len(tasks)
    task_to_sprint_actual = {}
    
    # Будемо формувати спринти по черзі, поки не розкинемо всі задачі
    while len(task_to_sprint_actual) < total_tasks_count:
        current_sprint_num = current_sprint_idx + 1
        current_cap = capacity[current_sprint_idx] if current_sprint_idx < len(capacity) else capacity[-1]
        
        # Формуємо список кандидатів для цього спринту:
        # 1. Відкладені раніше задачі (у порядку відкладання)
        candidates = list(pending_queue)
        pending_queue.clear()
        
        # 2. Задачі з початкового плану для цього спринту (якщо він є в plan)
        if current_sprint_idx < len(plan):
            for tid in plan[current_sprint_idx]:
                if tid not in task_to_sprint_actual and tid not in candidates:
                    candidates.append(tid)
        
        # Також якщо залишились інші нерозподілені задачі, а кандидати пусті (на випадок зсувів)
        # Але за алгоритмом кандидати беруться з pending_queue та plan[s-1]. 
        # Проте якщо в початковому плані на цей спринт нічого не було, а є відкладені — беремо їх.
        
        sprint_items = []
        sprint_load = 0
        
        next_candidates = []
        for tid in candidates:
            t_data = task_map[tid]
            # Перевірка залежностей: всі залежності мають бути розміщені в спринтах, що ПЕРЕДУЮТЬ поточному
            deps_met = all(dep in task_to_sprint_actual and task_to_sprint_actual[dep] < current_sprint_num for dep in t_data['depends_on'])
            
            if deps_met and (sprint_load + t_data['points'] <= current_cap):
                sprint_items.append(tid)
                sprint_load += t_data['points']
                task_to_sprint_actual[tid] = current_sprint_num
            else:
                next_candidates.append(tid)
                
        pending_queue = next_candidates
        
        sprints_result.append(sprint_items)
        load_result.append(sprint_load)
        current_sprint_idx += 1

    # Формуємо словник переміщень `moved`
    moved = {}
    for tid, actual_sprint in task_to_sprint_actual.items():
        orig_sprint = original_sprint_map[tid]
        if orig_sprint != actual_sprint:
            moved[tid] = [orig_sprint, actual_sprint]

    release_sprint = len(sprints_result)

    return {
        "sprints": sprints_result,
        "load": load_result,
        "moved": moved,
        "release_sprint": release_sprint
    }