import sqlite3

def initialize_database():
    conn = sqlite3.connect("family_budget.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS family_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            occupation TEXT NOT NULL,
            income REAL DEFAULT 0,
            expenses REAL DEFAULT 0
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS income_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER,
            salary REAL DEFAULT 0,
            bonus REAL DEFAULT 0,
            personal_income REAL DEFAULT 0,
            FOREIGN KEY (member_id) REFERENCES family_members (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expense_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER,
            internet REAL DEFAULT 0,
            water REAL DEFAULT 0,
            electricity REAL DEFAULT 0,
            food REAL DEFAULT 0,
            clothing REAL DEFAULT 0,
            household_chemicals REAL DEFAULT 0,
            heating REAL DEFAULT 0,
            taxes REAL DEFAULT 0,
            fines REAL DEFAULT 0,
            medicine REAL DEFAULT 0,
            FOREIGN KEY (member_id) REFERENCES family_members (id)
        )
    ''')

    conn.commit()
    conn.close()

def add_family_member(name, occupation, income, expenses):
    conn = sqlite3.connect("family_budget.db")
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO family_members (name, occupation, income, expenses)
        VALUES (?, ?, ?, ?)
    ''', (name, occupation, income, expenses))

    member_id = cursor.lastrowid

    cursor.execute('''
        INSERT INTO income_details (member_id) VALUES (?)
    ''', (member_id,))

    cursor.execute('''
        INSERT INTO expense_details (member_id) VALUES (?)
    ''', (member_id,))

    conn.commit()
    conn.close()

def update_income_details(member_id, salary, bonus, personal_income):
    conn = sqlite3.connect("family_budget.db")
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE income_details
        SET salary = ?, bonus = ?, personal_income = ?
        WHERE member_id = ?
    ''', (salary, bonus, personal_income, member_id))

    conn.commit()
    conn.close()

def update_expense_details(member_id, internet, water, electricity, food, clothing, household_chemicals, heating, taxes, fines, medicine):
    conn = sqlite3.connect("family_budget.db")
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE expense_details
        SET internet = ?, water = ?, electricity = ?, food = ?, clothing = ?, household_chemicals = ?, heating = ?, taxes = ?, fines = ?, medicine = ?
        WHERE member_id = ?
    ''', (internet, water, electricity, food, clothing, household_chemicals, heating, taxes, fines, medicine, member_id))

    conn.commit()
    conn.close()

def view_family_members():
    conn = sqlite3.connect("family_budget.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM family_members")
    members = cursor.fetchall()

    conn.close()
    return members

def view_income_expense_details():
    conn = sqlite3.connect("family_budget.db")
    cursor = conn.cursor()

    cursor.execute('''
        SELECT fm.name, fm.occupation, id.salary, id.bonus, id.personal_income,
               ed.internet, ed.water, ed.electricity, ed.food, ed.clothing,
               ed.household_chemicals, ed.heating, ed.taxes, ed.fines, ed.medicine
        FROM family_members fm
        JOIN income_details id ON fm.id = id.member_id
        JOIN expense_details ed ON fm.id = ed.member_id
    ''')

    details = cursor.fetchall()

    conn.close()
    return details

def calculate_totals():
    conn = sqlite3.connect("family_budget.db")
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(income) FROM family_members")
    total_income = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(expenses) FROM family_members")
    total_expenses = cursor.fetchone()[0] or 0

    conn.close()
    return total_income, total_expenses

def main():
    initialize_database()

    while True:
        print("\nҮй бухгалтериясы")
        print("1. Жанұя мүшесін қосу")
        print("2. Жанұя мүшелерін көру")
        print("3. Кіріс пен шығыс мәліметтерін жаңарту")
        print("4. Барлық кіріс пен шығыс мәліметтерін көру")
        print("5. Жалпы кірістер мен шығыстарды есептеу")
        print("6. Шығу")

        choice = input("Таңдауыңыз: ")

        if choice == "1":
            name = input("Мүшенің аты: ")
            occupation = input("Жұмысы: ")
            income = float(input("Кірісі: "))
            expenses = float(input("Шығысы: "))
            add_family_member(name, occupation, income, expenses)
            print(f"{name} деректер қорына қосылды.")

        elif choice == "2":
            members = view_family_members()
            print("\nЖанұя мүшелері:")
            for member in members:
                print(f"ID: {member[0]}, Аты: {member[1]}, Жұмысы: {member[2]}, Кіріс: {member[3]}, Шығыс: {member[4]}")

        elif choice == "3":
            member_id = int(input("Мүшенің ID-ін енгізіңіз: "))
            print("Кірістерді енгізіңіз:")
            salary = float(input("Жалақы: "))
            bonus = float(input("Премия: "))
            personal_income = float(input("Жеке табыс: "))
            update_income_details(member_id, salary, bonus, personal_income)

            print("Шығыстарды енгізіңіз:")
            internet = float(input("Интернет: "))
            water = float(input("Су: "))
            electricity = float(input("Энергия: "))
            food = float(input("Азық-түлік: "))
            clothing = float(input("Киім-кешек: "))
            household_chemicals = float(input("Тұрмыстық химия: "))
            heating = float(input("Жылу: "))
            taxes = float(input("Салық: "))
            fines = float(input("Штрафтар: "))
            medicine = float(input("Дәрі-дәрмек: "))
            update_expense_details(member_id, internet, water, electricity, food, clothing, household_chemicals, heating, taxes, fines, medicine)
            print("Мәліметтер жаңартылды.")

        elif choice == "4":
            details = view_income_expense_details()
            print("\nБарлық кіріс пен шығыс мәліметтері:")
            for detail in details:
                print(f"Аты: {detail[0]}, Жұмысы: {detail[1]}, Жалақы: {detail[2]}, Премия: {detail[3]}, Жеке табыс: {detail[4]},\n"
                      f"Интернет: {detail[5]}, Су: {detail[6]}, Энергия: {detail[7]}, Азық-түлік: {detail[8]}, Киім-кешек: {detail[9]},\n"
                      f"Тұрмыстық химия: {detail[10]}, Жылу: {detail[11]}, Салық: {detail[12]}, Штрафтар: {detail[13]}, Дәрі-дәрмек: {detail[14]}")

        elif choice == "5":
            total_income, total_expenses = calculate_totals()
            print(f"\nЖалпы кіріс: {total_income}")
            print(f"Жалпы шығыс: {total_expenses}")
            print(f"Қалған қаражат: {total_income - total_expenses}")

        elif choice == "6":
            print("Бағдарлама аяқталды.")
            break

        else:
            print("Қате! Дұрыс таңдау енгізіңіз.")

if __name__ == "__main__":
    main()
