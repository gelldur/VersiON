# How to integrate to C++ project
Please append `CMAKE_MODULE_PATH` so `include(VersionBuildFunctions)` may work.
```cmake
list(APPEND CMAKE_MODULE_PATH "${PATH_TO_ROOT_OF_VERSION}/cpp/cmake")
include(VersionBuildFunctions)

# Define your target
add_executable(MyApp src/main.cpp)

# Apply versioning with your style of choice :)
version_for(MyApp semantic)
```

Please also check [example implementation here](example/)

# What is done under the hood ?
If you are interested just check [cmake file](cmake/VersionBuildFunctions.cmake). In short
description for each function call of `version_for()` script add new target which will contain
version + generated C++ files so you can use them out of the box + resolve for you include paths.

Also it shouldn't rebuild your entire project because version data is "closed" in small static lib.
Maybe this need improvement for improve linking times. If you face issues please create issue ;)

## Other tips for cmake
As you read this document maybe you will find something useful for you :)

- How to set nice version in cmake
```cmake
set_target_properties(MyApp
	PROPERTIES
	VERSION 1.0.0
	DEBUG_POSTFIX "-debug"
)
```

- Set runtime destination
```cmake
install(TARGETS MyApp RUNTIME DESTINATION bin)
```
