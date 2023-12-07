include(GetGitRevisionDescription) # Thanks to this we will reload cmake if needed

# include guard
if(___GUARD_version_build_functions)
	return()
endif()
set(___GUARD_version_build_functions YES)

get_filename_component(_VERSION_ROOT ${CMAKE_CURRENT_LIST_DIR} DIRECTORY)
# message("_VERSION_ROOT path: ${_VERSION_ROOT}")

# the date of the HEAD commit
function(git_commit_date _var)
	if(NOT GIT_FOUND)
		find_package(Git QUIET)
	endif()
	get_git_head_revision(refspec hash)
	if(NOT GIT_FOUND)
		set(${_var} "GIT-NOTFOUND" PARENT_SCOPE)
		return()
	endif()
	if(NOT hash)
		set(${_var} "HEAD-HASH-NOTFOUND" PARENT_SCOPE)
		return()
	endif()

	execute_process(COMMAND
		"${GIT_EXECUTABLE}" log -1 --format=%ad --date=iso8601 ${hash}
		WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
		OUTPUT_VARIABLE out
		ERROR_QUIET
		OUTPUT_STRIP_TRAILING_WHITESPACE
		)
	set(${_var} ${out} PARENT_SCOPE)
endfunction()

################################################################################

function(git_short_sha1 _var)
	if(NOT GIT_FOUND)
		find_package(Git QUIET)
	endif()
	get_git_head_revision(refspec hash)
	if(NOT GIT_FOUND)
		set(${_var} "GIT-NOTFOUND" PARENT_SCOPE)
		return()
	endif()
	if(NOT hash)
		set(${_var} "HEAD-HASH-NOTFOUND" PARENT_SCOPE)
		return()
	endif()

	execute_process(COMMAND
		"${GIT_EXECUTABLE}" describe ${hash} --always --abbrev=4
		WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
		OUTPUT_VARIABLE out
		ERROR_QUIET
		OUTPUT_STRIP_TRAILING_WHITESPACE)
	set(${_var} ${out} PARENT_SCOPE)
endfunction()

################################################################################

function(git_commit_count_total _var)
	if(NOT GIT_FOUND)
		find_package(Git QUIET)
	endif()
	get_git_head_revision(refspec hash)
	if(NOT GIT_FOUND)
		set(${_var} "GIT-NOTFOUND" PARENT_SCOPE)
		return()
	endif()
	if(NOT hash)
		set(${_var} "HEAD-HASH-NOTFOUND" PARENT_SCOPE)
		return()
	endif()

	# GIT_COMMIT_COUNT
	execute_process(COMMAND
		"${GIT_EXECUTABLE}" rev-list ${hash} --count
		WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
		OUTPUT_VARIABLE out
		ERROR_QUIET
		OUTPUT_STRIP_TRAILING_WHITESPACE
		)

	set(${_var} ${out} PARENT_SCOPE)
endfunction()

################################################################################

function(git_current_tag target _out_var)
	if(NOT GIT_FOUND)
		find_package(Git QUIET)
	endif()
	get_git_head_revision(refspec hash)
	if(NOT GIT_FOUND)
		set(${_var} "GIT-NOTFOUND" PARENT_SCOPE)
		return()
	endif()
	if(NOT hash)
		set(${_var} "HEAD-HASH-NOTFOUND" PARENT_SCOPE)
		return()
	endif()

	# GIT_COMMIT_COUNT
	execute_process(COMMAND
		"${GIT_EXECUTABLE}" tag --points-at ${hash}
		WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
		OUTPUT_VARIABLE out
		ERROR_QUIET
		OUTPUT_STRIP_TRAILING_WHITESPACE
		)
	#message("OUT:${out}")
	if("${out}" STREQUAL "")
		message("No tags found for version at HEAD")
		return()
	endif()
	#message("----")

	set(_pattern "(${target}-)(.+)$")
	#message("Pattern: ${_pattern}")

	string(REPLACE "\n" ";" _tags ${out}) # Make list
	foreach(loop_var ${_tags})
		#message("Tag: ${loop_var}")
		string(REGEX MATCH ${_pattern} _match_tag "${loop_var}")
		if(NOT ${_match_tag})
			break()
		endif()
	endforeach(loop_var)

	if(NOT ${_match_tag})
		message("Found:'${_match_tag}'")
		set(${_out_var} ${_match_tag} PARENT_SCOPE)
	endif()
endfunction()

################################################################################
################################################################################

