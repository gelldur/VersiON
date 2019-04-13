# ![VersiON](./VersiON-logo.svg)

# Intro
Every application which is released uses some kind versioning. Doing this manually is exhausting and
bug prone. We don't want to think what version is next when we are during fixing super complex bug.

Idea of this project is to automate this process and make it more automated way. As we already use
`git` then we should squeeze more of it and make him to deal with versioning. It isn't only backup
storage of our code!

# Description
As mentioned in [Intro], as developers we shouldn't think about versioning in terms which version
part I should bump. Most common version "style" is with three dots `X.Y.Z` sure some can use
[semantic]() versioning other use their own convention. It is up to you how you want to deal with
it.

Currently there are few example versioning styles implemented which you can use out of the box.
As developer we it is easy to say how much important my change in code is. So you already done
the hard part, now you only need to "mark" your commit with importance mark. For example in semantic
versioning I can mark commit as "[MINOR]" rest is done by this tool!

What is only needed from your side ?
- One time integration of this tool (integration depends on language you use for your project).
It depends on language how time consuming it would be, but as goal of this project it should take
max 5m as quick bugfix :)
- During development just mark you commits with "marks" (you can define them)
- If you forgot about previous step no worry! You can `rebase` your commits or just make dummy
commit with "version bump" choice of flow is up to you. This tool shouldn't force you to change
your work flow.



Bunch of scripts & tools to make release life easier.
Designed to work with pure CLI, Clion, CMake, C++

## Requirements for this tool

- Easy to bump version
- Easy add to current project
- Should be able to release multiple apps/services from 1 repository
- Should be able to use custom names for release. Example:
	- [semantic versioning](https://semver.org/) (`1.2.3`)
	- revision build (`r2098`)
	- feature release (`34.2`)
	- date - feature release (`2019.3`)
	- other ?
- Minimize risk of deploy uncommited changes
- Verify that git tag was pushed
- Support change of versioning convention. At some point we decide to change style
- Check "[What's next](#What's-next-?)"

## Technology stack
Main technology is Python for easy of use + cross-platform
Integrations for specific languages:
- C++ & CMake

# Quick start

- Minimal [C++ example/](cpp/README.md)
- [Live demo](https://TODO)

## How to use in your project


# What's next ?
When this will be done ? It depends on needs of users :)
- CHANGELOG generation & management
- Bump version of specific component. For example we have in 1 repository, 2 apps which don't
have common code and we don't want version bumps interfere.
