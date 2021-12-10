from collections import namedtuple

from ohmuffin.models import Profile, Match

MatchGroup = namedtuple("MatchGroup", ["members", "interests"])


def matching_data():
    profiles = Profile.objects.all().prefetch_related("interests").order_by("?")
    previous_matches = Match.objects.all().prefetch_related("profiles")
    interests = {
        p: set(p.interests.all()) for p in profiles
    }

    return profiles, interests, previous_matches


def overlap_score(p1, p2, interests):
    return len(interests[p1] & interests[p2]) / max(1, len(interests[p2] | interests[p1]))


def dumb_match():
    profiles, interests, previous_matches = matching_data()

    match_map = {
        p1: {
            p2: previous_matches.filter(profiles__id=p1.id).filter(profiles__id=p2.id).count()
            for p2 in profiles if p2 != p1
        } for p1 in profiles
    }

    overlap_map = {
        p: sorted([
            [p2, overlap_score(p, p2, interests) * pow(0.5, match_map[p][p2]), interests[p] & interests[p2]]
            for p2 in profiles if p2 != p
        ], key=lambda t: t[1], reverse=True)
        for p in profiles
    }

    matched = set()
    groups = []

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

    for group in groups:
        m = Match.objects.create()
        for p in group.members:
            m.profiles.add(p)
        for i in group.interests:
            m.interests.add(i)
        m.save()

    return groups