function(version_for target style)
	if(NOT TARGET ${target})
		message(FATAL_ERROR "Target not definied: ${target}")
		return()
	endif()

	# TODO write documentation for style and define style=project?

	# If we have project 'cache' version use it.
	if(TARGET ${PROJECT_NAME}_version)
		message("Reusing project wide version: '${PROJECT_BUILD_VERSION}' @ '${PROJECT_NAME}_version' for target: '${target}'")
		target_link_libraries(${target} PRIVATE ${PROJECT_NAME}_version)

		if(NOT "${PROJECT_BUILD_VERSION}" STREQUAL "")
			set_target_properties(${target}
				PROPERTIES
				VERSION ${PROJECT_BUILD_VERSION}
				)
			# Because we create specific version binary (se why not needed is STATIC)
			# set_target_properties("${target}_version"
			# 	PROPERTIES
			# 	VERSION ${BUILD_VERSION_${target}}
			# 	)
		endif()
		return()
	endif()


	# Used by CPP configure_file Build.cpp.in
	get_git_head_revision(GIT_REFSPEC GIT_LONG_SHA1)
	git_short_sha1(GIT_SHORT_SHA1)
	git_commit_date(GIT_COMMIT_DATE)

	set(GIT_IS_DIRTY "false")
	git_local_changes(DIRTY)
	if(DIRTY STREQUAL "DIRTY")
		set(GIT_IS_DIRTY "true")
	endif()

	# TODO Debug dirty vs not dirty
	#	if((NOT DEFINED "BUILD_VERSION_${target}"))
	#		message(FATAL_ERROR "First invalid")
	#	elseif((NOT DEFINED "_CACHED_VARIABLE_${target}-${DIRTY}"))
	#		message(FATAL_ERROR "Second invalid")
	#	elseif((NOT _CACHED_VARIABLE_${target}-${DIRTY} STREQUAL GIT_LONG_SHA1))
	#		message(FATAL_ERROR "3 invalid")
	#	endif()

	# FIXME I broke this by intention for now
	# TODO bug with cache is global instead for target. Mostly issue with different semantic usage
	if((NOT DEFINED "BUILD_VERSION_${target}") OR (NOT DEFINED "_CACHED_VARIABLE_${target}-${DIRTY}") OR (NOT _CACHED_VARIABLE_${target}-${DIRTY} STREQUAL GIT_LONG_SHA1))
		message(WARNING "Generating build version for: ${target} at ${GIT_LONG_SHA1} with dirty:${DIRTY}")

		execute_process(COMMAND
			"${_VERSION_ROOT}/../python/get_build_version.py" --style-name=${style} --name=${target} --enable-mark-wip --verbose
			WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
			OUTPUT_VARIABLE BUILD_VERSION_OUT
			OUTPUT_STRIP_TRAILING_WHITESPACE
			RESULT_VARIABLE _exit_code
			)
		set(BUILD_VERSION_${target} ${BUILD_VERSION_OUT} CACHE STRING "Cached build version for target" FORCE)
		message("[Python] BUILD_VERSION: " ${BUILD_VERSION_${target}} " for " ${GIT_LONG_SHA1})
		if(NOT _exit_code EQUAL 0)
			message(FATAL_ERROR "'version_for' not working. Bad exit code:${_exit_code}")
		endif()
		set(_CACHED_VARIABLE_${target}-${DIRTY} ${GIT_LONG_SHA1} CACHE INTERNAL "Cached variable with last commit. Less reloads when no changes" FORCE)
	endif()

	if(NOT BUILD_VERSION_${target})
		message(WARNING "Can't get version")
	endif()

	#BUILD_VERSION veriable used in configure_file()
	set(BUILD_VERSION ${BUILD_VERSION_${target}})
	message("VersiON for: " ${target})
	message("BUILD_VERSION: " ${BUILD_VERSION})
	message("GIT_LONG_SHA1: " ${GIT_LONG_SHA1})
	message("GIT_SHORT_SHA1: " ${GIT_SHORT_SHA1})
	message("GIT_COMMIT_DATE: " ${GIT_COMMIT_DATE})
	message("GIT_IS_DIRTY: " ${GIT_IS_DIRTY})
	message("")

	if(GIT_IS_DIRTY STREQUAL "true" AND (CMAKE_BUILD_TYPE STREQUAL "Release" OR CMAKE_BUILD_TYPE STREQUAL "RelWithDebInfo"))
		message(WARNING "\n##################################\nCurrent build is dirty it shouldn't be released!\n##################################\n")
	endif()


	configure_file(${_VERSION_ROOT}/src/version/Build.cpp.in gen/src/version/Build.cpp @ONLY)

	# https://cmake.org/cmake/help/latest/manual/cmake-properties.7.html#target-properties
	get_target_property(_target_bin_dir ${target} BINARY_DIR)

	# We want always to include our code in other binary. Thanks to that
	#  we don't have to store previous versions of "VersiON" lib
	add_library("${target}_version" STATIC EXCLUDE_FROM_ALL
		${_target_bin_dir}/gen/src/version/Build.cpp
		)

	target_include_directories("${target}_version" PUBLIC
		${_VERSION_ROOT}/src/
		)

	target_link_libraries(${target} PRIVATE "${target}_version")

	if(NOT "${BUILD_VERSION_${target}}" STREQUAL "")
		set_target_properties(${target}
			PROPERTIES
			VERSION ${BUILD_VERSION_${target}}
			)
		# Because we create specific version binary (se why not needed is STATIC)
		# set_target_properties("${target}_version"
		# 	PROPERTIES
		# 	VERSION ${BUILD_VERSION_${target}}
		# 	)
	endif()
