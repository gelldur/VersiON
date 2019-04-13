cmake_minimum_required(VERSION 3.13)
project(example)

set(CMAKE_CXX_STANDARD 17)

# So include(PrepareBuild) can work
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/../cpp/cmake")
include(VersionBuildFunctions)

#-------------------------------------------------------------------------------

add_executable(ExampleRevisionApp src/main.cpp)

# Everything you need ###########################
version_for(ExampleRevisionApp revision) ######## is love <3
#################################################

set_target_properties(ExampleRevisionApp
	PROPERTIES
	DEBUG_POSTFIX "-debug"
	)

#-------------------------------------------------------------------------------

add_executable(ExampleSemanticApp src/main.cpp)

# Everything you need ##################
version_for(ExampleSemanticApp semantic)
########################################

set_target_properties(ExampleSemanticApp
	PROPERTIES
	DEBUG_POSTFIX "-debug"
	)

#-------------------------------------------------------------------------------
