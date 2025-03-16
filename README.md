<h1 align="center">
  <b>PDDL Plus Parser</b>
</h1>

<p align="center">
  <a href="https://pypi.org/project/pddl-plus-parser/">
    <img alt="PyPI" src="https://img.shields.io/pypi/v/pddl">
  </a>
  <a href="https://pypi.org/project/pddl">
    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/pddl" />
  </a>
  <a href="">
    <img alt="PyPI - Status" src="https://img.shields.io/pypi/status/pddl" />
  </a>
  <a href="">
    <img alt="PyPI - Implementation" src="https://img.shields.io/pypi/implementation/pddl">
  </a>
  <a href="">
    <img alt="PyPI - Wheel" src="https://img.shields.io/pypi/wheel/pddl">
  </a>
  <a href="https://github.com/AI-Planning/pddl/blob/main/LICENSE">
    <img alt="GitHub" src="https://img.shields.io/github/license/AI-Planning/pddl">
  </a>
</p>
<p align="center">
  <a href="">
    <img alt="test" src="https://github.com/AI-Planning/pddl/workflows/test/badge.svg">
  </a>
  <a href="">
    <img alt="lint" src="https://github.com/AI-Planning/pddl/workflows/lint/badge.svg">
  </a>
  <a href="">
    <img alt="docs" src="https://github.com/AI-Planning/pddl/workflows/docs/badge.svg">
  </a>
  <a href="https://codecov.io/gh/AI-Planning/pddl">
    <img alt="codecov" src="https://codecov.io/gh/AI-Planning/pddl/branch/main/graph/badge.svg?token=FG3ATGP5P5">
  </a>
</p>
<p align="center">
  <a href="https://img.shields.io/badge/flake8-checked-blueviolet">
    <img alt="" src="https://img.shields.io/badge/flake8-checked-blueviolet">
  </a>
  <a href="https://img.shields.io/badge/mypy-checked-blue">
    <img alt="" src="https://img.shields.io/badge/mypy-checked-blue">
  </a>
  <a href="https://img.shields.io/badge/code%20style-black-black">
    <img alt="black" src="https://img.shields.io/badge/code%20style-black-black" />
  </a>
  <a href="https://www.mkdocs.org/">
    <img alt="" src="https://img.shields.io/badge/docs-mkdocs-9cf">
  </a>
</p>


## Requirements

## Features


## Changelog:
* version 0.0.1 - Initial release. Support for discrete PDDL domain and problem parsing.
* version 1.0.0 - Major extension to support PDDL 2.1 in terms of numeric actions.
* version 1.1.0 - Added support for Metric-FF solutions parsing.
* version 1.2.0 - Added support for ENHSP solution parsing.
* version 1.3.0 - Added problem generators for some domains used in the experiments. 
* version 1.4.0 - Added negative preconditions for actions.
* version 2.0.0 - Added support for multi-agent PDDL domains and problems.
* version 2.1.0 - Added support for more complex type of multi-agent trajectories to support non-trivial interactions. 
* version 2.2.0 - Added support for domains with disjunctive numeric preconditions.
* version 3.0.0 - Added support for conditional effect without existential quantification and only conjunctive conditions.
* version 3.1.0 - Added support for universal effects containing only conjunctive conditions.
* version 3.1.4 - Added support for inapplicable actions and fixed a minor logical bug in the universal effects.
* version 3.3.0 - Added support for nested action schemas including universal preconditions.
* version 3.5.0 - Added simplification of numeric expression. This helps to prevent getting too complicated preconditions.
* version 3.5.7 - Added support for problem exportation to PDDL from a problem object.
* version 3.5.8 - Fixed a bug that displayed power expressions in PDDL even though this is not supported by the language.
* version 3.6.5 - performance **boost** for the tokenizer - credit @yarin-benyamin.
* version 3.7.0 - Added the ability to simplify preconditions by eliminating variables that are redundant and thus reducing the general size of the conditions.
* version 3.8.0 - Added code to better support multi-agent domains and problems.
* version 3.8.9 - Added bug fixes to the numeric expressions simplification.
* version 3.9.0 - Added the ability to query the size of an observation.
* version 3.10.0 - Added the ability to handle untyped domains and domains containing predicates / functions / actions where their parameters are grouped to the same type.
* version 3.10.2 - Added the ability to convert a string representing a predicate into a Predicate object.
* version 3.10.3 - Added the ability to support larger numerical error when comparing numbers.
* version 3.10.5 - Fixed a bug in the plan parser that caused the creation of invalid joint actions.
* version 3.11.0 - Added functionality to represent type hierarchy as a graph and iterate over it. 
* version 3.12.0 - Supporting zipping numeric multi-agent plans to some degree.
* version 3.13.0 - Added the ability to easily change the signature of the domain elements.

