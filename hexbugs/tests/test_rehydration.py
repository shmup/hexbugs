from hexbugs.mind.models import Game, Player, GamePlayer
from hexbugs.mind.database import Session
from hexbugs.tests.utils import add_db_defaults


def test_rehydration():
    session = Session()
    with session.begin_nested():
        [game_id, weasel_id, bravd_id] = add_db_defaults()

        data = (
            session.query(Game, Player).select_from(Game).join(
                GamePlayer, GamePlayer.game_id == Game.id).join(
                    Player, GamePlayer.player_id == Player.id).filter(
                        Game.id == game_id).all())
        assert data, "Rehydration should match as expected"

        session.query(GamePlayer).filter(GamePlayer.game_id == game_id).delete()
        session.query(Game).filter(Game.id == game_id).delete()
        session.query(Player).filter(Player.id.in_([weasel_id, bravd_id])).delete()

    session.close()
