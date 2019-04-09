# version

Bunch of scripts & tools to make release life easier.
Designed to work with pure CLI, Clion, CMake, C++

## Requirements

- Should be able to release multiple apps/services from 1 repository
- Should be able to use custom names for release. Example:
	- [semantic versioning](https://semver.org/) (`1.2.3`)
	- revision build (`r2098`)
	- feature release (`34.2`)
	- date - feature release (`2019.3`)
	- other ?
- Should consider CHANGELOG management
- Should be able to trigger script with release info ?
- Easy to bump version
- Minimize risk of deploy uncommited changes
- Easy add to current project
- Nice & easy rules
- Should be able to express change to which component ? Maybe multiple apps in 1 repository.
- Verify that git tag was pushed
- Support change of versioning convention

## How to add to your project

- Minimal [example/](example/)
- [Live demo](https://TODO)

Please append `CMAKE_MODULE_PATH` so `include(VersionBuildFunctions)` may work. 
```cmake
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
include(VersionBuildFunctions)

# Define your target
add_executable(MyApp src/main.cpp)

# Apply versioning :)
version_for(MyApp)
```


## How to use in your project



## Other tips
How to set nice version in cmake
```cmake
set_target_properties(MyApp
	PROPERTIES
	VERSION 1.0.0
	DEBUG_POSTFIX "-debug"
)
```

```cmake
install(TARGETS MyApp RUNTIME DESTINATION bin)
```
