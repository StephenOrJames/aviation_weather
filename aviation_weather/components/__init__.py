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


class _Component(object):
    """A superclass from which individual weather components should be derived"""

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.raw)

    def __str__(self):
        # TODO: change to self.decoded or self.raw after it is implemented on all components and tests are updated
        # TODO: "or self.raw" will support unparsed content (i.e. Remarks)
        return self.raw

    @property
    def decoded(self):
        """The component as a decoded (plain English) string"""
        raise NotImplementedError  # This should be overridden by all components.

    @property
    def raw(self):
        """The component as a raw (or encoded) string"""
        raise NotImplementedError  # This should be overridden by all components.
