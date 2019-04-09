// SPDX-License-Identifier: MIT
// Copyright © 2019 Dawid Drozd aka Gelldur
#pragma once

#include <cstdint>
#include <string_view>

namespace Build
{
namespace Git
{
/**
 * @return short SHA1 at current commit
 */
std::string_view getSHA1Short();
/**
 * @return full SHA1 at current commit
 */
std::string_view getSHA1Full();
std::string_view getCommitDate();

/**
 * @return was there any not commited changes in repository during build ?
 */
bool isDirty();

} // namespace Git

std::string_view getVersion();
std::string_view getDate();

namespace Environment
{
std::string_view getCompiler();
std::string_view getArchitecture();
std::string_view getSystem();
std::string_view getCMake();
} // namespace Environment

void printFullInformation(std::ostream& output);

} // namespace Build
