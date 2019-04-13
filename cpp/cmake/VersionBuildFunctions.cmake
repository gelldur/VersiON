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

	get_git_head_revision(GIT_REFSPEC GIT_LONG_SHA1)
	git_short_sha1(GIT_SHORT_SHA1)
	git_commit_date(GIT_COMMIT_DATE)

	execute_process(COMMAND
		"${_VERSION_ROOT}/../tool/get_build_version.py" --pattern-name=${style} --name=${target} --enable-rc
		WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
		OUTPUT_VARIABLE BUILD_VERSION
		OUTPUT_STRIP_TRAILING_WHITESPACE
		)

	if(NOT BUILD_VERSION)
		message(WARNING "Can't get version")
	endif()

	set(GIT_IS_DIRTY "false")
	git_local_changes(DIRTY)
	if(DIRTY STREQUAL "DIRTY")
		set(GIT_IS_DIRTY "true")
		if(CMAKE_BUILD_TYPE STREQUAL "Release" OR CMAKE_BUILD_TYPE STREQUAL "RelWithDebInfo")
			message(WARNING "Current build is dirty it shouldn't be released!")
		endif()
	endif()

	message("BUILD_VERSION: " ${BUILD_VERSION})
	message("GIT_LONG_SHA1: " ${GIT_LONG_SHA1})
	message("GIT_SHORT_SHA1: " ${GIT_SHORT_SHA1})
	message("GIT_COMMIT_DATE: " ${GIT_COMMIT_DATE})
	message("GIT_IS_DIRTY: " ${GIT_IS_DIRTY})

	configure_file(${_VERSION_ROOT}/src/version/Build.cpp.in gen/src/version/Build.cpp @ONLY)

	# https://cmake.org/cmake/help/latest/manual/cmake-properties.7.html#target-properties
	get_target_property(_target_bin_dir ${target} BINARY_DIR)

	# We want always static
	add_library("${target}_version" STATIC EXCLUDE_FROM_ALL
		${_target_bin_dir}/gen/src/version/Build.cpp
		)

	target_include_directories("${target}_version" PUBLIC
		${_VERSION_ROOT}/src/
		)

	target_link_libraries(${target} PRIVATE "${target}_version")

	if(${BUILD_VERSION})
		set_target_properties(${target}
			PROPERTIES
			VERSION ${BUILD_VERSION}
			)
		set_target_properties("${target}_version"
			PROPERTIES
			VERSION ${BUILD_VERSION}
			)
	endif()
endfunction()

################################################################################
