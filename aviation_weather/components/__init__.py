__all__ = [
    "pressure",
    "remarks",
    "runwayvisualrange",
    "skycondition",
    "station",
    "temperature",
    "time",
    "visibility",
    "weathergroup",
    "wind"
]

# TODO: Change tests and Report to use component.raw instead of str(component)


class Component(object):
    """A superclass from which individual weather components should be derived"""

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.raw)

    def __str__(self):
        """The component in its decoded form if available, or the raw form if not (for unparsed components)."""
        return self.decoded or self.raw

    def __eq__(self, other):
        """Components should be considered equal if they have the same type and their attributes are equal."""
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    @property
    def decoded(self) -> str:
        """The component as a decoded (plain English) string"""
        raise NotImplementedError  # This should be overridden by all components.

    @property
    def raw(self) -> str:
        """The component as a raw (or encoded) string"""
        raise NotImplementedError  # This should be overridden by all components.
