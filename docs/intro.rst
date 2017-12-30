INTRO
=====

This is a application with graphical user interface (GUI). This project is about simulation WaTor - predator/prey. Wator is a simulation of the interaction over time of predator and prey in a small toroid (rectangular area). The game is to arrange the parameters so the populations are stable when the area is made small.

The program is dependent upon 5 parameters and the size of the rectangular grid. Parameters are number of predators (sharks), number of prey (fish), breed time of shark, breed time of fish and shark starve time. 

Time goes in chronones - time cycles. Every chronon three phases happend. In phase one every fish moves by one space to free space. If fish is old enough to reproduce, the origin fish stay on its space and breed a child fish to free space. If there is no free space around fish, the fish makes no move and wait for next chronon. Next phase - sharks make move. The priority of sharks is to eat fish. So if there is a fish around them, they prefer to eat fish. If no fish around them, then they move to free space. If even no free space around them, then they wait. Last phase decrease amount of energy of sharks and control, if there is any shark without energy - dead shark.

Application is :ref:`installed<install-label>` as Python module. For examples how to run application see :ref:`use-manual` or :ref:`test-manual`. To see how to manage a GUI application move to :ref:`gui-config`.
