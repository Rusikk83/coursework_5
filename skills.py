from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from unit import BaseUnit

class Skill(ABC):
    """
    Базовый класс умения
    """
    user = None
    target = None

    @property
    @abstractmethod
    def name(self):
        return self.name

    @property
    @abstractmethod
    def stamina(self):
        return self.stamina

    @property
    @abstractmethod
    def damage(self):
        return self.damage

    @abstractmethod
    def skill_effect(self) -> str:
        pass

    def _is_stamina_enough(self):
        return self.user.stamina > self.stamina

    def use(self, user: BaseUnit, target: BaseUnit) -> str:
        """
        Проверка, достаточно ли выносливости у игрока для применения умения.
        Для вызова скилла везде используем просто use
        """
        self.user = user
        self.target = target
        if self._is_stamina_enough:
            self.user._is_skill_used = True
            return self.skill_effect()
        return f"{self.user.name} попытался использовать {self.name} но у него не хватило выносливости."


class FuryPunch(Skill):
    name = "Свирепый пинок"
    stamina = 6
    damage = 12

    def skill_effect(self):
        # TODO логика использования скилла -> return str
        # TODO в классе нам доступны экземпляры user и target - можно использовать любые их методы
        # TODO именно здесь происходит уменшение стамины у игрока применяющего умение и
        # TODO уменьшение здоровья цели.
        # TODO результат применения возвращаем строкой
        self.target.hp = round(self.target.hp - self.damage, 1) if self.target.hp > self.damage else 0
        self.user.stamina -= self.stamina
        if self.target.hp > 0:
            return f"{self.user.name}, используя умение {self.name}, поражает  соперника и наносит {self.damage} урона."
        else:
            return f"{self.user.name}, используя умение {self.name}, отправляет соперника в нокаут"


class HardShot(Skill):
    name = "Мощный укол"
    stamina = 5
    damage = 15

    def skill_effect(self):
        self.target.hp = round(self.target.hp - self.damage, 1) if self.target.hp > self.damage else 0
        self.user.stamina -= self.stamina
        if self.target.hp > 0:
            return f"{self.user.name}, используя умение {self.name}, поражает  соперника и наносит {self.damage} урона."
        else:
            return f"{self.user.name}, используя умение {self.name}, отправляет соперника в нокаут"
