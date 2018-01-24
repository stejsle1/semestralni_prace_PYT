import numpy

from wator import WaTor


def test_age_fish():
    creatures = numpy.zeros((2, 2))
    wator = WaTor(creatures)
    assert wator.age_fish != 123
    wator.setAge_fish(123)
    assert wator.age_fish == 123


def test_age_shark():
    creatures = numpy.zeros((2, 2))
    wator = WaTor(creatures)
    assert wator.age_shark != 456
    wator.setAge_shark(456)
    assert wator.age_shark == 456


def test_energy_eat():
    creatures = numpy.zeros((2, 2))
    wator = WaTor(creatures)
    assert wator.energy_eat != 42
    wator.setEnergy_eat(42)
    assert wator.energy_eat == 42


def test_opti_value():
    creatures = numpy.zeros((2, 2))
    wator = WaTor(creatures)
    assert wator.opti == 0
    wator.setOpti(42, 50)
    assert wator.opti == 22

