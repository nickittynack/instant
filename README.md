# Instant-feedback, instant-debugging

## Overall principles:

- Instant feedback
- Maximum visualization
- Optimized for *insight*

## Desired properties:

- Robust to slow function calls, infinite loops, large loops, etc etc
- Fearless coding: Prevents you from wiping your database, overloading your server (fully sandboxed)
- Seamless "faking" of resources so instant-feedback still works with external dependencies
- Pervasive, flexible, adaptable visualization-by-default of all kind of python objects

TODO: More detailed roadmappy stuff here

## Sprint ideas

- Evaluate pysnooper. Found out about this in Trent Lloyd's talk and wasn't aware of this when I hacked together this demo, but looks like some functionality overlap for code tracing. Haven't read the codebase in details yet, and need to figure out what kind of interface it offers, how flexible it is, and how much it could be used with/instead of my hacky tracing code. Let's not reinvent the wheel here.

- Add robustness: Provide responsiveness and useful output in the case of the aforementioned infinite loops etc.

- Add autocomplete: Autocomplete works easier when you run the code, because you don't need static code analysis, you just inspect the runtime state and see what properties are available. Starting point is take a code block and cursor position, figure out what objects are involved, and generate a list of autocomplete possibilities (ideally with their docs right alongside!).

- Add autoformatting: It would be cool to be able to reformat the code (probably with `black`) every but that means maintaining the cursor position.

- Auto importing: Try to support auto adding import statements, as this is always a nuisance. Could consult a greenlist of approved packages perhaps?

- Auto fakery: How could external resources be seamlessly faked? Need to try out a bunch of concepts and see what works most naturally.

- UI concepts: Haven't put GUI code up yet, but can still explore how data of various kinds (images, bytearrays, dates and times, tables, etc) could be best visualized in the context of the table-alongside layout. All kinds of concepts are possible.


