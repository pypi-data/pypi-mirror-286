# ``paranox``
Simple parameterisations for ``equinox``

This directory contains simple parameterisations that should be compatible with ``equinox`` modules, provided that each interaction with a parameter is wrapped in a ``jnp.asarray`` call at the first instance. Many of the default modules thus might not work. For the most part, this library is used internally by other repositories in the ``hypercoil`` organisation. We would be happy to support external use cases.

``paranox`` contains three kinds of parameterisation abstractions: initialisations, domain mappers, and stochastic parameters. More details and examples will be provided here at a later time.
