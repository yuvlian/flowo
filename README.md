# flowo

A Pythonic DSL for [Flowgorithm](http://www.flowgorithm.org/) (`.fprg`) that can simplify AI-assisted work by generating valid visual programs from Python code.

This thing is basically a port and redesign of the Rust crate `fgrs`.

## AI & Vibecoding
Flowgorithm's native XML format is a nightmare for LLMs (like Gemini, Claude, or ChatGPT) to generate correctly. **flowo** provides a clean, type-safe Python DSL that is significantly easier for AI coding assistants to write. 

By using **flowo**, you can "vibecode" your Flowgorithm assignments by prompting for Python code and letting the library handle the strict XML schema, reserved keywords, and variable declarations automatically.

## Features

- **Context Manager API**: Natural Pythonic syntax for nested structures (`with flow.if_():`, `with flow.for_():`).
- **Strict Validation**: Prevents invalid Flowgorithm variable names and reserved keyword usage.
- **Variable Tracking**: Ensures variables are declared before use.
- **Intrinsic Functions**: Helper functions for all Flowgorithm built-ins (`Abs`, `Sin`, `Len`, `ToInteger`, etc.).
- **Zero Dependencies**: Built entirely on the Python Standard Library.

## Installation

```
pip install flowo
```

## Quick Start

```python
from flowo import Flow, Type

flow = Flow("HelloWorld.fprg")

with flow.function("Main"):
    flow.declare("name", Type.STRING)
    flow.output('"What is your name?"')
    flow.input("name")
    flow.output('"Hello, " & name')

flow.to_fprg()
```

## Advanced Usage

**flowo** supports all Flowgorithm features (that I've used during my uni study) including arrays, multi-argument declarations, and nested loops:

```python
from flowo import Flow, Type, Sin, PI

flow = Flow()
with flow.function("Main"):
    flow.declare("i, n", Type.INTEGER)
    flow.declare("val", Type.REAL)
    
    flow.assign("n", "10")
    with flow.for_("i", "0", "n - 1"):
        flow.assign("val", Sin(f"(i / n) * 2 * {PI}"))
        flow.output("val")

flow.to_fprg("SineWave.fprg")
```

## License

MIT
