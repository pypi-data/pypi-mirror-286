#include "Rules.hpp"

#include "../util/string.hpp"
#include "GameProfile.hpp"
#include "TwoDACache.hpp"

#include <cstddef>

namespace nw::kernel {

Rules::~Rules()
{
    clear();
}

void Rules::clear()
{
    qualifier_ = qualifier_type{};
    selector_ = selector_type{};
    modifiers.clear();
    baseitems.clear();
    classes.clear();
    feats.clear();
    races.clear();
    spells.clear();
    skills.clear();
    master_feats.clear();
    appearances.clear();
    phenotypes.clear();
    traps.clear();
    placeables.clear();
}

void Rules::initialize(ServiceInitTime time)
{
    if (time != ServiceInitTime::kernel_start && time != ServiceInitTime::module_post_load) {
        return;
    }

    LOG_F(INFO, "kernel: rules system initializing...");
    if (auto profile = services().profile()) {
        profile->load_rules();
    }
}

bool Rules::match(const Qualifier& qual, const ObjectBase* obj) const
{
    if (!qualifier_) {
        return true;
    }
    return qualifier_(qual, obj);
}

bool Rules::meets_requirement(const Requirement& req, const ObjectBase* obj) const
{
    for (const auto& q : req.qualifiers) {
        if (req.conjunction) {
            if (!match(q, obj)) {
                return false;
            }
        } else if (match(q, obj)) {
            return true;
        }
    }
    return true;
}

RuleValue Rules::select(const Selector& selector, const ObjectBase* obj) const
{
    if (!selector_) {
        LOG_F(ERROR, "rules: no selector set");
        return {};
    }

    return selector_(selector, obj);
}

void Rules::set_qualifier(qualifier_type match)
{
    qualifier_ = std::move(match);
}

void Rules::set_selector(selector_type selector)
{
    selector_ = std::move(selector);
}

} // namespace nw::kernel
