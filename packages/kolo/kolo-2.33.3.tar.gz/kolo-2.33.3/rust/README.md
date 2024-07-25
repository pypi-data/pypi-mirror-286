# The Rust extension

In Kolo we have a parallel implementation of `KoloProfiler` in Rust to reduce the overhead of the CPython interpreter. Using Rust we are able to call into Python's C-API directly, instead of needing to go via Python apis, which have the overhead of creating Python objects and managing interpreter state.

## Code structure

The Rust codebase is split into several files:

* `lib.rs` - This is where we define the `kolo._kolo` module that can be imported by Python. This contains two functions, `register_profiler` and `register_noop_profiler` which can be called directly by Python code.
* `profiler.rs` - This is where the core profiling logic lives. The `KoloProfiler` struct is analogous to the `KoloProfiler` class in `src/kolo/profiler.py`. The `profile_callback` function is a thin layer to convert CPython types into Rust-friendly types.
* `plugins.rs` - This module contains the implementation of the plugin architecture for `default_include_frames`. The `PluginProcessor` struct is analogous to the `PluginProcessor` class in `src/kolo/plugins.py`.
* `filters.rs` - This module contains the implementation of the filtering logic for `default_ignore_frames`.
* `utils.rs` - This module contains various helper functions.

## How tracing in Rust works

The Rust `KoloProfiler` is registered with Python's profiling api using `PyEval_SetProfile`. Every time the Python interpreter calls or returns from a Python callable, or calls or returns a C function, the `profile_callback` function is called. This exits almost immediately for C functions, which gets us a lot of performance. After converting the ffi (foreign function interface) types provided by the C API into safe PyO3 wrapper types we call into `KoloProfiler.profile` to handle the rest of the profiling logic.

The Rust profiling logic calls back into Python in several places:

* Getting the current Kolo version (`utils::kolo_version`)
* Getting the current GIT commit sha (`utils::git_commit_sha`)
* Getting the program command line args (`utils::get_argv`)
* Saving the trace to the sqlite database (`KoloProfiler::save_in_db`)
* Converting Python objects to msgpack (`utils::dump_msgpack`)
* Getting the current thread name and `native_id` (`utils::current_thread`)
* Getting the qualname of the current frame (`utils::get_qualname`)
* Running frame processors (`PluginProcessor::matches` and `PluginProcessor::process`)
* Logging errors (`KoloProfiler::log_error`)

## Performance considerations

Rust is faster than Python, so implementing logic purely in Rust is ideal. Next best is introspecting existing Python objects with PyO3 apis. Finally, we can call back into python code for situations where re-implementing in Rust is difficult, impossible, or not performance critical.

## PyPy

We don't use Rust when the interpreter is PyPy. This is primarily because the `PyEval_SetProfile` API we need is not supported by PyPy.
