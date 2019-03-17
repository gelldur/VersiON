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
 * @return tag at current commit when available. If there is not tag it will return empty
 */
std::string_view getTag();
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
 * @return commit count from beginning
 */
std::uint32_t getCommitCount();

/**
 * @return was there any not commited changes in repository during build ?
 */
bool isDirty();

} // namespace Git

std::string_view getVersion();
std::string_view getVersionDate();

} // namespace Build
