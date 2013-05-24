"""
Initializes vengeance.
"""
from vengeance._direction import _Direction
from vengeance._game import _Game
from vengeance._room import _Room


def _create_directions(direction_data):
    """
    Creates the directions in the game.

    direction_data: Details of the directions in the game
    """
    directions = []
    for datum in direction_data:
        direction = _Direction(datum["name"])
        opposite_direction = _Direction(datum["opposite"])
        direction.opposite = opposite_direction
        opposite_direction.opposite = direction
        directions.append(direction)
        directions.append(opposite_direction)

    return directions


def _create_rooms(room_data):
    """
    Creates the rooms in the game.

    room_data: Details of the rooms in the game
    """
    rooms = []
    for room_datum in room_data:
        room_name = room_datum['name']
        room = _Room(room_name, room_datum['description'])
        rooms.append(room)

    return rooms


def _create_exit_data(room_data):
    """
    Creates exit data for the game.

    room_data: Details of the rooms in the game
    """
    exit_data = []
    for room_datum in room_data:
        room_name = room_datum['name']
        room_datum.setdefault('exits', [])
        for current_exit in room_datum['exits']:
            current_exit.setdefault('one_way', False)
            exit_datum = {
                'from': room_name,
                'to': current_exit['to'],
                'direction': current_exit['direction'],
                'one_way': current_exit['one_way']
            }
            exit_data.append(exit_datum)

    return exit_data


def _find_room(name, rooms):
    """
    Finds a room by name.

    Returns the room or None if the room was not found.

    name: The name of the room to find
    rooms: The rooms in which to search
    """
    for room in rooms:
        if room.name == name:
            return room

    return None


def _add_exits(rooms, directions, exit_data):
    """
    Adds exits to rooms.

    rooms: The rooms to which to add exits
    directions: The directions in which exits can lead
    exit_data: Details of the exits in the game
    """
    for datum in exit_data:
        from_name = datum['from']
        from_room = _find_room(from_name, rooms)
        to_name = datum['to']
        to_room = _find_room(to_name, rooms)
        if to_room is None:
            print('Unknown exit room ' + to_name +
                  ' from ' + from_name + "'")
            #sys.exit()

        direction_name = datum['direction']
        the_exit = None
        for direction in directions:
            if direction.name == direction_name:
                the_exit = direction
        if the_exit is None:
            print('Unknown direction ' + direction_name)
            #sys.exit()

        one_way = datum['one_way']
        add_exit_func = None
        if one_way:
            add_exit_func = _Room.add_one_way_exit
        else:
            add_exit_func = _Room.add_exit
        add_exit_func(from_room, the_exit, to_room)


def _load_rooms(game_data):
    """
    Loads rooms, and wires up their exits.

    game_data: Details of the rooms in the game
    """
    directions = _create_directions(game_data['directions'])
    room_data = game_data['rooms']
    rooms = _create_rooms(room_data)
    exit_data = _create_exit_data(room_data)
    _add_exits(rooms, directions, exit_data)

    return rooms


def _create_game(game_data):
    """
    Creates a game.

    game_data: Details of the rooms in the game
    """
    rooms = _load_rooms(game_data)

    if len(rooms) > 0:
        return _Game(rooms[0])

    return None


def run_game(game_data):
    """
    Runs a game.

    game_data: Details of the rooms in the game
    """
    game = _create_game(game_data)
    game.run()
