import time
import random

BOLD = "\033[1m"
ITALIC = "\033[3m"
RESET = "\033[0m"

class Level1:
    def __init__(self):
        self.player_inventory = []
        self.available_actions = ["осмотреть", "взять", "использовать", "идти", "инвентарь"]
        self.interacted_objects = set()
        
        self.objects_description = {
            "холл": "Забытый холл: пыльное помещение с высокими сводами. В воздухе витает запах старой пыли и металла.",
            "дверь": "Массивная дубовая дверь с железными скобами. Кажется, она заперта на века.",
            "ключ": "Ржавый железный ключ, покрытый паутиной. На нем виднеется герб Изумрудного города.",
            "сумка": "Старая кожаная сумка, забытая в углу холла.",
            "сундук": "Небольшой деревянный сундук, стоящий у стены.",
            "картина": "Потускневшая картина, изображающая волшебника Гудвина.",
            "ковер": "Истонченный ковер с выцветшими узорами."
        }
        
        self.objects_state = {
            "дверь": "заперта",
            "сундук": "заперт",
            "ключ": "не найден"
        }

    def show_inventory(self):
        if not self.player_inventory:
            print("\nИнвентарь пуст.")
        else:
            print(f"\nИнвентарь: {', '.join(self.player_inventory)}")

    def process_command(self, command):
        command = command.lower().strip()
        
        if command == "инвентарь":
            self.show_inventory()
            return True
        elif command == "помощь":
            self.show_help()
            return True
        elif command == "выход":
            return False
        
        parts = command.split()
        if len(parts) < 2:
            print("Не понял команду. Используйте: действие объект")
            return True
        
        action = parts[0]
        obj = "_".join(parts[1:])
        
        if action not in self.available_actions:
            print(f"Неизвестное действие. Доступные: {', '.join(self.available_actions)}")
            return True
        
        return self.execute_action(action, obj)

    def execute_action(self, action, obj):
        if action == "осмотреть":
            return self.examine_object(obj)
        elif action == "взять":
            return self.take_object(obj)
        elif action == "использовать":
            return self.use_object(obj)
        elif action == "идти":
            return self.move_to(obj)
        return True

    def examine_object(self, obj):
        if obj in self.objects_description:
            print(f"\n{self.objects_description[obj]}")
            self.interacted_objects.add(obj)
            
            if obj == "сундук" and self.objects_state["ключ"] == "не найден":
                print("Сундук заперт. Может быть, ключ где-то рядом?")
            elif obj == "картина":
                print("За картиной что-то блеснуло...")
            elif obj == "ковер" and "ключ" not in self.player_inventory:
                print("Ковер выглядит подозрительно. Может быть, под ним что-то есть?")
            elif obj == "дверь":
                if self.objects_state["дверь"] == "заперта":
                    print("Дверь надежно заперта. Нужно найти ключ.")
                else:
                    print("Дверь открыта! Можно пройти дальше.")
            
            return True
        else:
            print("\nНе вижу такого объекта для осмотра.")
            return True

    def take_object(self, obj):
        if obj == "ключ" and "ключ" not in self.player_inventory:
            if self.objects_state["ключ"] == "найден":
                self.player_inventory.append("ключ")
                print(f"{BOLD}\nВы взяли ржавый ключ!{RESET}")
                return True
            else:
                print("\nСначала нужно найти ключ!")
                return True
        elif obj == "ключ" and "ключ" in self.player_inventory:
            print("\nКлюч уже у вас в инвентаре")
            return True
        else:
            print("\nЭто нельзя взять.")
            return True

    def use_object(self, obj):
        if obj == "ключ":
            if "ключ" in self.player_inventory:
                return self.use_key()
            else:
                print("\nУ вас нет ключа!")
        elif obj == "дверь":
            return self.use_door()
        else:
            print("\nЭто нельзя использовать таким образом.")
        
        return True

    def move_to(self, obj):
        if obj == "картина":
            print("\nВы подошли к картине. При ближайшем рассмотрении замечаете, что она немного отходит от стены.")
            if "ключ" not in self.player_inventory and self.objects_state["ключ"] == "не найден":
                print("За картиной вы находите ржавый ключ!")
                self.objects_state["ключ"] = "найден"
            return True
        elif obj == "ковер":
            print("\nВы подняли край ковра. Под ним обычный каменный пол.")
            return True
        elif obj == "сундук":
            print("\nВы подошли к сундуку. Он заперт.")
            return True
        elif obj == "дверь":
            print("\nВы стоите перед массивной дверью.")
            if self.objects_state["дверь"] == "открыта":
                return self.complete_level()
            else:
                print("Дверь заперта. Нужно найти способ открыть ее.")
            return True
        else:
            print("\nНе могу подойти к этому объекту.")
            return True

    def use_key(self):
        print("\nВы пытаетесь использовать ключ...")
        time.sleep(1)
        
        if "дверь" in self.interacted_objects or input("Вы у двери? (да/нет): ").lower() == "да":
            print("Ржавый ключ с трудом поворачивается в замке...")
            time.sleep(2)
            print("ЩЕЛК! Замок поддается!")
            self.objects_state["дверь"] = "открыта"
            print("Дверь открыта! Теперь можно пройти дальше.")
            return True
        else:
            print("Здесь не к чему применить ключ. Попробуйте подойти к двери.")
            return True

    def use_door(self):
        if self.objects_state["дверь"] == "открыта":
            return self.complete_level()
        else:
            print("\nДверь заперта. Нужно найти ключ.")
            return True

    def complete_level(self):
        print(f"\n{BOLD}Дверь с скрипом открывается...{RESET}")
        time.sleep(2)
        print(f"{ITALIC}")
        print("Вы проходите через дверь и оказываетесь в следующем помещении.")
        print("Воздух наполняется странными ароматами трав и химикатов.")
        print("Это библиотека алхимика...")
        print(f"{RESET}")
        
        print(f"\n{BOLD}🎉 ВЫ УСПЕШНО ПРОШЛИ 1 УРОВЕНЬ! 🎉{RESET}")
        print("Элли попадает в Библиотеку знаний и ядовитого зелья...")
        
        time.sleep(3)
        return False

    def show_help(self):
        print("\n=== Доступные команды ===")
        print("осмотреть [объект] - осмотреть объект")
        print("взять [объект] - взять объект в инвентарь")
        print("использовать [объект] - использовать объект")
        print("идти [объект] - подойти к объекту")
        print("инвентарь - показать инвентарь")
        print("выход - выйти из игры")
        print("\n=== Объекты для изучения ===")
        print("холл, дверь, сундук, картина, ковер, ключ")

    def start_level(self):
        print("\n" + "="*60)
        print(f"{BOLD}УРОВЕНЬ 1: Забытый холл{RESET}")
        print("="*60)
        
        print(f"""{ITALIC}
Элли просыпается в Забытом холле Изумрудного замка. 
Воздух холоден и пылен. Впереди - массивная дверь, которая кажется 
единственным выходом из этого места. Где-то здесь должен быть ключ...
        {RESET}""")
        
        print("\nВведите 'помощь' для списка команд")
        
        while True:
            print("\n" + "-"*40)
            command = input("\nЧто вы хотите сделать? ")
            
            if not self.process_command(command):
                break
        
        return self.player_inventory

