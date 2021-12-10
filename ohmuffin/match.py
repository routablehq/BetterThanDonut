from collections import namedtuple

from ohmuffin.models import Profile

MatchGroup = namedtuple("MatchGroup", ["members", "interests"])


def dumb_match():
    profiles = Profile.objects.all().prefetch_related("interests")

    matched = set()
    groups = []

    interests = {
        p: set(p.interests.all()) for p in profiles
    }

    overlap_map = {
        p: sorted([
            [p2, len(interests[p] & interests[p2]) / max(1, len(interests[p2] | interests[p])), interests[p] & interests[p2]]
            for p2 in profiles if p2 != p
        ], key=lambda t: t[1], reverse=True)
        for p in profiles
    }

    for profile, overlaps in overlap_map.items():
        if profile not in matched:
            potentials = [o for o in overlaps if o[0] not in matched]
            if potentials:
                groups.append(MatchGroup([profile, potentials[0][0]], potentials[0][2]))
                matched = matched | {profile, potentials[0][0]}

    if len(matched) < len(profiles):
        profile_set = set(profiles)
        unmatched = profile_set - matched
        groups[-1].members.extend(unmatched)

    return groups
