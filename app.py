from flask import Flask, request, render_template, redirect, url_for

from base import Arena
from classes import unit_classes
from equipment import Equipment
from unit import BaseUnit, PlayerUnit, EnemyUnit

app = Flask(__name__)


heroes = {
    "player": BaseUnit,
    "enemy": BaseUnit
}

arena = Arena() # TODO инициализируем класс арены


eq = Equipment()
result = {
    "header": "Смертельный бой",      # для названия страниц
    "classes": unit_classes,    # для названия классов
    "weapons": eq.get_weapons_names(),    # для названия оружия
    "armors": eq.get_armors_names()   # для названия брони
}


@app.route("/")
def menu_page():
    with open("templates/index.html", encoding="UTF8") as file:
        page = file.read()
    return page


@app.route("/fight/")
def start_fight():
    # TODO выполняем функцию start_game экземпляра класса арена и передаем ему необходимые аргументы
    # TODO рендерим экран боя (шаблон fight.html)
    arena = Arena()
    arena.start_game(heroes["player"], heroes["enemy"])
    return render_template("fight.html", heroes=heroes, result="Бой начался!")


@app.route("/fight/hit")
def hit():
    # TODO кнопка нанесения удара
    # TODO обновляем экран боя (нанесение удара) (шаблон fight.html)
    # TODO если игра идет - вызываем метод player.hit() экземпляра класса арены
    # TODO если игра не идет - пропускаем срабатывание метода (простот рендерим шаблон с текущими данными)
    if arena.game_is_running:
        result = arena.player_hit()
        return render_template("fight.html", heroes=heroes, result=result)
    else:
        return render_template("fight.html", heroes=heroes, battle_result=arena.battle_result)



@app.route("/fight/use-skill")
def use_skill():
    # TODO кнопка использования скилла
    # TODO логика пркатикчески идентична предыдущему эндпоинту
    if arena.game_is_running:
        result = arena.player_use_skill()
        return render_template("fight.html", heroes=heroes, result=result)
    else:
        return render_template("fight.html", heroes=heroes, battle_result=arena.battle_result)


@app.route("/fight/pass-turn")
def pass_turn():
    # TODO кнопка пропус хода
    # TODO логика пркатикчески идентична предыдущему эндпоинту
    # TODO однако вызываем здесь функцию следующий ход (arena.next_turn())
    if arena.game_is_running:
        result = arena.next_turn()
        return render_template("fight.html", heroes=heroes, result=result)
    else:
        return render_template("fight.html", heroes=heroes, battle_result=arena.battle_result)


@app.route("/fight/end-fight")
def end_fight():
    # TODO кнопка завершить игру - переход в главное меню
    # return render_template("index.html", heroes=heroes)
    arena._end_game()
    return redirect(url_for('menu_page'))


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():
    # TODO кнопка выбор героя. 2 метода GET и POST
    # TODO на GET отрисовываем форму.
    # TODO на POST отправляем форму и делаем редирект на эндпоинт choose enemy
    if request.method == "GET":
        result["header"] = "Игрок"
        return render_template("hero_choosing.html", result=result)
    if request.method == "POST":
        heroes["player"] = PlayerUnit(request.form.get("name"), unit_classes[request.form.get("unit_class")])
        heroes["player"].equip_weapon(eq.get_weapon(request.form.get("weapon")))
        heroes["player"].equip_armor(eq.get_armor(request.form.get("armor")))
        return redirect(url_for('choose_enemy'))


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    # TODO кнопка выбор соперников. 2 метода GET и POST
    # TODO также на GET отрисовываем форму.
    # TODO а на POST отправляем форму и делаем редирект на начало битвы
    if request.method == "GET":
        result["header"] = "Противник"
        return render_template("hero_choosing.html", result=result)
    if request.method == "POST":
        heroes["enemy"] = EnemyUnit(request.form.get("name"), unit_classes[request.form.get("unit_class")])
        heroes["enemy"].equip_weapon(eq.get_weapon(request.form.get("weapon")))
        heroes["enemy"].equip_armor(eq.get_armor(request.form.get("armor")))
        return redirect(url_for('start_fight'))

if __name__ == "__main__":
    app.run()