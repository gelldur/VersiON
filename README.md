# ![VersiON](./VersiON-logo.svg)

# Intro
Every application which is released uses some kind of versioning. Doing this manually is exhausting and
bug prone. We don't want to think which version is next during fixing super complex bug.

Idea of this project is to automate this process and make it more automated way. As we already use
`git` then we should squeeze more of it and make it to deal with versioning. It's not only backup
storage of our code!

# Description
As mentioned in [Intro], as developers we shouldn't think about versioning in terms which version
part I should bump. Most common version "style" is with three dots `X.Y.Z`, some people can use
[semantic]() versioning, others use their own convention. It depends on you, how do you want to figure
it out.

Currently, there are few examples of versioning styles implemented, which you can use out of the box.
As developer, it is easy to say how important is my change in code. So you have already done
the hard part, now you only need to "mark" your commit with importance mark. For example in semantic
versioning I can mark commit as "[MINOR]" and rest of work is done by this tool!

What is only needed from your side ?
- One time integration of this tool (integration depends on language you use for your project).
It depends on language, how much time would it take, but as a goal of this project it should not take more than 5m as quick bugfix :)
- During development just mark you commits with "marks" (you can define them)
- If you forgot about previous step, no worries! You can `rebase` your commits or just make dummy
commit with "version bump" (choice of flow epends on your preferences). This tool shouldn't force you to change
your work flow.



Bunch of scripts & tools to make release life easier.
Designed to work with pure CLI, Clion, CMake, C++

## Goals for this tool

- Easy to bump version
- Easy add to current project
- Ability to release multiple apps/services from 1 repository
- Ability to use custom names for release. Example:
	- [semantic versioning](https://semver.org/) (`1.2.3`)
	- revision build (`r2098`)
	- feature release (`34.2`)
	- date - feature release (`2019.3`)
	- other ?
- Minimised risk of deploy uncommited changes
- Verify that git tag was pushed
- Support change of versioning convention. (e.g. when at some point you decide to change style)
- Check "[What's next](#What's-next-?)"

## Technology stack
Main technology is Python for easy of use + cross-platform
Integrations for specific languages:
- C++ & CMake

# Quick start

- Minimal [C++ example/](cpp/README.md)
- [Live demo](https://TODO)


# What's next ?
When would it be done? It depends on users' needs :)
- CHANGELOG generation & management
- Bump version of specific component. For example we have in 1 repository 2 apps which don't
have common code and we don't want version bumps interfere.
