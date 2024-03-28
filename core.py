import json
import logging
from difflib import SequenceMatcher

from constants import PLAYERS
from ocr import compute_img


def get_points() -> dict[str, int]:
    with open("data/points.json") as fp:
        points = json.load(fp)

    sorted_points = dict(sorted(points.items(), key=lambda x: x[1], reverse=True))
    return sorted_points


def get_weapons(players: list[str] = PLAYERS) -> dict[str, str]:
    with open("data/points.json") as fp:
        points = json.load(fp)

    with open("data/weapons.json") as fp:
        weapons = json.load(fp)

    points_rank = {
        key: rank
        for rank, key in enumerate(sorted(set(points.values()), reverse=True), 1)
    }
    rank = {k: points_rank[v] for k, v in points.items()}
    sub_rank = {k: rank[k] for k in rank.keys() if k in players}
    weapons = {k: weapons[str(v)] for k, v in sub_rank.items()}
    return weapons


def update_score(player_list: list[str]) -> None:
    with open("data/points.json") as fp:
        points = json.load(fp)

    reward = len(player_list)
    for player in player_list:
        points[player] += reward
        logging.info(f"{player} : +{reward}")
        reward -= 1

    with open("data/points.json", "w") as file:
        json.dump(points, file, indent=4)


def duel_result(player_win: str, player_lose: str) -> bool:
    with open("data/points.json") as fp:
        points = json.load(fp)

    player_win_points = points[player_win]
    player_lose_points = points[player_lose]

    if player_win_points < player_lose_points:
        points[player_win] = player_lose_points
        points[player_lose] = player_win_points

        with open("data/points.json", "w") as file:
            json.dump(points, file, indent=4)

        logging.info(f"Swapped scores for {player_win} and {player_lose}")
        return True

    return False


def get_ranks_from_image(image_path: str) -> list[str]:
    players_ordered = []
    leaderboard = compute_img(image_path)

    for index, row in leaderboard.iterrows():
        for player in PLAYERS:
            if SequenceMatcher(a=row["text"], b=player).ratio() > 0.6:
                players_ordered.append(player)

    logging.info(f"Ranking from game : {players_ordered}")
    return players_ordered


if __name__ == "__main__":
    a = get_weapons(["Tomygub", "Clavelloux", "ChokDi"])
    update_score(["Tomygub", "BetaKakarotene", "ChokDi"])
    d = duel_result("Poltibo", "Tomygub")