endfunction()

################################################################################

################################################################################
################################################################################

function(version_for_project style)
	# Used by CPP configure_file Build.cpp.in
	get_git_head_revision(GIT_REFSPEC GIT_LONG_SHA1)
	git_short_sha1(GIT_SHORT_SHA1)
	git_commit_date(GIT_COMMIT_DATE)

	set(GIT_IS_DIRTY "false")
	git_local_changes(DIRTY)
	if(DIRTY STREQUAL "DIRTY")
		set(GIT_IS_DIRTY "true")
	endif()

	# TODO Debug dirty vs not dirty
	#	if((NOT DEFINED "BUILD_VERSION_${target}"))
	#		message(FATAL_ERROR "First invalid")
	#	elseif((NOT DEFINED "_CACHED_VARIABLE_${target}-${DIRTY}"))
	#		message(FATAL_ERROR "Second invalid")
	#	elseif((NOT _CACHED_VARIABLE_${target}-${DIRTY} STREQUAL GIT_LONG_SHA1))
	#		message(FATAL_ERROR "3 invalid")
	#	endif()

	# FIXME I broke this by intention for now
	# TODO bug with cache is global instead for target. Mostly issue with different semantic usage
	if((NOT DEFINED PROJECT_BUILD_VERSION) OR (NOT DEFINED "_CACHED_VARIABLE_PROJECT-${DIRTY}") OR (NOT _CACHED_VARIABLE_PROJECT-${DIRTY} STREQUAL GIT_LONG_SHA1))
		message("Generating build version for: Project at ${GIT_LONG_SHA1} with dirty:${DIRTY}")

		execute_process(COMMAND
			"${_VERSION_ROOT}/../python/get_build_version.py" --style-name=${style} --name=${target} --enable-mark-wip --verbose
			WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
			OUTPUT_VARIABLE BUILD_VERSION_OUT
			OUTPUT_STRIP_TRAILING_WHITESPACE
			RESULT_VARIABLE _exit_code
			)
		set(PROJECT_BUILD_VERSION ${BUILD_VERSION_OUT} CACHE STRING "Cached build version for project" FORCE)
		if(NOT _exit_code EQUAL 0)
			message(FATAL_ERROR "'version_for' not working. Bad exit code:${_exit_code}")
		endif()
		set(_CACHED_VARIABLE_PROJECT-${DIRTY} ${GIT_LONG_SHA1} CACHE INTERNAL "Cached variable with last commit. Less reloads when no changes" FORCE)
	endif()

	if(NOT PROJECT_BUILD_VERSION)
		message(WARNING "Can't get version")
	endif()


		#BUILD_VERSION veriable used in configure_file()
	set(BUILD_VERSION ${PROJECT_BUILD_VERSION})
	message("\nVersiON for project wide: ${PROJECT_NAME}")
	message("BUILD_VERSION: " ${PROJECT_BUILD_VERSION})
	message("GIT_LONG_SHA1: " ${GIT_LONG_SHA1})
	message("GIT_SHORT_SHA1: " ${GIT_SHORT_SHA1})
	message("GIT_COMMIT_DATE: " ${GIT_COMMIT_DATE})
	message("GIT_IS_DIRTY: " ${GIT_IS_DIRTY}\n)

	if(GIT_IS_DIRTY STREQUAL "true" AND (CMAKE_BUILD_TYPE STREQUAL "Release" OR CMAKE_BUILD_TYPE STREQUAL "RelWithDebInfo"))
		message(WARNING "\n##################################\nCurrent build is dirty it shouldn't be released!\n##################################\n")
	endif()

	configure_file(${_VERSION_ROOT}/src/version/Build.cpp.in gen/src/version/Build.cpp @ONLY)

	# We want always to include our code in other binary. Thanks to that
	#  we don't have to store previous versions of "VersiON" lib
	add_library("${PROJECT_NAME}_version" STATIC EXCLUDE_FROM_ALL
		${PROJECT_BINARY_DIR}/gen/src/version/Build.cpp
		)

	target_include_directories("${PROJECT_NAME}_version" PUBLIC
		${_VERSION_ROOT}/src/
		)
endfunction()

# This should be called only once


################################################################################
