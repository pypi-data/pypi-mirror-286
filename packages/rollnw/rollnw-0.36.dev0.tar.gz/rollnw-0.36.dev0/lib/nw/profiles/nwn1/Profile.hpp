#pragma once

#include "constants.hpp"
#include "rules.hpp"

#include "../../kernel/GameProfile.hpp"

namespace nwn1 {

/// NWN1 Game Profile
struct Profile : nw::GameProfile {
    virtual ~Profile() = default;

    /**
     * @brief Loads rules
     *
     * - Load Selector and Matcher
     * - Load Components
     * - Load 2DAs
     * - Load Constants
     * - Post Process 2DAs
     *
     */
    bool load_rules() const override;

    /// Loads containers into resman
    bool load_resources() override;
};

} // namespace nwn1
