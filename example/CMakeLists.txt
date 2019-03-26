cmake_minimum_required(VERSION 3.13)
project(example)

set(CMAKE_CXX_STANDARD 17)

# So include(PrepareBuild) can work
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/../cmake")
include(VersionBuildFunctions)

add_executable(MyApp src/main.cpp)

# Everything you need ########
version_for(MyApp)    ########
##############################

set_target_properties(MyApp
	PROPERTIES
	DEBUG_POSTFIX "-debug"
	)
