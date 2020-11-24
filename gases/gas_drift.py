import numpy as np
from numba import types, njit
from numba.core.errors import TypingError
from numba.extending import overload


@overload(np.clip)
def impl_clip(a, a_min, a_max):
	# Check that `a_min` and `a_max` are scalars, and at most one of them is None.
	if not isinstance(a_min, (types.Integer, types.Float, types.NoneType)):
		raise TypingError("a_min must be a_min scalar int/float")
	if not isinstance(a_max, (types.Integer, types.Float, types.NoneType)):
		raise TypingError("a_max must be a_min scalar int/float")
	if isinstance(a_min, types.NoneType) and isinstance(a_max, types.NoneType):
		raise TypingError("a_min and a_max can't both be None")

	if isinstance(a, (types.Integer, types.Float)):
		# `a` is a scalar with a valid type
		if isinstance(a_min, types.NoneType):
			# `a_min` is None
			def impl(a, a_min, a_max):
				return min(a, a_max)
		elif isinstance(a_max, types.NoneType):
			# `a_max` is None
			def impl(a, a_min, a_max):
				return max(a, a_min)
		else:
			# neither `a_min` or `a_max` are None
			def impl(a, a_min, a_max):
				return min(max(a, a_min), a_max)
	elif (
			isinstance(a, types.Array) and
			a.ndim == 1 and
			isinstance(a.dtype, (types.Integer, types.Float))
	):
		# `a` is a 1D array of the proper type
		def impl(a, a_min, a_max):
			# Allocate an output array using standard numpy functions
			out = np.empty_like(a)
			# Iterate over `a`, calling `np.clip` on every element
			for i in range(a.size):
				# This will dispatch to the proper scalar implementation (as
				# defined above) at *compile time*. There should have no
				# overhead at runtime.
				out[i] = np.clip(a[i], a_min, a_max)
			return out
	else:
		raise TypingError("`a` must be an int/float or a 1D array of ints/floats")

	# The call to `np.clip` has arguments with valid types, return our
	# numba-compatible implementation
	return impl


def move_gases(gas_map: np.array):
	gas_filled_squares, xs, ys = accelerated_gas_code(gas_map)
	gas_map[gas_filled_squares[0], gas_filled_squares[1]] -= 1
	gas_map[xs, ys] += 1


@njit
def accelerated_gas_code(gas_map):
	gas_filled_squares = np.nonzero(gas_map)
	x_movement = np.random.randint(-1, 2, len(gas_filled_squares[0]))
	y_movement = np.random.randint(-1, 2, len(gas_filled_squares[1]))
	xs = np.clip(gas_filled_squares[0] - x_movement, 0, len(gas_map) - 1)
	ys = np.clip(gas_filled_squares[1] - y_movement, 0, len(gas_map) - 1)
	return gas_filled_squares, xs, ys


def emit_gases(world, emitters):
	for emitter in emitters:
		world['carbon_dioxide_map'][emitter['x']][emitter['y']] += 1

		# TODO: Every 100 frames or so randomly decide whether to flip velocities
		# Crappy hack job POC below
		if world['global_creature_id_counter'] % 100 == 0:
			emitter['x'] = np.random.randint(5, world['world_size'] - 5)
			emitter['y'] = np.random.randint(5, world['world_size'] - 5)

		if emitter['x'] < 5 and emitter['vx'] < 0:
			emitter['vx'] = -emitter['vx']
		if emitter['y'] < 5 and emitter['vy'] < 0:
			emitter['vy'] = -emitter['vy']

		if emitter['x'] > world['world_size'] - 5 and emitter['vx'] > 0:
			emitter['vx'] = -emitter['vx']
		if emitter['y'] > world['world_size'] - 5 and emitter['vy'] > 0:
			emitter['vy'] = -emitter['vy']

		emitter['x'] += emitter['vx']
		emitter['y'] += emitter['vy']
