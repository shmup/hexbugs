from hexbugs.models import Player, Game, GamePlayer
from hexbugs.database import Session


def add_db_defaults():
    with Session() as session:
        try:
            weasel = Player(name='Weasel')
            bravd = Player(name='Bravd')

            game = Game()

            session.add(weasel)
            session.add(bravd)
            session.add(game)
            session.commit()

            game_players_weasel = GamePlayer(game_id=game.id, player_id=weasel.id)
            game_players_bravd = GamePlayer(game_id=game.id, player_id=bravd.id)

            session.add(game_players_weasel)
            session.add(game_players_bravd)

            session.commit()

            return [game.id, weasel.id, bravd.id]

        except Exception as e:
            session.rollback()
            raise e

        finally:
            session.close()
