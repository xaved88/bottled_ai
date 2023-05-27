# PLEASE NOTE! #

The interfaces package is meant to be entirely independent. It exits so that we can have interdependencies between
parts (such as cards affecting the game state effecting cards again). Python hates this circular dependency, but with
using interfaces we can avoid it. What this means for you as a dev:

- If you're doing something in the interfaces package, it must only import from interfaces or enums - nothing else in
  the calculator. If it does, you're doing it wrong and there's ways to refactor that.

- If you are working outside the interfaces package and in the battle state or somewhere, USE INTERFACES instead of the
  concrete classes. Anything outside of interfaces (like cards, battle state, player, etc) - should only have usages in
  the places where it's specifically created, like tests and the game state converter. Everything else, should be using
  the interface instead.

- We need to keep interfaces up to date. If you make a change in the concrete class (adding a public method or value),
  then make sure to add it to the interface as well.

Ideally we would have tooling do this for us automatically. But I'm lazy to write it, and this is python, so it will let
us accidentally make mistakes without complaining til it becomes a monstrosity. **So it's up to you!**
