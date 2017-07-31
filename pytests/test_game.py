#!/usr/bin/env python
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2015-2017
# Leandro Toledo de Souza <devs@python-telegram-bot.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].
import json

import pytest

from telegram import MessageEntity, Game, PhotoSize, Animation


@pytest.fixture(scope='class')
def json_dict():
    return {
        'title': TestGame.title,
        'description': TestGame.description,
        'photo': [TestGame.photo[0].to_dict()],
        'text': TestGame.text,
        'text_entities': [TestGame.text_entities[0].to_dict()],
        'animation': TestGame.animation.to_dict()
    }


@pytest.fixture()
def game():
    return Game(TestGame.title,
                TestGame.description,
                TestGame.photo,
                text=TestGame.text,
                text_entities=TestGame.text_entities,
                animation=TestGame.animation)


class TestGame:
    title = 'Python-telegram-bot Test Game'
    description = 'description'
    photo = [PhotoSize('Blah', 640, 360, file_size=0)]
    text = (b'\\U0001f469\\u200d\\U0001f469\\u200d\\U0001f467'
            b'\\u200d\\U0001f467\\U0001f431http://google.com').decode('unicode-escape')
    text_entities = [MessageEntity(13, 17, MessageEntity.URL)]
    animation = Animation('blah')

    def test_game_de_json(self, json_dict, bot):
        game = Game.de_json(json_dict, bot)

        assert game.title == self.title
        assert game.description == self.description
        assert game.photo == self.photo
        assert game.text == self.text
        assert game.text_entities == self.text_entities
        assert game.animation == self.animation

    def test_game_to_json(self, game):
        json.loads(game.to_json())

    def test_parse_entity(self, game):
        entity = MessageEntity(type=MessageEntity.URL, offset=13, length=17)
        game.text_entities = [entity]
        assert game.parse_text_entity(entity) == 'http://google.com'

    def test_parse_entities(self, game):
        entity = MessageEntity(type=MessageEntity.URL, offset=13, length=17)
        entity_2 = MessageEntity(type=MessageEntity.BOLD, offset=13, length=1)
        game.text_entities = [entity_2, entity]
        assert game.parse_text_entities(MessageEntity.URL) == {entity: 'http://google.com'}
        assert game.parse_text_entities() == {entity: 'http://google.com', entity_2: 'h'}