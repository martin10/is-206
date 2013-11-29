from nose.tools import *
from gothonweb.maps.map import Room


def test_room():
    hovedrom = Room("Main Street",
                """This room has gold in it you can grab. There's a
                door to the north.""")
    assert_equal(hovedrom.name, "Main Street")
    assert_equal(hovedrom.paths, {})

def test_room_paths():
    hovedrom = Room("Main Street", "Test room in the center.")
    west = Room("West", "Test room in the north.")
    punsh = Room("You hit him hard!", "Test room in the south.")

    hovedrom.add_paths({'Main Street': hovedrom, 'West': west})
    assert_equal(hovedrom.go('Main Street'), hovedrom)
    assert_equal(hovedrom.go('West'), west)

