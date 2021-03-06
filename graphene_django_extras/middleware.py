# -*- coding: utf-8 -*-
from promise import Promise
from .registry import get_global_registry


class ExtraGraphQLDirectiveMiddleware(object):

    def resolve(self, next, root, info, **kwargs):
        context = info.context
        result = next(root, info, **kwargs)
        return result.then(
            lambda resolved: self.__process_value(resolved, root, info, **kwargs),
            lambda error: Promise.rejected(error)
        )

    def __process_value(self, value, root, info, **kwargs):
        registry = get_global_registry()
        field = info.field_asts[0]
        if not field.directives:
            return value

        new_value = value
        for directive in field.directives:
            directive_class = registry.get_directive(directive.name.value)
            new_value = directive_class.resolve(new_value, directive, root, info, **kwargs)

        return new_value
