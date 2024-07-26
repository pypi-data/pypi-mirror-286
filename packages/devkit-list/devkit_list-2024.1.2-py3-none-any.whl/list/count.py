def elemcount(ls):
    if type(ls) != type(list()):
        return None
    vis = []
    for l in ls:
        if not l in vis:
            vis.append(l)
    return {v: ls.count(v) for v in vis}