class Level2:
    def __init__(self, previous_inventory=None):
        self.player_inventory = previous_inventory if previous_inventory else []
        self.available_actions = ["осмотреть", "взять", "использовать", "читать", "инвентарь"]
        self.interacted_objects = set()
        
        self.objects_description = {
            "стол": "Алхимический стол с колбами, ретортами и ступками",
            "флаконы": "Два флакона: голубоватый и багряный",
            "голубой_флакон": "Флакон с призрачным голубоватым сиянием",
            "багряный_флакон": "Флакон, пульсирующий зловещим багряным светом",
            "свитки": "Два старинных свитка на столе",
            "первый_свиток": "Свиток с обгоревшими краями и символами зодиака вокруг пламени",
            "второй_свиток": "Свиток с символами: полумесяц, капля, перевернутая пирамида",
            "фолиант": "Толстая книга в кожаном переплете о алхимии",
            "полки": "Запыленные полки с книгами и свитками"
        }
        
        self.level_tasks = {
            "уровень_2": {
                "осмотрено_стол": False,
                "прочитано_свитки": False,
                "найдена_книга": False,
                "выбрано_зелье": False
            }

        
        self.player_stats = {
            "здоровье": 100,
            "отравление": 30,
            "статус": "отравлен"
        }

    def show_inventory(self):
        if not self.player_inventory:
            print("\nИнвентарь пуст.")
        else:
            print(f"\nИнвентарь: {', '.join(self.player_inventory)}")

    def show_health(self):
        print(f"\nЗдоровье: {self.player_stats['здоровье']}%")
        print(f"Отравление: {self.player_stats['отравление']}%")
        print(f"Статус: {self.player_stats['статус']}")

    def process_command(self, command):
        command = command.lower().strip()
        
        if command == "инвентарь":
            self.show_inventory()
            return True
        elif command == "здоровье":
            self.show_health()
            return True
        elif command == "помощь":
            self.show_help()
            return True
        elif command == "выход":
            return False
        
        parts = command.split()
        if len(parts) < 2:
            print("Не понял команду. Используйте: действие объект")
            return True
        
        action = parts[0]
        obj = "_".join(parts[1:])
        
        if action not in self.available_actions:
            print(f"Неизвестное действие. Доступные: {', '.join(self.available_actions)}")
            return True
        
        return self.execute_action(action, obj)

    def execute_action(self, action, obj):
        if action == "осмотреть":
            return self.examine_object(obj)
        elif action == "взять":
            return self.take_object(obj)
        elif action == "использовать":
            return self.use_object(obj)
        elif action == "читать":
            return self.read_object(obj)
        return True

    def examine_object(self, obj):
        if obj in self.objects_description:
            print(f"\n{self.objects_description[obj]}")
            self.interacted_objects.add(obj)
            
            if obj == "стол":
                self.level_tasks["уровень_2"]["осмотрено_стол"] = True
                print("На столе вы видите два флакона и свитки.")
            elif obj == "флаконы":
                print("Один флакон излучает голубоватое сияние, другой - багряное.")
            
            return True
        else:
            print("\nНе вижу такого объекта для осмотра.")
            return True

    def take_object(self, obj):
        takable_objects = ["голубой_флакон", "багряный_флакон", "фолиант", "первый_свиток", "второй_свиток"]
        
        if obj in takable_objects:
            if obj not in self.player_inventory:
                self.player_inventory.append(obj)
                print(f"{BOLD}\nВы взяли {obj.replace('_', ' ')}{RESET}")
                
                if obj == "фолиант":
                    self.level_tasks["уровень_2"]["найдена_книга"] = True
            else:
                print(f"\n{obj.replace('_', ' ')} уже в инвентаре")
        else:
            print("\nЭто нельзя взять.")
        
        return True

    def read_object(self, obj):
        readable_objects = {
            "первый_свиток": "Вы изучаете первый свиток: странные символы зодиака вокруг рисунка пламени. Непонятная надпись на незнакомом языке.",
            "второй_свиток": "Вы изучаете второй свиток: символы - полумесяц, капля, перевернутая пирамида.",
            "фолиант": f"""{BOLD}Вы находите раздел "Лечение Недуга Огненного Сердца":
Рецепт исцеляющего зелья: 
"Для усмирения пламени внутреннего, возьми траву лунного серебра (символ - полумесяц), 
добавь каплю росы утренней (символ - капля), и укроти силу земли (символ - перевернутая пирамида)."

ПРЕДОСТЕРЕЖЕНИЕ: 
"Берегись подделок! Зелье, созданное из тени смертной (багровый флакон), 
лишь усилит пламя, приведя к неминуемой гибели.{RESET}"""
        }
        
        if obj in readable_objects:
            if obj in self.player_inventory or obj in ["первый_свиток", "второй_свиток"]:
                print(f"\n{readable_objects[obj]}")
                
                if obj in ["первый_свиток", "второй_свиток"]:
                    self.level_tasks["уровень_2"]["прочитано_свитки"] = True
                
                return True
            else:
                print(f"\nСначала нужно взять {obj.replace('_', ' ')}")
                return True
        else:
            print("\nЭто нельзя прочитать.")
            return True

    def use_object(self, obj):
        if obj == "голубой_флакон":
            if obj in self.player_inventory:
                return self.drink_potion("голубой")
            else:
                print("\nСначала нужно взять голубой флакон")
        elif obj == "багряный_флакон":
            if obj in self.player_inventory:
                return self.drink_potion("багряный")
            else:
                print("\nСначала нужно взять багряный флакон")
        else:
            print("\nЭто нельзя использовать таким образом.")
        
        return True

    def drink_potion(self, potion_type):
        print(f"\nЭлли выпивает {potion_type} флакон...")
        time.sleep(2)
        
        if potion_type == "голубой":
            print("Она чувствует, как жар постепенно уходит.")
            print("Тело наполняется приятной прохладой. Исцеление успешно!")
            self.player_stats["здоровье"] = 100
            self.player_stats["отравление"] = 0
            self.player_stats["статус"] = "здоров"
            self.level_tasks["уровень_2"]["выбрано_зелье"] = True
            
            print("\n🎉 ВЫ УСПЕШНО ПРОШЛИ 2 УРОВЕНЬ! 🎉")
            print("Элли исцелилась и готова к следующим приключениям!")
            return False
        else:
            print("При первом же глотке жар в теле усиливается втрое!")
            print("Пламя жизни угасает, оставляя лишь ледяную пустоту...")
            self.player_stats["здоровье"] = 0
            self.player_stats["отравление"] = 100
            self.player_stats["статус"] = "мертв"
            print("Игра окончена. Элли стала еще одной жертвой библиотеки.")
            return False

    def show_help(self):
        print("\n=== Доступные команды ===")
        print("осмотреть [объект] - осмотреть объект")
        print("взять [объект] - взять объект в инвентарь")
        print("использовать [объект] - использовать объект")
        print("читать [объект] - прочитать объект")
        print("инвентарь - показать инвентарь")
        print("здоровье - показать состояние здоровья")
        print("выход - выйти из игры")
        print("\n=== Объекты для изучения ===")
        print("стол, флаконы, голубой_флакон, багряный_флакон")
        print("свитки, первый_свиток, второй_свиток, фолиант, полки")

    def start_level(self):
        print("\n" + "="*60)
        print(f"{BOLD}УРОВЕНЬ 2: Библиотека знаний и ядовитого зелья{RESET}")
        print("="*60)
        
        print(f"""{ITALIC}
Элли входит в библиотеку, чувствуя как по телу разливается неведомый жар.
В центре залы возвышается алхимический стол, словно алтарь научного колдовства.
На нем, среди колб, реторт и ступок, покоятся два флакона...
        {RESET}""")
        
        self.show_health()
        print("\nВведите 'помощь' для списка команд")
        
        while True:
            print("\n" + "-"*40)
            command = input("\nЧто вы хотите сделать? ")
            
            if not self.process_command(command):
                break
            
            if self.player_stats["здоровье"] <= 0:
                print("\nИгра окончена!")
                break
            elif self.level_tasks["уровень_2"]["выбрано_зелье"]:
                print("\nПоздравляем! Вы успешно прошли уровень 2!")
                break
        
        return self.player_inventory

class Level3:
    def __init__(self, previous_inventory=None):
        self.player_inventory = previous_inventory if previous_inventory else []
        self.available_actions = ["осмотреть", "взять", "использовать", "читать", "ответить", "инвентарь"]
        self.interacted_objects = set()
        
        self.objects_description = {
            "комната": "Круглая комната без окон с призрачным лунным светом, исходящим от огромного зеркала",
            "зеркало": "Огромное зеркало, занимающее почти всю стену. В нем мерцают размытые образы воспоминаний",
            "надпись": "Выгравированная надпись на древнем языке над зеркалом",
            "столик": "Небольшой столик из слоновой кости под зеркалом",
            "золотая_рамка": "Тонкая золотая рамка на столике, предназначенная для обрамления чего-либо",
            "клетка_с_щеглом": "Серебряная клетка с беспокойно мечущимся щеглом",
            "клубок_ниток": "Большой клубок сверкающих золотых ниток, кажущихся бесконечными",
            "глиняная_маска": "Простая глиняная маска, изображающая лицо мудреца с закрытыми глазами",
            "постаменты": "Три постамента вдоль стен с магическими предметами"
        }
        
        self.riddle_solved = False
        self.riddle_answer = "зеркало"

    def show_inventory(self):
        if not self.player_inventory:
            print("\nИнвентарь пуст.")
        else:
            print(f"\nИнвентарь: {', '.join(self.player_inventory)}")

    def process_command(self, command):
        command = command.lower().strip()
        
        if command == "инвентарь":
            self.show_inventory()
            return True
        elif command == "помощь":
            self.show_help()
            return True
        elif command == "выход":
            return False
        
        parts = command.split()
        if len(parts) < 2:
            print("Не понял команду. Используйте: действие объект")
            return True
        
        action = parts[0]
        obj = "_".join(parts[1:])
        
        if action not in self.available_actions:
            print(f"Неизвестное действие. Доступные: {', '.join(self.available_actions)}")
            return True
        
        return self.execute_action(action, obj)

    def execute_action(self, action, obj):
        if action == "осмотреть":
            return self.examine_object(obj)
        elif action == "взять":
            return self.take_object(obj)
        elif action == "использовать":
            return self.use_object(obj)
        elif action == "читать":
            return self.read_object(obj)
        elif action == "ответить":
            return self.answer_riddle(obj)
        return True

    def examine_object(self, obj):
        if obj in self.objects_description:
            print(f"\n{self.objects_description[obj]}")
            self.interacted_objects.add(obj)
            
            if obj == "зеркало":
                print("В зеркале вы видите размытые образы - воспоминания из прошлого...")
                print("Над зеркалом есть какая-то надпись.")
            elif obj == "постаменты":
                print("На трех постаментах расположены: клетка с щеглом, клубок ниток и глиняная маска.")
            elif obj == "столик":
                print("На столике лежит золотая рамка.")
            
            return True
        else:
            print("\nНе вижу такого объекта для осмотра.")
            return True

    def take_object(self, obj):
        takable_objects = ["золотая_рамка", "клетка_с_щеглом", "клубок_ниток", "глиняная_маска"]
        
        if obj in takable_objects:
            if obj not in self.player_inventory:
                self.player_inventory.append(obj)
                print(f"{BOLD}\nВы взяли {obj.replace('_', ' ')}{RESET}")
            else:
                print(f"\n{obj.replace('_', ' ')} уже в инвентаре")
        else:
            print("\nЭто нельзя взять.")
        
        return True

    def read_object(self, obj):
        if obj == "надпись":
            print(f"""
{BOLD}Надпись над зеркалом гласит:
"Я - отражение того, что было и есть, но никогда не смогу быть тем, что будет. 
Я храню правду в искаженной форме, и лишь тот, кто сумеет разглядеть 
сквозь мои иллюзии, найдет путь дальше. Ключ к разгадке лежит 
в переплетении прошлого и настоящего..."

{ITALIC}Вспомнив слова из закодированной книги, вы понимаете продолжение:
"Я отражаю Истину, но искажаю Лица. Кто я?"{RESET}
            """)
            return True
        else:
            print("\nЭто нельзя прочитать.")
            return True

    def use_object(self, obj):
        if obj == "золотая_рамка":
            if obj in self.player_inventory:
                print(f"\n{BOLD}Вы подносите золотую рамку к зеркалу...{RESET}")
                time.sleep(2)
                print("Рамка начинает светиться, и в зеркале проявляются четкие образы.")
                print("Теперь загадка стала понятнее!")
                return True
            else:
                print("\nСначала нужно взять золотую рамку")
                return True
        else:
            print("\nЭто нельзя использовать здесь.")
            return True

    def answer_riddle(self, answer):
        print(f"\nВы отвечаете: '{answer}'...")
        time.sleep(2)
        
        if answer.lower() == self.riddle_answer:
            print(f"{BOLD}Зеркало начинает мерцать и медленно отодвигается в сторону!{RESET}")
            print("За ним открывается проход в следующую комнату...")
            self.riddle_solved = True
            return False
        else:
            print("Ничего не происходит. Похоже, это неправильный ответ.")
            print("Попробуйте еще раз или поищите подсказки в комнате.")
            return True

    def show_help(self):
        print("\n=== Доступные команды ===")
        print("осмотреть [объект] - осмотреть объект")
        print("взять [объект] - взять объект в инвентарь")
        print("использовать [объект] - использовать объект")
        print("читать [объект] - прочитать объект")
        print("ответить [ответ] - ответить на загадку")
        print("инвентарь - показать инвентарь")
        print("выход - выйти из игры")
        print("\n=== Объекты для изучения ===")
        print("комната, зеркало, надпись, столик, золотая_рамка")
        print("клетка_с_щеглом, клубок_ниток, глиняная_маска, постаменты")

    def start_level(self):
        print("\n" + "="*60)
        print(f"{BOLD}УРОВЕНЬ 3: Загадочная комната с зеркалом{RESET}")
        print("="*60)
        
        print(f"""{ITALIC}
Элли проходит через открывшуюся дверь и попадает в круглую комнату без окон.
Воздух здесь неподвижен и прохладен. Единственный источник света - призрачное 
свечение огромного зеркала, занимающего всю стену. В отражении мелькают 
размытые образы, словно воспоминания, пытающиеся пробиться сквозь пелену времени.

Вдоль стен стоят три постамента с таинственными предметами, а под зеркалом 
виднеется небольшой столик с золотой рамкой.
        {RESET}""")
        
        print("\nВведите 'помощь' для списка команд")
        
        while True:
            print("\n" + "-"*40)
            command = input("\nЧто вы хотите сделать? ")
            
            if not self.process_command(command):
                break
            
            if self.riddle_solved:
                print(f"\n{BOLD}🎉 ВЫ УСПЕШНО ПРОШЛИ 3 УРОВЕНЬ! 🎉{RESET}")
                print("Загадка разгадана! Путь к логову крылатой обезьяны открыт...")
                time.sleep(3)
                break
        
        return self.player_inventory

class Level4:
    def __init__(self, previous_inventory=None):
        self.player_inventory = previous_inventory if previous_inventory else []
        self.available_actions = ["осмотреть", "взять", "использовать", "атаковать", "убежать", "инвентарь"]
        self.interacted_objects = set()
        
        self.objects_description = {
            "логово": "Просторная пещера с высоким сводом, откуда свисают лианы и корни деревьев",
            "обезьяна": "Мощная крылатая обезьяна с горящими красными глазами и огромными крыльями",
            "выход": "Светящийся портал в дальнем конце логова - путь к свободе",
            "кости": "Разбросанные по полу кости предыдущих жертв обезьяны",
            "гнездо": "Большое гнездо из веток и перьев в центре логова",
            "сокровища": "Блестящие безделушки и драгоценности, собранные обезьяной"
        }
        
        self.monkey_stats = {
            "здоровье": 100,
            "атака": 30,
            "защита": 20,
            "состояние": "бодрствует"
        }
        
        self.player_stats = {
            "здоровье": 100,
            "атака": 15,
            "защита": 10
        }
        
        self.level_completed = False

    def show_inventory(self):
        if not self.player_inventory:
            print("\nИнвентарь пуст.")
        else:
            print(f"\nИнвентарь: {', '.join(self.player_inventory)}")

    def show_stats(self):
        print(f"\n{ITALIC}=== ВАШИ ХАРАКТЕРИСТИКИ ===")
        print(f"Здоровье: {self.player_stats['здоровье']}%")
        print(f"Атака: {self.player_stats['атака']}")
        print(f"Защита: {self.player_stats['защита']}{RESET}")
        
        print(f"\n{ITALIC}=== ХАРАКТЕРИСТИКИ ОБЕЗЬЯНЫ ===")
        print(f"Здоровье: {self.monkey_stats['здоровье']}%")
        print(f"Атака: {self.monkey_stats['атака']}")
        print(f"Защита: {self.monkey_stats['защита']}")
        print(f"Состояние: {self.monkey_stats['состояние']}{RESET}")

    def process_command(self, command):
        command = command.lower().strip()
        
        if command == "инвентарь":
            self.show_inventory()
            return True
        elif command == "статус":
            self.show_stats()
            return True
        elif command == "помощь":
            self.show_help()
            return True
        elif command == "выход":
            return False
        
        parts = command.split()
        if len(parts) < 2:
            print("Не понял команду. Используйте: действие объект")
            return True
        
        action = parts[0]
        obj = "_".join(parts[1:])
        
        if action not in self.available_actions:
            print(f"Неизвестное действие. Доступные: {', '.join(self.available_actions)}")
            return True
        
        return self.execute_action(action, obj)

    def execute_action(self, action, obj):
        if action == "осмотреть":
            return self.examine_object(obj)
        elif action == "взять":
            return self.take_object(obj)
        elif action == "использовать":
            return self.use_object(obj)
        elif action == "атаковать":
            return self.attack_monkey(obj)
        elif action == "убежать":
            return self.escape()
        return True

    def examine_object(self, obj):
        if obj in self.objects_description:
            print(f"\n{self.objects_description[obj]}")
            self.interacted_objects.add(obj)
            
            if obj == "обезьяна":
                print("Крылатая обезьяна внимательно следит за вашими движениями.")
                if "кости" in self.interacted_objects:
                    print("Она выглядит голодной и агрессивной.")
            elif obj == "выход":
                print("Портал мерцает призывно, но обезьяна преграждает путь.")
            
            return True
        else:
            print("\nНе вижу такого объекта для осмотра.")
            return True

    def take_object(self, obj):
        if obj == "сокровища":
            print("\nОбезьяна рычит, когда вы пытаетесь взять ее сокровища!")
            print("Лучше не злить ее без необходимости.")
            return True
        else:
            print("\nЭто нельзя взять.")
            return True

    def use_object(self, obj):
        if obj in self.player_inventory:
            if obj == "клетка_с_щеглом":
                return self.use_birdcage()
            elif obj == "клубок_ниток":
                return self.use_thread_ball()
            elif obj == "глиняная_маска":
                return self.use_clay_mask()
            elif obj == "золотая_рамка":
                print("\nВы пытаетесь использовать золотую рамку, но она не оказывает эффекта на обезьяну.")
                return True
            else:
                print(f"\n{obj.replace('_', ' ')} не оказывает эффекта здесь.")
                return True
        else:
            print(f"\nСначала нужно взять {obj.replace('_', ' ')}")
            return True

    def use_birdcage(self):
        print(f"\n{BOLD}Вы открываете клетку и выпускаете щегла!{RESET}")
        time.sleep(2)
        print("Щегол вылетает и начинает порхать перед обезьяной.")
        print("Обезьяна заинтересовано следит за птицей, отвлекаясь от вас.")
        
        self.monkey_stats["состояние"] = "отвлечена"
        self.player_inventory.remove("клетка_с_щеглом")
        
        print("Теперь у вас есть шанс атаковать или попытаться убежать!")
        return True

    def use_thread_ball(self):
        print(f"\n{BOLD}Вы разматываете клубок золотых ниток!{RESET}")
        time.sleep(2)
        print("Волшебные нити опутывают лапы обезьяны, сковывая ее движения.")
        
        self.monkey_stats["защита"] = max(5, self.monkey_stats["защита"] - 10)
        self.monkey_stats["атака"] = max(15, self.monkey_stats["атака"] - 10)
        self.monkey_stats["состояние"] = "опутана"
        self.player_inventory.remove("клубок_ниток")
        
        print("Обезьяна стала медленнее и уязвимее!")
        return True

    def use_clay_mask(self):
        print(f"\n{BOLD}Вы надеваете глиняную маску мудреца!{RESET}")
        time.sleep(2)
        print("Маска начинает светиться, и ваш голос становится глубоким и властным.")
        print("Вы приказываете обезьяне: 'УЙДИ ОТСЮДА И НЕ МЕШАЙ МНЕ!'")
        time.sleep(2)
        
        if random.random() > 0.3:  
            print("Обезьяна в ужасе отступает и улетает вглубь пещеры!")
            self.monkey_stats["состояние"] = "напугана"
            self.monkey_stats["здоровье"] = 0
            self.level_completed = True
            self.player_inventory.remove("глиняная_маска")
            return False
        else:
            print("Обезьяна лишь разозлилась еще больше!")
            self.monkey_stats["атака"] += 10
            self.player_inventory.remove("глиняная_маска")
            return True

    def attack_monkey(self, weapon):
        print(f"\n{BOLD}Вы атакуете крылатую обезьяну!{RESET}")
        time.sleep(2)
        
 
        player_damage = max(5, self.player_stats["атака"] - self.monkey_stats["защита"] // 2)
        monkey_damage = max(10, self.monkey_stats["атака"] - self.player_stats["защита"] // 2)
        
 
 
        self.monkey_stats["здоровье"] -= player_damage
        print(f"Вы наносите обезьяне {player_damage} урона!")
        
        if self.monkey_stats["здоровье"] <= 0:
            print("Крылатая обезьяна повержена!")
            self.level_completed = True
            return False
        
        print("Обезьяна контратакует!")
        time.sleep(1)
        self.player_stats["здоровье"] -= monkey_damage
        print(f"Обезьяна наносит вам {monkey_damage} урона!")
        
        if self.player_stats["здоровье"] <= 0:
            print("Вы повержены! Игра окончена.")
            return False
        
        self.show_stats()
        return True

    def escape(self):
        print(f"\n{BOLD}Вы пытаетесь убежать от обезьяны!{RESET}")
        time.sleep(2)
        
        escape_chance = 0.4 
        
        if self.monkey_stats["состояние"] in ["отвлечена", "опутана"]:
            escape_chance += 0.3
            print("Обезьяна отвлечена - у вас больше шансов на успех!")
        
        if random.random() < escape_chance:
            print("Вам удалось проскочить мимо обезьяны к светящемуся порталу!")
            self.level_completed = True
            return False
        else:
            print("Обезьяна перехватывает вас и атакует!")
            damage = max(15, self.monkey_stats["атака"] - self.player_stats["защита"] // 3)
            self.player_stats["здоровье"] -= damage
            print(f"Обезьяна наносит вам {damage} урона!")
            
            if self.player_stats["здоровье"] <= 0:
                print("Вы повержены! Игра окончена.")
                return False
            
            self.show_stats()
            return True

    def show_help(self):
        print("\n=== Доступные команды ===")
        print("осмотреть [объект] - осмотреть объект")
        print("взять [объект] - взять объект в инвентарь")
        print("использовать [объект] - использовать объект из инвентаря")
        print("атаковать [обезьяну] - атаковать крылатую обезьяну")
        print("убежать - попытаться убежать к выходу")
        print("инвентарь - показать инвентарь")
        print("статус - показать характеристики")
        print("выход - выйти из игры")
        print("\n=== Объекты для изучения ===")
        print("логово, обезьяна, выход, кости, гнездо, сокровища")

    def start_level(self):
        print("\n" + "="*60)
        print(f"{BOLD}УРОВЕНЬ 4: Логово крылатой обезьяны{RESET}")
        print("="*60)
        
        print(f"""{ITALIC}
Элли входит в просторную пещеру с высоким сводом. Воздух тяжел и влажен.
В центре логова, на груде костей и перьев, восседает огромная крылатая обезьяна.
Ее красные глаза горят яростью, а мощные крылья расправлены в угрожающей позе.

В дальнем конце пещеры мерцает светящийся портал - путь к свободе.
Но чтобы достичь его, нужно преодолеть свирепого стража...
        {RESET}""")
        
        self.show_stats()
        print("\nВведите 'помощь' для списка команд")
        
        while True:
            print("\n" + "-"*40)
            command = input("\nЧто вы хотите сделать? ")
            
            if not self.process_command(command):
                break
            
            if self.level_completed:
                print(f"\n{BOLD}🎉 ВЫ УСПЕШНО ПРОШЛИ 4 УРОВЕНЬ! 🎉{RESET}")
                print("Крылатая обезьяна побеждена! Путь к свободе открыт...")
                time.sleep(3)
                break
            elif self.player_stats["здоровье"] <= 0:
                print("\nИгра окончена! Элли не смогла преодолеть последнее испытание.")
                break
        
        return self.level_completed


def main():
    print(f"{BOLD}=== ВОЛШЕБНИК ИЗУМРУДНОГО ГОРОДА ==={RESET}")
    print("Приключение Элли начинается...")
    time.sleep(2)
    
    level1 = Level1()
    inventory = level1.start_level()
    
    if inventory is not None:
        print("\nПереход к следующему уровню...")
        time.sleep(2)
        
        level2 = Level2(previous_inventory=inventory)
        inventory = level2.start_level()
    
    if inventory is not None:
        print("\nПереход к следующему уровню...")
        time.sleep(2)
        
        level3 = Level3(previous_inventory=inventory)
        inventory = level3.start_level()
    
    if inventory is not None:
        print("\nПереход к финальному уровню...")
        time.sleep(2)
        
        level4 = Level4(previous_inventory=inventory)
        game_completed = level4.start_level()
        
        if game_completed:
            print(f"""
{BOLD}=== ПОБЕДА! ==={RESET}

{ITALIC}
Элли проходит через светящийся портал и оказывается на солнечной поляне 
за пределами мрачного замка. Воздух свеж и наполнен ароматами полевых цветов.

Вдали виднеются изумрудные башни родного города. Приключение подошло к концу, 
но впереди ее ждет долгая и счастливая жизнь, полная новых открытий.

Спасибо, что помогли Элли пройти этот трудный путь!
{RESET}
            """)
        else:
            print(f"""
{ITALIC}
К сожалению, Элли не удалось преодолеть все испытания...
Но ее дух останется в стенах замка как напоминание о смелости 
и упорстве перед лицом опасности.
{RESET}
            """)

if __name__ == "__main__":
    main()
