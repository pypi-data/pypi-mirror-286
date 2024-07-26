def for_each(ls, func, *args, **kwargs):
	if type(ls) != type(list()):
		return None
	return [func(l, *args, **kwargs) for l in ls]
