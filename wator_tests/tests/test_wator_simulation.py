import numpy

from wator import WaTor


def test_optimalization_many_creatures_do_nothing():
    creatures = numpy.zeros((20, 20))
    creatures[0, :] = 1 
    creatures[3, :] = 1 
    creatures[6, :] = 1 
    creatures[18, :] = 1 # 80 fish
    creatures[9, :] = -1 
    creatures[12, :] = -1
    creatures[15, :] = -1 # 60 sharks
    wator = WaTor(creatures)
    wator.setOpti(wator.count_fish()+wator.count_sharks(), 12) # 80+60 creatures, 12 percentage
    assert wator.count_fish() == 80
    assert wator.count_sharks() == 60
    lim_f, lim_s = wator.optimalize() # do nothing
    assert lim_f == 0
    assert lim_s == 0
    assert wator.count_fish() == 80
    assert wator.count_sharks() == 60


def test_optimalization_one_fish():
    creatures = numpy.zeros((20, 20))
    creatures[0, :] = 1 # 20 fish
    creatures[9, :] = -1 
    creatures[12, :] = -1
    creatures[15, :] = -1 # 60 sharks
    wator = WaTor(creatures)
    wator.setOpti(wator.count_fish()+wator.count_sharks(), 12) # 20+60 creatures, 12 percentage
    assert wator.count_fish() == 20
    assert wator.count_sharks() == 60
    lim_f, lim_s = wator.optimalize() # do nothing
    assert lim_f == 0
    assert lim_s == 0
    assert wator.count_fish() == 20
    assert wator.count_sharks() == 60

    # simulation of tick() function, where sharks eat most of fish, last one fish standing
    creatures[0, :] = 0 # water
    creatures[0, 0] = 1 # 1 fish
    lim_f, lim_s = wator.optimalize() # add 9 fish
    assert lim_f == 9
    assert lim_s == 0
    assert wator.count_fish() == 10
    assert wator.count_sharks() == 60


def test_optimalization_high_percentage():
    creatures = numpy.zeros((20, 20))
    creatures[0, :] = 1 # 20 fish
    creatures[9, :] = -1 
    creatures[12, :] = -1
    creatures[15, :] = -1 # 60 sharks
    wator = WaTor(creatures)
    wator.setOpti(wator.count_fish()+wator.count_sharks(), 75) # 20+60 creatures, 12 percentage
    lim_f, lim_s = wator.optimalize() # add 41 fish and 1 shark
    assert lim_f == 41
    assert lim_s == 1
    assert wator.count_fish() == 61
    assert wator.count_sharks() == 61


def test_optimalization_overplaced():
    creatures = numpy.ones((20, 20)) # all fish
    wator = WaTor(creatures)
    wator.setOpti(wator.count_fish()+wator.count_sharks(), 10) # 400+0 creatures, 10 percentage
    # optimalize() woudl like to add some sharks but cant, array is full, return 0 added
    lim_f, lim_s = wator.optimalize() # add 41 fish and 1 shark
    assert lim_f == 0
    assert lim_s == 0
    assert wator.count_fish() == 400
    assert wator.count_sharks() == 0
