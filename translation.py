class Text:
    def __init__(self, language, code, text):
        self.Code = code
        self.Language = language
        self.Text = text

__en = 'en'
__ru = 'ru'
__default_language = __en
__wrong_code = 'Wrong text code'
__current_language = __default_language
__available_languages = [__en, __ru]
__translations = [
    Text(__en, 'CANT_DEFINE_DECK', 'Can\'t define deck'),
    Text(__ru, 'CANT_DEFINE_DECK', 'Не удалось определить колоду'),

    Text(__en, 'INCORRECT_DECK_TYPE', 'Incorrect deck type'),
    Text(__ru, 'INCORRECT_DECK_TYPE', 'Некорректный тип колоды'),

    Text(__en, 'NO_CARDS_IN_DECK', 'There are no cards in the deck!'),
    Text(__ru, 'NO_CARDS_IN_DECK', 'В колоде нет карт!'),

    Text(__en, 'DECK_SHUFFLED', 'Deck shuffled'),
    Text(__ru, 'DECK_SHUFFLED', 'Колода перемешана'),

    Text(__en, 'DECK_FILLED_BY_COUNT', 'Deck is filled with {0} cards'),
    Text(__ru, 'DECK_FILLED_BY_COUNT', 'Колода заполнена {0} картами'),

    Text(__en, 'TRUMP_CARD_IN_DECK', 'Trump card in the deck: {0}'),
    Text(__ru, 'TRUMP_CARD_IN_DECK', 'Козырная карта в колоде: {0}'),

    Text(__en, 'TRUMP_NOT_DEFINED', 'Trump is not defined!'),
    Text(__ru, 'TRUMP_NOT_DEFINED', 'Козырь не определён!'),

    Text(__en, 'PLAYERS_HAVE_NOT_TRUMPS', 'Players do not have trumps. Determined randomly'),
    Text(__ru, 'PLAYERS_HAVE_NOT_TRUMPS', 'У игроков нет козырей. Определяем случайным образом'),

    Text(__en, 'NEED_TWO_PLAYERS', 'You need at least 2 players to play!'),
    Text(__ru, 'NEED_TWO_PLAYERS', 'Для игры необходимо минимум 2 игрока!'),

    Text(__en, 'FIRST_PLAYER_NOT_DEFINED', 'The player who goes first is not defined!'),
    Text(__ru, 'FIRST_PLAYER_NOT_DEFINED', 'Не определен игрок, который ходит первым!'),

    Text(__en, 'PLAYER_NAME', 'Enter player name: '),
    Text(__ru, 'PLAYER_NAME', 'Введите имя игрока: '),

    Text(__en, 'EXIT', 'exit'),
    Text(__ru, 'EXIT', 'выход'),

    Text(__en, 'PLAYER_MOVE', '{0}{1}) {2} Move '),
    Text(__ru, 'PLAYER_MOVE', '{0}{1}) {2} Ходит '),

    Text(__en, 'PLAYER_DEFENSE', ' -> {0} Defense '),
    Text(__ru, 'PLAYER_DEFENSE', ' -> {0} Отбивает '),

    Text(__en, 'PLAYER_END_MOVE', '{0}The player {1} has completed his turn{2}'),
    Text(__ru, 'PLAYER_END_MOVE', '{0}Игрок {1} завершил ход{2}'),

    Text(__en, 'PLAYER_TAKE_CARDS', '{0}The player {1} has taken cards{2}'),
    Text(__ru, 'PLAYER_TAKE_CARDS', '{0}Игрок {1} взял(-а) карты{2}'),

    Text(__en, 'TAKE', 'take'),
    Text(__ru, 'TAKE', 'беру'),

    Text(__en, 'PASS', 'pass'),
    Text(__ru, 'PASS', 'бита'),

    Text(__en, 'PLAYER_DOESNT_NEED_CARDS', 'Player {0} doesn\'t need cards'),
    Text(__ru, 'PLAYER_DOESNT_NEED_CARDS', 'Игроку {0} не нужны карты'),

    Text(__en, 'PLAYER_TAKE_COUNT_CARDS', 'The player {0} took {1} cards from the deck'),
    Text(__ru, 'PLAYER_TAKE_COUNT_CARDS', 'Игрок {0} взял(-а) {1} карт из колоды'),

    Text(__en, 'YOUR_TURN', '{0}Your turn, {1}{2}'),
    Text(__ru, 'YOUR_TURN', '{0}Ваш ход, {1}{2}'),

    Text(__en, 'YOUR_DEFENSE', '{0}Defense, {1}{2}'),
    Text(__ru, 'YOUR_DEFENSE', '{0}Отбивайтесь, {1}{2}'),

    Text(__en, 'ENTER_COMMAND_FOR_END_MOVE', '{0} Enter the command for complete move: {1}{2}{3}'),
    Text(__ru, 'ENTER_COMMAND_FOR_END_MOVE', '{0} Для завершения хода введите команду: {1}{2}{3}'),

    Text(__en, 'ENTER_COMMAND_FOR_TAKE_CARDS', '{0} To take cards enter the command: {1}{2}{3}'),
    Text(__ru, 'ENTER_COMMAND_FOR_TAKE_CARDS', '{0} Чтобы взять карты введите команду: {1}{2}{3}'),

    Text(__en, 'SHOW_TRUMP_CARD', '{0} Trump card: {1}'),
    Text(__ru, 'SHOW_TRUMP_CARD', '{0} Козырная карта: {1}'),

    Text(__en, 'ENTER_CARD_NUMBER', '{0} {1}. Enter card number {0}'),
    Text(__ru, 'ENTER_CARD_NUMBER', '{0} {1}. Введите номер карты {0}'),

    Text(__en, 'WRONG_MOVE', 'Wrong move'),
    Text(__ru, 'WRONG_MOVE', 'Не допустимый ход'),

    Text(__en, 'WRONG_LANGUAGE', 'Wrong language'),
    Text(__ru, 'WRONG_LANGUAGE', 'Не допустимый язык'),

    Text(__en, 'PLAYER_LOSE', '{0}{1}The player {2} lose! Game over.{3}'),
    Text(__ru, 'PLAYER_LOSE', '{0}{1}Игрок {2} проиграл! Игра закончена.{3}'),

    Text(__en, 'END_OR_RESTART_GAME', 'To end the game, enter the command {0}exit{1}, to start a new one, enter any command: '),
    Text(__ru, 'END_OR_RESTART_GAME', 'Для завершения игры введите команду {0}выход{1}, для начала новой введите любую команду: '),

    Text(__en, 'PLAYERS_PLAY_DRAW', '{0}{1}The players played a draw!{2}'),
    Text(__ru, 'PLAYERS_PLAY_DRAW', '{0}{1}Игроки сыграли в ничью!{2}'),

    Text(__en, 'SELECT_LANGUAGE', 'Select the game language, available ({0}): '),
    Text(__ru, 'SELECT_LANGUAGE', 'Выберите язык игры, доступны: ({0}): '),

    Text(__en, 'DEFAULT_LANGUAGE', ''),
    Text(__ru, 'DEFAULT_LANGUAGE', 'Язык не найден, будет выбран язык по умолчанию'),
]

def getText(code):
    text = next((e for e in __translations if e.Code == code and e.Language == __current_language), None)
    if (text == None):
        text = next((e for e in __translations if e.Code == code and e.Language == __default_language), None)
    if (text == None):
        text = Text(__default_language, __wrong_code, __wrong_code)
    return text.Text

def getAvailableLanguages():
    languages = ''
    for x in __available_languages:
        languages = languages + x + ', '
    languages = languages.rstrip().rstrip(',')
    return languages

def checkLanguageAvailable(language):
    return any(i for i in __available_languages if i == language)

def setLanguage(language):
    global __current_language
    __current_language = language

