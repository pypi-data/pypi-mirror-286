# Generate colored noise with sparse convolutions

The sparse convolution algorithm is an effective way to generate a noise signal, which can among other things then be used to simulate noisy inputs. The original presentation by Lewis [(1989)](https://doi.org/doi:10.1145/74333.74360), as well as most subsequent implementations, focus on applications to computer graphics. Here the implementation is geared more towards scientific applications; in this context we find the sparse convolution algorithm convenient for a number of reasons:
- The returned noise function is *dense* (or *solid*): it can be evaluated at any *t*.
- The algorithm allows quite a lot of control over the statistics of the noise, and in particular of its autocorrelation function.
- The algorithm does not rely on performing FFTs, and thus avoids all the pitfalls those entail.
  It is also faster to evaluate, and does not struggle with long time traces.

For more information on how this works, see the [doc page](https://alcrene.github.io/colored-noise).

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.12802822.svg)](https://doi.org/10.5281/zenodo.12802822)

## Design goals & usage

In applications, often we characterize signals by their autocorrelation function; when we want to characterize them by a single number, that number is generally the *correlation time*, describing the width the of autocorrelation function. Computing the autocorrelation function for a given stochastic system is often a difficult analytical problem. Therefore, an algorithm which promises to solve the *inverse* problem – going from autocorrelation function to a noise – is a valuable tool in the practitioner’s toolkit. This is what the sparse convolution algorithm purports to offer.

This particular implementation focuses on the case where a user desires to generate noise with a particular correlation time. At present only a single class is provided, which generates noise signals with Gaussian autocorrelation. In use one simply specifies the desired time range, correlation time and noise strength:

```python
from colored_noise_sc import ColoredNoise

noise = ColoredNoise(0, 10, scale=2.4, corr_time=1.2)
```

Then one simply evaluates the noise at any time `t`:

```python
noise(t)
```

Specifying values with `pint` units is supported, which can be an effective way to sanity-check your calculations.

Conveniently, because the produced noise is dense, it can even be used in integration schemes like adaptive Runge-Kutta, where the required time points are not known ahead of time.

The `noise` object has a few convenience methods, most notably `autocorr` which evaluates the theoretical autocorrelation.

## Package compatibility

### Pint compatibility

Noise parameters can be specified with [Pint](https://pint.readthedocs.io) units, which can be an effective way to validate calculations. This does add measurable overhead (it is about 15x slower per call), so for performance-critical code, one will see significant speed-up by switching to plain NumPy arrays.

(Note that `pint`'s overhead is not *that* large. So the fact that we see such a large speed-up is more a reflection of the efficiency with which the sparse convolution algorithm can be implemented.)

### JAX compatibility

If [JAX](https://jax.readthedocs.io) is installed, `ColoredNoise` will use JAX arrays and operations in its noise generation call. This allows it to be jitted with `jax.jit`.
Jitting the noise generator on its own does not provide much benefit (it is already quite efficient), but this allows it to be used within a larger function, and still jit that entire function. This is useful for example to compile differential equations which will then be integrated with an ODE solver.

## Installation

- **From PyPI**

  This package can be installed from PyPI with the usual command:

  ```python
  pip install colored-noise-sc
  ```

If all you need is a colored noise with Gaussian autocorrelation, a `pip install` is certainly the easiest method.
  
That said, if you need anything more, you are encouraged to use one of the methods below to include the source file directly into your code base.
This has a few advantages:
- It makes it easy to make modifications to add new functionality.
- It ensures that people who download your code always get the current version of `colored-noise-sc`, with any potential patches.
- It encourages you to take ownership of the code, and maybe peek inside if things don’t work exactly as you expect.

- **Direct copy**
  Everything is contained in the file *colored_noise.py* – about 150 lines of code and 400 lines of documentation & validation. So a very reasonably option is actually to just copy the file into your project and import it as any other module.

- **As a subrepo**
  A more sophisticated option is to clone this repo directly into your project with [git-subrepo](https://github.com/ingydotnet/git-subrepo):

  ```bash
  git subrepo clone https://github.com/alcrene/colored-noise my-project/colored-noise`
  ```

  This creates a directory under *my-project/colored-noise* containing the files in this repo – effectively *colored-noise* becomes a subpackage of your own. You can then import the noise class as with any subpackage:
  
  ```python
  from colored_noise import ColoredNoise
  ```

  or
  
  ```python
  from my_project.colored_noise import ColoredNoise
  ```

  The main advantage of a subrepo installation is that it makes it easy to pull code updates:

  ```bash
  git subrepo pull my-project/colored-noise
  ```

  It also makes it easier to open pull requests.


## Dependencies

The only dependencies are [NumPy](https://numpy.org). If you want to build the docs yourself, they you also need:

- [SciPy](https://scipy.org)
- [HoloViews](https://holoviews.org/)
- [Matplotlib](https://matplotlib.org)
- [Pint](https://pint.readthedocs.io)
- [Jupytext](https://jupytext.readthedocs.io/)
- [Jupyter-Book](https://jupyterbook.org)
- [ghp-import](https://github.com/davisp/ghp-import)  (optional)

## Building the documentation

First make sure that the above dependencies are installed, and then that Jupyter Notebook version of the code file *colored_noise* exists. The occurs automatically when you open it in the Jupyter Lab interface with "Open as notebook"[^jupytext], and then click "Save". Alternatively, you can run `jupytext --sync colored_noise.py`.
The actual build command is then

```bash
jb build colored_noise.ipynb
```

This will produce some HTML files inside a *_build* folder. For this package we build the docs in a separate `gh-pages` branch, so that users can pull the source without pulling the docs. This is done automatically by `ghp-import`:

```bash
ghp-import -n -p _build/_page/colored_noise/html
```

See the [Jupyter Book docs](https://jupyterbook.org/en/stable/basics/building/index.html) for more information.

[^jupytext]: The "Open as notebook" context menu item is provided by the Jupytext plugin.