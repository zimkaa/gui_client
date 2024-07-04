from __future__ import annotations
import json
import re
from functools import cache
from pathlib import Path
from typing import Any

from pandas import DataFrame
from pandas import concat

from .config_fight import get_fight_config
from src.config import logger
from src.config.game import hits
from src.domain.pattern.fight import pattern as fight_pattern
from src.domain.value_object.classes import PersonType
from src.domain.value_object.schemas import FightConfig
from src.domain.value_object.schemas import Hit


@cache
def get_pattern(*, value: str) -> re.Pattern:
    if value == "lives_g2":
        pattern = fight_pattern.FIND_LIVES_G2
    else:
        pattern = fight_pattern.FIND_FIGHT_VARIABLES_PART1 + value + fight_pattern.FIND_FIGHT_VARIABLES_PART2
    return re.compile(pattern)


class Fight:
    def __init__(self, nickname: str, person_type: PersonType = PersonType.MAG) -> None:
        self._nickname = nickname
        self.person_type = person_type
        self._read_json()
        self._stop = False
        self._scroll = True
        self._hits_df: DataFrame = DataFrame()
        self._dict_hit: dict[str, dict[str, str]]
        self.fight_pm: list[str]
        self.fight_ty: list[str] = []
        self.param_en: list[str]
        self.param_ow: list[str]
        self.lives_g1: list[str]
        self.lives_g2: list[str]
        self.magic_in: list[str]
        self.alchemy: list[str]
        self.logs: list[str]
        self._bot_count: int = 0

        self.logger = logger

        self._bot_level = "unknown"
        self._bot_name = "unknown"

        self._my_od = 0
        self._my_mp = 0.0
        self._my_hp = 0.0
        self._my_all_mp = 0.0
        self._my_all_hp = 0.0

        self._simple_hit_od = 0

    def setup_value(self, page_text: str) -> None:
        self._page_text = page_text
        self._list_hits: list[int] = []

        self._ina = ""
        self._inb = ""
        self._inu = ""

        self._prepare_data()

        if self.param_en:
            self._get_self_info()
            self._get_enemy_info()
            self._print_log()
        else:
            text = f"{self._nickname} wait hit from enemy"
            self.logger.error(text)

    def _prepare_data(self) -> None:
        name_list = (
            "fight_ty",
            "param_ow",
            "lives_g1",
            "lives_g2",
            "alchemy",
            "magic_in",
            "param_en",
            "fight_pm",
            "logs",
        )
        for attribute_name in name_list:
            data = self._find_value(attribute_name)
            if data:
                setattr(self, attribute_name, data)
            else:
                setattr(self, attribute_name, [])

    def _find_value(self, value: str) -> list[str] | list[Any]:  # noqa: PLR0911
        pattern = get_pattern(value=value)
        result: list[str] = pattern.findall(self._page_text)
        if result:
            if value == "logs":
                new_res = result[0].replace(",,", ',"was empty in log",').replace(",,", ',"was empty in log",')
                new_res2 = f"[{new_res}]"
                return eval(new_res2)  # noqa: S307
            result_value: list[str] = result[0].replace("]", "").replace('"', "").replace("[", "").split(",")
            return result_value

        if self.fight_ty and self.fight_ty[4] == "2":
            self.logger.debug("end battle value = %s", value)
            return []

        if value == "alchemy":
            text = f"{self._nickname} alchemy empty Потому что нет свитка и банок"
            self.logger.debug(text)
            return []

        if value in ("lives_g1", "lives_g2", "magic_in", "param_en", "fight_pm", "logs"):
            text = f"{self._nickname} {value} Потому что только часть атрибутов доступна"
            self.logger.debug(text)
            return []

        if value in ("fight_ty",):
            text = f"{self._nickname} {value} Потому что только часть атрибутов доступна"
            self.logger.debug(text)
            return []

        text = f"{self._nickname} {value} Потому что только часть атрибутов доступна"
        self.logger.debug(text)
        return []

    def _get_self_info(self) -> None:
        if self.param_ow:
            self._my_mp = float(self.param_ow[3])
            self._my_all_mp = float(self.param_ow[4])
            self._my_hp = float(self.param_ow[1])
            self._my_all_hp = float(self.param_ow[2])
        if self.fight_pm:
            self._simple_hit_od = int(self.fight_pm[2])
            self._my_od = int(self.fight_pm[1])

    def _get_enemy_info(self) -> None:
        self._bot_name = self.param_en[0] if self.param_en else "unknown"
        self._bot_hp = float(self.param_en[1]) if self.param_en else 0.0
        self._bot_max_hp = float(self.param_en[2]) if self.param_en else 0.0
        self._bot_mp = float(self.param_en[3]) if self.param_en else 0.0
        self._bot_max_mp = float(self.param_en[4]) if self.param_en else 0.0
        self._bot_level = self.param_en[5] if self.param_en else "unknown"

    def _print_log(self) -> None:
        first = f"bot_level={self._bot_level} bot_hp={self._bot_hp}"
        second = f" my_od={self._my_od} my_mp={self._my_mp}"
        third = f" my_hp={self._my_hp}"
        text = first + second + third
        self.logger.info(text)

    def get_state(self) -> tuple[int, float, float]:
        return self._my_od, self._my_mp, self._my_hp

    def _heal_check(self, value: float, need_to_check: float) -> bool:
        if value <= need_to_check:
            return True
        return False

    def _check_potion(self, my_list: list[int]) -> list[int]:
        magic = []
        for value in self.magic_in:
            int_value = int(value)
            if int_value in my_list:
                magic.append(int_value)
        if not magic:
            text = f"{self._nickname} No item on belt in fight or scroll"
            self.logger.critical(text)
        return magic

    def _create_sorted_df(self, df: DataFrame, magic: list[int]) -> DataFrame:
        query = []
        list_element = []
        for num, element in enumerate(magic):
            for index_num in df.index:
                if df["code"][index_num] == element:
                    query.append(f"{element}_{self.alchemy[num]}@")
                    list_element.append(element)
        new_df = DataFrame()
        for name in list_element:
            result = df[df["code"] == name]
            new_df = concat([new_df, result], ignore_index=True)
        new_df["query"] = query
        return new_df.sort_values(by="priority")

    def _using_mp(self) -> None:
        self.logger.info("---------------Use MP--------------------")
        boost_mp = 0
        for index_num in self._sorted_df.index:
            boost_mp += int(self._sorted_df["mp_boost"][index_num])
            query_mp = self._sorted_df["query"][index_num]
            if self._my_od <= 30:  # noqa: PLR2004
                break
            condition = boost_mp - self._fight_config.MP_NEED_INSIDE_BATTLE
            self._my_od -= int(self._sorted_df["od"][index_num])
            if condition >= 0:
                self._ina += query_mp
                break
            self._ina += query_mp

        part1 = f"{self._nickname} USING MP ina={self._ina} my_mp={self._my_mp}"
        part2 = f" MP_NEED_INSIDE_BATTLE={self._fight_config.MP_NEED_INSIDE_BATTLE}"
        part3 = f" condition {condition} boost_mp={boost_mp}"
        part4 = f" my_od={self._my_od}"
        text = part1 + part2 + part3 + part4
        self.logger.critical(text)

    def _heal_mp(self) -> None:
        magic = self._check_potion(hits.MP_LIST_MP)
        if magic:
            data_frame = DataFrame(hits.DICT_NAME_BOOST_MP)
            self._sorted_df = self._create_sorted_df(data_frame, magic)
            self._using_mp()

    def _using(self, sorted_df: DataFrame) -> None:
        self.logger.info("---------------Use--------------------")
        if self._my_od >= 110:  # noqa: PLR2004
            for index_num in sorted_df.index:
                query_mp = sorted_df["query"][index_num]
                self._ina += query_mp
                self._my_od -= int(sorted_df["od"][index_num])

    def _heal_hp(self) -> None:
        self._ina += "320@"
        self._my_od -= 30

    def _read_json(self) -> None:
        dir_path = Path(__file__).parent.resolve()
        file_name = "hit_dict"
        file_path = dir_path / "settings" / f"{file_name}.json"

        with Path(file_path).open("r", encoding="utf8") as file:
            self._dict_hit = json.loads(file.read())

    def _check_use_hp(self) -> None:
        if self._fight_config.HP:
            need_hp = self._conditions_heal(self._my_all_hp, needed_percent=self._fight_config.NEED_HP_PERCENT)
            if self._heal_check(self._my_hp, need_hp):
                self._heal_hp()

    def _check_use_mp(self) -> None:
        if self._fight_config.MP:
            need_mp = self._conditions_heal(self._my_all_mp, need=self._fight_config.MP_NEED_INSIDE_BATTLE)
            if self._heal_check(self._my_mp, need_mp):
                text = f"\n{need_mp=} {self._my_mp=}\n"
                self.logger.debug(text)
                self._heal_mp()

    def _check_use_stable_mag_hit(self) -> None:
        min_mp_coefficient = self._fight_config.MIN_MP_COEFFICIENT
        min_mp_for_hits = self._my_all_mp * min_mp_coefficient

        self._hit = DataFrame()

        if self._my_mp > min_mp_for_hits:
            if self._fight_config.STABLE_MAGIC_HIT:
                stable_magic_hit = self._prepares_stable_magic_hit()
                self._hit = DataFrame(stable_magic_hit).sort_values(by="priority")
        else:
            text = f"{self._nickname} Not enough MP for mag hit {self._my_mp} < {min_mp_for_hits}"
            self.logger.warning(text)

    def _check_use_stable_hit(self) -> None:
        if self._fight_config.STABLE_HIT:
            stable_hit = self._prepares_stable_hit()
            if self._hit.empty:
                self._hit = DataFrame(stable_hit).sort_values(by="priority")

    def _check_use_kick(self) -> None:
        if self._fight_config.KICK:
            if self.person_type == PersonType.WARRIOR:
                self._use_kick(hits.WARRIOR_KICK)
            else:
                self._use_kick(hits.MAG_KICK)

    def _check_use_potion(self) -> None:
        self.logger.debug("_check_use_potion")
        if self.person_type == PersonType.MAG:
            item_id = "330"
            item_name = "Зелье Элементалиста"
        else:
            item_id = "328"
            item_name = "Зелье Ярость Берсерка"

        if item_id in self.magic_in:
            self._using_potion(item_name)

    def _using_potion(self, item_name: str) -> None:
        self.logger.debug("_using_potion")
        self._convert_name_to_value(item_name)
        if self._my_od >= self._item_od:
            for num, element in enumerate(self.magic_in):
                if self._item_value == element:
                    self._ina += f"{self._item_value}_{self.alchemy[num]}@"
                    self._my_od -= self._item_od

            text = f"{self._nickname} USING POTION ina={self._ina} my_od={self._my_od}"
            self.logger.critical(text)

    def _check_use_scroll(self) -> None:
        if self._fight_config.SCROLL and self._scroll:
            self._use_scroll(hits.HIT_SCROLLS[5])

    def _init_fight_config(self) -> None:
        config = None
        bot_group = None

        file_name = f"fight_config_{self.person_type}"
        fight_conf = get_fight_config(file_name)
        for element in fight_conf:
            if self._bot_name in element["names"]:
                bot_group = element
                for key, value in element["level_group"].items():
                    if self._bot_level in value:
                        config = element["level"].get(key)
                        break
                break

        if not config and bot_group:
            config = bot_group["level"].get("default")
            text = f"Set default {config=}"
            self.logger.debug(text)

        if config:
            self._fight_config = FightConfig(**config)
        else:
            text = f"{self._nickname} Fight config not found. {self._bot_name=} Use default!!!"
            self.logger.critical(text)
            self._fight_config = FightConfig()

    def _init_config(self) -> None:
        self._init_fight_config()

        self._check_use_hp()

        self._check_use_mp()

        self._check_use_stable_mag_hit()

        self._check_use_stable_hit()

        self._check_use_scroll()

    def _prepares_stable_hit(self) -> dict:
        hit_od = self._simple_hit_od
        return {
            "name": [
                "Прицельный",
                "Простой",
            ],
            "code": [1, 0],
            "mp_cost": [0, 0],
            "od": [hit_od + 20, hit_od],
            "priority": [1, 0],
        }

    def _prepares_stable_magic_hit(self) -> dict:
        mp_hit = self._fight_config.MP_HIT
        return {
            "name": [
                "Mind Blast",
                "Spirit Arrow",
            ],
            "code": [3, 2],
            "mp_cost": [mp_hit, mp_hit],
            "od": [90, 50],
            "priority": [0, 1],
        }

    def fight(self, bait: bool = False) -> None:  # noqa: FBT001, FBT002
        text = f"fight {bait=}"
        self.logger.debug(text)
        self._all_info()

        self._init_config()

        self._get_hit()

        if bait:
            self._check_use_potion()

        self._check_use_kick()

        self._get_query()

    def _all_info(self) -> None:
        number = 2
        hp_bots = []
        len_lives_g1 = len(self.lives_g1)
        if len_lives_g1 % 5 == 0:
            value = self.lives_g1
            max_number_iter = int(len_lives_g1 / 5)
        else:
            max_number_iter = int(len(self.lives_g2) / 5)
            value = self.lives_g2
        for _ in range(max_number_iter):
            hp_bots.append(value[number])
            number += 5
        text = f"hp_bots = {hp_bots}"
        self._bot_count = len(hp_bots)
        self.logger.info(text)
        text2 = f"bot_name = {self._bot_name}"
        self.logger.debug(text2)

    def _conditions_heal(self, maximum: float, needed_percent: float = 0.0, need: float = 0.0) -> float:
        if needed_percent and need:
            min_value = maximum * needed_percent
            if min_value > need:
                return min_value
            return need
        if needed_percent:
            return maximum * needed_percent
        return need

    def _use_scroll(self, scroll: str) -> None:
        self._convert_name_to_value(scroll)
        if self._my_od >= (30 + self._item_od):
            for num, element in enumerate(self.magic_in):
                if self._item_value == element:
                    self._ina += f"{self._item_value}_{self.alchemy[num]}@"
                    self._my_od -= self._item_od

    def _convert_name_to_value(self, name: str) -> None:
        self._item_value = str(self._dict_hit[name]["number"])
        self._item_od = int(self._dict_hit[name]["od"])
        self._item_mp = int(self._dict_hit[name]["mp"])

    def _use_kick(self, kicks: list[str]) -> None:
        count = self._fight_config.KICK_COUNT
        for item in kicks:
            if count:
                self._convert_name_to_value(item)
                if (
                    self._my_od >= self._item_od
                    and self._item_value in self.magic_in
                    and f"{self._item_value}@" not in self._ina
                ):
                    self._ina += f"{self._item_value}@"
                    self._my_od -= self._item_od
                    count -= 1
                    text = f"using KICK {self._item_value=}"
                    self.logger.debug(text)

    def _get_hit(self) -> None:
        if self.person_type == PersonType.MAG and self._my_mp > 300 or self.person_type == PersonType.WARRIOR:  # noqa: PLR2004
            self._check_in_prof_hits()
            self._preparation_big_hit()

        self._preparation_small_hit()

        self._aggregate_df_hits()

    def _check_in_prof_hits(self) -> None:
        self._hits_df = DataFrame()
        if self._fight_config.SUPER_HIT:
            all_hits_df = DataFrame(hits.ANY_PROF_HITS)
            for element in self.magic_in:
                self._hits_df = concat(
                    [self._hits_df, all_hits_df[all_hits_df["code"] == int(element)]],
                    ignore_index=True,
                )

        if self._hits_df.empty:
            self.logger.info("cooldown magic hit skills")
            self._check_use_kick()
        else:
            self._hits_df = self._hits_df.sort_values(by="priority")

    def _preparation_big_hit(self) -> None:
        first_hit_boost_od = 0
        second_hit_boost_od = 25
        third_hit_boost_od = 50
        od_dict = {0: first_hit_boost_od, 1: second_hit_boost_od, 2: third_hit_boost_od}
        num_iteration = 3

        if not self._hits_df.empty:
            for iteration in range(num_iteration):
                for num in self._hits_df["od"].index:
                    if self._hits_df["name"][num] == "Цепная молния":
                        continue

                    od = od_dict.get(iteration) + self._hits_df["od"][num]
                    if self._my_od >= int(od):
                        element = self._hits_df["code"][num]
                        self._my_od -= od
                        self._list_hits.append(element)
                        break

    def _preparation_small_hit(self) -> None:
        first_hit_boost_od = 0
        second_hit_boost_od = 25
        third_hit_boost_od = 50
        if self._list_hits:
            have_count = len(self._list_hits)
            if have_count == 1:
                od_dict = {0: second_hit_boost_od, 1: third_hit_boost_od}
            elif have_count == 2:  # noqa: PLR2004
                od_dict = {0: third_hit_boost_od}
        else:
            od_dict = {
                0: first_hit_boost_od,
                1: second_hit_boost_od,
                2: third_hit_boost_od,
            }
            have_count = 0

        new_count = 3 - have_count

        if new_count != 0:
            self._od_hit_check(new_count, od_dict)

    def _od_hit_check(self, count: int, od_dict: dict) -> None:
        for iteration in range(count):
            if not self._hit.empty:
                for num in self._hit["od"].index:
                    od = od_dict.get(iteration) + self._hit["od"][num]
                    if self._my_od >= int(od):
                        element = self._hit["code"][num]
                        self._my_od -= od
                        self._list_hits.append(element)
                        break

    def _aggregate_df_hits(self) -> None:
        self._aggregate_hits = concat([self._hits_df, self._hit], ignore_index=True)

    def _get_query(self) -> None:
        for num, value in enumerate(self._list_hits):
            mp = self._aggregate_hits[self._aggregate_hits["code"] == value].iloc[0]["mp_cost"]
            self._inu += f"{num}_{value}_{mp}@"

    def get_queries_param(self) -> Hit:
        data = {"inu": self._inu, "inb": self._inb, "ina": self._ina}
        return Hit(**data)

    def get_data(self) -> dict[str, str]:
        if self._stop:
            return {"retry": "True"}
        if self.fight_ty and self.fight_pm:
            return {
                "post_id": "7",
                "vcode": self.fight_pm[4],
                "enemy": self.fight_pm[5],
                "group": self.fight_pm[6],
                "inf_bot": self.fight_pm[7],
                "inf_zb": self.fight_pm[10],
                "lev_bot": self.param_en[5],
                "ftr": self.fight_ty[2],
                "inu": self._inu,
                "inb": self._inb,
                "ina": self._ina,
            }
        return {"ended_fight": "True"}
