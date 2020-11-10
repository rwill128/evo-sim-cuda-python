# evo-sim-cuda-python

This a GPU-based evolution simulation, inspired by Biogenesis on Sourceforge.

I am organizing the proof of concept code into Jupyter notebooks, and adding unit and performance tests as I refine the evolution dynamics I am seeking to create.

Please inquire if you would like to contribute in any way.

:oxygen expulsion from plants
:incorporating smoothed land maps and using height-based photosynthesis effectiveness
:oxygen drift that is aware of carbon dioxide density
:only allowing plants to grow when touching water
:reproduction via seeds or some other method, with tweaked growth tendencies and parameters based on that
:segment maintenance cost implemented for plants
:lifespan potentially?
:at death, disappear or decompose?
:better displays of plant data
:charts of world stats over its lifetime for seeing when I've found sensible parameters
:automated builds that run performance / parameter tests on a server?

:seed cost gives the spawned plants more energy! 
    :so essentially each seed gets donated a certain amount of energy from parent plant
    :seed attraction factors could be subject to mutation
:extra energy is funneled into growth until a certain age, then extra energy gets put into seeds/reproduction!
    :this age is subject to mutation also
:make creatures/plants into dictionaries that actually make sense. the segments can still be an np array for performance.
